import re, os, io, sys
import json, codecs

import urllib

from tqdm import tqdm
from loguru import logger

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

appHeader = f"{bcolors.HEADER}move files to current folder{bcolors.ENDC}"


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
