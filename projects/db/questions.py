import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    as_of = "2026-10-30"
    return (as_of,)


@app.cell
def _():
    import marimo as mo
    import duckdb

    return duckdb, mo


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 1: What did each portfolio trade in the last 30 days?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT portfolio_id,
               COUNT(*) AS trades,
               ROUND(SUM(CASE WHEN side = 'buy' THEN quantity * price_per_unit + fee ELSE 0 END), 2) AS spent,
               ROUND(SUM(CASE WHEN side = 'sell' THEN quantity * price_per_unit - fee ELSE 0 END), 2) AS received
        FROM trades
        WHERE trade_date > DATE '{as_of}' - INTERVAL 30 DAY AND trade_date <= DATE '{as_of}'
        GROUP BY portfolio_id
        ORDER BY portfolio_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the 30 days ending on 2026-10-30, 17 of the 20 portfolios made 41 trades, spending $200,211.12 on buys and receiving $31,500.44 from sells, and the table only shows the portfolios that traded in that window.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 2: How many portfolios does each member have, and how much have they bought?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT m.member_id, m.first_name, m.last_name,
               COUNT(DISTINCT p.portfolio_id) AS portfolios,
               ROUND(COALESCE(SUM(CASE WHEN t.side = 'buy' THEN t.quantity * t.price_per_unit END), 0), 2) AS value_bought
        FROM members m
        LEFT JOIN portfolios p ON p.member_id = m.member_id
        LEFT JOIN trades t ON t.portfolio_id = p.portfolio_id
        GROUP BY m.member_id, m.first_name, m.last_name
        ORDER BY m.member_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Liam Nguyen bought the most, $191,285.51 across 3 portfolios, while Ryan Walsh and Zoe Fischer own no portfolio and show 0, and these totals leave out fees.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3: What does each portfolio hold on the as_of date?
    """)
    return


@app.cell
def _(ask):
    ask("SELECT * FROM holdings ORDER BY portfolio_id, asset_id")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using the holdings view from build.py, the 19 portfolios that have traded hold 177 positions on 2026-10-30, and the view gives the holdings on that date because every trade is on or before as_of.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 4: How close was each trade price to the closing price in the last 90 days?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT t.trade_id, t.trade_date, a.name, t.price_per_unit, c.close_price,
               ROUND((t.price_per_unit - c.close_price) / c.close_price * 100, 2) AS pct_diff
        FROM trades t
        JOIN assets a ON a.asset_id = t.asset_id
        JOIN closing_prices c ON c.asset_id = t.asset_id AND c.price_date = t.trade_date
        WHERE t.trade_date > DATE '{as_of}' - INTERVAL 90 DAY AND t.trade_date <= DATE '{as_of}'
        ORDER BY t.trade_date, t.trade_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There were 104 trades in the 90 days ending on 2026-10-30, and their trade price was on average 0.70% away from that day's close and never more than 1.49% away.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 5: Which assets has no portfolio ever traded?
    """)
    return


@app.cell
def _(ask):
    ask("SELECT asset_id, name FROM assets WHERE asset_id NOT IN (SELECT asset_id FROM trades)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ford and Pfizer are the only two assets that no portfolio has ever traded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 6: Which asset changed its ticker, and how much of it did the club trade?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT k.ticker, k.valid_from, k.valid_to,
               (SELECT ROUND(SUM(t.quantity * t.price_per_unit), 2)
                FROM trades t
                WHERE t.asset_id = k.asset_id
                  AND t.trade_date > DATE '{as_of}' - INTERVAL 1 YEAR AND t.trade_date <= DATE '{as_of}') AS value_traded
        FROM asset_tickers k
        WHERE k.asset_id IN (SELECT asset_id FROM asset_tickers GROUP BY asset_id HAVING COUNT(*) > 1)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Meta Platforms traded as FB until 2026-03-31 and as META from 2026-04-01, and the club traded $455,395.06 of it over the year under both tickers.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 7: Which trades happened on a day their asset has no closing price?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT t.trade_id, t.trade_date, t.asset_id
        FROM trades t
        LEFT JOIN closing_prices c ON c.asset_id = t.asset_id AND c.price_date = t.trade_date
        WHERE c.close_price IS NULL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Trades 34 and 216 are the only trades on a day with no closing price, and both are Saturday buys (Apple on 2026-01-17 and Nike on 2026-07-11).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 8: Which sells were for more units than the portfolio held?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT s.trade_id, s.portfolio_id, s.asset_id, s.trade_date, s.quantity
        FROM trades s
        WHERE s.side = 'sell'
          AND (SELECT SUM(CASE WHEN t.side = 'buy' THEN t.quantity ELSE -t.quantity END)
               FROM trades t
               WHERE t.portfolio_id = s.portfolio_id AND t.asset_id = s.asset_id
                 AND t.trade_date <= s.trade_date) < 0
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Trades 45 and 299 are the only sells of more units than the portfolio held, and both are by portfolio 13 (1.2542 Ethereum and 16 Johnson & Johnson shares).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 9: How much did the club pay in fees in each of the last 6 full months?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT date_trunc('month', trade_date) AS month, SUM(fee) AS total_fees
        FROM trades
        WHERE trade_date >= date_trunc('month', DATE '{as_of}') - INTERVAL 6 MONTH
          AND trade_date < date_trunc('month', DATE '{as_of}')
        GROUP BY month
        ORDER BY month
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From April to September 2026 the club paid $130.08 in fees, with the most in May ($34.70) and the least in June ($8.78).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 10: Which 3 assets did the club trade the most over the year?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT a.name, a.type, ROUND(SUM(t.quantity * t.price_per_unit), 2) AS value_traded
        FROM trades t
        JOIN assets a ON a.asset_id = t.asset_id
        WHERE t.trade_date > DATE '{as_of}' - INTERVAL 1 YEAR AND t.trade_date <= DATE '{as_of}'
        GROUP BY a.name, a.type
        ORDER BY value_traded DESC
        LIMIT 3
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The three most traded assets over the year were Meta Platforms ($455,395.06), Microsoft ($202,908.70) and JPMorgan Chase ($132,628.46), and all three are stocks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How I Know These Numbers Are Right
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Working With the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading It Back

    I picked Question 3, what each portfolio holds on the as_of date. It joins trades, portfolios and assets. My prediction is that the joins produce 352 rows before any grouping. Every trade belongs to exactly one portfolio and one asset, so joining on those keys should not add or remove rows, and all 352 trades fall on or before the as_of date.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Going Further
    """)
    return


if __name__ == "__main__":
    app.run()
