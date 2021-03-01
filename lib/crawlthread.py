#
# crawlthread.py - ツイート収集スレッド
#
from lib.statusfilter import StatusFilter
from lib.statusqueue import StatusQueue
import threading, time
from lib.crawler import Crawler

class CrawlThread(threading.Thread):

    def __init__(self, crawler: Crawler, queue: StatusQueue, endreq_event: threading.Event):
        self.crawler = crawler
        self.queue = queue
        self.endreq_event = endreq_event
        self.status_filter = StatusFilter()
        super(CrawlThread, self).__init__()

    def run(self):
        # ツイートを取得して
        statuses = self.crawler.fetch_tweets()

        # フィルタにかかったツイートを抽出し削除キューに追加
        candidate_statuses = list(filter(lambda status: self.status_filter.should_delete(status), statuses))
        for status in candidate_statuses:
            self.queue.put(status)

        # 出力
        print(f"{len(statuses)} tweets was fetched, and {len(candidate_statuses)} tweets will be removed.")

        print("[CrawlThread: process finished]")

