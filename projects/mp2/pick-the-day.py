import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import requests
    import csv
    import datetime

    return datetime, mo, requests


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
    max_rain_chance = 60
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
    return (rows,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Section 5: The Answer
    """)
    return


@app.cell
def _(location, rows):
    print(f"7-day forecast for {location['name']}, {location['state']}")
    print()
    print(f"{'Date':<12}{'High °F':>9}{'Low °F':>9}{'Rain %':>8}{'Wind mph':>10}{'Passes':>8}")
    print("-" * 56)
    for _row in rows:
        if _row["passes"]:
            _passes = "Yes"
        else:
            _passes = "No"
        print(
            f"{_row['date']:<12}"
            f"{_row['high_f']:>9.1f}"
            f"{_row['low_f']:>9.1f}"
            f"{_row['rain_chance']:>8}"
            f"{_row['wind_mph']:>10.1f}"
            f"{_passes:>8}"
        )
    return


@app.cell
def _(rows):
    passing_days = []
    for _row in rows:
        if _row["passes"]:
            passing_days.append(_row)

    if len(passing_days) > 0:
        best_day = passing_days[0]
        for _row in passing_days:
            if _row["rain_chance"] < best_day["rain_chance"]:
                best_day = _row
            elif _row["rain_chance"] == best_day["rain_chance"] and _row["wind_mph"] < best_day["wind_mph"]:
                best_day = _row
    else:
        best_day = rows[0]
        for _row in rows:
            if _row["rules_broken"] < best_day["rules_broken"]:
                best_day = _row

    best_day
    return best_day, passing_days


@app.cell
def _(best_day, datetime, location, passing_days):
    _day_label = datetime.date.fromisoformat(best_day["date"]).strftime("%A, %B %d")

    if len(passing_days) > 0:
        answer = (
            f"The best day for the event in {location['name']}, {location['state']} is {_day_label}: "
            f"of the {len(passing_days)} days that meet every rule, it has the lowest chance of rain "
            f"({best_day['rain_chance']}%), with a high of {best_day['high_f']:.1f}°F "
            f"and wind up to {best_day['wind_mph']:.1f} mph."
        )
    else:
        answer = (
            f"No day in the next week in {location['name']}, {location['state']} meets every rule. "
            f"The closest is {_day_label}, which breaks {best_day['rules_broken']} rule(s), "
            f"with a high of {best_day['high_f']:.1f}°F, a {best_day['rain_chance']}% chance of rain "
            f"and wind up to {best_day['wind_mph']:.1f} mph."
        )

    print(answer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Section 6: How to know these numbers are right?
    """)
    return


@app.cell
def _(
    highest_high_f,
    location,
    lowest_high_f,
    max_rain_chance,
    max_wind_mph,
    passing_days,
    requests,
    rows,
):
    _raw = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "America/New_York",
            "forecast_days": 7,
        },
        timeout=10,
    ).json()
    _daily = _raw["daily"]

    # Check 1: did I keep every day?
    _days_in_reply = len(_daily["time"])
    print(f"Check 1 - days in raw reply: {_days_in_reply}, rows in my table: {len(rows)}, match: {_days_in_reply == len(rows)}")

    # Check 2: does my first row match the raw reply?
    print(f"Check 2 - first day high in raw reply: {_daily['temperature_2m_max'][0]}, in my table: {rows[0]['high_f']}, "
          f"match: {_daily['temperature_2m_max'][0] == rows[0]['high_f']}")

    # Check 3: count passing days a different way
    _passing_second_way = 0
    for _i in range(_days_in_reply):
        _high = _daily["temperature_2m_max"][_i]
        _rain = _daily["precipitation_probability_max"][_i]
        _wind = _daily["wind_speed_10m_max"][_i]
        if lowest_high_f <= _high <= highest_high_f and _rain <= max_rain_chance and _wind <= max_wind_mph:
            _passing_second_way += 1
    print(f"Check 3 - passing days counted a second way: {_passing_second_way}, from my rules: {len(passing_days)}, "
          f"match: {_passing_second_way == len(passing_days)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To check my work, I built three tests that each verify my table a different way. Check 1 calls the API fresh and counts its dates, comparing that to my row count, since it skips my zip loop, it would catch any day I dropped or duplicated, and it printed True. Check 2 grabs the first day's high temp straight from the raw list by position and compares it to my first row, showing my rows hold the right values, not something scrambled. Check 3 recounts passing days straight from the raw lists, using a position loop instead of zip, and flips the rule logic to ask "is this inside the limits?" instead of my original is this outside the limits? If I'd made a mistake right at a limit, these two versions would disagree, but they matched, printing True. Since three different approaches all landed on the same answer, I'm confident the table is right.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Section 7
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    While building this notebook, I ran into a chain of Error messages things like name mo is not defined, name requests is not defined, and name get_forecast is not defined. At first this was confusing, but reading the last line of each traceback told me exactly which name was missing, and I traced each one back to either a missing import (marimo, requests) or an earlier cell that hadn't been added yet, like the get_forecast function or the best_day cell. This taught me something specific about marimo: a cell can only use names that another cell actually defines, and if one cell fails, every cell that depends on it fails too with an "Ancestor raised" error, so I had to add cells in the right order. I knew each one was fixed when the cell ran clean and, eventually, all three of my Section 6 checks printed match: True.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Section 8: Part 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    get_coordinates(town_name, state_name) takes in the name of a town, like "Wellesley," and the name of a state, like "Massachusetts," so it knows which match to use if more than one town shares that name. It gives back a single dictionary with four things: the official name, the state, the latitude, and the longitude — and if nothing in that state matches the town name, it raises an error instead of returning anything. The line I had to think hardest about was results = data.get("results", []). This pulls out the list of matches the API sent back, but if the town wasn't found at all, there's no "results" key, so it hands back an empty list instead of crashing the whole program right there.

    get_forecast(latitude, longitude) takes in the two coordinates get_coordinates found, so it knows exactly which location to ask the weather API about. It gives back a list of 7 dictionaries, one for each day, and each one holds that day's date, high, low, rain chance, and wind. The line I had to ask about here was for date, high, low, rain, wind in zip(...). The API sends back five separate lists (all the dates in one list, all the highs in another, and so on), so this loop walks through all five lists at the same time, grabbing the matching day's values from each one, so I can bundle them into a single record per day instead of five disconnected lists.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Section 8: Part 2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    My Change: max_rain_chance = 60
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    My prediction: I expect day 2026-11-05 (rain 34%), 2026-11-06 (rain 54%), and 2026-11-07 (rain 58%) to flip from No to Yes, since all three are at or under 60% and their temps and wind already fit the rules. That would bring the number of passing days from 4 up to 7. I don't expect the best day to change which already has the lowest rain chance (0%) and lowest wind (7.9 mph) of any day in the table, so even with three more days now qualifying, none of them can beat 0% rain.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What actually happened: After changing max_rain_chance to 60 and letting marimo rerun, the table showed all seven days as Yes, the three days that previously failed now pass since their rain chances (34%, 54%, 58%) are all under the new 60% ceiling. The passing count went from 4 to 7. The best day stayed 2026-11-01, also as predicted, since it still has the lowest rain chance (0%) of the full week and ties with 2026-11-04 on rain but wins on lower wind. I changed max_rain_chance back to 30 afterward, so Section 5 still answers the original question with the club's real rule rather than my loosened test value.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
