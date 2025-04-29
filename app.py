# app.py
from flask import Flask, render_template, request
import requests
import pandas as pd
from datetime import datetime

app = Flask(__name__)

def fetch_debt_data():
    url = ('https://api.fiscaldata.treasury.gov/services/api/fiscal_service'
           '/v2/accounting/od/debt_to_penny'
           '?fields=record_date,tot_pub_debt_out_amt'
           '&sort=record_date'
           '&page[size]=10000')
    data = requests.get(url).json()['data']
    df = pd.DataFrame(data)
    df['record_date'] = pd.to_datetime(df['record_date'])  # Keep this as datetime
    df['tot_pub_debt_out_amt'] = pd.to_numeric(df['tot_pub_debt_out_amt'])
    return df

def get_weekly_insights(df):
    df['record_date'] = pd.to_datetime(df['record_date'])
    df = df.sort_values('record_date')
    df = df.set_index('record_date')

    weekly = df['tot_pub_debt_out_amt'].resample('W-SAT').last()
    weekly_change = weekly.diff()

    max_increase_date = weekly_change.idxmax()
    max_decrease_date = weekly_change.idxmin()

    max_increase = (
        max_increase_date - pd.Timedelta(days=6),  # start
        max_increase_date,                         # end
        weekly_change.max()
    )

    max_decrease = (
        max_decrease_date - pd.Timedelta(days=6),  # start
        max_decrease_date,                         # end
        weekly_change.min()
    )

    return max_increase, max_decrease



@app.route('/')
def index():
    df = fetch_debt_data()
    all_years = sorted(df['record_date'].dt.year.unique(), reverse=True)  # full list first, sorted newest to oldest

    year = request.args.get('year')
    if year:
        df = df[df['record_date'].dt.year == int(year)]

    df = df.sort_values('record_date', ascending=False) # sort largest to smallest

    # weekly stats
    insights = get_weekly_insights(df)

    # Display copy with string dates for frontend rendering
    df_display = df.copy()
    df_display['record_date'] = df_display['record_date'].dt.strftime('%Y-%m-%d')

    years = sorted(df['record_date'].dt.year.unique())

    # Prepare chart data (sorted oldest to newest)
    chart_df = df.sort_values('record_date', ascending=True)
    chart_dates = chart_df['record_date'].dt.strftime('%Y-%m-%d').tolist()
    chart_values = chart_df['tot_pub_debt_out_amt'].tolist()

    # get most recent debt
    latest_debt = df.iloc[0]['tot_pub_debt_out_amt']
    latest_date = df.iloc[0]['record_date'].strftime('%Y-%m-%d')

    # Progress toward 37 trillion
    progress_to_target = (latest_debt / 37_000_000_000_000) * 100
    progress_to_target = min(progress_to_target, 100)  # cap at 100%

    # Countdown to 37 trillion
    target_debt = 37_000_000_000_000
    debt_to_target = target_debt - latest_debt

    # Determine countdown color class
    if debt_to_target <= 100_000_000_000:
        countdown_color_class = 'text-danger'  # bright red if less than $100B
    elif debt_to_target <= 500_000_000_000:
        countdown_color_class = 'text-warning'  # orange-ish if less than $500B
    else:
        countdown_color_class = ''  # normal black if more than $500B


    return render_template(
        'index.html',
        data=df_display.to_dict(orient='records'),
        years=all_years,
        selected_year=year,
        insights=insights,
        chart_dates=chart_dates,
        chart_values=chart_values,
        latest_debt=latest_debt,
        latest_date=latest_date,
        debt_to_target=debt_to_target,
        countdown_color_class=countdown_color_class,
        progress_to_target=progress_to_target
    )

if __name__ == '__main__':
    app.run(debug=True)
