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
    # Ensure record_date is datetime
    df['record_date'] = pd.to_datetime(df['record_date'])

    # Sort just in case
    df = df.sort_values('record_date')

    # Set date as index
    df = df.set_index('record_date')

    # Take the *last known value* of each week (Saturday)
    weekly = df['tot_pub_debt_out_amt'].resample('W-SAT').last()

    # Calculate week-to-week changes
    weekly_change = weekly.diff()

    # Get max and min changes
    max_increase = weekly_change.idxmax(), weekly_change.max()
    max_decrease = weekly_change.idxmin(), weekly_change.min()

    return max_increase, max_decrease


@app.route('/')
def index():
    df = fetch_debt_data()
    all_years = sorted(df['record_date'].dt.year.unique())  # full list first

    year = request.args.get('year')
    if year:
        df = df[df['record_date'].dt.year == int(year)]

    insights = get_weekly_insights(df)

    # Display copy with string dates for frontend rendering
    df_display = df.copy()
    df_display['record_date'] = df_display['record_date'].dt.strftime('%Y-%m-%d')

    years = sorted(df['record_date'].dt.year.unique())

    return render_template(
        'index.html',
        data=df_display.to_dict(orient='records'),
        years=all_years,
        selected_year=year,
        insights=insights
    )

if __name__ == '__main__':
    app.run(debug=True)
