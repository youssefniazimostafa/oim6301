import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    How much did I spend on Groceries from September 2025 - August 2026?
    """)
    return


@app.cell
def _():
    monthly_spending = [452, 469, 497, 542, 432, 418, 460, 472, 486, 464, 501, 480]
    print(monthly_spending)
    return (monthly_spending,)


@app.cell
def _(monthly_spending):
    sept_2025 = monthly_spending[0]
    oct_2025 = monthly_spending[1]
    nov_2025 = monthly_spending[2]
    dec_2025 = monthly_spending[3]
    jan_2026 = monthly_spending[4]
    feb_2026 = monthly_spending[5]
    mar_2026 = monthly_spending[6]
    apr_2026 = monthly_spending[7]
    may_2026 = monthly_spending[8]
    jun_2026 = monthly_spending[9]
    jul_2026 = monthly_spending[10]
    aug_2026 = monthly_spending[11]

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each value in my list represents the spending of a single month between sept 2025 and aug 2026
    """)
    return


@app.cell
def _():
    monthly_spendingerror = [452, 469, 497, 542, 432, 418, 460, 472, 486, 464, 501, 480, "na"]
    return (monthly_spendingerror,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The last line say unsupported opperand type meaning all the values in the list are a int type which means whole number or integer  except one which is a str type which is text.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I want to exclude that variable when creating a new list without it. This isinstance(spending, (int, float) helps determine what operand type the variable is and the if statesment selects it if the isinstance relusts to true.
    """)
    return


@app.cell
def _(monthly_spendingerror):
    monthly_spendingclean = []
    for spending in monthly_spendingerror:
        if isinstance(spending, (int, float)):
            monthly_spendingclean.append(spending)
    monthly_spendingclean
    return (monthly_spendingclean,)


@app.cell
def _(monthly_spendingclean):
    total = sum(monthly_spendingclean)
    total
    return (total,)


@app.cell
def _(monthly_spendingclean, total):
    print(f"Groceries from Sept 2025 to Aug 2026 cost {total}$, or {total/len(monthly_spendingclean)}$ per month")
    return


if __name__ == "__main__":
    app.run()
