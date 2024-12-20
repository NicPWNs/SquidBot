from os import getenv
from json import dumps
from boto3 import client
from dotenv import load_dotenv
from nacl.signing import VerifyKey


# Load Secrets
load_dotenv()
PUBLIC_KEY = getenv("PUBLIC_KEY")


# Signature Verification
def verify_signature(event):
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    signature = event["params"]["header"]["x-signature-ed25519"]
    timestamp = event["params"]["header"]["x-signature-timestamp"]
    body = event["rawBody"]

    verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))


# Lambda Executes
def lambda_handler(event, context):

    # Signature Headers
    try:
        verify_signature(event)
    except:
        raise Exception("401: Invalid Request Signature")

    # Ping Messages
    body = event.get("body-json")
    if body["type"] == 1:
        return {"type": 1}

    # SQS Queue
    sqs = client("sqs")
    sqs.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/087441767329/squidbot-discord-queue",
        MessageBody=dumps(body),
    )

    # 200 Response
    embeds = [{"title": "⏳  Loading...", "color": 0xFEE9B6}]

    return {"type": 4, "data": {"embeds": embeds}}
