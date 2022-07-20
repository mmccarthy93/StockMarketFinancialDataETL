import yahoo_fin.stock_info as si
import pandas as pd
import csv


# Open the master ticker file and read in the tickers to a list. Reads the items in as separate list items vs the
# entire list as a list item.
def get_tickers():
    file = open('master_ticker_list.csv', 'r')
    csv_reader = csv.reader(file)
    list_from_csv = []
    for row in csv_reader:
        list_from_csv.append(row)
    master_list = []
    for item in list_from_csv[0]:
        master_list.append(item)
    file.close()
    return master_list


# Runs through a switch scenario, allowing the user to choose from running the program for just 1 ticker, multiple
# tickers, or the entire master ticker list.
def choose_operation(list2run, master_list):
    close_loop = 0
    choice = 0
    while close_loop == 0:
        operation = int(input('Choose an option:\n1 - RUN SINGLE TICKER\n2 - RUN CUSTOM TICKERS\n3 - RUN MASTER TICKER'
                              ' LIST\n'))
        if operation == 1:
            ticker = input('Which ticker would you like to run?\n ')
            list2run.append(ticker)
            choice = operation
            close_loop += 1
        elif operation == 2:
            count = 1
            end_list = 0
            while end_list == 0:
                ticker = input('Enter ticker #' + str(count) + ', or ! to end\n')
                if ticker == '!':
                    end_list += 1
                else:
                    list2run.append(ticker)
                    count += 1
            choice = operation
            close_loop += 1
        elif operation == 3:
            for ticker in master_list:
                list2run.append(ticker)
            choice = operation
            close_loop += 1
    return choice


# Choose to run list, or master list
def master_or_run(choice):
    if choice == 1:
        append_data_to_summary(list_to_run)
    elif choice == 2:
        append_data_to_summary(list_to_run)
    elif choice == 3:
        get_financial_summary(master_ticker_list)


# Cross references the entered tickers to the master ticker list, and combines and sorts the two lists into one list.
def combine_lists(master_list, run_list):
    combined_list = []
    for ticker in master_list:
        combined_list.append(ticker)
    for ticker in run_list:
        if ticker not in master_list:
            combined_list.append(ticker)
    combined_list = sorted(combined_list)
    return combined_list


# Overwrites the master ticker list to contain all the tickers in the new combined list.
def new_list_to_csv(master_list):
    file = open('master_ticker_list.csv', 'w')
    write = csv.writer(file)
    write.writerow(master_list)
    file.close()


# Get the finance summary for each ticker in the run list.
def get_financial_summary(master_list):
    prices = []
    eps_ttm = []
    eps_yield = []
    market_cap = []
    previous_close = []

    print('Processing Financial Summary...')
    for ticker in master_list:
        try:
            price = si.get_quote_table(ticker)["Quote Price"]
            prices.append(price)
        except IndexError as e:
            prices.append("Error")
        except ValueError as v:
            prices.append("Error")
        except KeyError as k:
            prices.append("Error")

        try:
            eps = si.get_quote_table(ticker)["EPS (TTM)"]
            eps_ttm.append(eps)
        except IndexError as e:
            eps_ttm.append("Error")
        except ValueError as v:
            eps_ttm.append("Error")
        except KeyError as k:
            eps_ttm.append("Error")

        try:
            mc = si.get_quote_table(ticker)["Market Cap"]
            market_cap.append(mc)
        except IndexError as e:
            market_cap.append("Error")
        except ValueError as v:
            market_cap.append("Error")
        except KeyError as k:
            market_cap.append("Error")

        try:
            pc = si.get_quote_table(ticker)["Previous Close"]
            previous_close.append(pc)
        except IndexError as e:
            previous_close.append("Error")
        except ValueError as v:
            previous_close.append("Error")
        except KeyError as k:
            previous_close.append("Error")

        eps_yield.append(eps / price)
        print('Processing data for ' + ticker)

    # Call Dataframe constructor after zipping lists together. Each list is a column.
    df = pd.DataFrame(list(zip(master_list, prices, eps_ttm, eps_yield, market_cap, previous_close)),
                      columns=['Ticker', 'Price', 'EPS (TTM)', 'EPS Yield', 'Market Cap', 'Previous Close'])
    df.to_csv('Financial Summary - Master List.csv')
    print('Done.')


# Append data to Financial Summary
def append_data_to_summary(run_list):
    prices = []
    eps_ttm = []
    eps_yield = []
    market_cap = []
    previous_close = []

    print('Processing Financial Summary...')
    for ticker in run_list:
        try:
            price = si.get_quote_table(ticker)["Quote Price"]
            prices.append(price)
        except IndexError as e:
            prices.append("Error")
        except ValueError as v:
            prices.append("Error")
        except KeyError as k:
            prices.append("Error")

        try:
            eps = si.get_quote_table(ticker)["EPS (TTM)"]
            eps_ttm.append(eps)
        except IndexError as e:
            eps_ttm.append("Error")
        except ValueError as v:
            eps_ttm.append("Error")
        except KeyError as k:
            eps_ttm.append("Error")

        try:
            mc = si.get_quote_table(ticker)["Market Cap"]
            market_cap.append(mc)
        except IndexError as e:
            market_cap.append("Error")
        except ValueError as v:
            market_cap.append("Error")
        except KeyError as k:
            market_cap.append("Error")

        try:
            pc = si.get_quote_table(ticker)["Previous Close"]
            previous_close.append(pc)
        except IndexError as e:
            previous_close.append("Error")
        except ValueError as v:
            previous_close.append("Error")
        except KeyError as k:
            previous_close.append("Error")

        eps_yield.append(eps / price)
        print(ticker)

    # Call Dataframe constructor after zipping lists together. Each list is a column.
    df = pd.DataFrame(list(zip(run_list, prices, eps_ttm, eps_yield, market_cap, previous_close)),
                      columns=['Ticker', 'Price', 'EPS (TTM)', 'EPS Yield', 'Market Cap', 'Previous Close'])
    df.to_csv('Financial Summary - Master List.csv', mode='a', header=False)


# Get the Balance Sheet for each ticker in the run list.
def get_balance_sheet_data(run_list, choice):
    # Get all balance sheets and compile into one.
    print('Processing Balance Sheets...')
    count = 1
    bs_df = pd.DataFrame(columns=['Breakdown', 'Fiscal Year Ending', 'Value', 'Ticker'])
    for ticker in run_list:
        print('Working on Balance Sheet ' + str(count) + ' of ' + str(len(run_list)))
        balance_sheet = si.get_balance_sheet(ticker)
        df = pd.DataFrame(balance_sheet)
        df.to_csv('temp.csv')
        df = pd.read_csv('temp.csv')

        # Transpose the Fiscal Year Ending Columns
        try:
            df = df.melt(id_vars=['Breakdown'], var_name='Fiscal Year Ending', value_name='Value')
        except KeyError:
            pass

        # Create a column with the ticker N times and add to dataframe
        t_column = [ticker] * len(df)
        df['Ticker'] = t_column

        # Append data to Master Balance Sheet
        bs_df = bs_df.append(df, ignore_index=True)

        # increase count
        count += 1
    if choice == 1:
        bs_df.to_csv('master_balance_sheet.csv', mode='a', header=False)
    elif choice == 2:
        bs_df.to_csv('master_balance_sheet.csv', mode='a', header=False)
    else:
        bs_df.to_csv('master_balance_sheet.csv')


# Get the Income Statement for each ticker in the run list.
def get_income_statement_data(run_list, choice):
    # Get all balance sheets and compile into one.
    print('Processing Income Statements...')
    count = 1
    is_df = pd.DataFrame(columns=['Breakdown', 'Fiscal Year Ending', 'Value', 'Ticker'])
    for ticker in run_list:
        print('Working on Income Statement ' + str(count) + ' of ' + str(len(run_list)))
        try:
            income_statement = si.get_income_statement(ticker)
        except KeyError:
            pass
        except TypeError:
            pass
        df = pd.DataFrame(income_statement)
        df.to_csv('temp.csv')
        df = pd.read_csv('temp.csv')

        # Transpose the Fiscal Year Ending Columns
        df = df.melt(id_vars=['Breakdown'], var_name='Fiscal Year Ending', value_name='Value')

        # Create a column with the ticker N times and add to dataframe
        t_column = [ticker] * len(df)
        df['Ticker'] = t_column

        # Append data to Master Balance Sheet
        is_df = is_df.append(df, ignore_index=True)

        # increase count
        count += 1
    if choice == 1:
        is_df.to_csv('master_income_statement.csv', mode='a', header=False)
    elif choice == 2:
        is_df.to_csv('master_income_statement.csv', mode='a', header=False)
    else:
        is_df.to_csv('master_income_statement.csv')


# Get the Cashflow Statement for each ticker in the run list.
def get_cashflow_data(run_list, choice):
    # Get all balance sheets and compile into one.
    print('Processing Cashflow Statements...')
    count = 1
    cf_df = pd.DataFrame(columns=['Breakdown', 'Fiscal Year Ending', 'Value', 'Ticker'])
    for ticker in run_list:
        print('Working on Cashflow Statement ' + str(count) + ' of ' + str(len(run_list)))
        try:
            cashflow_statement = si.get_cash_flow(ticker)
        except KeyError:
            pass
        except TypeError:
            pass
        df = pd.DataFrame(cashflow_statement)
        df.to_csv('temp.csv')
        df = pd.read_csv('temp.csv')

        # Transpose the Fiscal Year Ending Columns
        df = df.melt(id_vars=['Breakdown'], var_name='Fiscal Year Ending', value_name='Value')

        # Create a column with the ticker N times and add to dataframe
        t_column = [ticker] * len(df)
        df['Ticker'] = t_column

        # Append data to Master Balance Sheet
        cf_df = cf_df.append(df, ignore_index=True)

        # increase count
        count += 1
    if choice == 1:
        cf_df.to_csv('master_cashflow_statement.csv', mode='a', header=False)
    elif choice == 2:
        cf_df.to_csv('master_cashflow_statement.csv', mode='a', header=False)
    else:
        cf_df.to_csv('master_cashflow_statement.csv')


def getQuoteData(run_list, choice):
    count = 1
    dfm = pd.DataFrame()
    print('Processing Quote Data for ticker...')
    for ticker in run_list:
        print('... ' + str(count) + ' of ' + str(len(run_list)))
        data = si.get_quote_data(ticker)
        df = pd.DataFrame.from_dict(data, orient='index')
        t_column = [ticker] * len(df)
        df['Ticker'] = t_column
        dfm = dfm.append(df)
        if choice == 1:
            dfm.to_csv('quote_data.csv', mode='a', header=False)
        elif choice == 2:
            dfm.to_csv('quote_data.csv', mode='a', header=False)
        elif choice == 3:
            dfm.to_csv('quote_data.csv', header=False)
        count += 1
    print('Done.\nQuote Data Saved.')


def quarterly_statements(run_list):
    q_Balance_Sheets = pd.DataFrame()
    q_Income_Statements = pd.DataFrame()
    q_Cashflow_Statements = pd.DataFrame()
    y_Balance_Sheets = pd.DataFrame()
    y_Income_Statements = pd.DataFrame()
    y_Cashflow_Statements = pd.DataFrame()
    count = 1
    for ticker in run_list:
        data = si.get_financials(ticker)
        listing = list(data)
        print("Getting financial statements for $" + str(ticker) + " (" + str(count) + " of " + str(len(run_list)) + ")")
        count += 1
        for name in listing:
            df = data[name]
            print(df)
            if name == "yearly_income_statement":
                y_Income_Statements.append(df)
            elif name == "yearly_balance_sheet":
                y_Balance_Sheets.append(df)
            elif name == "yearly_cash_flow":
                y_Cashflow_Statements.append(df)
            elif name == "quarterly_income_statement":
                q_Income_Statements.append(df)
            elif name == "quarterly_balance_sheet":
                q_Balance_Sheets.append(df)
            elif name == "quarterly_cash_flow":
                q_Cashflow_Statements.append(df)
    y_Balance_Sheets.to_csv("y_Balance_Sheets.csv")
    y_Income_Statements.to_csv("y_Income_Statements.csv")
    y_Cashflow_Statements.to_csv("y_Cashflow_Statements.csv")
    q_Balance_Sheets.to_csv("q_Balance_Sheets.csv")
    q_Income_Statements.to_csv("q_Income_Statements.csv")
    q_Cashflow_Statements.to_csv("q_Cashflow_Statements.csv")




#decision = input("Do you want to:\n1 - Refresh Prices\n2 - Run prices and statements\n")

# Instantiate the list to run each time.
list_to_run = []

#quarterly_statements(list_to_run)

# Run the program
run_path = int(input("What do you want to do?\n1 - Run Prices\n2 - Run Everything\n"))
master_ticker_list = get_tickers()
list_run_choice = choose_operation(list_to_run, master_ticker_list)

# Combine run list and master list and save to CSV
master_ticker_list = combine_lists(master_ticker_list, list_to_run)
new_list_to_csv(master_ticker_list)

if run_path == 1:
    getQuoteData(list_to_run, list_run_choice)
elif run_path == 2:
    getQuoteData(list_to_run, list_run_choice)
    get_balance_sheet_data(list_to_run, list_run_choice)
    get_income_statement_data(list_to_run, list_run_choice)
    get_cashflow_data(list_to_run, list_run_choice)


