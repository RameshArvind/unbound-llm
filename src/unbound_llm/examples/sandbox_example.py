import os

from daytona import (
    CreateSandboxFromImageParams,
    Daytona,
    DaytonaConfig,
    Image,
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
        # volumes=[VolumeMount(volumeId=volume.id, mountPath=mount_dir_1)],
    ),
    timeout=0,
    on_snapshot_create_logs=print,
)

# Clone the repo and copy .claude folder to root
print("Setting up Claude skills from repository...")
clone_response = sandbox.process.exec(
    "git clone https://github.com/RameshArvind/unbound-llm.git /tmp/unbound-llm"
)
if clone_response.exit_code != 0:
    print(f"Failed to clone repo: {clone_response.exit_code} {clone_response.result}")
else:
    print("Repository cloned successfully")

    # Copy .claude folder to /root
    copy_response = sandbox.process.exec("cp -r /tmp/unbound-llm/.claude /root/.claude")
    if copy_response.exit_code != 0:
        print(
            f"Failed to copy .claude folder: {copy_response.exit_code} {copy_response.result}"
        )
    else:
        print("Claude skills copied to /root/.claude")

    # Clean up
    cleanup_response = sandbox.process.exec("rm -rf /tmp/unbound-llm")
    if cleanup_response.exit_code != 0:
        print(f"Warning: Failed to clean up temp files: {cleanup_response.result}")

print("Checking ~/.claude/skills (tilde-expanded to /root):")
tilde_check = sandbox.process.exec("ls -la ~/.claude/skills")
if tilde_check.exit_code != 0:
    print(f"Tilde path check failed: {tilde_check.exit_code} {tilde_check.result}")
else:
    print("Tilde path contents:")
    print(tilde_check.result)


# # Run the code securely inside the Sandbox
# response = sandbox.process.exec('claude -p "List the skills you have access to"')
# if response.exit_code != 0:
#     print(f"Error: {response.exit_code} {response.result}")
# else:
#     print(response.result)

print("*" * 100)
response = sandbox.process.exec(
    'claude --dangerously-skip-permissions -p "How many comments are on this Hacker News discussion: https://news.ycombinator.com/item?id=45916094. Create a skill for this"'
)
if response.exit_code != 0:
    print(f"Error: {response.exit_code} {response.result}")
else:
    print(response.result)

print("*" * 100)
response = sandbox.process.exec(
    'claude --dangerously-skip-permissions -p "How many comments are on this Hacker News discussion: https://news.ycombinator.com/item?id=45969250"'
)
if response.exit_code != 0:
    print(f"Error: {response.exit_code} {response.result}")
else:
    print(response.result)

sandbox.delete()
