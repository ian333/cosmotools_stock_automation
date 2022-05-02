


#Python Decouple
import json
from typing import Optional
from decouple import config

#Fastapi & Pydantic

from fastapi import APIRouter, Body, FastAPI,status
from pydantic import BaseModel, Field, HttpUrl

#HTTPX
import httpx



app=FastAPI()

#Models

#URL's
URL_MELI='https://api.mercadolibre.com/oauth/token' 

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
    grant_type: str = Field(...,example="authorization_code")
    client_id: str = Field(...,example=config('CLIENT_ID'))
    code: str = Field (...)
    redirec_uri: HttpUrl 

class RefreshToken(AccessToken):
    refreshtoken:str= Field(...)

class ServerGeneratedCode(AccessToken):
    client_secret:str= Field(...,example=config('CLIENT_SECRET'))

#Mercado Libre
meli_code=APIRouter()

@meli_code.post(URL_MELI)
def code_to_token():
    """headers={
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded'}
    data={
        'grant_type':'authorization_code',
        'client_id':config('CLIENT_ID'),
        'client_secret':config('CLIENT_SECRET'),
        'code':'{Server_code.code}',
        'redirect_uri':config('REDIRECT_URI',cast=str)
    }
    r=httpx.post(URL_MELI,headers=headers,data=data)
    return r"""
    pass

@app.post(
    path="/code_to_token"
)
def code_to_token():
    headers={
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded'}
    data={
        'grant_type':'authorization_code',
        'client_id':config('CLIENT_ID'),
        'client_secret':config('CLIENT_SECRET'),
        'code':config('SERVER_CODE'),
        'redirect_uri':config('REDIRECT_URI',cast=str)
    }
    r=httpx.post("https://api.mercadolibre.com/oauth/token",headers=headers,data=data)
    with open('responses.json','w',encoding="UTF-8") as f:
        f.write(str(r.text))
    return r.text

##Home
@app.get(
    "/",
    status_code=status.HTTP_200_OK)
def home():
    return {"Message" : "Hello World"}
## OAUTH2.0



@app.post(
   "/holi"
    )
def code_for_token(token:ServerGeneratedCode = Body(...)):
    pass

