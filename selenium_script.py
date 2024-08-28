from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import os
import pandas as pd
from openpyxl import load_workbook
from sqlalchemy import create_engine
import psycopg2
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")



username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
stock_code = os.environ.get('STOCK_CODE')

print(username)
print(password)

current_dir = os.getcwd()
prefs = {
    "download.default_directory": current_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

service = Service('/usr/local/bin/chromedriver')

driver = webdriver.Chrome(service=service, options=chrome_options)

def login(username, password):
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "account", " " ))]'))
    )
    login_button.click()

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[(@id = "id_username")]'))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[(@id = "id_password")]'))
    )

    email_input.send_keys(username)
    password_input.send_keys(password)

    second_login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-user", " " ))]'))
    )
    second_login_button.click()



driver.get("https://www.screener.in/company/RELIANCE/consolidated/")

export = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-download", " " ))]'))
)
export.click()

login(username, password)
# login("firstscreener123@gmail.com", "Asdf!234")

export = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "icon-download", " " ))]'))
)
export.click()
time.sleep(10)
download_dir = current_dir
print("Files in download directory before wait:", os.listdir(download_dir))



# Read Excel file into pandas DataFrame
# df = pd.read_excel(os.path.join(download_dir, "Reliance Industr.xlsx"),header=0)

# # Read Excel file into pandas DataFrame
# # df = pd.read_excel("Reliance Industr.xlsx")

# # Print column names
# print(df.columns)

# # Select rows and columns
# df = df.iloc[1:20, :11]

# # Print resulting DataFrame
# print(df)

col = ["Section", "Mar-15", "Mar-16", "Mar-17", "Mar-18", "Mar-19", "Mar-20", "Mar-21", "Mar-22", "Mar-23", "Mar-24"]

df = pd.read_excel("Reliance Industr.xlsx", sheet_name="Data Sheet", skiprows=1, header=None, names=col)

# Print column names
print(df.columns)

# Select rows and columns
df = df.iloc[15:30, :11]

stock_code = os.environ.get('STOCK_CODE')
df['Stock_Code'] = stock_code

# Print resulting DataFrame
print(df)




db_host = "172.27.80.1" #"192.168.29.101"
db_name = "exampledb"
db_user = "docker"
db_password = "docker"
db_port = "5432"

# Create the database engine
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Load the transposed DataFrame into the PostgreSQL database
df.to_sql('companies_data', engine, if_exists='replace', index=False)




print("Data loaded successfully into PostgreSQL database!")
