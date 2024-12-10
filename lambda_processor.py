from os import getenv
from json import loads
from dotenv import load_dotenv
from requests import patch


# Load secrets
load_dotenv()
DISCORD_TOKEN = getenv("DISCORD_TOKEN")
GITHUB_API_KEY = getenv("GITHUB_API_KEY")

# Headers
discord_headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}


# Lambda executes
def lambda_processor(event, context):

    # Deserialize SQS event
    try:
        event = loads(event["Records"][0]["body"])
    except KeyError:
        pass

    # Get items from command
    application = event["application_id"]
    token = event["token"]

    # Respond with link to GitHub repo
    data = {"embeds": [{"title": "Pong!", "color": 0xBD2C00}]}

    patch(
        url=f"https://discord.com/api/webhooks/{application}/{token}/messages/@original",
        json=data,
        headers=discord_headers,
    )

    return
