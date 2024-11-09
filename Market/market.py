from flask import Blueprint , Flask , render_template

market = Blueprint('market',__name__)

@market.route('/market')
def market_page():
    items = [
        {'id':1,'name':'Phone', 'barcode':'213984219', 'price':500 },
        {'id':2,'name':'Laptop', 'barcode':'512132119', 'price':900}
    ]
    return render_template('market.html', items=items)