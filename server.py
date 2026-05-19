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

    flash("You do not have access to booking.")
    return redirect(url_for('index'))


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
    elif found_club and not found_competition:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=found_club, competitions=competitions)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for('index'))


@app.route('/purchase-places',methods=['POST'])
def purchase_places():
    selected_competition = None
    for competition in competitions:
        if competition['name'] == request.form['competition_name']:
            selected_competition = competition
    selected_club = None
    for club in clubs:
        if club['name'] == request.form['club_name']:
            selected_club = club
    booked_places = int(request.form['places'])

    if selected_club and selected_competition:
        if booked_places > int(selected_competition['number_of_places']):
            flash(f"You can't book this number of places. "
                  f"This competition have {selected_competition['number_of_places']} places remaining.")
            return render_template('booking.html',
                                   club=selected_club, competition=selected_competition)
        elif booked_places > int(selected_club["points"]):
            flash(f"You can't book this number of places with your club points. "
                  f"You have {selected_club["points"]} points.")
            return render_template('booking.html',
                                   club=selected_club, competition=selected_competition)
        elif booked_places > 12:
            flash("You can't book more than 12 number of places")
            return render_template('booking.html',
                                   club=selected_club, competition=selected_competition)
        elif booked_places < 0:
            flash("You can't book a negative number of places")
            return render_template('booking.html',
                                   club=selected_club, competition=selected_competition)
        else:
            selected_competition['number_of_places'] = int(selected_competition['number_of_places']) - booked_places
            selected_club["points"] = int(selected_club["points"]) - booked_places
            flash('Great-booking complete!')
            return render_template('welcome.html', club=selected_club, competitions=competitions)

    elif selected_club and not selected_competition:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=selected_club, competitions=competitions)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for('index'))

# Gestion sauvegarde des fichiers json

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))