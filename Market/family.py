from flask import request, redirect, url_for, flash , Blueprint , render_template
from .models import User, Family , UserFamilies , Notification
from . import db
from flask_login import current_user , login_required


family = Blueprint("family",__name__)


@family.route('/family_view')
@login_required
def family_view():
    families = Family.query.join(UserFamilies).filter(UserFamilies.user_id == current_user.id).all()
    return render_template('family.html',families=families)


@family.route('/view_family/<int:family_id>', methods=["GET"])
@login_required
def view_family(family_id):
    family = Family.query.get_or_404(family_id)
    family_members = family.users
    return render_template('view_family.html', family=family, family_members=family_members)




@family.route('/create_family', methods=["GET", "POST"])
@login_required
def create_family():
    if request.method == 'POST':
        family_name = request.form.get('family_name')


        new_family =Family(family_name=family_name)
        db.session.add(new_family)
        db.session.commit()

        flash('Family created successfully !', category='success')
        return redirect(url_for('family.family_view'))
    
    families = Family.query.all()
    return render_template('family.html', families=families)

@family.route('/delete_family/<int:family_id>',methods=["GET", "POST"])
@login_required
def delete_family(family_id):
    family = Family.query.get_or_404(family_id)

    db.session.delete(family)
    db.session.commit()
    flash("Family deleted!", category="success")
    return redirect(url_for('family.family_view'))

@family.route('/add_user_family/<int:family_id>', methods=["GET", "POST"])
@login_required
def add_user_family(family_id):
    if request.method == "POST":
        username = request.form.get('username')

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("User not found", category='error')
            return redirect(url_for('family.family_view'))
        
        family = Family.query.get_or_404(family_id)
        if user in family.users:
            flash("User is already a member of this family", category='error')
            return redirect(url_for('family.family_view'))
        family.users.append(user)  
        db.session.commit()

        flash("User added to family successfully!", category="success")
        return redirect(url_for('family.family_view'))
    
@family.route('/notification/<int:family_id>/<int:user_id>', methods=["POST"])
@login_required
def notification(family_id, user_id):
    if request.method == "POST":
        notif_message = request.form.get("notif")

        user = User.query.get_or_404(user_id)
        family = Family.query.get_or_404(family_id)

        new_notification = Notification(message=notif_message, user_id=user.id)
        db.session.add(new_notification)
        db.session.commit()

        flash("Notification sent successfully!", "success")
        return redirect(url_for('family.view_family', family_id=family.id))

@family.route('/notification_view', methods=["POST", "GET"])
@login_required
def notifications():

    messages = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.date_created.desc()).all()

    return render_template('notif.html', messages=messages)