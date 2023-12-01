import requests
import schedule
import time
import smtplib
from email.message import EmailMessage

def kelvinToC(x):
    f=round((int(x)-273.15)*1.8+32,1)
    return str(f)
def timeFormat(str):
    date=""
    format=""
    if(str[0]=='0'):
        date+=str[1]
        format+=" AM"
    else:
        date+=str[0]+str[1]
        format+="PM"
    return date+format
    

city="" #write a city name
api_key="" #enter your api key
url1=f"http://api.openweathermap.org/data/2.5/forecast?appid={api_key}&q={city}"
url2=f"http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}"
response1=requests.get(url1).json()
response2=requests.get(url2).json()
currDescription=response2['weather'][0]['description']
currTemp=kelvinToC(response2['main']['temp'])
rain=False
time=""
for x in response1['list']:
    str=x['dt_txt'].split()
    if str[1]=="00:00:00": #breaks when it reaches midnight
        break

    weatherMain=x['weather'][0]['main'].lower()
    weatherDescription=x['weather'][0]['description'].lower()
    if(weatherMain.find('rain') or weatherDescription.find('rain')):
        time=str[1]
        rain=True
        break
    
    # print(x)
msg="It is currently "+currTemp+" F outside. Description: "+currDescription+".\n"
if rain==True:
    msg+="(Rain Alert) TAKE AN UMBRELLA WITH YOU! It is gonna rain around "+timeFormat(time)+"."

print(msg)
def send_message(x):
    to_number = '**********@tmomail.net' #enter your phone number (this works for mint mobile only) you can change the extension for non-mint mobile phones
    my_email = ""  #enter your email address
    my_password = ""  #enter your app password 
    msg=EmailMessage()
    text=x
    msg.set_content(text)
    msg['Subject']="Weather Update"
    msg['From']=my_email
    msg['To']=to_number
        
    try:
        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        server.starttls()
        server.login(my_email, my_password)
        server.sendmail( my_email, to_number, msg.as_string())
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error sending message: {e}")
send_message(msg)

