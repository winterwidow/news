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
        if data.get("status") == "ok" and data.get("totalResults", 0) > 0: 
            results[company] = data["articles"]
        else:
            results[company] = []
    
    return results

#main
#companies=['IDFC FIRST BANK LIMITED']
companies=load_companies('comp.txt')
api_key = open('news_api.txt','r').read().strip()
news_results = check_news(companies, api_key)

with open("news_results.csv",'w',newline='',encoding='utf-8')as file:

    csvwriter=csv.writer(file)
    csvwriter.writerow(['Company','Title','Description','Published Date'])

    for company,articles in news_results.items():
        
        if len(articles)==0:  #no recent news
            continue
        else:
            #print(f"\nNews for {company}:")
            '''date_only = articles['publishedAt'].split("T")[0]
            csvwriter.writerow([company,articles,date_only])'''

            for article in articles:
                date_only = article['publishedAt'].split("T")[0]
                #print(f"- {article['title']} (Published on: {date_only})")
                csvwriter.writerow([
                company,
                article['title'],
                article['description'],
                date_only
            ])
print(news_results)