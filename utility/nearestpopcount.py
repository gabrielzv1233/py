import requests

GEONAMES_USERNAME = "GeoNames username right here broski"  # Replace with your GeoNames username


def get_countries():
    """Fetch all countries with their populations."""
    url = "http://api.geonames.org/countryInfoJSON"
    params = {"username": GEONAMES_USERNAME}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: API returned status code {response.status_code}")
        print(response.text)
        return []

    try:
        data = response.json()
        return [
            {"name": country["countryName"], "population": int(country["population"])}
            for country in data.get("geonames", [])
            if "population" in country
        ]
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(response.text)
        return []


def get_states(country_code="US"):
    """Fetch all states for a given country with their populations."""
    url = "http://api.geonames.org/childrenJSON"
    params = {"geonameId": 6252001, "username": GEONAMES_USERNAME}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: API returned status code {response.status_code}")
        print(response.text)
        return []

    try:
        data = response.json()
        return [
            {"name": state["name"], "population": int(state["population"])}
            for state in data.get("geonames", [])
            if "population" in state
        ]
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(response.text)
        return []


def find_closest_under(target, locations):
    """Find the closest location under the target population."""
    closest = None
    closest_diff = float("inf")

    for loc in locations:
        diff = target - loc["population"]
        if 0 <= diff < closest_diff:
            closest = loc
            closest_diff = diff

    return closest


def main():
    target_population = int(input("Enter a population number: "))
    print("\nFetching data, please wait...")

    countries = get_countries()
    states = get_states()

    closest_country = find_closest_under(target_population, countries)
    closest_state = find_closest_under(target_population, states)

    print("\nResults:")
    if closest_country:
        print(
            f"The closest country under {target_population} is {closest_country['name']} "
            f"with a population of {closest_country['population']}."
        )
    else:
        print("No country found with a population under the target.")

    if closest_state:
        print(
            f"The closest state under {target_population} is {closest_state['name']} "
            f"with a population of {closest_state['population']}."
        )
    else:
        print("No state found with a population under the target.")


if __name__ == "__main__":
    main()
