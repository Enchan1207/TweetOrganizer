#
# 伸びなかったツイートをアーカイブして自動削除
#
from lib.eliminator import Eliminator
from lib.crawler import Crawler
from lib.eliminatethread import EliminateThread
from lib.statusqueue import StatusQueue

import os, sys, threading
import dotenv, tweepy

from lib.crawlthread import CrawlThread

endreq_event = threading.Event()

def main():
    # .envか実行引数からアクセストークンを取得
    if dotenv.load_dotenv():
        consumer_key = os.getenv("CLIENT_ID")
        consumer_secret = os.getenv("CLIENT_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    elif len(sys.argv) >= 5:
        consumer_key = sys.argv[1]
        consumer_secret = sys.argv[2]
        access_token = sys.argv[3]
        access_token_secret = sys.argv[4]
    else:
        print("\033[31mERROR\033[0m: No credentials has been passed.")
        return

    # アクセストークンを渡してtweepy.apiのインスタンスを生成
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # ログインユーザの情報を吐き出す(auth.status的なものが見つからなかったのでこれで妥協)
    try:
        target_user_object = api.me()
        print(f"Fetch target: {target_user_object.name}(@{target_user_object.screen_name})")
    except tweepy.TweepError:
        print("\033[31mERROR\033[0m: Couldn't get user object.Make sure whether you have passed a valid token.")
        return
    
    # ツイート収集・削除を行うスレッドをそれぞれ起動し、キューを直結
    tweetqueue = StatusQueue()
    crawlthread = CrawlThread(Crawler(api), tweetqueue, endreq_event)
    eliminatethread = EliminateThread(Eliminator(api), tweetqueue, endreq_event)
    crawlthread.start()
    eliminatethread.start()
    print("Process started.")

    try:
        crawlthread.join()
        eliminatethread.join()
    except KeyboardInterrupt:
        print("Ctrl+C")
        endreq_event.set()
        crawlthread.join()
        eliminatethread.join()
    
if __name__ == "__main__":
    main()
