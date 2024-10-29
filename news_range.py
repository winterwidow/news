'''news for 5 years'''
import requests
from datetime import datetime,timedelta
import csv

def load_companies(filename):

    with open(filename, 'r') as file:
        companies = [line.strip() for line in file if line.strip()]
    return companies

def check_news(companies, api_key):
    url = "https://newsapi.org/v2/everything"
    headers = {"Authorization": f"Bearer {api_key}"}
    results = {} #to store the articles in dict form 'comp:article'

    fromdate=(datetime.today()-timedelta(days=5*365)).strftime("%y-%m-%d")
    todate=datetime.today().strftime("%y-%m-%d")

    for company in companies:
        params = {"q": company,
                  "sortBy": "publishedAt", 
                  'from':fromdate,
                  'to':todate,
                  'language':'en'}  #parameters for the api

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        #save recent articles for each company
        if data["status"] == "ok" and data["totalResults"] > 0: #"ok": success(defined by api)
            results[company] = data["articles"]
        else:
            results[company] = []
    
    return results

#main
companies=load_companies('companies.txt')
api_key = open('news_api_2.txt','r').read()
news_results = check_news(companies, api_key)

with open("news_results.csv",'w',newline='',encoding='utf-8')as file:
    csvwriter=csv.writer(file)
    csvwriter.writerow(['Company','Article','Date'])
    for company,articles in news_results.items():
        if len(articles)==0:  #no recent news
            continue
        else:
            print(f"\nNews for {company}:")
            for article in articles:
                date_only = article['publishedAt'].split("T")[0]
                #print(f"- {article['title']} (Published on: {date_only})")
                csvwriter.writerow([company,article,date_only])
file.close()