from flask import Blueprint


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def index():
    return 'HI'
