import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

url = 'https://screener.in/company/RELIANCE/consolidated/'
webpage = requests.get(url)
soup = bs(webpage.text,'html.parser')

data = soup.find('section', id="profit-loss")
tdata= data.find("table")

table_data = []

for row in tdata.find_all('tr'):
    row_data = []
    for cell in row.find_all(['th','td']):
        row_data.append(cell.text.strip())
    table_data.append(row_data)


df_table = pd.DataFrame(table_data)
df_table.iloc[0,0] = 'Section'
df_table.columns = df_table.iloc[0]

df_table = df_table.iloc[1:,:-1]

# Transpose the dataframe
df_table_transposed = df_table.transpose()

# Reset the index to get a clean column name
df_table_transposed.reset_index(inplace=True)

# Rename the columns
df_table_transposed.columns = ['Section', 'Values']

# Now you can load the transposed dataframe to PostgreSQL
df_table_transposed.to_sql('profit_loss_data_transposed', engine, if_exists='replace', index=False)

print("Data loaded to PostgreSQL")


db_host = "172.27.80.1" #"192.168.29.101"
db_name = "exampledb"
db_user = "docker"
db_password = "docker"
db_port = "5432"

engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

df_table.to_sql('profit_loss_data', engine, if_exists='replace', index=True)

print("Data loaded to PostgreSQL")
