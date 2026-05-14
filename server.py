import json
from flask import Flask,render_template,request,redirect,flash,url_for


def load_clubs():
    with open('clubs.json') as c:
         club_list = json.load(c)['clubs']
         return club_list


def load_competitions():
    with open('competitions.json') as comps:
         competition_list = json.load(comps)['competitions']
         return competition_list


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def show_summary():
    for club in clubs:
        if club['email'] == request.form['email']:
            return render_template('welcome.html',club=club,competitions=competitions)
    return render_template('index.html', message="You do not have access to booking.")



@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))