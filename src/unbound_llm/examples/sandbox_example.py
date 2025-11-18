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
print("\n" + "=" * 80)
print("📦 SETUP: Installing Claude Skills")
print("=" * 80)
clone_response = sandbox.process.exec(
    "git clone https://github.com/RameshArvind/unbound-llm.git /tmp/unbound-llm"
)
if clone_response.exit_code != 0:
    print(
        f"❌ Failed to clone repo: {clone_response.exit_code} {clone_response.result}"
    )
else:
    print("✓ Repository cloned")

    # Copy .claude folder to /root
    copy_response = sandbox.process.exec("cp -r /tmp/unbound-llm/.claude /root/.claude")
    if copy_response.exit_code != 0:
        print(
            f"❌ Failed to copy .claude folder: {copy_response.exit_code} {copy_response.result}"
        )
    else:
        print("✓ Skills copied to /root/.claude")

    # Clean up
    cleanup_response = sandbox.process.exec("rm -rf /tmp/unbound-llm")
    if cleanup_response.exit_code != 0:
        print(f"⚠️  Warning: Failed to clean up temp files: {cleanup_response.result}")
    else:
        print("✓ Cleanup complete")

print("\n📋 Initial skills available:")
skills_list = sandbox.process.exec(
    "ls -1 /root/.claude/skills 2>/dev/null || echo '(none)'"
)
for skill in skills_list.result.strip().split("\n"):
    print(f"   • {skill}")


# Define test requests
requests = [
    "How many comments are on this Hacker News discussion: https://news.ycombinator.com/item?id=45916094. Create a skill for this",
    "How many comments are on this Hacker News discussion: https://news.ycombinator.com/item?id=45969250",
    "Count the number of emojis in the string 'Hello, world! 🌍'. Create a skill for this",
    """Count the number of emojis in this multi-line string:
'Hello! 👋 Welcome to our app 🎉
We hope you enjoy using it! 😊
Have a great day! ☀️'""",
]

# Execute requests
for idx, prompt in enumerate(requests, 1):
    print("\n" + "=" * 80)
    print(f"Task #{idx}")
    print("=" * 80)

    response = sandbox.process.exec(
        f'claude --dangerously-skip-permissions -p "{prompt}"'
    )

    if response.exit_code != 0:
        print(f"❌ Error: {response.exit_code} {response.result}")
    else:
        print(response.result)

    # Show skills list after each request
    print("\n" + "-" * 80)
    print(f"📋 Skills after Task #{idx}:")
    skills_list = sandbox.process.exec(
        "ls -1 /root/.claude/skills 2>/dev/null || echo '(none)'"
    )
    for skill in skills_list.result.strip().split("\n"):
        print(f"   • {skill}")

print("\n" + "=" * 80)
print("✅ DEMO COMPLETE")
print("=" * 80)

sandbox.delete()
