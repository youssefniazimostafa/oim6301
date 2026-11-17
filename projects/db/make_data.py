# Makes fake data for the Babson Investment Club database.
# It writes one CSV per table into projects/db/data/ and then checks the CSVs.
# Run with: uv run projects/db/make_data.py

import csv
import os
import random
from datetime import date, timedelta

random.seed(42)

AS_OF = date(2026, 10, 30)
START = date(2025, 10, 31)
TICKER_CHANGE = date(2026, 4, 1)  # FB becomes META on this day
META_ID = 3

# The folder this file is in, so the script works from any folder.
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

FIRST_NAMES = ["Ava", "Liam", "Maya", "Noah", "Priya", "Lucas", "Sofia", "Ethan",
               "Chloe", "Omar", "Grace", "Mateo", "Hana", "Ryan", "Zoe"]
LAST_NAMES = ["Carter", "Nguyen", "Patel", "Brooks", "Shah", "Ramos", "Rossi", "Kim",
              "Dubois", "Haddad", "Turner", "Silva", "Sato", "Walsh", "Fischer"]

STRATEGIES = ["growth", "value", "dividend income", "index tracking", "tech focus", "crypto mix"]

# asset_id, name, type, sector, ticker, starting price
ASSETS = [
    [1, "Apple", "stock", "Technology", "AAPL", 230],
    [2, "Microsoft", "stock", "Technology", "MSFT", 420],
    [3, "Meta Platforms", "stock", "Communication Services", "META", 580],
    [4, "JPMorgan Chase", "stock", "Financials", "JPM", 240],
    [5, "Johnson & Johnson", "stock", "Health Care", "JNJ", 155],
    [6, "Coca-Cola", "stock", "Consumer Staples", "KO", 68],
    [7, "Exxon Mobil", "stock", "Energy", "XOM", 115],
    [8, "Nike", "stock", "Consumer Discretionary", "NKE", 75],
    [9, "Ford", "stock", "Consumer Discretionary", "F", 11],
    [10, "Pfizer", "stock", "Health Care", "PFE", 25],
    [11, "SPDR S&P 500 ETF", "etf", "Broad Market", "SPY", 450],
    [12, "Invesco QQQ", "etf", "Technology", "QQQ", 430],
    [13, "Bitcoin", "crypto", "", "BTC", 65000],
    [14, "Ethereum", "crypto", "", "ETH", 3200],
]
NEVER_TRADED = [9, 10]


def write_csv(name, columns, rows):
    path = os.path.join(DATA, name)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for row in rows:
            writer.writerow(row)


def read_csv(name):
    path = os.path.join(DATA, name)
    with open(path, newline="") as f:
        # DictReader gives each row as a dict keyed by the column names.
        return list(csv.DictReader(f))


def all_days(start, end):
    days = []
    day = start
    while day <= end:
        days.append(day)
        day = day + timedelta(days=1)
    return days


def is_weekend(day):
    # weekday() is 0 for Monday up to 6 for Sunday.
    return day.weekday() >= 5


def asset_type(asset_id):
    for a in ASSETS:
        if a[0] == asset_id:
            return a[2]



def make_members():
    members = []
    for i in range(15):
        first = FIRST_NAMES[i]
        last = LAST_NAMES[i]
        email = first[0].lower() + last.lower() + "@babson.edu"
        class_year = random.choice([2026, 2027, 2028, 2029])
        # Everyone joined before October 2025, so before any portfolio exists.
        join_date = date(2023, 9, 1) + timedelta(days=random.randint(0, 730))
        members.append([i + 1, first, last, email, class_year, join_date])
    return members



def make_portfolios():
    # Members 1 to 13 own one portfolio each, then 7 more go to random members.
    # Members 14 and 15 own none.
    owners = []
    for member_id in range(1, 14):
        owners.append(member_id)
    for i in range(7):
        owners.append(random.randint(1, 13))
    owners.sort()

    portfolios = []
    count_per_owner = {}
    for i in range(20):
        portfolio_id = i + 1
        member_id = owners[i]
        count_per_owner[member_id] = count_per_owner.get(member_id, 0) + 1
        name = LAST_NAMES[member_id - 1] + " Portfolio " + str(count_per_owner[member_id])

        if portfolio_id == 20:
            created = date(2026, 10, 15)  # new portfolio, no trades yet
        else:
            created = date(2025, 10, 1) + timedelta(days=random.randint(0, 240))

        if portfolio_id in [4, 11, 17]:
            strategy = ""
        else:
            strategy = random.choice(STRATEGIES)

        portfolios.append([portfolio_id, member_id, name, created, strategy])
    return portfolios



def make_assets():
    rows = []
    for a in ASSETS:
        rows.append([a[0], a[1], a[2], a[3]])
    return rows


def make_tickers():
    rows = []
    ticker_id = 1
    for a in ASSETS:
        if a[0] == META_ID:
            rows.append([ticker_id, META_ID, "FB", date(2012, 5, 18), TICKER_CHANGE - timedelta(days=1)])
            ticker_id = ticker_id + 1
            rows.append([ticker_id, META_ID, "META", TICKER_CHANGE, ""])
        else:
            rows.append([ticker_id, a[0], a[4], date(2015, 1, 1), ""])
        ticker_id = ticker_id + 1
    return rows



def make_prices():
    prices = {}  # (asset_id, day) -> close
    rows = []
    for a in ASSETS:
        asset_id = a[0]
        kind = a[2]
        price = a[5]
        if kind == "crypto":
            daily_move = 0.03
        elif kind == "etf":
            daily_move = 0.01
        else:
            daily_move = 0.015

        for day in all_days(START, AS_OF):
            if kind != "crypto" and is_weekend(day):
                continue
            # Random walk: each day the price moves a small random percent.
            price = price * (1 + random.gauss(0, daily_move))
            close = round(price, 2)
            prices[(asset_id, day)] = close
            rows.append([asset_id, day, close])
    return prices, rows



def buy_amount(asset_id):
    kind = asset_type(asset_id)
    if asset_id == 13:
        return round(random.uniform(0.01, 0.2), 4)
    if asset_id == 14:
        return round(random.uniform(0.1, 3), 4)
    if kind == "etf":
        return random.randint(1, 15)
    return random.randint(1, 40)


def sell_amount(asset_id, held):
    if asset_type(asset_id) == "crypto":
        quantity = round(held * random.uniform(0.2, 1.0), 4)
        if quantity <= 0:
            quantity = held
        return quantity
    return random.randint(1, held)


def pick_events(portfolios, prices):
    # An event is one (day, portfolio, asset) that will become one trade.
    created = {}
    for p in portfolios:
        created[p[0]] = p[3]

    price_days = {}
    for key in prices:
        asset_id = key[0]
        if asset_id not in price_days:
            price_days[asset_id] = []
        price_days[asset_id].append(key[1])

    traded = []
    for a in ASSETS:
        if a[0] not in NEVER_TRADED:
            traded.append(a[0])

    events = []
    used = set()
    while len(events) < 350:
        portfolio_id = random.randint(1, 19)  # portfolio 20 gets no trades
        asset_id = random.choice(traded)
        days = []
        for day in price_days[asset_id]:
            if day > created[portfolio_id]:
                days.append(day)
        day = random.choice(days)
        key = (day, portfolio_id, asset_id)
        if key in used:
            continue  # at most one trade per portfolio, asset and day
        used.add(key)
        events.append(key)
    return events, created


def weekend_events(created, used):
    # Planted rule break (a): stock buys on a Saturday, when there is no closing price.
    plants = []
    for day, asset_id in [(date(2026, 1, 17), 1), (date(2026, 7, 11), 8)]:
        for portfolio_id in range(1, 20):
            key = (day, portfolio_id, asset_id)
            if created[portfolio_id] < day and key not in used:
                plants.append(key)
                break
    return plants


def make_trades(portfolios, prices):
    events, created = pick_events(portfolios, prices)
    plants = weekend_events(created, set(events))
    events = events + plants
    events.sort()

    holdings = {}  # (portfolio_id, asset_id) -> units held
    trades = []
    for day, portfolio_id, asset_id in events:
        pair = (portfolio_id, asset_id)
        held = holdings.get(pair, 0)

        if (day, portfolio_id, asset_id) in plants:
            side = "buy"
            label = "weekend"
        elif held > 0 and random.random() < 0.4:
            side = "sell"
            label = ""
        else:
            side = "buy"
            label = ""

        if side == "buy":
            quantity = buy_amount(asset_id)
            holdings[pair] = round(held + quantity, 4)
        else:
            quantity = sell_amount(asset_id, held)
            holdings[pair] = round(held - quantity, 4)

        close = prices.get((asset_id, day))
        if close is None:
            close = prices[(asset_id, day - timedelta(days=1))]  # use Friday's close
        price = round(close * random.uniform(0.985, 1.015), 2)

        if random.random() < 0.2:
            fee = round(random.uniform(0.5, 5), 2)
        else:
            fee = 0

        trades.append([day, portfolio_id, asset_id, side, quantity, price, fee, held, label])

    return plant_oversells(trades)


def plant_oversells(trades):
    # Planted rule break (b): two sells of more units than the portfolio holds.
    # Later trades of the same portfolio and asset are dropped so only these two rows break the rule.
    weekend_pairs = []
    for t in trades:
        if t[8] == "weekend":
            weekend_pairs.append((t[1], t[2]))

    chosen_pairs = []
    oversell_day = {}
    while len(chosen_pairs) < 2:
        t = random.choice(trades)
        pair = (t[1], t[2])
        if t[3] != "sell" or pair in weekend_pairs or pair in chosen_pairs:
            continue
        held = t[7]
        if asset_type(t[2]) == "crypto":
            t[4] = round(held + 0.5, 4)
        else:
            t[4] = held + random.randint(3, 10)
        t[8] = "oversell"
        chosen_pairs.append(pair)
        oversell_day[pair] = t[0]

    kept = []
    dropped = 0
    for t in trades:
        pair = (t[1], t[2])
        if pair in oversell_day and t[0] > oversell_day[pair]:
            dropped = dropped + 1
            continue
        kept.append(t)
    print("dropped", dropped, "later trades in the two oversold pairs")
    return kept



def check_csvs():
    members = read_csv("members.csv")
    portfolios = read_csv("portfolios.csv")
    assets = read_csv("assets.csv")
    tickers = read_csv("asset_tickers.csv")
    prices = read_csv("closing_prices.csv")
    trades = read_csv("trades.csv")

    print()
    print("Rows breaking each rule:")

    # Primary keys must be unique.
    print("duplicate member_id:", count_duplicates(members, ["member_id"]))
    print("duplicate member email:", count_duplicates(members, ["email"]))
    print("duplicate portfolio_id:", count_duplicates(portfolios, ["portfolio_id"]))
    print("duplicate asset_id:", count_duplicates(assets, ["asset_id"]))
    print("duplicate ticker_id:", count_duplicates(tickers, ["ticker_id"]))
    print("duplicate price (asset_id, price_date):", count_duplicates(prices, ["asset_id", "price_date"]))
    print("duplicate trade_id:", count_duplicates(trades, ["trade_id"]))
    print("more than one trade per portfolio, asset, day:",
          count_duplicates(trades, ["portfolio_id", "asset_id", "trade_date"]))

    # Foreign keys must point at a real row.
    member_ids = column_set(members, "member_id")
    portfolio_ids = column_set(portfolios, "portfolio_id")
    asset_ids = column_set(assets, "asset_id")
    print("portfolio with unknown member:", count_missing(portfolios, "member_id", member_ids))
    print("ticker with unknown asset:", count_missing(tickers, "asset_id", asset_ids))
    print("price with unknown asset:", count_missing(prices, "asset_id", asset_ids))
    print("trade with unknown portfolio:", count_missing(trades, "portfolio_id", portfolio_ids))
    print("trade with unknown asset:", count_missing(trades, "asset_id", asset_ids))

    print("portfolio created before owner joined:", check_join_dates(members, portfolios))
    print("crypto with a sector or other asset without one:", check_sectors(assets))
    print("ticker periods that do not line up:", check_tickers(tickers))
    print("missing or extra price days:", check_price_days(assets, prices))

    bad_side = 0
    bad_numbers = 0
    for t in trades:
        if t["side"] not in ["buy", "sell"]:
            bad_side = bad_side + 1
        if float(t["quantity"]) <= 0 or float(t["price_per_unit"]) <= 0 or float(t["fee"]) < 0:
            bad_numbers = bad_numbers + 1
    print("side not buy or sell:", bad_side)
    print("quantity, price or fee out of range:", bad_numbers)

    print("trade on or before portfolio created date:", check_created(portfolios, trades))

    close = {}
    for p in prices:
        close[(p["asset_id"], p["price_date"])] = float(p["close_price"])
    no_close = 0
    far_price = 0
    for t in trades:
        key = (t["asset_id"], t["trade_date"])
        if key not in close:
            no_close = no_close + 1
        elif abs(float(t["price_per_unit"]) - close[key]) > 0.02 * close[key]:
            far_price = far_price + 1
    print("(a) trade on a day with no closing price:", no_close)
    print("trade price more than 2% from close:", far_price)
    print("(b) sell of more than held:", check_holdings(trades))

    print()
    print_facts(members, portfolios, assets, tickers, trades)


def count_duplicates(rows, columns):
    seen = set()
    duplicates = 0
    for row in rows:
        key = []
        for c in columns:
            key.append(row[c])
        key = tuple(key)
        if key in seen:
            duplicates = duplicates + 1
        seen.add(key)
    return duplicates


def column_set(rows, column):
    values = set()
    for row in rows:
        values.add(row[column])
    return values


def count_missing(rows, column, allowed):
    missing = 0
    for row in rows:
        if row[column] not in allowed:
            missing = missing + 1
    return missing


def check_join_dates(members, portfolios):
    joined = {}
    for m in members:
        joined[m["member_id"]] = m["join_date"]
    bad = 0
    for p in portfolios:
        # ISO dates (YYYY-MM-DD) compare correctly as text.
        if p["date_created"] < joined[p["member_id"]]:
            bad = bad + 1
    return bad


def check_sectors(assets):
    bad = 0
    for a in assets:
        if a["type"] == "crypto" and a["sector"] != "":
            bad = bad + 1
        if a["type"] != "crypto" and a["sector"] == "":
            bad = bad + 1
    return bad


def check_tickers(tickers):
    # For an asset with two tickers, the old valid_to must be the day before the new valid_from.
    by_asset = {}
    for t in tickers:
        if t["asset_id"] not in by_asset:
            by_asset[t["asset_id"]] = []
        by_asset[t["asset_id"]].append(t)
    bad = 0
    for asset_id in by_asset:
        # Sort the periods by start date. Each tuple starts with valid_from, so sort() orders by it.
        periods = []
        for t in by_asset[asset_id]:
            periods.append((t["valid_from"], int(t["ticker_id"]), t))
        periods.sort()
        rows = []
        for p in periods:
            rows.append(p[2])
        for i in range(len(rows) - 1):
            old_end = date.fromisoformat(rows[i]["valid_to"])
            new_start = date.fromisoformat(rows[i + 1]["valid_from"])
            if old_end + timedelta(days=1) != new_start:
                bad = bad + 1
        if rows[-1]["valid_to"] != "":
            bad = bad + 1  # the last ticker should still be current
    return bad


def check_price_days(assets, prices):
    have = set()
    for p in prices:
        have.add((p["asset_id"], p["price_date"]))
    bad = 0
    for a in assets:
        for day in all_days(START, AS_OF):
            expected = a["type"] == "crypto" or not is_weekend(day)
            present = (a["asset_id"], day.isoformat()) in have
            if expected != present:
                bad = bad + 1
    return bad


def check_created(portfolios, trades):
    created = {}
    for p in portfolios:
        created[p["portfolio_id"]] = p["date_created"]
    bad = 0
    for t in trades:
        if t["trade_date"] <= created[t["portfolio_id"]]:
            bad = bad + 1
    return bad


def check_holdings(trades):
    # Walk the trades in date order and keep a running total per portfolio and asset.
    ordered = []
    for t in trades:
        ordered.append((t["trade_date"], int(t["trade_id"]), t))
    ordered.sort()
    held = {}
    bad = 0
    for p in ordered:
        t = p[2]
        pair = (t["portfolio_id"], t["asset_id"])
        now = held.get(pair, 0)
        quantity = float(t["quantity"])
        if t["side"] == "buy":
            held[pair] = round(now + quantity, 4)
        else:
            if quantity > now:
                bad = bad + 1
            held[pair] = round(now - quantity, 4)
    return bad


def print_facts(members, portfolios, assets, tickers, trades):
    owners = column_set(portfolios, "member_id")
    no_portfolio = 0
    for m in members:
        if m["member_id"] not in owners:
            no_portfolio = no_portfolio + 1
    print("members with no portfolio:", no_portfolio)

    traded_portfolios = column_set(trades, "portfolio_id")
    no_trades = 0
    for p in portfolios:
        if p["portfolio_id"] not in traded_portfolios:
            no_trades = no_trades + 1
    print("portfolios with no trades:", no_trades)

    no_strategy = 0
    for p in portfolios:
        if p["strategy"] == "":
            no_strategy = no_strategy + 1
    print("portfolios with no strategy:", no_strategy)

    traded_assets = column_set(trades, "asset_id")
    never = 0
    for a in assets:
        if a["asset_id"] not in traded_assets:
            never = never + 1
    print("assets never traded:", never)

    before = 0
    after = 0
    for t in trades:
        if t["asset_id"] == str(META_ID):
            if t["trade_date"] < TICKER_CHANGE.isoformat():
                before = before + 1
            else:
                after = after + 1
    print("Meta trades under FB:", before, "under META:", after)



members = make_members()
portfolios = make_portfolios()
assets = make_assets()
tickers = make_tickers()
prices, price_rows = make_prices()
trades = make_trades(portfolios, prices)

trade_rows = []
weekend_ids = []
oversell_ids = []
trade_id = 1
for t in trades:
    trade_rows.append([trade_id, t[1], t[2], t[0], t[3], t[4], t[5], t[6]])
    if t[8] == "weekend":
        weekend_ids.append(trade_id)
    if t[8] == "oversell":
        oversell_ids.append(trade_id)
    trade_id = trade_id + 1

os.makedirs(DATA, exist_ok=True)
write_csv("members.csv", ["member_id", "first_name", "last_name", "email", "class_year", "join_date"], members)
write_csv("portfolios.csv", ["portfolio_id", "member_id", "name", "date_created", "strategy"], portfolios)
write_csv("assets.csv", ["asset_id", "name", "type", "sector"], assets)
write_csv("asset_tickers.csv", ["ticker_id", "asset_id", "ticker", "valid_from", "valid_to"], tickers)
write_csv("closing_prices.csv", ["asset_id", "price_date", "close_price"], price_rows)
write_csv("trades.csv", ["trade_id", "portfolio_id", "asset_id", "trade_date", "side",
                         "quantity", "price_per_unit", "fee"], trade_rows)

print("planted (a) weekend trades:", weekend_ids)
print("planted (b) oversell trades:", oversell_ids)
print()
for name in ["members.csv", "portfolios.csv", "assets.csv", "asset_tickers.csv",
             "closing_prices.csv", "trades.csv"]:
    print(name + ":", len(read_csv(name)), "rows")

check_csvs()
