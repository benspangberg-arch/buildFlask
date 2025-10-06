from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def benMovies():
    return render_template( 'benSite.html')



@app.route('/aboutme')

def aboutMe():
    return render_template("aboutme.html")