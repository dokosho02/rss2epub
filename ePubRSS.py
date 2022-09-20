import feedparser
from datetime import datetime
from tqdm import tqdm

import json, codecs
import re, os, io, sys
from loguru import logger
import time

from ebooklib import epub

from Style import Style
from Article import Article
from util import readJsonContent, bcolors


homePath = os.path.expanduser('~')

"""
created on 2021-03-21
modified on 2022-09-19
"""

# -------------------------

class RSS():
    def __init__(self,rssLink):
        self.rssLink    = rssLink

        # folders
        self.lastFolder = "last"
        self.jsonFolder = "json"
        self.epubFolder = "epub"
        self.lastRSS    = ""
        
        # 
        self.createFolders()



    # --------------------------
    def createFolders(self):
        for fd in [self.lastFolder, self.jsonFolder, self.epubFolder]:
            if (os.path.exists(fd) == False ):
                os.mkdir(fd)
    # --------------------------
    def rss2json(self):
        print(f"{bcolors.HEADER}{self.rssLink}{bcolors.ENDC}")
        # store rss information as beautiful json file
        self.feed = feedparser.parse(self.rssLink)
        self.feedSaved = feedparser.parse(self.rssLink)

        print( self.feed.keys() )
        # logger.debug(self.feed)

        self.getUpdateTime()

        self.feedTitle = ( self.feed['feed']['title'].split(' - ') )[0]
        
        z = len( self.feed['entries'] )
        print(f"{bcolors.HEADER}{self.feedTitle}{bcolors.ENDC}")
        logger.success("-"*2 + " entries in this feed ---- {}".format( z ) )

        self.lastRSS = os.path.join( self.lastFolder, f"last_{self.feedTitle}.json")
        logger.debug(self.lastRSS)

        # feedTime processing for format
        feedTime  = (self.updateTime.replace(' ', '-') ).replace(':','-')
        self.feedTime = feedTime
        self.keepLatestUpdate()

        self.updateNo = len( self.feed['entries'] )
        logger.success("-"*2 + " update(s) in this feed ---- {}".format( self.updateNo ) )

        if self.updateNo > 0:
            for i in range(self.updateNo):
                title = self.feed['entries'][i]['title']
                print( "{0} -- {1}".format(i+1, title) )

            # save current update content
            feedJson = json.dumps(self.feed, indent=4)
            self.storeRSS = os.path.join(self.jsonFolder, f"{self.feedTitle}-{self.feedTime}.json")
            f = codecs.open(self.storeRSS, 'w', encoding='utf-8')        
            f.write(feedJson)
            f.close()
    # --------------------------
    def getUpdateTime(self):
        updateTime = ''
        tempTime = ""

        # timeLabel = ['update', 'published', 'updated']
        timeLabel = ['update_parsed', 'published_parsed', 'updated_parsed']
        try:
            for lbl in timeLabel:
                if lbl in self.feed['feed']:
                    logger.debug(lbl)
                    logger.debug("Time in feed, not entries...")
                    tempTime = self.feed['feed'][lbl]
                elif lbl in self.feed['entries'][0]:
                    tempTime = self.feed['entries'][0][lbl]
                
                tempTime = list(tempTime)
                logger.debug(tempTime)
                if len(tempTime) > 0:
                    y, m, d, h, mi, s, wd, yd, dst = map(str, tempTime)
                    updateTime = '_'.join( [y.zfill(4), m.zfill(2), d.zfill(2), h.zfill(2), mi.zfill(2), s.zfill(2) ] )

        except:
            updateTime = "today"


        logger.info( "- "*2 +  updateTime )
        self.updateTime = updateTime
    # --------------------------
    def saveUpdateInfo(self):
        f = codecs.open(self.lastRSS, 'w', encoding='utf-8')        
        f.write(json.dumps(self.feedSaved, indent=4))
        f.close()
    # --------------------------
    def keepLatestUpdate(self):
        tp = self.feed

        if os.path.exists(self.lastRSS):
            self.lastJsonContent = readJsonContent(self.lastRSS)
            z = len(self.lastJsonContent['entries'])
            logger.trace(z)
            for i in range( z ):
                title = self.lastJsonContent['entries'][i]['title']
                print("{0} -- {1}".format(i+1, title) )

            duplicateIndex = []
            for i in range( len(self.lastJsonContent['entries']) ):
                for j in range( len(self.feed['entries'])):
                    if (self.lastJsonContent['entries'][i]['title']==self.feed['entries'][j]['title']):
                        duplicateIndex.append(j)
                    # tp['entries'].remove(self.feed['entries'][j])

            logger.debug(duplicateIndex)
            if len(duplicateIndex) > 0:
                duplicateIndex.sort()
                tp['entries']=tp['entries'][: duplicateIndex[0] ]
                logger.info("Removing duplicates...")
                
                # if len(duplicateIndex) == len(self.feed['entries']):
                #     logger.info("No updates...\nKeep the last json file...")
            else:
                logger.info("All are new contents!")
        else:
            logger.info("New last json file will be created...")

        self.feed = tp

    # --------------------------
    def json2epub(self):
        jsonContent = readJsonContent(self.storeRSS)

        self.bookTitle = jsonContent['feed']['title'].split(' - ')[0] + ' (' + self.updateTime + ')'

        book = epub.EpubBook()
        book.set_title(self.bookTitle)
        # book.add_author('Liu Bin Chan')

        # css
        style = Style()
        defaultCSS = epub.EpubItem(
            uid="style_default",
            file_name="style/default.css",
            media_type="text/css",
            content=style.defaultStyle)
        book.add_item(defaultCSS)

        # chapters
        z = range( len( jsonContent['entries'] ) )
        
        logger.debug(z)
        # z=1
        chapters = [""]*len(z)
        logger.info( "{} article(s)".format( len(chapters) )  )

        for j in  range( len(z) ):
            # logger.debug(j)
            k = len(z) - j - 1  # for chapters reversed
            article = Article(book, chapters, jsonContent, z[j], k, defaultCSS)
            book, chapters = article.generateContent()

        # add toc
        chapt_tuple = tuple(chapters)
        book.toc = (chapt_tuple)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # add css file
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css", 
            content=style.secondStyle)
        book.add_item(nav_css)

        # create spin, add cover page as first page
        # book.spine = ['cover', 'nav']
        book.spine = ['nav']
        for i in chapters:
            book.spine.append(i)

        # create epub file
        epubFileName = self.feedTitle.replace(" ", "_").replace("|", "_").replace(",","_").replace(":", "_").replace("__", "_")
        epubFile = os.path.join(self.epubFolder,  epubFileName + '-' + self.feedTime + '.epub')
        epub.write_epub(epubFile, book)


# -------------------------------------------
# if __name__ == '__main__':
#     main()

"""
Todos
- time format   - updated_parsed
- make emoji smaller
- keep the original image extension

"""
