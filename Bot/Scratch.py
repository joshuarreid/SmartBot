from groupy.client import Client

client = Client.from_token('j0uo0ElyoFkVWdKAwXEuBsS8JLvvr925BOZCqik0')
for group in client.groups.list():
    print(str(group.id) + " " + str(group.name))