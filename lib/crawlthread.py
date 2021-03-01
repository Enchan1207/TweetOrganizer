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
        while True:
            # ツイートを取得して
            statuses = self.crawler.fetch_tweets()

            # フィルタにかかった画像を抽出しキューに追加
            for status in statuses:
                if self.status_filter.should_delete(status):
                    self.queue.put(status)

            # APIリミット待ち
            if self.endreq_event.wait(1.1):
                print("Endreq accepted. end processing...")
                break

            time.sleep(1)

        print("[CrawlThread: process finished]")

