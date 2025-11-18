import os
from pathlib import Path

from daytona import (
    CreateSandboxFromImageParams,
    Daytona,
    DaytonaConfig,
    FileUpload,
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

# Upload .claude folder directly to sandbox
print("\n" + "=" * 80)
print("📦 SETUP: Installing Claude Skills")
print("=" * 80)

# Get the project root directory
project_root = Path(__file__).parent.parent.parent.parent
claude_dir = project_root / ".claude"

if not claude_dir.exists():
    print(f"❌ .claude directory not found at {claude_dir}")
else:
    # Collect all files in .claude directory
    files_to_upload = []
    for file_path in claude_dir.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(claude_dir)
            destination = f"/root/.claude/{relative_path.as_posix()}"

            with open(file_path, "rb") as f:
                files_to_upload.append(
                    FileUpload(
                        source=f.read(),
                        destination=destination,
                    )
                )

    print(f"📤 Uploading {len(files_to_upload)} files...")
    sandbox.fs.upload_files(files_to_upload)
    print("✓ Skills uploaded successfully")

print("\n📋 Initial skills available:")
skills_list = sandbox.process.exec(
    "ls -1 /root/.claude/skills 2>/dev/null || echo '(none)'"
)
for skill in skills_list.result.strip().split("\n"):
    print(f"   • {skill}")


# Define test requests to demonstrate skill creation and reuse
requests = [
    # Task 1: Scrape HN comments & create a new skill for counting them
    "How many comments are on this Hacker News discussion: https://news.ycombinator.com/item?id=45916094. Create a skill for this",
    # Task 2: Reuse the HN skill created in Task 1 on a different discussion
    "How many comments are on this Hacker News discussion: https://news.ycombinator.com/item?id=45969250",
    # Task 3: Count emojis & create a new skill for emoji counting
    "Count the number of emojis in the string 'Hello, world! 🌍'. Create a skill for this",
    # Task 4: Reuse the emoji counting skill created in Task 3 on a multi-line string
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
