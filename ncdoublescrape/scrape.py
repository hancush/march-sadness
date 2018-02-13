import json
import os

from lxml import etree
import requests


class Command(object):
    name = 'scrape'
    description = 'get the data to impress your friends'

    def __init__(self, subparsers):
        self.subparser = subparsers.add_parser(self.name, description=self.description)

        self.subparser.add_argument(
            '--colors', action='store_true', default=False,
            help='scrape team colors from https://teamcolorcodes.com/ncaa-color-codes/'
        )

        self.subparser.add_argument(
            '--bpi', action='store_true', default=False,
            help='scrape team power index from http://www.espn.com/mens-college-basketball/bpi/_/view/bpi'
        )

        self.subparser.add_argument(
            '--seeds', nargs='?', const='2017',
            help='scrape seeds, bpi, & color blob for the given year from http://games.espn.com/tournament-challenge-bracket/YEAR/en/nationalBracket'
        )

        self.subparser.add_argument(
            '--datadir', default='scraped',
            help='directory in which to stash scraped stuff'
        )

    def _make_if_not_exists(self, datadir):
        if not os.path.isdir(datadir):
            os.makedirs(datadir)

    def _write_json(self, filename, content):
        with open(filename, 'w') as f:
            f.write(json.dumps(content))

    def _parse_color_style(self, style_str):
        '''
        Accept an inline style string, i.e., 'background-color: #9e1b32; color:
        white; border-bottom: 4px solid #828A8f; text-shadow: 1px 1px #828A8f;',
        and return a dict of style / value pairs.
        '''
        properties = style_str.split(';')
        key_val = [p.split(':') for p in properties if all(p.split(':'))]
        return {key[0].strip(): key[1].strip() for key in key_val}

    def team_colors(self):
        page = requests.get('https://teamcolorcodes.com/ncaa-color-codes/')
        tree = etree.HTML(page.text)
        teams = [
            (a.text, self._parse_color_style(a.attrib['style']))
            for a in tree.xpath('//a[@class="team-button"]')
        ]

        team_colors = []

        for team, style in teams:
            team_colors.append({
                'team': team,
                'primary_color': style['background-color'],
                'secondary_color': style['border-bottom'].split(' ')[-1],
            })

        return team_colors

    def _get_text(self, cell):
        link = cell.find('a/span')
        if link:
            return link.find('span').text, link.find('abbr').text
        else:
            return cell.text

    def _parse_data_table(self, page):
        tree = etree.HTML(page.text)
        table_rows = tree.xpath('//table[@class="bpi__table"]/tbody/tr')

        rows = []

        for row in table_rows:
            data = []
            for td in row.iterchildren('td'):
                text = self._get_text(td)
                if type(text) == tuple:  # team name / team abbreviation
                    data += [*text]
                else:
                    data.append(text)
            rows.append(data)

        return rows

    def team_bpi(self):
        base_url = 'http://www.espn.com/mens-college-basketball/bpi/_/view/bpi/'

        page = requests.get(base_url)
        tree = etree.HTML(page.text)
        last_page = tree.xpath('//ul[@class="pagination"]/li/a')[-2].text

        data = []

        fields = ['rank', 'team', 'abbreviated_team', 'conference', 'record',
                  'offensive_bpi', 'defensive_bpi', 'bpi']

        for i in range(1, int(last_page) + 1):
            page = requests.get(base_url + 'page/{}'.format(i))
            rows = self._parse_data_table(page)
            for row in rows:
                data.append(dict(zip(fields, row)))

        return data

    def team_seeds(self, year=2017):
        base_url = 'http://games.espn.com/tournament-challenge-bracket/{year}/en/nationalBracket'

        page = requests.get(base_url.format(year=str(year)))
        tree = etree.HTML(page.text)

        script, = tree.xpath('//div[@id="global-viewport"]/following::script[1]')
        data = script.text.partition('scoreboard_teams = [')[2].partition(']')[0]

        return json.loads('[{}]'.format(data))

    def handle(self, args, other):
        self._make_if_not_exists(args.datadir)

        if args.colors:
            colors = self.team_colors()
            self._write_json(os.path.join(args.datadir, 'colors.json'), colors)

        if args.bpi:
            bpi = self.team_bpi()
            self._write_json(os.path.join(args.datadir, 'bpi.json'), bpi)

        if args.seeds:
            year = args.seeds
            seeds = self.team_seeds(year)
            self._write_json(os.path.join(args.datadir, 'seeds.json'), seeds)
