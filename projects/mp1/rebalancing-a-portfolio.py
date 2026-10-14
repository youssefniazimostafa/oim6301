# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A financial advisor or anyone who manages their own investments could use this tool. They can use this tool to rebalance their investments to the agreed upon percentage targets in order to adjust for changes made by market fluctuations over time. This allows for realloction of investments so that risks can be mitigated and investment goals can continue to be met over time. It is basically a way to organise a restructure your investing plans based on your own goals and risk tolerance.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    My loop will carry a running total of the portfolio value. It will start with th 5000 in cash and adds shares x price for each company until I have the full value of the account. that total i how much money I have to work with so I multiply it by each target weight to see how much should go into each stock. For example. if the account is worth 20k and apples target is 20% then 4000 goes into apple and I divide the price by that 4000 and round down to get whole shares. I then build a new list with the rebalanced shares, values and whatever cash will be left over. For my check in sction 6 I will compare each stocks target dollar amount which is total x weight to its actual value after rebalancing, since we round down to whole shares, they should agree within one shares price. I will also make sure the total value before rebalancing matches the total after, since they should be the same value as no money should be gained or lost.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]
    cash = 5000.00
    target_weights = {"AAPL": 0.20, "MSFT": 0.20, "GOOG": 0.15,
                      "AMZN": 0.15, "NVDA": 0.15, "TSLA": 0.15}
    return cash, holdings, target_weights


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(cash, holdings):
    total_value = holdings[0][1] * holdings[0][2] + holdings[1][1] * holdings[1][2] + holdings[2][1] * holdings[2][2] + holdings[3][1] * holdings[3][2] + holdings[4][1] * holdings[4][2] + holdings[5][1] * holdings[5][2] + cash

    total_value
    return


@app.cell
def _(cash, holdings):
    total_portfolio_value = cash
    for ticker, shares, price in holdings:
        total_portfolio_value += shares * price

    total_portfolio_value
    return (total_portfolio_value,)


@app.cell
def _(holdings, target_weights, total_portfolio_value):
    rebalanced = []
    for _ticker, _shares, _price in holdings:
        target_dollars = total_portfolio_value * target_weights[_ticker]
        target_shares = int(target_dollars // _price)
        rebalanced.append((_ticker, target_shares, _price))
    rebalanced
    return (rebalanced,)


@app.cell
def _(rebalanced, total_portfolio_value):
    rebalanced_stock_value = rebalanced[0][1] * rebalanced[0][2] + rebalanced[1][1] * rebalanced[1][2] + rebalanced[2][1] * rebalanced[2][2] + rebalanced[3][1] * rebalanced[3][2] + rebalanced[4][1] * rebalanced[4][2] + rebalanced[5][1] * rebalanced[5][2]
    remaining_cash = total_portfolio_value - rebalanced_stock_value
    remaining_cash = round(remaining_cash, 2)
    remaining_cash
    return rebalanced_stock_value, remaining_cash


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(rebalanced):
    for row in rebalanced:
        print(row)
    return


@app.cell
def _(rebalanced):
    print(f"{'Ticker':<8}{'Shares':>8}{'Price':>10}")
    for _ticker, _shares, _price in rebalanced:
        print(f"{_ticker:<8}{_shares:>8}{_price:>10.2f}")
    return


@app.cell
def _(remaining_cash):
    print(f" The amount of cash remaining: {remaining_cash}")
    return


@app.cell
def _(remaining_cash):
    print(f"The portfolio can be purchased according close to target weights by buying and selling the calculated number of shares, with all six stocks ending within 0.24 percentage points of their targets and {remaining_cash}$ remaining in cash")
    return


@app.cell
def _(holdings, rebalanced, target_weights, total_portfolio_value):
    print(f"{'Ticker':<8}{'Old':>6}{'New':>6}{'Trade':>8}{'Value After':>14}{'Weight After':>14}{'Gap pp':>10}")
    for i in range(len(holdings)):
        _ticker, _old_shares, _price = holdings[i]
        _, _new_shares, _ = rebalanced[i]
        _trade = _new_shares - _old_shares
        _value_after = _new_shares * _price
        _weight_after = _value_after / total_portfolio_value
        _gap = (_weight_after - target_weights[_ticker]) * 100
        print(f"{_ticker:<8}{_old_shares:>6}{_new_shares:>6}{_trade:>+8}{_value_after:>14.2f}{_weight_after:>14.2%}{_gap:>10.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(rebalanced_stock_value, remaining_cash, total_portfolio_value):
    rebalanced_total_value = rebalanced_stock_value + remaining_cash

    print(f"Total value from original holdings (running total): {total_portfolio_value}")
    print(f"Total value after rebalancing (stocks + leftover cash): {rebalanced_total_value}")
    print(f"Difference: {round(total_portfolio_value - rebalanced_total_value, 2)}")
    return


@app.cell
def _(rebalanced, total_portfolio_value):
    for _ticker, _shares, _price in rebalanced:
        _value = _shares * _price
        _weight = _value / total_portfolio_value
        print(f"{_ticker}: {_weight:.2%}")
    return


@app.cell
def _(holdings, rebalanced, target_weights, total_portfolio_value):
    max_gap = 0
    for x in range(len(holdings)):
        _ticker, _old_shares, _price = holdings[x]
        _, _new_shares, _ = rebalanced[x]
        _value_after = _new_shares * _price
        _weight_after = _value_after / total_portfolio_value
        _gap = abs((_weight_after - target_weights[_ticker]) * 100)
        if _gap > max_gap:
            max_gap = _gap

    max_gap
    return (max_gap,)


@app.cell
def _(max_gap, remaining_cash):
    print(f"The portfolio can be bought close to target weights by trading the shares above, with all six stocks ending within {max_gap:.2f} percentage points of their targets and {remaining_cash}$ remaining in cash")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this code I confirmed that the portfolio value is still the same after rebalancing and that the target weights are correct.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When trying to create a table for my final answer I asked the AI to create a table based on the rebalanced list using an f string, it ended up making an extensive table that included a lot of variables that I did not desire and asked it to create an easier table that just states the ticker its price and the number of shares.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In another instance I made code to calculate the full price of the whole portfolio based on the holdings list. I then asked AI to verify whether it was correct they stated it was but then gave me a much easier alternative to calculating the total portfolio value that I ended up using instead and helped make the project a lot easier.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following shows my code vs what AI reccomended.
    """)
    return


@app.cell
def _(cash, holdings):
    total_value = holdings[0][1] * holdings[0][2] + holdings[1][1] * holdings[1][2] + holdings[2][1] * holdings[2][2] + holdings[3][1] * holdings[3][2] + holdings[4][1] * holdings[4][2] + holdings[5][1] * holdings[5][2] + cash

    total_value
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(cash, holdings, rebalanced):
    trade_fee = 5.00
    min_trade_value = 500.00

    actual_holdings = []
    total_fees = 0.0
    skipped_trades = 0
    cash_after_trades = cash

    for y in range(len(holdings)):
        _ticker, _current_shares, _price = holdings[y]
        _target_shares = rebalanced[y][1]
        _share_diff = _target_shares - _current_shares
        _trade_value = abs(_share_diff) * _price

        if _trade_value < min_trade_value:
            actual_holdings.append((_ticker, _current_shares, _price))
            skipped_trades += 1
        else:
            actual_holdings.append((_ticker, _target_shares, _price))
            cash_after_trades -= _share_diff * _price
            cash_after_trades -= trade_fee
            total_fees += trade_fee

    actual_holdings
    return actual_holdings, cash_after_trades, skipped_trades, total_fees


@app.cell
def _(
    actual_holdings,
    cash_after_trades,
    skipped_trades,
    total_fees,
    total_portfolio_value,
):
    actual_stock_value = 0.0
    for _ticker, _shares, _price in actual_holdings:
        actual_stock_value += _shares * _price

    actual_total_value = actual_stock_value + cash_after_trades

    print(f"Trades skipped (under $500): {skipped_trades}")
    print(f"Total fees paid: ${total_fees}")
    print(f"Total value before trading: ${total_portfolio_value}")
    print(f"Total value after trading and fees: ${round(actual_total_value, 2)}")
    return (actual_total_value,)


@app.cell
def _(actual_holdings, actual_total_value, target_weights):
    print(f"{'Ticker':<8}{'Target %':>10}{'Actual %':>10}{'Diff %':>10}")
    for _ticker, _shares, _price in actual_holdings:
        _actual_weight = (_shares * _price) / actual_total_value
        _target_weight = target_weights[_ticker]
        _diff = (_actual_weight - _target_weight) * 100
        print(f"{_ticker:<8}{_target_weight*100:>9.2f}%{_actual_weight*100:>9.2f}%{_diff:>9.2f}%")
    return


@app.cell
def _(cash, cash_after_trades, remaining_cash, total_fees):
    print(f"Starting cash: ${cash:.2f}")
    print(f"Cash after trades and fees: ${cash_after_trades:.2f}")
    print(f"Total spent on trade fees: ${total_fees:.2f}")
    print(f"Share of starting cash spent on fees: {total_fees/remaining_cash:.2%}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I tried to create a code that can calculate how much charges I will inccur in trading and how much it will cost out of the remaining cash funds. It came to say that it would cost 30$ and that it would leave my remaining cash at about 695.62 from 725.62.
    """)
    return


if __name__ == "__main__":
    app.run()
