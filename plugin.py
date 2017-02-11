'''
plugin.py
Author: Alvin Charles, https://github.com/avncharlie
Description: This is a Flashlight plugin that shows either the latest or a
random xkcd comic in the Spotlight preview window. When enter is pressed in
Spotlight, the currently viewed comic is opened with the default webbrowser.
'''
import urllib2
import json
import time
import random
import os

def xkcdImageRetriever(random_comic=False):
    '''Return requested info through xkcd's JSON interface'''
    info = json.loads(urllib2.urlopen('https://xkcd.com/info.0.json').read())

    if random_comic:
        comic_num = random.randint(1, info['num'])
        info = json.loads(urllib2.urlopen('https://xkcd.com/' \
            + str(comic_num) + '/info.0.json').read())

    return info

def results(fields, original_query):
    '''Return generated html with requested comic and title'''
    text = fields['~text']

    if 'latest' in original_query.lower():
        title = 'latest xkcd'
        info = xkcdImageRetriever()
        run_args = 'http://xkcd.com'

    else:
        title = 'random xkcd'
        info = xkcdImageRetriever(random_comic=True)
        run_args = 'http://xkcd.com/' + str(info['num']) + '/'


    comic_info = 'Comic number ' + str(info['num']) + ': ' + info['title']

    heading_styles = ["font-family:Helvetica", "font-size:20px", \
        "font-weight:800", "text-align:center", "font-variant:small-caps"]

    html = '<p style="' + ';'.join(heading_styles) + '">' \
            + comic_info + '</p>' + '<img src=' + info['img'] + '>'

    return {
        "title": title,
        "run_args": [run_args],
        "html": html
    }

def run(url):
    '''Open current comic in defualt webbrowser'''
    os.system('open "{0}"'.format(url))
