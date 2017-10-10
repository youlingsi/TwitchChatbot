import boto3
from boto3.dynamodb.conditions import Key, Attr
import time

def createTable(channel):
    dydb = boto3.resource('dynamodb')
    try:
        tbl = dydb.create_table(
            TableName = channel,
            KeySchema = [
                {
                    'AttributeName': 'session',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'username',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'session',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                }
            ],

            ProvisionedThroughput = {
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        # wait until table exist
        tbl.meta.client.get_waiter('table_exists').wait(TableName=channel)
    except:
        pass


def updateAttempt(channel, session, user):
    dydb = boto3.resource('dynamodb')
    tb = dydb.Table(channel)
    try:
        itm = tb.update_item(
            Key ={
                'username': user,
                'session': session
            },
            UpdateExpression = "SET attempts = attempts + :val ",
            ExpressionAttributeValues = {
                ':val' : 1,
            },
            ReturnValues="UPDATED_NEW"
        )
    except:
        tb.put_item(
            Item ={
                'session': session,
                'username': user,
                'attempts': 1,
                'win': 0
            }
        )

def maxAttempt(channel, session):
    dydb = boto3.resource('dynamodb')
    tb = dydb.Table(channel)
    response = tb.query(
        KeyConditionExpression = Key('session').eq(session)
    )
    sortList = []
    for i in response['Items']:
        sortList.append(i)
    maxItems = findMax(sortList, 'attempts')
    txtReturn = ''
    for i in maxItems:
        txtReturn += i['username'] + ', '
    return txtReturn + "tried the most! Hardworker!"

def findMax(lst, attr):
    maxVale = 0
    maxItem = []
    for i in range(len(lst)):
        if lst[i][attr] > maxVale:
            maxVale = lst[i][attr]
            maxItem.clear
            maxItem.append(lst[i])
        elif lst[i][attr] == maxVale:
            maxItem.append(lst[i])
    return maxItem

def updateWinner(channel, session, user):
    dydb = boto3.resource('dynamodb')
    tb = dydb.Table(channel)
    try:
        itm = tb.update_item(
            Key ={
                'username': user,
                'session': session
            },
            UpdateExpression = "SET win = :val ",
            ExpressionAttributeValues = {
                ':val' : 1,
            },
            ReturnValues="UPDATED_NEW"
        )
    except:
        tb.put_item(
            Item ={
                'session': session,
                'username': user,
                'win': 1,
                'attempts': 1
            }
        )
