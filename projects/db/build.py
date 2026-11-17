import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl
    import altair as alt

    return alt, duckdb, mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Tables

    This cell deletes the old database, creates the tables in foreign key order, loads the CSVs and creates the view.
    """)
    return


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"
    data = mo.notebook_dir() / "data"

    if database.exists():
        database.unlink()

    with duckdb.connect(database) as _con:
        _con.sql("""
            CREATE TABLE members (
                member_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                email VARCHAR UNIQUE NOT NULL,
                class_year INTEGER NOT NULL,
                join_date DATE NOT NULL
            )
        """)
        _con.sql("""
            CREATE TABLE assets (
                asset_id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL,
                type VARCHAR NOT NULL CHECK (type IN ('stock', 'etf', 'crypto')),
                sector VARCHAR
            )
        """)
        _con.sql("""
            CREATE TABLE portfolios (
                portfolio_id INTEGER PRIMARY KEY,
                member_id INTEGER NOT NULL REFERENCES members (member_id),
                name VARCHAR NOT NULL,
                date_created DATE NOT NULL,
                strategy VARCHAR
            )
        """)
        _con.sql("""
            CREATE TABLE asset_tickers (
                ticker_id INTEGER PRIMARY KEY,
                asset_id INTEGER NOT NULL REFERENCES assets (asset_id),
                ticker VARCHAR NOT NULL,
                valid_from DATE NOT NULL,
                valid_to DATE
            )
        """)
        _con.sql("""
            CREATE TABLE closing_prices (
                asset_id INTEGER REFERENCES assets (asset_id),
                price_date DATE,
                close_price DOUBLE NOT NULL CHECK (close_price > 0),
                PRIMARY KEY (asset_id, price_date)
            )
        """)
        _con.sql("""
            CREATE TABLE trades (
                trade_id INTEGER PRIMARY KEY,
                portfolio_id INTEGER NOT NULL REFERENCES portfolios (portfolio_id),
                asset_id INTEGER NOT NULL REFERENCES assets (asset_id),
                trade_date DATE NOT NULL,
                side VARCHAR NOT NULL CHECK (side IN ('buy', 'sell')),
                quantity DOUBLE NOT NULL CHECK (quantity > 0),
                price_per_unit DOUBLE NOT NULL CHECK (price_per_unit > 0),
                fee DOUBLE NOT NULL DEFAULT 0 CHECK (fee >= 0),
                UNIQUE (portfolio_id, asset_id, trade_date)
            )
        """)

        # Load in the same order so every foreign key finds its parent row.
        for _table in ["members", "assets", "portfolios", "asset_tickers", "closing_prices", "trades"]:
            _con.sql(f"INSERT INTO {_table} SELECT * FROM read_csv('{data / _table}.csv')")

        _con.sql("""
            CREATE VIEW holdings AS
            SELECT t.portfolio_id, t.asset_id, a.name AS asset_name,
                   ROUND(SUM(CASE WHEN t.side = 'buy' THEN t.quantity ELSE -t.quantity END), 4) AS units
            FROM trades t
            JOIN assets a ON a.asset_id = t.asset_id
            GROUP BY t.portfolio_id, t.asset_id, a.name
            HAVING units > 0
        """)

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return ask, data, database


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Data

    The data comes from make_data.py with seed 42 and covers 2025-10-31 to as_of 2026-10-30.

    I planted four rows that break rules. Trades 34 and 216 are Saturday buys with no closing price (Apple on 2026-01-17, Nike on 2026-07-11). Trades 45 and 299 are sells by portfolio 13 of more than it holds (Ethereum, Johnson & Johnson). The tables accept these rows because neither rule can be a CHECK. Questions 7 and 8 find them.

    ## A Look at the Data
    """)
    return


@app.cell
def _(alt, data, pl):
    _prices = pl.read_csv(data / "closing_prices.csv", try_parse_dates=True)
    apple = _prices.filter(pl.col("asset_id") == 1)

    alt.Chart(apple).mark_line().encode(
        x=alt.X("price_date:T", title="Date"),
        y=alt.Y("close_price:Q", title="Apple closing price ($)"),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It looks like a real stock: it moves up and down every day, drops to about $189 and ends the year at its high of about $264, but it has none of the sudden jumps a real stock gets on earnings days.

    ## Row Counts
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT 'members' AS table_name, COUNT(*) AS row_count FROM members
        UNION ALL SELECT 'portfolios', COUNT(*) FROM portfolios
        UNION ALL SELECT 'assets', COUNT(*) FROM assets
        UNION ALL SELECT 'asset_tickers', COUNT(*) FROM asset_tickers
        UNION ALL SELECT 'closing_prices', COUNT(*) FROM closing_prices
        UNION ALL SELECT 'trades', COUNT(*) FROM trades
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A Row It Refuses
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.sql("INSERT INTO trades VALUES (999, 1, 1, '2026-01-05', 'buy', -5, 200, 0)")
    except Exception as e:
        print(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The CHECK (quantity > 0) constraint on trades refused it, so the bad row never got into the table.

    ## Answers You Already Knew
    """)
    return


@app.cell
def _(ask):
    ask("SELECT COUNT(*) AS members FROM members")  # expect 15
    return


@app.cell
def _(ask):
    ask("SELECT COUNT(*) AS trades FROM trades")  # expect 352
    return


@app.cell
def _(ask):
    ask("SELECT COUNT(*) AS never_traded FROM assets WHERE asset_id NOT IN (SELECT asset_id FROM trades)")  # expect 2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A View

    The club would check holdings every week because it shows what each portfolio owns right now, without anyone adding up the trades by hand.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT * FROM holdings")
    return


if __name__ == "__main__":
    app.run()
