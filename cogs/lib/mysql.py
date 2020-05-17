import mysql.connector
import urllib.request
from dotenv import load_dotenv
from os import getenv

load_dotenv()

config = {
  'user': 'sam',
  'password': getenv("MYSQLPW"),
  'database': 'wca_stats',
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)
