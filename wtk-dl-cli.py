#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wtk download
# version 0.1
# author: Bohdan Bobrowski bohdan@bobrowski.com.pl

import pycurl
import re
import sys
import urllib2

class WWWDownloader:
    def __init__(self):
        self.contents = ''
    def body_callback(self, buf):
        self.contents = self.contents + buf

def DownloadWebPage(url):
    try:
        www = WWWDownloader()
        c = pycurl.Curl()        
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION, www.body_callback)
        c.setopt(c.HEADER, 1);
        c.setopt(c.FOLLOWLOCATION, 1)
        c.setopt(c.COOKIEFILE, '')
        c.setopt(c.CONNECTTIMEOUT, 30)
        c.setopt(c.TIMEOUT, 30)
        c.setopt(c.COOKIEFILE, '')
        c.perform()
    except Exception, err:
        print "- Connection error."
        print err
        exit()
        www_html = ''            
    else:
        www_html = www.contents
    return www_html

if len(sys.argv) > 1:
    www_html = DownloadWebPage(sys.argv[1])
    video_id = re.findall('<img src="graphics_new/video/embed.png" class="embed_button" id="embeed_video_[0-9]*-([0-9]*)-[0-9]*" alt="embed" />',www_html);
    if len(video_id) > 0:
        for id in video_id:
            vid_html = DownloadWebPage('http://play.wtk.insys.pl/video/'+str(id));
            video_mp4 = re.findall('<title>([^<]*)</title>',vid_html)
            video_url = re.findall('"(http://[0-9a-zA-Z\.\/\-_]*.mp4)"',vid_html)
            if len(video_mp4) > 0 and len(video_url) > 0:
                video_mp4 = str.lower(video_mp4[0].replace('WtkPlay | ','').replace('_','-'))+".mp4"
                video_url = video_url[0]
                # print video_url
                # print video_mp4
                u = urllib2.urlopen(video_url)
                f = open(video_mp4, 'wb')
                meta = u.info()
                file_size = int(meta.getheaders("Content-Length")[0])
                print("Pobieranie: {0} Rozmiar: {1}".format(video_url, file_size))            
                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break
                    file_size_dl += len(buffer)
                    f.write(buffer)
                    p = float(file_size_dl) / file_size
                    status = r"{0}  [{1:.2%}]".format(file_size_dl, p)
                    status = status + chr(8)*(len(status)+1)                
                    sys.stdout.write(status)
                f.close()
