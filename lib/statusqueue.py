#
# statusqueue.py: カスタムキュー(queue.Emptyを握り潰すだけのクソ実装)
#
import queue
from typing import Optional

import tweepy

class StatusQueue(queue.Queue):

    def get_status(self, block: bool = False, timeout: Optional[float] = None) -> Optional[tweepy.Status]:
        """ Get tweet object in queue.

            Args:
                block `bool`: whether this method blocks thread
                timeout `float?`: time limit for blocking thread
            Returns:
                tweet object (`tweepy.Status`) or `None`
        """
        try:
            return self.get(block, timeout)
        except queue.Empty:
            return None

    def put_status(self, status: tweepy.Status, block: bool = False, timeout: Optional[float] = None) -> bool:
        """ Put tweet object in queue.

            Args:
                status `tweepy.Status`: tweet object to put
                block `bool`: whether this method blocks thread
                timeout `float?`: time limit for blocking thread
            Returns:
                bool (if queue is not Full, return `True`)
        """
        try:
            self.put(status, block, timeout)
            return True
        except queue.Full:
            return False
