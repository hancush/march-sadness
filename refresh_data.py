import json
import sys

from lxml import etree
import requests

from march_sadness.app_config import YEAR


base_url = 'http://games.espn.com/tournament-challenge-bracket/{year}/en/nationalBracket'
page = requests.get(base_url.format(year=str(YEAR)))

tree = etree.HTML(page.text)
script, = tree.xpath('//div[@id="global-viewport"]/following::script[1]')
data = script.text.partition('scoreboard_teams = [')[2].partition(']')[0]

sys.stdout.write('[{}]'.format(data))
