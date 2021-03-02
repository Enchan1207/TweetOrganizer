#
# statusfilter.py: 削除対象のツイートか判定する
#
from typing import Optional
from datetime import datetime
import json

import tweepy


class StatusFilter:

    def __init__(self, config_path: Optional[str] = None):
        # TODO: フィルタのコンフィグをjsonかなんかで呼び出したりしたくないですか?
        pass

    def should_delete(self, status: tweepy.Status) -> bool:
        """ Validate passed status object satisfies the delete rules.

            Args: 
                status `tweepy.Status`: target status object.
            Returns:
                if passed object satisfies rules, return `True`.
        """

        # -- フィルタリングに使う要素を取得 --

        # リプライかどうか
        is_status_reply = status.in_reply_to_user_id is not None

        # 自分へのリプライかどうか
        is_status_reply_to_myself = is_status_reply and status.in_reply_to_user_id == status.user.id

        # リツイートかどうか
        is_status_retweet = hasattr(status, "retweeted_status")

        # ツイート後の経過時間
        delta_date = (datetime.utcnow() - status.created_at)
        delta_second = delta_date.total_seconds()
        delta_day = delta_date.days

        # fav数, RT数
        favorite_count = status.favorite_count
        retweet_count = status.retweet_count

        # メディアエンティティの数
        entities_count = len(status.extended_entities["media"]) if hasattr(
            status, "extended_entities") else 0

        # -- フィルタリング処理 --

        # メディアエンティティを持たず
        # 自分以外へのリプライでなく
        # fav数が5、RT数が1を下回るツイートは
        # 消す
        if entities_count == 0\
           and ((not is_status_reply) or is_status_reply_to_myself)\
           and favorite_count < 4 and retweet_count < 1:
            return True

        return False
