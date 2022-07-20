import requests
import pandas as pd


def connect_to_api():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token xxxx'
    }
    request_response = requests.get("https://api.tiingo.com/tiingo/fundamentals/msft/statements?startDate=2016-01-01",
                                    headers=headers)
    return request_response.json()


def request_to_dataframe(response):
    df = pd.DataFrame.from_dict(response)
    column_needed = (df['statementData'])
    for row in column_needed:
        for item in row:

            print(row[item])
    #df.to_csv('IDK WTF THIS IS.csv')
    final_df = pd.DataFrame(columns=['Date', 'Quarter', 'Year','Statement Name','Attribute', 'Value'])
    final_df['Date'] = df['date']
    final_df['Quarter'] = df['quarter']
    final_df['Year'] = df['year']
    print(final_df)


request_to_dataframe(connect_to_api())
