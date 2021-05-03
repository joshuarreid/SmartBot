from groupy.client import Client
from Token import bot_id
from LastfmAPIWrapper.LastFmWrapper import LastfmWrapper as Lastfm
from Token import lastfm_api_key, lastfm_api_secret, lastfm_username, lastfm_password_hash
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from Token import groupyToken

lastfm = Lastfm(lastfm_api_key, lastfm_api_secret, lastfm_username, lastfm_password_hash)
client = Client.from_token(groupyToken)
members = client.groups.get(57087652).members





top_artists = lastfm.get_top_tracks_legacy("bumi_", "7day")[:9]
listofArtists = []
listofPlays = []
for item in top_artists:
    listofArtists.append(item.item.get_name())
    listofPlays.append(int(item.weight))

top_artists = list(zip(listofArtists, listofPlays))
artistdf = pd.DataFrame(top_artists, columns=['Artist', 'Plays'])[::-1]
fig = plt.figure(1)
fig.set_figheight(5)
fig.set_figwidth(10)
ax = plt.gca()
for i, (plays, artist) in enumerate(zip(artistdf['Plays'], artistdf['Artist'])):
    ax.text(plays, i, " " + str(plays), ha='left', size=11)  # 38: plays
plt.barh(artistdf['Artist'], artistdf['Plays'], color='#2dba4e')
plt.xticks()
plt.savefig('topartists.png')
plt.close('all')

with open("topartists.png", 'rb') as f:
    image = client.images.from_file(f)
    client.bots.post(bot_id=bot_id, text="Test", attachments=[image])