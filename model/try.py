import os
from dotenv import load_dotenv
load_dotenv()

sql_password = os.getenv("SQL_PASSWORD")

print(sql_password)