from groupy.client import Client
from Token import groupyToken, groupy_id

client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)


messages = group.messages.list()
allMessages = list(group.messages.list().autopage())
last_message = allMessages[0]

## Test commit
