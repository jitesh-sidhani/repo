
import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2


 
# URL of the webpage to scrape
url = "https://www.screener.in/company/RELIANCE/consolidated/"
 
# Send a GET request to the URL
response = requests.get(url)
 
# Check if the request was successful
if response.status_code == 200:
    print("Page retrieved successfully.")
else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
    exit()
 
# Parse the HTML content of the page
soup = BeautifulSoup(response.content, "html.parser")
 
# Scrape the "Profit & Loss" data
profit_loss_table = soup.find("section", {"id": "profit-loss"}, class_="card card-large")
 
if profit_loss_table:
    datatable = profit_loss_table.find("table")
    
    table_data = []
    for row in datatable.find_all('tr'):
        row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
        table_data.append(row_data)
 
    # Convert the data into a DataFrame
    df = pd.DataFrame(table_data)
 
    # Display the DataFrame
    #+print(df)
 
    # Save the DataFrame to a CSV file
    df.to_csv("profit_m.csv", index=False)
    print("Profit & Loss data saved to 'profit_m.csv'.")
else:
    print("Profit & Loss table not found on the page.")
    exit()
 
# Clean the data
df.replace(',', '', regex=True, inplace=True)
df.replace('%', '', regex=True, inplace=True)
 
# Assuming the first row is the header and the rest is data
df.columns = df.iloc[0]
df = df.drop(0).reset_index(drop=True)
 
# Convert columns to numeric, ignoring errors
df = df.apply(lambda x: pd.to_numeric(x, errors='coerce'))
 
# Fill NaN values with 0
df.fillna(0, inplace=True)
 
# Database connection parameters (retrieved from Vault or environment variables)
db_name = "concourse"
db_user = "concourse_user"
db_password = "concourse_pass"
db_host = "localhost"
db_port = "5432"
 
# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)
cursor = conn.cursor()
 
# Create table if not exists
create_table_query = '''
CREATE TABLE IF NOT EXISTS profit_loss (
    year TEXT,
    sales BIGINT,
    expenses BIGINT,
    operating_profit BIGINT,
    opm_percentage FLOAT,
    other_income BIGINT,
    interest BIGINT,
    depreciation BIGINT,
    profit_before_tax BIGINT,
    tax_percentage FLOAT,
    net_profit BIGINT,
    eps_in_rs FLOAT,
    dividend_payout_percentage FLOAT
);
'''
cursor.execute(create_table_query)
conn.commit()
 
# Insert data into the PostgreSQL table
for _, row in df.iterrows():
    cursor.execute('''
    INSERT INTO profit_loss (
        year, sales, expenses, operating_profit, opm_percentage,
        other_income, interest, depreciation, profit_before_tax,
        tax_percentage, net_profit, eps_in_rs, dividend_payout_percentage
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    ''', tuple(row[:13]))  # Ensure the tuple matches the columns
 
conn.commit()
 
cursor.close()
conn.close()






























# import requests
# from bs4 import BeautifulSoup as bs
# import pandas as pd
# import csv
# url = 'https://screener.in/company/RELIANCE/consolidated/' 
# webpage = requests.get(url)
# soup = bs(webpage.text,'html.parser')
# data = soup.find('section', id="profit-loss", class_="card card-large")
# tdata= data.find("table")

# table_data = []
 
# for row in tdata.find_all('tr'):
#     row_data = []
#     for cell in row.find_all(['th','td']):
#         row_data.append(cell.text.strip())
#     table_data.append(row_data)

# with open("table_data.csv", 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(table_data)


# df_table = pd.DataFrame(table_data)
# df_table.columns = df_table.iloc[0]
# df_table = df_table[1:]
# df_table = df_table.set_index('')
# print(df_table)



















