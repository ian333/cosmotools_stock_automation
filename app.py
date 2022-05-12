#Python Decouple
import json
from typing import Optional
from decouple import config

#Fastapi & Pydantic

from fastapi import  Body, FastAPI,status
from pydantic import BaseModel, HttpUrl

#HTTPX
import httpx



app=FastAPI()

#Models

#URL's
URL_MELI='https://api.mercadolibre.com/oauth/token' 
URL_MELI_SERVER='https://auth.mercadolibre.com.mx/authorization'

#curl -X POST \
#-H 'accept: application/json' \
#-H 'content-type: application/x-www-form-urlencoded' \
#'https://api.mercadolibre.com/oauth/token' \
#-d 'grant_type=authorization_code' \
#-d 'client_id=$APP_ID' \
#-d 'client_secret=$SECRET_KEY' \
#-d 'code=$SERVER_GENERATED_AUTHORIZATION_CODE' \
#-d 'redirect_uri=$REDIRECT_URI'

class AccessToken(BaseModel):
    grant_type: str 
    client_id: str 
    redirec_uri: HttpUrl = None
    client_secret:str

class RefreshToken(AccessToken):
    refreshtoken:str
    accesstoken:str 
    user_id:Optional[str]

class ServerGeneratedCode(AccessToken):
    
    code: str 
    redirect_uri: HttpUrl 

headers={
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded'}


#Mercado Libre

@app.post(
    path="/code_to_token",
    tags=["Login"]
)
async def code_to_token():
    data={
        'grant_type':'authorization_code',
        'client_id':config('CLIENT_ID'),
        'client_secret':config('CLIENT_SECRET'),
        'code':config('SERVER_CODE'),
        'redirect_uri':config('REDIRECT_URI')
    }

    r=httpx.post("https://api.mercadolibre.com/oauth/token",headers=headers,data=data)
    with open('responses.json','w',encoding="UTF-8") as f:
        f.write(str(r.text))
    return r.json()

@app.post(
    path="/refresh_token",
    tags=["Login"]
)
def refresh_token():
    with open ('responses.json','r+',encoding='UTF-8') as f:
        info = json.load(f)
        data={
        'grant_type':'refresh_token',
        'client_id':config('CLIENT_ID'),
        'client_secret':config('CLIENT_SECRET'),
        'refresh_token':info['refresh_token']
        }
        r = httpx.post(URL_MELI,headers=headers,data=data)
        response=r.json()
        f.seek(0)
        f.truncate(0)
        f.write(json.dumps(response))
    return response           
    
@app.get("/get_code")
def get_code_server():
    params={
        "response_type":"code",
        "client_id":config('CLIENT_ID'),
        "redirect_uri":config('REDIRECT_URI')
    }
    req=httpx.get(URL_MELI_SERVER,params=params)

##Home
@app.get(
    "/",
    status_code=status.HTTP_200_OK)
def home():
    return {"Message" : "Hello World"}
## OAUTH2.0



@app.post(
   "/hola"
    )
def code_for_token(token:ServerGeneratedCode = Body(...)):
    pass

@app.post(
    "/test_user",
    tags=["Test User"]
)
def test_user():
    with open ('responses.json','r',encoding='UTF-8') as f:
            info = json.load(f)
            headers ={
                'Authorization': f'Bearer {info["access_token"]}',
                'content-type':'application/json'
            }
            data="{'site_id':'MLM'}"
            r = httpx.post('https://api.mercadolibre.com/users/test_user',headers=headers,data=data)
    with open("user.json","r+",encoding='UTF-8') as f:
        results=json.loads(f.read())
        results.append(r.json())
        f.seek(0)
        f.write(json.dumps(results))

    return r.json()