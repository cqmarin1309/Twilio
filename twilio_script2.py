"""
************************************************************************
* Author = @alexbonella                                                *
* Date = '15/09/2022'                                                  *
* Description = Envio de mensajes Twilio con Python                    *
************************************************************************
"""


import os
from twilio.rest import Client
from twilio_config import * #Se está importando todo el contenido del módulo twilio_config (es un archivo .py)
import time

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


import pandas as pd
import requests
from bs4  import BeautifulSoup
from tqdm import tqdm #Esto es para ver la barra de progreso

from datetime import datetime



query = 'Cuzco'
api_key = API_KEY_WAPI


def get_forecast(response,i):
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']

    return fecha, hora, condicion, tempe, rain, prob_rain


datos = [] #Creamos un array vacio

#Es para iterar sobre todas las horas (24 h), de 0 a 23 horas
for i in tqdm(range(len(response['forecast']['forecastday'][0]['hour'])),colour = 'blue'):
    
    datos.append(get_forecast(response,i))


#Creamos las columnas
col = ['Fecha', 'Hora', 'Condicion','Temperatura', 'Lluvia', 'Prob.rain']
df = pd.DataFrame(datos,columns=col)

#Filtramos el dataset por las horas de lluvia y en un rango de horas adecuado (6am a 22pm)
df_rain = df[(df['Lluvia']==1) & (df['Hora']>6) & (df['Hora']<22)]
df_rain = df_rain[['Hora','Condicion']] #Escogemos las columnas que queremos
df_rain.set_index('Hora',inplace=True) #Colocamos como index las horas


time.sleep(2)
account_sid = TWILIO_ACCOUNT_SID 
auth_token = TWILIO_AUTH_TOKEN

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body='\nHola! \n\n\n El pronostico de lluvia hoy '+ df['Fecha'][0] +' en ' + query +' es : \n\n\n ' + str(df_rain),
                     from_=PHONE_NUMBER,
                     to='+51944477278'
                 )

print('Mensaje Enviado ' + message.sid)
