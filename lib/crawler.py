#
# crawler.py - ツイート収集クラス
#
import tweepy
from typing import List

class Crawler():

    def __init__(self, api: tweepy.API):
        self.api = api

    def fetch_tweets(self) -> List[tweepy.Status]:
        """ fetch target tweets.
            Args: 
                none (in details, see TODO)
            Returns:
                fetched status objects (`[tweepy.Status]`).
        """

        # TODO: パラメータ注入 (screen_nameに限ってはapi.me().idでもいい気もしないでもないがそれはここでやるもんじゃない)
        statuses = self.api.user_timeline(
            screen_name = "EnchanLab",
            count = 200,
            trim_user = True,
            exclude_replies = False)

        return statuses
