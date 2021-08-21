from flask import Blueprint, render_template
views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')


@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/stock')
def stock():
    return render_template('stockstats.html')

@views.route('/nifty')
def nifty():
    return render_template('nifty.html')

@views.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')
