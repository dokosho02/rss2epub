from util import replaceImageLinks
from ebooklib import epub
from loguru import logger


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
