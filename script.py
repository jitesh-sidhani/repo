import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv
url = 'https://screener.in/company/RELIANCE/consolidated/' #f'https://screener.in/company/{n50_company_list[1]}/consolidated/'
webpage = requests.get(url)
soup = bs(webpage.text,'html.parser')
data = soup.find('section', id="profit-loss", class_="card card-large")
tdata= data.find("table")

table_data = []
 
for row in tdata.find_all('tr'):
    row_data = []
    for cell in row.find_all(['th','td']):
        row_data.append(cell.text.strip())
    table_data.append(row_data)

with open("table_data.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(table_data)


df_table = pd.DataFrame(table_data)
df_table.columns = df_table.iloc[0]
df_table = df_table[1:]
df_table = df_table.set_index('')
print(df_table)





















# import os
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# def login(username, password):
#     login_button = WebDriverWait(driver, 5).until(
#         EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "account", " " ))]'))
#     )
#     login_button.click()
#     email_input = WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located((By.XPATH, '//*[(@id = "id_username")]'))
#     )
#     password_input = WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located((By.XPATH, '//*[(@id = "id_password")]'))
#     )
#     email_input.send_keys(username)
#     password_input.send_keys(password)
#     second_login_button = WebDriverWait(driver, 5).until(
#         EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-user", " " ))]'))
#     )
#     second_login_button.click()

# driver = webdriver.Chrome()
# driver.maximize_window()
# driver.get("https://www.screener.in/company/RELIANCE/consolidated/")
# login(os.environ['VAULT_USERNAME'], os.environ['VAULT_PASSWORD'])

# export = WebDriverWait(driver, 5).until(
#     EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-download", " " ))]'))
# )
# export.click()
