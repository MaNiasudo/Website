from flask import request, redirect, url_for, flash , Blueprint , render_template
from .models import User, Family
from . import db
from flask_login import current_user , login_required


family = Blueprint("family",__name__)


@family.route('/family_view')
def family_view():
    return render_template('family.html')



@family.route('/create_family', methods="POST")
def create_family():
    if request.method == 'POST':
        family_name = request.form.get('family_name')


        new_family =Family(family_name=family_name)
        db.session.add(new_family)
        db.session.commit()

        flash('Family created successfully !', category='success')
        return redirect(url_for('family.family_view'))

@family.route('/delete_family/<int:family_id>',methods="POST")
def delete_family(family_id):
    family = Family.query.get_or_404(family_id)

    db.session.delete(family)
    db.session.commit()
    flash("Family deleted!", category="success")
    return redirect(url_for('family.family_view'))

@family.route('/add_user_family/<int:family_id>', methods=["POST"])
def add_user_family(family_id):
    username = request.form.get('username')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found", category='error')
        return redirect(url_for('family.family_view'))
    
    
    family = Family.query.get_or_404(family_id)
    family.users.append(user)
    db.session.commit()
    
    flash("User added to family successfully!", category="success")
    return redirect(url_for('family.family_view'))



