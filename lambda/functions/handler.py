import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Notes')

def lambda_handler(event, context):
    http_method = event.get('requestContext', {}).get('http', {}).get('method')
    path = event.get('rawPath', '')

    if http_method == 'POST':
        body = json.loads(event['body'])
        note_id = str(uuid.uuid4())
        table.put_item(Item={"noteId": note_id, "content": body["content"]})
        return {"statusCode": 200, "body": json.dumps({"message": "Note added", "noteId": note_id})}

    elif http_method == 'GET':
        response = table.scan()
        return {"statusCode": 200, "body": json.dumps(response.get("Items", []))}

    elif http_method == 'PUT':
        body = json.loads(event['body'])
        note_id = body.get("noteId")
        if not note_id:
            return {"statusCode": 400, "body": json.dumps({"error": "noteId required"})}
        table.update_item(
            Key={"noteId": note_id},
            UpdateExpression="SET content = :c",
            ExpressionAttributeValues={":c": body["content"]}
        )
        return {"statusCode": 200, "body": json.dumps({"message": "Note updated"})}

    elif http_method == 'DELETE':
        body = json.loads(event['body'])
        note_id = body.get("noteId")
        if not note_id:
            return {"statusCode": 400, "body": json.dumps({"error": "noteId required"})}
        table.delete_item(Key={"noteId": note_id})
        return {"statusCode": 200, "body": json.dumps({"message": "Note deleted"})}

    return {"statusCode": 400, "body": json.dumps({"message": "Unsupported method"})}
