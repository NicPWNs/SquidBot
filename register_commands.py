from os import getenv
from requests import post
from dotenv import load_dotenv

# Load Secrets
load_dotenv()
DISCORD_APP_ID = getenv("DISCORD_APP_ID")
DISCORD_TOKEN = getenv("DISCORD_TOKEN")

# Discord Auth
headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}

# /github Command
json = {
    "name": "test",
    "description": "test",
}

# Register Commands
response = post(
    f"https://discord.com/api/applications/{DISCORD_APP_ID}/commands",
    headers=headers,
    json=json,
)

# Status
if int(response.status_code) == 200:
    print("Command Registration Succeeded!")
else:
    print(f"Command Registration Failed: {response.json()}")
