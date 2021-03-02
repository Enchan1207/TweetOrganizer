#
# eliminatethread.py - ツイート削除スレッド
#
from lib.statusqueue import StatusQueue
import threading
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
                create_date_str = status.created_at.strftime("%Y/%m/%d %H:%M:%S")
                status_id = status.id
                sliced_text = status.text[:30].replace("\n", " ")
                status_description = f"@{status.user.screen_name} at {create_date_str}: \n\t{sliced_text}… \n\t(identifier: {status_id} {status.favorite_count} likes, {status.retweet_count} RT)"
                print(status_description)
                self.eliminator.eliminate(status)

            # APIリミット対策 兼 スレッド終了リクエストの受理
            if self.endreq_event.wait(1):
                print("Endreq accepted. end processing...")
                break

        print("[EliminateThread: process finished]")

