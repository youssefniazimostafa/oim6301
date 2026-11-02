import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import requests
    import csv

    return mo, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Section 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This would be something that a droup or club would use to help them plan and coordinate events. It helps them decide the ideal day to plan or create an event. They will get a 7 day table with one day reccomended as the best day.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Section 2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For this project, I'll turn the town name into coordinates using Open-Meteo's geocoding link, making sure to grab the first match in the right state since a few towns share names across Massachusetts. Then I'll use those coordinates to pull a 7-day forecast with highs, lows, rain chance, and wind, all in °F and mph. Since the forecast comes back as separate lists, I'll loop through each day and pull matching values into one row per day, building a table. Each day gets checked against the four rules (high temp range, rain chance, wind), and if any days pass, I'll pick the one with the least rain, breaking ties with lower wind. If no days pass, I'll pick the one that breaks the fewest rules, with ties going to the earlier day. At the end, I'll print the table and a sentence naming the best day. To check my work, I'll count the rows I built and compare that to the number of dates the forecast gave me, they should match at 7.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Section 3: Inputs
    """)
    return


@app.cell
def _():
    place = "Wellesley"
    state = "Massachusetts"
    lowest_high_f = 55
    highest_high_f = 80
    max_rain_chance = 30
    max_wind_mph = 15
    return (
        highest_high_f,
        lowest_high_f,
        max_rain_chance,
        max_wind_mph,
        place,
        state,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Section 4
    """)
    return


@app.cell
def _(requests):
    def get_coordinates(town_name, state_name):
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": town_name, "count": 100, "language": "en", "format": "json"}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        for result in results:
            if result.get("admin1") == state_name:
                return {
                    "name": result["name"],
                    "state": result["admin1"],
                    "latitude": result["latitude"],
                    "longitude": result["longitude"],
                }
        raise ValueError(f"No place named {town_name} found in {state_name}")

    return (get_coordinates,)


@app.cell
def _(get_coordinates, place, state):
    location = get_coordinates(place, state)
    location
    return (location,)


@app.function
def count_broken_rules(day, low_limit, high_limit, rain_limit, wind_limit):
    broken = 0
    if day["high_f"] < low_limit:
        broken += 1
    if day["high_f"] > high_limit:
        broken += 1
    if day["rain_chance"] > rain_limit:
        broken += 1
    if day["wind_mph"] > wind_limit:
        broken += 1
    return broken


@app.cell
def _(requests):
    def get_forecast(latitude, longitude):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "America/New_York",
            "forecast_days": 7,
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        daily = response.json()["daily"]

        days = []
        for date, high, low, rain, wind in zip(
            daily["time"],
            daily["temperature_2m_max"],
            daily["temperature_2m_min"],
            daily["precipitation_probability_max"],
            daily["wind_speed_10m_max"],
        ):
            days.append({
                "date": date,
                "high_f": high,
                "low_f": low,
                "rain_chance": rain,
                "wind_mph": wind,
            })
        return days

    return (get_forecast,)


@app.cell
def _(get_forecast, location):
    forecast = get_forecast(location["latitude"], location["longitude"])
    forecast
    return (forecast,)


@app.cell
def _(forecast, highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph):
    rows = []
    for _day in forecast:
        _broken = count_broken_rules(_day, lowest_high_f, highest_high_f, max_rain_chance, max_wind_mph)
        rows.append({
            "date": _day["date"],
            "high_f": _day["high_f"],
            "low_f": _day["low_f"],
            "rain_chance": _day["rain_chance"],
            "wind_mph": _day["wind_mph"],
            "rules_broken": _broken,
            "passes": _broken == 0,
        })
    rows
    return


if __name__ == "__main__":
    app.run()
