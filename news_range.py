import requests
from datetime import datetime,timedelta
def check_news(companies, api_key):
    url = "https://newsapi.org/v2/everything"
    headers = {"Authorization": f"Bearer {api_key}"}
    results = {} #to store the articles in dict form 'comp:article'

    fromdate=(datetime.today()-timedelta(days=5*365)).strftime("%y-%m-%d")
    todate=datetime.today().strftime("%y-%m-%d")
    for company in companies:
        params = {"q": company, "sortBy": "publishedAt", "pageSize": 5,'from':fromdate,'to':todate}  #parameters for the api
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
news_results = check_news(companies, api_key)
for company, articles in news_results.items():

    print(f"\nNews for {company}:")

    for article in articles:
        print(f"- {article['title']} (Published on: {article['publishedAt']})")
