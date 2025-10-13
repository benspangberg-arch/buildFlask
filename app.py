from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
app = Flask(__name__)
app.secret_key = 'top-secret'

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'guestlist.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    pokemon = db.Column(db.Text)
    type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

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






@app.route('/admin/profile')
def admin_profiles():
    profiles = Profile.query.all()
    return render_template('Admin_profile.html', profiles=profiles)



@app.route('/admin/feedback')
def admin_feedback():
    feedbacks = Feedback.query.all()
    return render_template('Admin_feedback.html', feedbacks=feedbacks)


      
    #return render_template(
          #  'profileSuccess.html',name=name,email=email,height=height,pokemon=pokemon,type=type,accommodations=accommodations)
   # return render_template('profileForm.html')