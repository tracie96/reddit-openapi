import os
import requests
from fastapi import FastAPI
from dotenv import load_dotenv
from newsapi import NewsApiClient

load_dotenv()
app=FastAPI()

PER_SCRIPT=os.getenv('PER_SCRIPT')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')
headers = {'User-Agent': 'MyBot/0.0.1'}
USERNAME=os.getenv('USERNAME')
PASSWORD=os.getenv('PASSWORD')
NEWSAPIKEY=os.getenv('NEWSAPIKEY')

newsapi = NewsApiClient(api_key=NEWSAPIKEY)

auth = requests.auth.HTTPBasicAuth(PER_SCRIPT, CLIENT_SECRET)
data = {'grant_type': 'password','username': USERNAME,'password': PASSWORD}

res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers,timeout=3)

# Initialize array to store objects
allist=[]

# Make call  to receive api token from reddit
TOKEN = res.json()['access_token']

# Set token to  header
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

allist=[]

# endpoint for api calls
def api():
    list = requests.get('https://oauth.reddit.com/hot', headers=headers)
    # Looping through to store value
    for post in list.json()['data']['children']:
        allist.append({'headline': post['data']['title'], 'link': post['data']['url'], 'source': 'reddit'})
    #newsapi fetch
    all_articles = newsapi.get_everything(q='bitcoin')
    # Looping through to store value
    for posts in all_articles['articles']:
        allist.append({'headline': posts['title'], 'link': posts['url'], 'source': 'newsapi'})
    return allist

#fetches all the post

@app.get("/news")
def index():
    fetchmylist = api()
    return fetchmylist

#search through news content for query strings

@app.get("/news/")
def search(query:str):
    fetchmylist = api()
    cleandata = []
    querysearch=[query]
    for d in fetchmylist:
        if any(word in d['headline'] for word in querysearch):
            cleandata.append(d)
    return cleandata