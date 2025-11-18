import os
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

# Create a new volume or get an existing one
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

# List the contents of the volume to verify
print(f"\nListing volume contents at {mount_dir}:")
list_cmd = f"find {mount_dir} -type f | head -20"
list_response = sandbox.process.exec(list_cmd)
if list_response.exit_code == 0:
    print("Files in volume:")
    print(list_response.result)
else:
    print(
        f"Error listing volume contents: {list_response.exit_code} {list_response.result}"
    )

# Clean up
sandbox.delete()
print(
    "\nClaude skills have been copied to the 'claude-skills' volume and will be available in any sandbox that mounts this volume."
)
