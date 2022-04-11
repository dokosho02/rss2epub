import feedparser
from datetime import datetime
from tqdm import tqdm
import json, codecs
import re, os, io, sys
from glob import glob
from loguru import logger
import time

import urllib
from PIL import Image
from ebooklib import epub

from Style import Style


homePath = os.path.expanduser('~')


"""
created on 2021-03-21

"""

def readJsonContent(jsonFile, mode="r"):
    f = codecs.open(jsonFile, mode, encoding='utf-8')

    k = f.readlines()
    g = ''.join( k )
    f.close()

    list_data = json.loads(g)
    return list_data

def checkASCII(s):
    return all(ord(c) < 128 for c in s)

def replaceImageLinks(text, articleNo):
    # <img alt=\"\u4e0d\u89c1\u56fe \u8bf7\u7ffb\u5899\" src=\"https://lh5.googleusercontent.com/At9Xef32Ry42u9eNuLjSOyuQ6bBUWLPNDWdoPr5tGAZx9zScNK42JOuKRBBTZ_2sIelVgeLELny6DukSeXQI2rZE1ITkgnHnpjcjdfiBGr1WwC0XI7M_mvFKdLwTyBzAW8BAtOARq6s\" />
    srcStr = 'src="(.*?)"'
    # imgStr = '<img(.*?)/>'

    txt2 = text
    temp = re.findall(srcStr, txt2)
    pathLocals = []

    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36')

    for i in tqdm( range( len(temp) ) ):
        # fileName, fileExt = os.path.splitext(temp[i])
        fileExt = ".png"
        # pathLocal = os.path.join( homePath , "{0}_{1}{2}".format( str(articleNo).zfill(3), str(i+1).zfill(3), fileExt ) )
        pathLocal = "{0}_{1}{2}".format( str(articleNo).zfill(3), str(i+1).zfill(3), fileExt )

        logger.trace(temp[i])

        # replace non-ascii characters
        k = temp[i]
        for j in temp[i]:
            if (checkASCII(j) == False):
                k = k.replace(j, urllib.parse.quote(j) )

        logger.trace(k)
        try:
            filename, headers = opener.retrieve(k, pathLocal)
        except:
            logger.debug("download failed...")
        pathLocals.append(pathLocal)
        txt2 = txt2.replace(temp[i], pathLocal)

    return (txt2, pathLocals)

# -------------------------

class RSS():
    def __init__(self,rssLink,rssHubLink=""):
        self.rssLink    = rssLink
        self.rssHubLink = rssHubLink
        self.lastFolder = "last"
        self.jsonFolder = "json"
        self.epubFolder = "epub"
        self.lastRSS    = "" 
        for i in [self.lastFolder, self.jsonFolder, self.epubFolder]:
            if (os.path.exists(i) ==False ):
                os.mkdir(i)



    def rss2json(self):
        # store rss information as beautiful json file
        self.feed = feedparser.parse(self.rssLink)
        self.feedSaved = feedparser.parse(self.rssLink)
        self.getUpdateTime()

        self.feedTitle = ( self.feed['feed']['title'].split(' - ') )[0]
        
        z = len( self.feed['entries'] )
        logger.success("- "*2 + self.feedTitle)
        logger.info(self.rssLink)
        logger.success("-"*2 + " entries in this feed ---- {}".format( z ) )

        self.lastRSS = os.path.join( self.lastFolder, 'last_' + self.feedTitle + '.json')
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
            self.storeRSS = os.path.join(self.jsonFolder, self.feedTitle + '-' + self.feedTime + '.json')
            f = codecs.open(self.storeRSS, 'w', encoding='utf-8')        
            f.write(feedJson)
            f.close()
    
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

    def saveUpdateInfo(self):
        f = codecs.open(self.lastRSS, 'w', encoding='utf-8')        
        f.write(json.dumps(self.feedSaved, indent=4))
        f.close()
    
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

# ----------------------

class Article():
    def __init__(self, book, chapters, jsonContent,jsonIndex,chapterIndex, cssStyle):
        self.book = book
        self.chapters = chapters
        self.jsonContent = jsonContent
        self.index = jsonIndex
        self.j = chapterIndex
        self.css = cssStyle

        i = self.index
        self.title = jsonContent['entries'][i]['title']
        logger.trace(self.title)

        try:
            self.author = dictData['entries'][i]['author']
        except:
            self.author = ""

    def generateContent(self):
        i = self.index
        c1 = epub.EpubHtml(
            title    = self.title,
            file_name= self.title.replace(' ', '_') + '.xhtml',
            lang     = 'hr'
            )

        titlePart   = '<h1>' + self.title + '</h1>\n'
        authorPart  = '<p>' + self.author + '</p>\n'

        publishDate = ''
        if ('published' in self.jsonContent['entries'][i]):
            publishDate = '<p>' + self.jsonContent['entries'][i]['published'] + '</p>\n'
        
        link = self.jsonContent['entries'][i]['link']
        linkPart = '<p>' + '<a href="{0}">Web</a>'.format(link) + '</p>\n'

        contentPart = ''
        try:
            contentPart = self.jsonContent['entries'][i]['content'][0]['value']
        except:
            logger.debug("no content label, please check the summary label")

        summaryPart = ''
        if contentPart == '':
            summary = self.jsonContent['entries'][i]['summary_detail']['value']
            summaryPart = summary

        textPart = summaryPart + contentPart
        textPart, localImages = replaceImageLinks(textPart, i+1)

        c1.content= titlePart + authorPart + publishDate + linkPart + textPart
        self.book.add_item(c1)
        c1.add_item(self.css)
        
        # load Image file
        for imgPath in localImages:
            try:
                fileName, fileExt = os.path.splitext(imgPath)
                fileExtName = fileExt.lstrip(".")

                img1 = Image.open(imgPath)  # 'image1.jpeg' should locate in current directory for this example
                b = io.BytesIO()
                img1.save(b, fileExtName)
                b_image1 = b.getvalue()

                # define Image file path in .epub
                image1_item = epub.EpubItem(
                    uid=fileName,
                    file_name= os.path.basename(imgPath), 
                    media_type='image/' + fileExtName, 
                    content=b_image1
                    )

                # add Image file
                self.book.add_item(image1_item)
            except:
                logger.debug(imgPath + " may not be an image...")

        self.chapters[self.j] = c1

        return (self.book, self.chapters)

# -------------------

def go(link, i):
    start = datetime.now()
    # logger.success("-"*70 + "    {0}".format(i+1) )

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

# -------------------------------------
rssList = [

    # 'https://www.techradar.com/rss',
    # 'https://rsshub.app/verge',
    # 'http://www.solidot.org/index.rss',              # solidot
    'https://chinadigitaltimes.net/chinese/feed',    # 中国数字时代 (VPN is necessary)
    # 'https://sspai.com/feed',                        # 少数派
    # 'http://www.weiphone.com/rss.xml',               # 威锋网
      'https://rsshub.app/huxiu/article'              # 虎嗅网 首页资讯
]

rssListWeekly = [
    "https://feeds.feedburner.com/bookfere",
    # 'https://feeds2.feedburner.com/programthink'     # 编程随想的博客 (he is said to be arrested by Chinese police)
]

rssListDaily = [
    'https://rsshub.app/dapenti/tugua',              # 喷嚏圖卦
    'http://www.gutenberg.org/cache/epub/feeds/today.rss', # Project Gutenberg Recently Posted or Updated EBooks
    "https://www.haru-no-nihongo.com/blog-feed.xml",  # Haru Japanese Language Podcast 
    # 'https://book.zhishikoo.com/feed',    # 书籍知识库
    # 'https://www.iyd.wang/feed/',          # 爱悦读网
    # 'https://bookzhai.com/feed',           # bookZhai
    'https://biz.trans-suite.jp/feed',               # TRANS.Biz
    'http://koshoken.seesaa.net/index.rdf',          # 京都古書研究会ブログ
   'http://www.kyoto-u.ac.jp/ja/RSS',               # 京都大学
   "https://rsshub.app/zhihu/hotlist",              # 知乎热榜 
   "https://rsshub.app/zhihu/daily",                # 知乎日报
#   "http://feed.williamlong.info/",                 # 月光博客
#   "http://www.weiphone.com/rss.xml",               # 威锋网-首页
   "https://www.pythoncheatsheet.org/latest/feed/", # Python
    "https://www.raywenderlich.com/android/feed/",   # Android
    "https://blog.kotlin-academy.com/feed/",         # kotlin
   'https://rsshub.app/nhk/news_web_easy'           # NHK News
]

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


class DailyRun(Run):
    def __init__(self):
        self.rssList = rssListDaily

class WeeklyRun(Run):
    def __init__(self):
        self.rssList = rssListWeekly



# -------------------------------------------
# if __name__ == '__main__':
#     main()

"""
Todos
- time format   - updated_parsed
- make emoji smaller
- keep the original image extension

"""
