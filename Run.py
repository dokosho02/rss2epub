from datetime import datetime
import os
from loguru import logger

from glob import glob


from ePubRSS import RSS
from Journals import journalRSS
from DailyRSS import rssListDaily

# -------------------

def go(link, i):
    # start = datetime.now()

    rss = RSS(
        rssLink=link
    )
    
    rss.rss2json()
    
    if rss.updateNo > 0:
        rss.json2epub()
        # remove images
        # time.sleep(20)
        [ os.remove(i) for i in glob( "*.png") ]
        
        # save update info
        rss.saveUpdateInfo()

    # end = datetime.now()
    # timeDuration = str(end - start).zfill(4)
    # logger.info( 'Time cost -- {}'.format(timeDuration) )
    
    return rss.lastRSS

# --------------------------
def go_try(link, i):
    last_rss = ""
    try:
        last_rss = go(link, i)
    except:
        logger.info("Failed -- {} -- {}".format(i+1, link) )
        if (last_rss!= ""):
            os.remove(last_rss)
            logger.info("{} removed".format(last_rss) )
        last_rss = go(link, i)

# -------------------------------------------

class Run():
    def __init__(self):
        self.rssList = rssList

    def run(self):
        start = datetime.now()

        for i in range( len(self.rssList) ):
            go_try(self.rssList[i], i)

        end = datetime.now()
        timeDuration = str(end - start).zfill(4)
        logger.info( 'Total time -- {}'.format(timeDuration) )



# -------------------------------------


class JournalRun(Run):
    def __init__(self):
        self.rssList = journalRSS

# ----------------------

class DailyRun(Run):
    def __init__(self):
        self.rssList = rssListDaily

# ----------------------
# class WeeklyRun(Run):
#     def __init__(self):
#         self.rssList = rssListWeekly

