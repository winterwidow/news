'''news for the day before'''

import requests
from datetime import datetime,timedelta
def check_news(companies, api_key,date):
    url = "https://newsapi.org/v2/everything"
    headers = {"Authorization": f"Bearer {api_key}"}
    results = {} #to store the articles in dict form 'comp:article'

    for company in companies:
        params = {"q": company, "sortBy": "publishedAt", "pageSize": 5,"from":date,"to":datetime.today(),'language':'en'}  #parameters for the api
        #limits to 5 recent articles sorted with the most recent on top
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        # Save recent articles for each company
        if data["status"] == "ok" and data["totalResults"] > 0: #"ok": success(defined by api)
            results[company] = data["articles"]
        else:
            results[company] = []
    
    return results 

#main
companies = ["Apple"]
api_key = open('news_api.txt','r').read()
date= (datetime.today()-timedelta(days=1*365)).strftime("%y-%m-%d") #yesterday 
news_results = check_news(companies, api_key,date)
for company, articles in news_results.items():

    print(f"\nNews for {company}:")

    for article in articles:
        print(f"- {article['title']} (Published on: {article['publishedAt']})")
