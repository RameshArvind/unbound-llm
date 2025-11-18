import os

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
mount_dir_1 = "/root/.claude/skills"


# Define a simple declarative image with Python packages
declarative_image = Image.from_dockerfile("daytona-dockerfile")

# Create a new Sandbox with the declarative image and stream the build logs
sandbox = daytona.create(
    CreateSandboxFromImageParams(
        image=declarative_image,
        ephemeral=True,
        env_vars={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "IS_SANDBOX": "1",
        },
        volumes=[VolumeMount(volumeId=volume.id, mountPath=mount_dir_1)],
    ),
    timeout=0,
    on_snapshot_create_logs=print,
)
# Verify the volume mount worked by listing the mounted directory
print(f"Checking mounted volume at {mount_dir_1}:")
mount_check = sandbox.process.exec(f"ls -la {mount_dir_1}")
if mount_check.exit_code != 0:
    print(f"Volume mount check failed: {mount_check.exit_code} {mount_check.result}")
else:
    print("Volume contents:")
    print(mount_check.result)

# Also check using the tilde path (should expand to /root/.claude/skills)
print("Checking ~/.claude/skills (tilde-expanded to /root):")
tilde_check = sandbox.process.exec("ls -la ~/.claude/skills")
if tilde_check.exit_code != 0:
    print(f"Tilde path check failed: {tilde_check.exit_code} {tilde_check.result}")
else:
    print("Tilde path contents:")
    print(tilde_check.result)

# # Run the code securely inside the Sandbox
# response = sandbox.process.exec(
#     'claude --dangerously-skip-permissions -p "Create a new skill called that explains how to use grep into your skills directory"'
# )
# if response.exit_code != 0:
#     print(f"Error: {response.exit_code} {response.result}")
# else:
#     print(response.result)

print("Checking ~/.claude/skills (tilde-expanded to /root):")
tilde_check = sandbox.process.exec("ls -la ~/.claude/skills/grep-guide")
if tilde_check.exit_code != 0:
    print(f"Tilde path check failed: {tilde_check.exit_code} {tilde_check.result}")
else:
    print("Tilde path contents:")
    print(tilde_check.result)

print("Checking ~/.claude/skills (tilde-expanded to /root):")
tilde_check = sandbox.process.exec("ls -la ~/.claude/skills")
if tilde_check.exit_code != 0:
    print(f"Tilde path check failed: {tilde_check.exit_code} {tilde_check.result}")
else:
    print("Tilde path contents:")
    print(tilde_check.result)


# Run the code securely inside the Sandbox
response = sandbox.process.exec('claude -p "List the skills you have access to"')
if response.exit_code != 0:
    print(f"Error: {response.exit_code} {response.result}")
else:
    print(response.result)

sandbox.delete()
