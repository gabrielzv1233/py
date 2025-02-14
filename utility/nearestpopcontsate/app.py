from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GEONAMES_USERNAME = "gabrielzv1233"  # Replace with your GeoNames username

# Variables to store the lowest population
lowest_country = None
lowest_state = None


def get_countries():
    """Fetch all countries with their populations."""
    url = "http://api.geonames.org/countryInfoJSON"
    params = {"username": GEONAMES_USERNAME}
    response = requests.get(url, params=params)
    data = response.json()
    return [
        {"name": country["countryName"], "population": int(country["population"])}
        for country in data.get("geonames", [])
        if "population" in country and int(country["population"]) > 0
    ]


def get_states():
    """Fetch all states in the United States with their populations."""
    url = "http://api.geonames.org/childrenJSON"
    params = {"geonameId": 6252001, "username": GEONAMES_USERNAME}  # US geonameId
    response = requests.get(url, params=params)
    data = response.json()
    return [
        {"name": state["name"], "population": int(state["population"])}
        for state in data.get("geonames", [])
        if "population" in state and int(state["population"]) > 0
    ]


def find_closest_under(target, locations):
    """Find the closest location under the target population."""
    closest = None
    closest_diff = float("inf")

    for loc in locations:
        diff = target - loc["population"]
        if 0 <= diff < closest_diff:  # Must be under the target
            closest = loc
            closest_diff = diff

    return closest


@app.route("/")
def index():
    """Serve the homepage with the disclaimer and lowest population data."""
    global lowest_country, lowest_state

    if lowest_country is None or lowest_state is None:
        # Fetch data only once when the server starts
        countries = get_countries()
        states = get_states()
        lowest_country = min(countries, key=lambda x: x["population"])
        lowest_state = min(states, key=lambda x: x["population"])

    disclaimer = (
        "Due to factors no one can truly control, population data is an estimate, "
        "may not be exact, and could be out of date."
    )

    return render_template(
        "index.html",
        disclaimer=disclaimer,
        lowest_country=lowest_country,
        lowest_state=lowest_state,
    )


@app.route("/check", methods=["POST"])
def check_population():
    """Handle live population checks based on user input."""
    data = request.get_json()
    target_population = data.get("population")

    # Get live data
    countries = get_countries()
    states = get_states()

    closest_country = find_closest_under(target_population, countries)
    closest_state = find_closest_under(target_population, states)

    response = {
        "closest_country": closest_country,
        "closest_state": closest_state,
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
