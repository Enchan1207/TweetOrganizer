#
# statusfilter.py: 削除対象のツイートか判定する
#
from typing import Optional
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


        return False
