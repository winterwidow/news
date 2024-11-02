'''news for the day before'''
import requests
from datetime import datetime,timedelta

def load_companies(filename):

    with open(filename, 'r') as file:
        companies = [line.strip() for line in file if line.strip()]
    return companies

def check_news(companies, api_key,date):

    url = "https://newsapi.org/v2/everything"
    headers = {"Authorization": f"Bearer {api_key}"}
    results = {} #to store the articles in dict form 'comp:article'

    for company in companies:
        params = {"q": company, 
                  "sortBy": "publishedAt", 
                  "from":date,
                  "to":date,
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
#companies=['IDFC FIRST BANK LIMITED']
companies=load_companies('comp.txt')
api_key = open('news_api.txt','r').read()

date= (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d') #yesterday 

news_results = check_news(companies, api_key,date)

for company,articles in news_results.items():
    if len(articles)==0:  #no recent news
        continue
    else:
        print(f"\nNews for {company}:")
        for article in articles:
            date_only = article['publishedAt'].split("T")[0]
            print(f"- {article['title']} (Published on: {date_only})")
#print(news_results)
