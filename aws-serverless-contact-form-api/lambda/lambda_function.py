import json
import boto3
import uuid
import logging
from datetime import datetime

# ── Logging ────────────────────────────────────────────────────────────────────
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ── AWS Clients ────────────────────────────────────────────────────────────────
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
ses_client = boto3.client('ses', region_name='ap-south-1')

# ── Config — update these values ──────────────────────────────────────────────
TABLE_NAME    = 'ServerlessContactForm'          # Your DynamoDB table name
SENDER_EMAIL  = 'rohannikam9798@gmail.com'       # Must be verified in SES
RECEIVER_EMAIL = 'rohannikam9798@gmail.com'      # Where to receive notifications


def lambda_handler(event, context):
    logger.info("Event received: %s", json.dumps(event))

    # ── 1. Parse body ──────────────────────────────────────────────────────────
    try:
        body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event
    except (json.JSONDecodeError, TypeError):
        return _response(400, 'Invalid JSON in request body.')

    # ── 2. Validate required fields ────────────────────────────────────────────
    name    = str(body.get('name', '')).strip()
    email   = str(body.get('email', '')).strip()
    message = str(body.get('message', '')).strip()

    if not name or not email or not message:
        return _response(400, 'Missing required fields: name, email, message.')

    if '@' not in email or '.' not in email:
        return _response(400, 'Invalid email address format.')

    # ── 3. Save to DynamoDB ────────────────────────────────────────────────────
    submission_id = str(uuid.uuid4())
    timestamp     = datetime.utcnow().isoformat()

    table = dynamodb.Table(TABLE_NAME)
    try:
        table.put_item(Item={
            'submissionId': submission_id,   # Partition key
            'name':         name,
            'email':        email,
            'message':      message,
            'timestamp':    timestamp
        })
        logger.info("Saved to DynamoDB — submissionId: %s", submission_id)

    except Exception as e:
        logger.error("DynamoDB error: %s", str(e))
        return _response(500, 'Failed to save message. Please try again.')

    # ── 4. Send SES Email Notification ────────────────────────────────────────
    email_body = (
        f"New Contact Form Submission\n\n"
        f"Name      : {name}\n"
        f"Email     : {email}\n"
        f"Message   : {message}\n\n"
        f"Timestamp : {timestamp}\n"
        f"ID        : {submission_id}"
    )
    try:
        ses_client.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [RECEIVER_EMAIL]},
            Message={
                'Subject': {'Data': 'New Contact Form Submission'},
                'Body':    {'Text': {'Data': email_body}}
            }
        )
        logger.info("SES email sent for submissionId: %s", submission_id)

    except Exception as e:
        # Non-fatal — data is already saved in DynamoDB
        logger.warning("SES email failed (non-fatal): %s", str(e))

    # ── 5. Return success ──────────────────────────────────────────────────────
    return _response(200, 'Submission successful!', {'submissionId': submission_id})


# ── Helper ─────────────────────────────────────────────────────────────────────
def _response(status_code: int, message: str, extra: dict = None):
    body = {'message': message}
    if extra:
        body.update(extra)
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type':                'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(body)
    }
