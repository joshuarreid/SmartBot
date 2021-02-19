from groupy.client import Client
import LastfmAPIWrapper.LastFmWrapper as pylast
import pandas as pd
import matplotlib.pyplot as plt
from Token import groupyToken
client = Client.from_token(groupyToken)

class Statify:
    """The Statify Class.

    This class is responsible for taking in list inputs and returning meaningful
    statistics on the data

    """
    #TODO method should take list as input and return dict in format {item : count}
    def get_most_frequent(self, item_list):
        df = pd.DataFrame({'Item': item_list})
        df1 = pd.DataFrame(data=df['Item'].value_counts(), columns=[['Item', 'Count']])
        df1['Count'] = df1["Item"].index
        ranked_list = list(df1[df1['Item'] == df1.Item.max()]['Count'])
        return ranked_list



    #TODO method could be more generic
    def graph_top_artists(lastfm_username, period):
        top_artists = pylast.getTopArtist(lastfm_username, period)[:14]
        listofArtists = []
        listofPlays = []
        for item in top_artists:
            listofArtists.append(item.item.get_name())
            listofPlays.append(int(item.weight))
        top_artists = list(zip(listofArtists, listofPlays))
        artistdf = pd.DataFrame(top_artists, columns=['Artist', 'Plays'])[::-1]
        fig = plt.figure(1)
        fig.set_figheight(11)
        fig.set_figwidth(11)
        ax = plt.gca()
        for i, (plays, artist) in enumerate(zip(artistdf['Plays'], artistdf['Artist'])):
            ax.text(plays, i, " " + str(plays), ha='left', size=11)  # 38: plays
        plt.barh(artistdf['Artist'], artistdf['Plays'], color='#2dba4e')
        plt.xticks()
        plt.savefig('topartists.png')
        plt.close('all')
        with open("topartists.png", 'rb') as f:
            image = client.images.from_file(f)
            return image





