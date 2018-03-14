import json
import sys

from lxml import etree
import requests


_, year = sys.argv

base_url = 'http://games.espn.com/tournament-challenge-bracket/{year}/en/nationalBracket'
url = base_url.format(year=year)
page = requests.get(url)

tree = etree.HTML(page.text)
script, = tree.xpath('//div[@id="global-viewport"]/following::script[1]')
data = script.text.partition('scoreboard_teams = [')[2].partition(']')[0]

sys.stdout.write('[{}]'.format(data))
