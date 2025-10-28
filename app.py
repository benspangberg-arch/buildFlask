from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime, timezone
app = Flask(__name__)
app.secret_key = 'top-secret'

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'guestlist.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

admin = Admin(app, name='frmstr')

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    pokemon = db.Column(db.Text)
    type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

admin.add_view(ModelView(Profile, db.session))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


with app.app_context():
    db.create_all()

    


@app.route('/')
def index():
    return redirect(url_for('profile'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        height = request.form.get('height', '').strip()
        type = request.form.get('type', '').strip()
        pokemon = request.form.get('pokemon', '').strip()
        # Validation
        if not name or not email or not height or not type:
            error = "Please fill in all required fields"
            return render_template('profileForm.html', error=error)
        
        try:
            new_profile = Profile(
                name=name,
                email=email,
                height=int(height),
                pokemon=pokemon,
                type=type,
            )
            db.session.add(new_profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("DEBUG ERROR:", e)
            error = "An error occured while saving your profile. Please try again."
            return render_template('profileForm.html', error=error)
        
        
        
        
        
        return render_template(
            'profileSuccess.html',name=name,email=email,height=height,pokemon=pokemon,type=type)
    return render_template('profileForm.html')

        
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        rating = request.form.get('rating', '').strip()
        comment_text = request.form.get('feedback', '').strip()
        if not rating:
            error = "Please provide a rating"
            return render_template('feedbackForm.html', error=error)
        
        try:
            new_feedback = Feedback(
                rating=int(rating),
                comment=comment_text
            )
            db.session.add(new_feedback)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = "An error occured while saving your feedback. Please try again" 
            return render_template('feedbackForm.html', error=error)
        return render_template(
                    'feedbackSuccess.html',
                    rating=rating,
                    feedback=comment_text
                )
    return render_template('feedbackForm.html')


@app.route('/admin/feedback/rating_1')
def admin_feedback_rating_1():
    feedbacks = Feedback.query.filter_by(rating=1).all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)

@app.route('/admin/feedback/rating_2')
def admin_feedback_rating_2():
    feedbacks = Feedback.query.filter_by(rating=2).all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)

@app.route('/admin/feedback/rating_3')
def admin_feedback_rating_3():
    feedbacks = Feedback.query.filter_by(rating=3).all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)

@app.route('/admin/feedback/rating_4')
def admin_feedback_rating_4():
    feedbacks = Feedback.query.filter_by(rating=4).all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)

@app.route('/admin/feedback/rating_5')
def admin_feedback_rating_5():
    feedbacks = Feedback.query.filter_by(rating=5).all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)

@app.route('/admin/profiles/AppendComments')
def admin_profiles_appendComments():
    try:
        profiles_to_update = Profile.query.filter_by(accommodations=True).all()
        
        for profile in profiles_to_update:
            profile.pokemon += " - email accommodations form"
        db.session.commit()
        return redirect(url_for('admin_profiles'))
    except Exception as e:
        db.session.rollback()
        error = f"Error updating profiles: {str(e)}"
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles, error=error)

@app.route('/admin/profiles/delete_first')
def admin_profiles_deleteFirst():
    try:
        all_profiles = Profile.query.order_by(Profile.id).all()

        if len(all_profiles) < 1:
            error = "You have no profiles to delete"
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)
        first_profile = all_profiles[0]

        db.session.delete(first_profile)
        db.session.commit()

        return redirect(url_for('admin_profiles'))
    except Exception as e:
        db.session.rollback()
        error = f"Error deleting profile: {str(e)}"
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles,)





@app.route('/admin/profile')
def admin_profiles():
    profiles = Profile.query.all()
    return render_template('Admin_profile.html', profiles=profiles)



@app.route('/admin/feedback')
def admin_feedback():
    feedbacks = Feedback.query.all()
    return render_template('Admin_feedback.html', feedbacks=feedbacks)

@app.route('/admin/profile/deleteButton', methods=['POST'])
def admin_profileDeleteButton():
    try:
        profileId = request.form.get('profileId', '').strip()

        if not profileId:
            error = f"No profile id included for deletion"
            profiles = Profile.query.all()
            return render_template('admin_profile.html)', profile=profiles, error=error)

        profile_to_delete = Profile.query.filter_by(id=profileId).first()

        if not profile_to_delete:
            error = f"No profile id included for deletion"
            profiles = Profile.query.all()
            return render_template('admin_profile.html', profile=profiles, error=error)
        
        db.session.delete(profile_to_delete)

        db.session.commit()

        return redirect(url_for('admin_profile'))
    except Exception as e:
        error = f"Error deleting profile: {str(e)}"
        profiles = Profile.query.all()
        return render_template('admin_profile.html', profiles=profiles, error=error)


      
    #return render_template(
          #  'profileSuccess.html',name=name,email=email,height=height,pokemon=pokemon,type=type,accommodations=accommodations)
   # return render_template('profileForm.html')

@app.route('/admin/profile/edit', methods=['GET', 'POST'])
def admin_profiles_edit():
    if request.method == 'POST':
        profileId = request.form.get("profileId", '', type=int)

        if not profileId:
            error = "No profile id provided."
            profiles = Profile.query.all()
            return redirect(url_for('admin_profiles_edit')+f'?profileId={profileId}', error=error)
        
        profileToUpdate = Profile.query.filter_by(id=profileId).first()

        if not profileToUpdate:
            error = f"No profile with id {profileId} found."
            profiles = Profile.query.all()
            return render_template('admin_profile.html', profiles=profiles, error=error)
        
        try:
            profileToUpdate.name = request.form.get('name', profileToUpdate.name)
            profileToUpdate.email = request.form.get('email', profileToUpdate.email)
            profileToUpdate.height = request.form.get('height', profileToUpdate.height)
            profileToUpdate.type = request.form.get('type', profileToUpdate.type)
            profileToUpdate.pokemon = request.form.get('pokemon', profileToUpdate.pokemon)
            db.session.commit()
            return redirect(url_for('admin_profile'))
        except Exception as e:
            db.session.rollback()
            error = f"Error writing changes to database: {str(e)}"
            profiles = Profile.query.all()
            return render_template("admin_profile.html", profiles=profiles, error=error)

    profileId = request.args.get('profileId')

    if not profileId:
        error = "no profile id provided."
        profiles = Profile.query.all()
        return render_template('admin_profile.html', profiles=profiles, error=error)
    
    profileToEdit = Profile.query.filter_by(id=profileId).first()

    if not profileToEdit:
        error = f"No profile found with id {profileId}."
        profiles = Profile.query.all()
        return render_template('admin_profile.html', profiles=profiles, error=error)
    return render_template('profileEdit.html', profile=profileToEdit)
    

@app.route('/admin/profile/deleteAudaciousGuests')
def admin_profiles_delete_audacious_guests():
    try:
        deleted_count = Profile.query.filter(Profile.height >100 ).delete()
        db.session.commit()

        return redirect(url_for('admin_profiles'))
    except Exception as e:
        db.session.rollback()
        error = f"Error dealing with such audacity: {str(e)}"
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles, error=error)


@app.route('/admin/profiles/deleteQuantity', methods=['POST'])
def admin_profilesDeleteByQuantity():
    try:
        quantity_str = request.form.get('quantity', '').strip()

        if not quantity_str:
            error = "Please enter a quantity"
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)
        
        try:
            quantity = int(quantity_str)
        except ValueError:
            error = "Please enter a valid number"
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)
        profiles_to_delete = Profile.query.filter(Profile.height >= quantity).all()
        if not profiles_to_delete:
            error = f"No profiles found with {quantity} or more guests"
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)

        for profile in profiles_to_delete:
            db.session.delete(profile)
            
            
        db.session.commit()

        return redirect(url_for('admin_profiles'))
    except Exception as e:
        db.session.rollback()
        error = f"Error deleting profiles: {str(e)}"
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles, error=error)
    



