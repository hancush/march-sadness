from flask import Blueprint


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def index():
    return 'HI'


@views.route('/data', methods=['GET'])
def data():
    base_url = 'http://games.espn.com/tournament-challenge-bracket/{year}/en/nationalBracket'

    page = requests.get(base_url.format(year=str(year)))
    tree = etree.HTML(page.text)

    script, = tree.xpath('//div[@id="global-viewport"]/following::script[1]')
    data = script.text.partition('scoreboard_teams = [')[2].partition(']')[0]

    return json.loads('[{}]'.format(data))
