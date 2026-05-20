import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    """Load and return the list of clubs from the clubs.json file."""
    with open('clubs.json') as c:
        club_list = json.load(c)['clubs']
        return club_list


def load_competitions():
    """Load and return the list of competitions from the competitions.json file."""
    with open('competitions.json') as comps:
        competition_list = json.load(comps)['competitions']
        return competition_list


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')


@app.route('/show-summary', methods=['POST'])
def show_summary():
    """
    Authenticate a club by email and display its dashboard.

    Looks up the club matching the submitted email. If found, renders the
    welcome page with the club's data and available competitions. Otherwise,
    flashes an error and redirects to the home page.
        """
    for club in clubs:
        if club['email'] == request.form['email']:
            return render_template('welcome.html', club=club, competitions=competitions)

    flash("You do not have access to booking.")
    return redirect(url_for('index'))


@app.route('/book/<competition_name>/<club_name>')
def book(competition_name, club_name):
    """
    Render the booking page for a given competition and club.

    Looks up the competition and club by name. If both are found, renders the
    booking form. If only the club is found, flashes an error and redirects to
    the welcome page. If neither is found, flashes an error and redirects to
    the home page.

    Args:
        competition_name (str): The name of the competition to book.
        club_name (str): The name of the club making the booking.
    """
    found_club = None
    for club in clubs:
        if club['name'] == club_name:
            found_club = club
    found_competition = None
    for competition in competitions:
        if competition['name'] == competition_name:
            found_competition = competition
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    elif found_club and not found_competition:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=found_club, competitions=competitions)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for('index'))


@app.route('/purchase-places', methods=['POST'])
def purchase_places():
    """
    Handle the purchase of places in a competition.

    Validates the number of places requested against the following rules:
    - Cannot exceed the number of remaining places in the competition.
    - Cannot exceed the club's available points.
    - Cannot be more than 12.
    - Cannot be negative.

    If validation passes, deducts the booked places from both the competition
    and the club's points, then renders the welcome page with a success message.
    If validation fails, flashes error messages and re-renders the booking form.
    If the club or competition is not found, flashes an error and redirects
    accordingly.
    """
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
        messages = []
        if booked_places > int(selected_competition['number_of_places']):
            messages.append(f"You can't book this number of places. "
                            f"This competition have {selected_competition['number_of_places']} places remaining.")
        if booked_places > int(selected_club["points"]):
            messages.append(f"You can't book this number of places with your club points. "
                            f"You have {selected_club["points"]} points.")
        if booked_places > 12:
            messages.append("You can't book more than 12 number of places")

        if booked_places < 0:
            messages.append("You can't book a negative number of places")

        if messages:
            for message in messages:
                flash(message)
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


@app.route('/clubs-table')
def clubs_table():
    """Render the clubs table page displaying all clubs and their points."""
    return render_template('clubs_table.html', clubs=clubs)


@app.route('/logout')
def logout():
    """Log out the current user and redirect to the home page."""
    return redirect(url_for('index'))
