#
# eliminator.py - ツイート削除クラス
#
import tweepy

class Eliminator():

    def __init__(self, api: tweepy.API):
        self.api = api

    # 指定されたツイートを消す
    def eliminate(self, status: tweepy.Status) -> bool:
        # .destroyは使いません(便利だけどapiのインスタンス渡した意味がわからなくなる)

        # Statusオブジェクトにidが含まれるかよくわからなかったので
        if not hasattr(status, "id"):
            return False
        status_id = status.id

        # 消す
        self.api.destroy_status(status_id)
        return True

