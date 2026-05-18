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

@app.route('/show-summary',methods=['POST'])
def show_summary():
    for club in clubs:
        if club['email'] == request.form['email']:
            return render_template('welcome.html',club=club,competitions=competitions)
    return render_template('index.html', message="You do not have access to booking.")



@app.route('/book/<competition_name>/<club_name>')
def book(competition_name,club_name):
    found_club = None
    for club in clubs:
        if club['name'] == club_name:
            found_club = club
    found_competition = None
    for competition in competitions:
        if competition['name'] == competition_name:
            found_competition = competition
    if found_club and found_competition:
        return render_template('booking.html',club=found_club,competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=found_club, competitions=competitions)


@app.route('/purchase-places',methods=['POST'])
def purchase_places():
    booked_places = int(request.form['places'])

    for competition in competitions:
        if competition['name'] == request.form['competition']:
            competition['number_of_places'] -= booked_places
            selected_competition = competition

    for club in clubs:
        if club['name'] == request.form['club']:
            # club["points"] -= booked_places
            selected_club = club

    flash('Great-booking complete!')
    return render_template('welcome.html', club=selected_club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))