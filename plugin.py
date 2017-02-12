'''
plugin.py
Author: Alvin Charles, https://github.com/avncharlie
Description: This is a Flashlight plugin that shows either the latest or a
random xkcd comic in the Spotlight preview window. When enter is pressed in
Spotlight, the currently viewed comic is opened with the default webbrowser.
'''
import urllib2
import json
import datetime
import random
import os

def xkcdImageRetriever(random_comic=False):
    '''Return requested info through xkcd's JSON interface'''
    info_cache = 'xkcd'+datetime.datetime.now().strftime("%Y.%m.%d")+'.json'
    info_address = 'https://xkcd.com/info.0.json'

    cache_cleanup(info_cache)

    # If there is a cached json, read from it. Otherwise make get the json 
    # and make the cache. Caches is made once a day.
    if info_cache in ''.join(os.listdir('.')):
        info = json.load(open(info_cache, 'r'))

    else:
        xkcd_json = urllib2.urlopen(info_address).read()
        info = json.loads(xkcd_json)

        f = open(info_cache, 'w')
        f.write(xkcd_json)
        f.close()

    if random_comic:
        comic_num = random.randint(1, info['num'])
        info = json.loads(urllib2.urlopen('https://xkcd.com/' \
            + str(comic_num) + '/info.0.json').read())

    return info

def cache_cleanup(info_cache):
    '''Delete all caches not being used'''
    for file in os.listdir('.'):
        if file[:4] == 'xkcd' and file[-4:] == 'json' and file != info_cache:
            os.remove(file)

def results(fields, original_query):
    '''Identify needed information and retrieve resources to present it'''
    text = fields['~text']
    settings = json.load(open('preferences.json'))
    random_comic = False

    if 'latest' in original_query.lower():
        title = 'latest xkcd'
        info = xkcdImageRetriever()
        run_args = 'http://xkcd.com'

    else:
        title = 'random xkcd'
        random_comic = True
        info = xkcdImageRetriever(random_comic=random_comic)
        run_args = 'http://xkcd.com/' + str(info['num']) + '/'

    html = gen_html(info, settings, random_comic)

    return {
        "title": title,
        "run_args": [run_args],
        "html": html,
        "webview_transparent_background": True
    }

def gen_html(info, settings, random):
    '''Based on given information and settings, return generated html'''
    if settings['view'] == 'minimalistic':
        comic_info = 'Comic number ' + str(info['num']) + ': ' \
            + info['title']
    
        heading_styles = ["font-family:Helvetica", "font-size:20px", \
            "font-weight:800", "text-align:left", \
            "font-variant:small-caps", "padding-top:10px"]
    
        alt_text_styles = ["font-family:Helvetica", "font-size:20px", \
            "font-weight:500", "text-align:left", "font-variant:small-caps"]
    
        html = '<p style="' + ';'.join(heading_styles) + '">' \
                + comic_info + '</p>' + '<img src=' + info['img'] + '>' 
    
        if settings['alt_text']:
            html += '<p style="' + ';'.join(alt_text_styles) + '">' + \
                info['alt'] + '</p>'

    else:
        link = 'http://m.xkcd.com'
        if random:
            link += '/' + str(info['num']) + '/'

        html = '''
        <script>
            setTimeout(function() {
              window.location = ''' + "'" + link + "'" + '''
            }, 500);
        </script>'''

    return html
   

def run(url):
    '''Open current comic in defualt webbrowser'''
    os.system('open "{0}"'.format(url))
