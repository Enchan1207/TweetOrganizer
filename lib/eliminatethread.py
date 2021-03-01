#
# eliminatethread.py - ツイート削除スレッド
#
from lib.statusqueue import StatusQueue
import threading, time, queue
from lib.eliminator import Eliminator

class EliminateThread(threading.Thread):

    def __init__(self, crawler: Eliminator, queue: StatusQueue, endreq_event: threading.Event):
        self.eliminator = crawler
        self.queue = queue
        self.endreq_event = endreq_event
        super(EliminateThread, self).__init__()

    def run(self):
        while True:
            # キューからツイートを取得できたら
            status = self.queue.get_status()
            if status is not None:
                # 消す
                self.eliminator.eliminate(status)

            # APIリミット対策 兼 スレッド終了リクエストの受理
            if self.endreq_event.wait(1):
                print("Endreq accepted. end processing...")
                break

        print("[EliminateThread: process finished]")

