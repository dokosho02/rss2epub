from datetime import datetime
import os
from loguru import logger

from glob import glob


from ePubRSS import RSS
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
        logger.info(f"Failed -- {i+1} -- {link}")
        if (last_rss!= ""):
            os.remove(last_rss)
            logger.info(f"{last_rss} removed")
        last_rss = go(link, i)

# -------------------------------------------
class Run():
    def __init__(self):
        self.rssList = rssList

    def run(self):
        # start = datetime.now()

        for i in range( len(self.rssList) ):
            go_try(self.rssList[i], i)

        # end = datetime.now()
        # timeDuration = str(end - start).zfill(4)
        # logger.info( 'Total time -- {}'.format(timeDuration) )
# ----------------------
class DailyRun(Run):
    def __init__(self):
        self.rssList = rssListDaily
# ----------------------
# class WeeklyRun(Run):
#     def __init__(self):
#         self.rssList = rssListWeekly

# ----------------------
def main():
    dr = DailyRun()
    dr.run()
# ----------------------
if __name__ == '__main__':
    start = datetime.now()
    print(start)
    # --------------
    main()
    # --------------
    end = datetime.now()
    timeDuration = str(end - start).zfill(4)
    print(end)
    print( 'Total time -- {}'.format(timeDuration) )
