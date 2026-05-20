from locust import HttpUser, task

email = "john@simplylift.co"
competition = "Spring Festival"
club = "Simply Lift"


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("/")

    @task
    def login(self):
        self.client.post("/show-summary", {"email": email})

    @task
    def book(self):
        self.client.get(f"/book/{competition}/{club}")

    @task
    def purchase_places(self):
        self.client.post("/purchase-places", {"competition_name": competition, "club_name": club, "places": 1})

    @task
    def logout(self):
        self.client.get("/logout")

    @task
    def clubs_table(self):
        self.client.get("/clubs-table")
