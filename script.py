import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
name=os.getenv('VAULT_USERNAME')

# # URL of the webpage
# url = 'https://screener.in/company/RELIANCE/consolidated/'

# # Fetch the webpage
# webpage = requests.get(url)

# # Parse the HTML content
# soup = bs(webpage.text, 'html.parser')

# # Find the profit and loss section
# data = soup.find('section', id="profit-loss")

# # Find the table within the section
# tdata = data.find("table")

# # Extract table data
# table_data = []
# for row in tdata.find_all('tr'):
#     row_data = []
#     for cell in row.find_all(['th', 'td']):
#         row_data.append(cell.text.strip())
#     table_data.append(row_data)

# # Create a DataFrame from the table data
# df_table = pd.DataFrame(table_data)

# # Set the first row as the header and drop it from the DataFrame
# df_table.iloc[0, 0] = 'Section'
# df_table.columns = df_table.iloc[0]
# df_table = df_table.iloc[1:, :-1]

# # Clean and transform the data
# for i in df_table.iloc[:, 1:].columns:
#     df_table[i] = df_table[i].str.replace(',', '').str.replace('%', '').apply(eval)

# # Transpose the DataFrame
# df_table_transposed = df_table.T
# df_table_transposed.columns = df_table_transposed.iloc[0]
# df_table_transposed = df_table_transposed[1:]

# df_table_transposed.index.name= "year_month"

# # Reset index to make 'year_month' a column
# df_table_transposed.reset_index(inplace=True)

# db_host = "172.27.80.1" #"192.168.29.101"
# db_name = "exampledb"
# db_user = "docker"
# db_password = "docker"
# db_port = "5432"

# # Create the database engine
# engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# # Load the transposed DataFrame into the PostgreSQL database
# df_table_transposed.to_sql('profit_loss_data_transposed', engine, if_exists='replace', index=True)


print(name)

print("Data loaded successfully into PostgreSQL database!")
 



