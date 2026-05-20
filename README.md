# P11 : Python Bug Fixes

Project carried out as part of the development of an application for Güdlft.
The application coordinates strength competitions (deadlifting, strongman) in North America and Australia.

The goal of this project is to fix blocking bugs and add a feature to display club points.

---

## Features

- Authentication: club login via email address
- Dashboard: display of available competitions and club points
- Booking: place reservation for a competition with the following rules:
  - Maximum 12 places per booking
  - Cannot book more places than the club's available points
  - Cannot book more places than the competition's remaining places
  - Cannot book a negative number of places
- Clubs table: public display of clubs and their points
- Logout: return to the home page

---

## Project Structure

```
P11_Python_Testing/

    readme_img/                             # Documentation images
    templates/                              # HTML templates
    tests/                                  # Test directory
        functionals/                            # Functional tests
        integrations/                           # Integration tests
        performance/                            # Performance tests
        units/                                  # Unit tests
        conftest.py                             # Test configuration file
    .coveragerc                             # Coverage report configuration
    .flake8                                 # Flake8 report configuration
    .gitignore                              # Files and folders ignored by git
    clubs.json                              # Clubs database (JSON format)
    competitions.json                       # Competitions database (JSON format)
    pytest.ini                              # Pytest configuration file
    README.md                               # Documentation
    requirements.txt                        # Dependencies
    server.py                               # Application source code
```

---

## Technologies

- Python / Flask : https://flask.palletsprojects.com/en/stable/
- pytest : https://docs.pytest.org/en/stable/
- coverage : https://coverage.readthedocs.io/en/7.14.0/
- locust : https://docs.locust.io/en/stable/
- flake8 : https://flake8.pycqa.org/en/latest/

---

## Conventions 

Naming and style conventions follow PEP8.

---

## Installation

### Prerequisites

- Python 3.10 or newer
- Internet connection

---

### Clone the repository

```bash
git clone https://github.com/duncan-g-hub/P11_Python_Testing.git
cd P11_Python_Testing
```

---

### Create and activate the virtual environment

```bash
python -m venv .venv

# Git Bash
source .venv/Scripts/activate

# Windows CMD / PowerShell
.venv\Scripts\activate
```


---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

### Configure and run the Flask server

Set the application entry point:
```bash
export FLASK_APP=server.py
```

Enable debug mode (optional):
```bash
export FLASK_DEBUG=1
```

Run the server:
```bash
flask run
```

---

## Tests

### Unit tests (tests/units/)
Verify the isolated behavior of each route:
login, logout, booking, purchase, clubs table.
Each nominal case and error case is covered individually.

---

### Integration tests (tests/integrations/)
Verify interactions between components:
for example, that a booking correctly updates the club's points and the competition's remaining places.

---

### Functional tests (tests/functionals/)
Verify end-to-end user flows: login, complete booking, logout.

---

### Performance tests (tests/performance/)
Run with Locust with 6 simultaneous users. Verify that:
- Page load time does not exceed 5 seconds
- Updates (POST) do not exceed 2 seconds

Results:
![results_graph_locust.png](readme_img/results_graph_locust.png)
![results_table_locus.png](readme_img/results_table_locus.png)

---

### Running the tests

Run unit, integration and functional tests:

```bash
pytest
```

Some warnings may be raised. They are related to package version compatibility issues and are suppressed via the pytest.ini file.

Run performance tests (Flask server must be running):

```bash
locust -f tests/performance/locustfile.py
```

Configuration : 
![config_locust.png](readme_img/config_locust.png)
WinError 10048 failures are not related to the application. They are caused by a Windows limitation on TCP port exhaustion under heavy load.
---

### Test coverage

Run the coverage report in the terminal:

```bash
pytest --cov=.
```

Run the coverage report in HTML format:

```bash
pytest --cov=. --cov-report html
```

Results:
![results_coverage.png](readme_img/results_coverage.png)

---

## Code Quality

Run the flake8 analysis:
```bash
flake8
```

---

## Branches 

### Master
Main branch, corresponding to the production state of the application.

---

### bug/error-500-when-logging-with-wrong-email
Used to fix a bug generating a 500 error when logging in with an incorrect email.

---

### bug/available_points_not_deducted
Used to fix a bug preventing club points from being deducted when booking competition places.

---

### bug/missing-conditions-to-use-points
Used to fix bugs related to club point spending conditions:
- A club cannot spend more points than it owns.
- A club cannot spend more points than the number of available places in a competition.
- A club cannot spend more than 12 points per competition.
- A club cannot spend a negative number of points.

---

### feature/table-to-display-clubs-points
Used to add a route allowing the display of each club's points.

---

### QA
Used for code review.

---

## Contact

For any questions:  
Duncan GAURAT - duncan.dev@outlook.fr



