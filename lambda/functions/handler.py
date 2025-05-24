import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Notes')

def lambda_handler(event, context):
    http_method = event.get('requestContext', {}).get('http', {}).get('method')

    if http_method == 'POST':
        body = json.loads(event['body'])
        note_id = str(uuid.uuid4())
        table.put_item(Item={"noteId": note_id, "content": body["content"]})
        return {"statusCode": 200, "body": json.dumps({"message": "Note added", "noteId": note_id})}

    elif http_method == 'GET':
        response = table.scan()
        return {"statusCode": 200, "body": json.dumps(response.get("Items", []))}

    return {"statusCode": 400, "body": json.dumps({"message": "Unsupported method"})}