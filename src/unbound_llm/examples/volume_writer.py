import json
import os
from datetime import datetime
from pathlib import Path

from daytona import (
    CreateSandboxFromImageParams,
    Daytona,
    DaytonaConfig,
    Image,
    VolumeMount,
)
from dotenv import load_dotenv

load_dotenv()

# Define the configuration
config = DaytonaConfig(api_key=os.getenv("DAYTONA_API_KEY"))

# Initialize the Daytona client
daytona = Daytona(config)

# Get the existing volume or create new one
volume = daytona.volume.get("claude-skills", create=True)

# Mount the volume to the sandbox
mount_dir = "/root/.claude/skills"

# Define a simple declarative image with Python packages
declarative_image = Image.from_dockerfile("daytona-dockerfile")

# Create a new Sandbox with the declarative image and mounted volume
sandbox = daytona.create(
    CreateSandboxFromImageParams(
        image=declarative_image,
        ephemeral=True,
        env_vars={"ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY")},
        volumes=[VolumeMount(volumeId=volume.id, mountPath=mount_dir)],
    ),
    timeout=0,
    on_snapshot_create_logs=print,
)

# Local path to the Claude skills folder
local_skills_path = Path(".claude/skills")


# Function to copy directory contents recursively via sandbox commands
def copy_directory_to_volume(local_path, volume_path):
    """Copy a local directory to the volume using sandbox commands"""

    # First, ensure the volume directory exists
    mkdir_cmd = f"mkdir -p {volume_path}"
    response = sandbox.process.exec(mkdir_cmd)
    if response.exit_code != 0:
        print(f"Error creating directory {volume_path}: {response.result}")
        return False

    # Copy each file and subdirectory
    for item in local_path.rglob("*"):
        if item.is_file():
            # Get relative path from the skills directory
            relative_path = item.relative_to(local_path)
            volume_file_path = f"{volume_path}/{relative_path}"

            # Create parent directories
            volume_parent = Path(volume_file_path).parent
            mkdir_parent_cmd = f"mkdir -p {volume_parent}"
            response = sandbox.process.exec(mkdir_parent_cmd)
            if response.exit_code != 0:
                print(
                    f"Error creating parent directory {volume_parent}: {response.result}"
                )
                continue

            # Read local file content
            try:
                with open(item, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                # If it's not a text file, copy as binary
                with open(item, "rb") as f:
                    content_bytes = f.read()
                # For binary files, we'll use base64 encoding
                import base64

                content = base64.b64encode(content_bytes).decode("utf-8")
                is_binary = True
            else:
                is_binary = False

            # Write to volume
            if is_binary:
                # Use base64 decoding for binary files
                write_cmd = f"""python3 -c "
import base64
import sys
with open('{volume_file_path}', 'wb') as f:
    f.write(base64.b64decode(sys.argv[1]))
" "{content}" """
            else:
                # Escape single quotes in content for shell
                escaped_content = content.replace("'", "'\"'\"'")
                write_cmd = f"""cat > '{volume_file_path}' << 'EOF'
{escaped_content}
EOF"""

            response = sandbox.process.exec(write_cmd)
            if response.exit_code != 0:
                print(f"Error copying {item} to {volume_file_path}: {response.result}")
            else:
                print(f"Successfully copied {item} -> {volume_file_path}")

    return True


# Copy the skills folder to the volume
print(f"Copying skills from {local_skills_path} to volume at {mount_dir}...")
if local_skills_path.exists():
    success = copy_directory_to_volume(local_skills_path, mount_dir)
    if success:
        print("Skills folder copied successfully!")
    else:
        print("Failed to copy skills folder")
else:
    print(f"Local skills path {local_skills_path} does not exist")

# Create some sample files in the volume
sample_data = {
    "metadata": {
        "created_at": datetime.now().isoformat(),
        "source": "volume_writer.py",
        "description": "Sample data written to claude-skills volume",
    },
    "numbers": list(range(1, 11)),
    "message": "Hello from the volume writer!",
}

# Write JSON data
json_content = json.dumps(sample_data, indent=2)
write_json_cmd = f"""cat > {mount_dir}/sample_data.json << 'EOF'
{json_content}
EOF"""

# Write a simple text file
text_content = f"""This is a sample text file written to the Daytona volume.

Created at: {datetime.now().isoformat()}

This file demonstrates persistent storage across sandboxes.
"""

write_text_cmd = f"""cat > {mount_dir}/sample_text.txt << 'EOF'
{text_content}
EOF"""

# Write a Python script
python_content = """#!/usr/bin/env python3
\"\"\"
Sample Python script stored in Daytona volume.
This demonstrates executable files can be stored persistently.
\"\"\"

def main():
    print("Hello from the volume-stored Python script!")
    print("This script was written to the volume and can be executed from any sandbox.")

if __name__ == "__main__":
    main()
"""

write_python_cmd = f"""cat > {mount_dir}/sample_script.py << 'EOF'
{python_content}
EOF"""

# Execute the commands to write files
commands = [write_json_cmd, write_text_cmd, write_python_cmd]

for i, cmd in enumerate(commands, 1):
    print(f"Writing file {i}/3...")
    response = sandbox.process.exec(cmd)
    if response.exit_code != 0:
        print(f"Error writing file {i}: {response.exit_code} {response.result}")
    else:
        print(f"Successfully wrote file {i}")

# List the contents of the volume to verify
print("\nListing volume contents:")
list_cmd = f"ls -la {mount_dir}/"
list_response = sandbox.process.exec(list_cmd)
if list_response.exit_code == 0:
    print(list_response.result)
else:
    print(f"Error listing volume: {list_response.exit_code} {list_response.result}")

# Test executing the stored Python script
print("\nTesting execution of stored Python script:")
exec_cmd = f"python3 {mount_dir}/sample_script.py"
exec_response = sandbox.process.exec(exec_cmd)
if exec_response.exit_code == 0:
    print("Script executed successfully:")
    print(exec_response.result)
else:
    print(f"Error executing script: {exec_response.exit_code} {exec_response.result}")

# Clean up
sandbox.delete()
print(
    "\nVolume writer completed. Your local Claude skills and sample files are now persisted in the volume 'claude-skills' and can be accessed from other sandboxes."
)
