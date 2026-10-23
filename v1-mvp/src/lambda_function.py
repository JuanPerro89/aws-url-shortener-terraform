import json
import boto3
import string
import random

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('url-shortener')


def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def lambda_handler(event, context):
    method = event['requestContext']['http']['method']
    path = event['rawPath']

    if method == 'GET' and path != '/':
        short_id = path.strip('/')
        response = table.get_item(Key={'shortId': short_id})

        if 'Item' in response:
            return {
                'statusCode': 301,
                'headers': {'Location': response['Item']['longUrl']}
            }
        return {'statusCode': 404, 'body': json.dumps('URL no encontrada')}

    elif method == 'POST':
        body = json.loads(event.get('body', '{}'))
        long_url = body.get('url')

        short_id = generate_short_id()
        table.put_item(Item={'shortId': short_id, 'longUrl': long_url})

        host = event['headers'].get('host', '')
        shortened_url = f"https://{host}/{short_id}"

        return {
            'statusCode': 200,
            'body': json.dumps({'shortUrl': shortened_url})
        }

    return {'statusCode': 400, 'body': 'Peticion incorrecta'}