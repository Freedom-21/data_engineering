import requests
from bs4 import BeautifulSoup
import pandas as pd 
import sqlite3

url = "https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films"
db_name = 'Movie.db'
table_name = 'Top 50'
csv_path = '/home/freedom/Documents/IBM_DE/course _3_project/web_scraping/top_50_films.csv'
df = pd.DataFrame(columns=['Film','Year','Rotten Tomatoes'])
count = 0

# let's load the web page for webscraping

html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

#scraping of required information
tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows:
    if count < 25:
        col = row.find_all('td')
        if len(col)!=0:
            data_dict = {
                            "Film":col[1].contents[0],
                            "Year":col[2].contents[0],
                            "Rotten Tomatoes":col[3].contents[0]
                        }
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
            count += 1
    else:
        break


print(df)
# print(df.groupby('Rotten Tomatoes'))

#storing the data

# to csv file we define when we start 
df.to_csv(csv_path)

# to the database file we defined at the start
conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()


