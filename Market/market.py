from flask import Blueprint , Flask , render_template , request , flash
from . import db
from .models import Item


market = Blueprint('market',__name__)

@market.route('/market',methods=['POST' , 'GET'])
def market_page():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('item_price')
        barcode = request.form.get('barcode')
        desc = request.form.get('desc')

        new_item = Item(name=name , price=price, barcode=barcode, description=desc)
        db.session.add(new_item)
        db.session.commit()

        flash("Item Added Successfully", category='success')

    items = Item.query.all()
    
    return render_template('market.html',items=items)