from datetime import datetime
from requests import Session
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import time
from psycopg2.extras import RealDictCursor

page_url = "https://www.nseindia.com/get-quotes/equity?symbol=LT"
chart_data_url = "https://www.nseindia.com/api/chart-databyindex"

s= Session()

h = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }

s.headers.update(h)
r = s.get(page_url)
def fetch_data(symbol):
    data = {"index": symbol + "EQN"}
    r = s.get(chart_data_url, params=data)
    data = r.json()['grapthData']
    return [[datetime.utcfromtimestamp(d[0]/1000),d[1]] for d in data]

data = fetch_data("MARUTI")
with psycopg2.connect(
    host="localhost",
    database="tickdata",
    port="5432",
    user="postgres",
    password="passkey",
    cursor_factory=RealDictCursor,
) as conn:
    with conn.cursor() as cur:
        sql = """INSERT INTO pytick (data,sequence) VALUES (%s,%s) RETURNING *"""
        
        cur.executemany(sql, data)









#while True:
 #   try:
  #      conn=psycopg2.connect(host='localhost',database='tickdata',port='5432',user='postgres',password='passkey',cursor_factory=RealDictCursor)
   #     cursor=conn.cursor()
    #    print("Connected")
     #   break
    #except Exception as e:
     #   print("Connection to database failed")
      #  print("Error",e)
       # time.sleep(2)

#sqlcode=cursor.execute("""INSERT INTO pytick (id,sequence) VALUES (%s,%s) RETURNING *""")
#dat=cursor.fetchone()
#conn.commit()

#for i in exe:
 #   cursor.execute(sqlcode,(i['id'],i[se]))
