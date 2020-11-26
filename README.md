# SmartBot

## Description
This project provides a front-end to my other projects through a GroupMe chatbot. The chatbot can complete commands through a groupchat.

<p align="center">
  <img width="300" src="https://github.com/joshuarreid/SmartBot/blob/master/SmartBot.gif" />
</p>

## Statify Implementation
Currently the SmartBot project implements [Statify](https://github.com/joshuarreid/Statify) to give some Last.Fm functionality. The current **commands** that utilize Statify are:
* !musiclastyear - fetches the tracks the user listened to within the same hour one year ago.
* !recentlyplayed - fetches the tracks the user listened to in the past 24 hours.
* !toptracks *{week, month, year}* - fetches the users most played tracks. 
* !topartists *{week, month, year}* - fetches the users most played artists. 
* !playcount - fetches the total number of plays the user has tied to their Last.Fm account
* !compareme *{@user} {week, month, year}* - compares listened to artists and tracks between two users
* !rank *{week, month, year}* - not implemented yet, but will rank users based on total number of plays within a time interval

## Lazy-Listener Future Implementation
In the future, I plan to implement lazy-listener's music recommendation algorithm so that SmartBot can recommend songs to users and add them to their spotify playlists.

## Credits

* Last.Fm API Wrapper - [Pylast](https://github.com/pylast/pylast)
* GroupMe API Wrapper - [GroupyAPI](https://pypi.org/project/GroupyAPI/)






