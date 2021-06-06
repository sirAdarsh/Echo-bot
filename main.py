import discord
import json
import urllib.request
import key


my_secret = key.bot_key
my_api = key.api_key



def convert(lst):
    return ' '.join(lst).split()

client = discord.Client()

def get_weather(city):

  try:
    source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&appid='+str(my_api)).read()

    list_of_data = json.loads(source)

    city_name=city
    coordinate= "sdsd"

    temp= str(list_of_data['main']['temp']) + ' °C'
    pressure= str(list_of_data['main']['pressure'])
    humidity= str(list_of_data['main']['humidity'])
    main= str(list_of_data['weather'][0]['main'])
    description= str(list_of_data['weather'][0]['description'])

    list_ = [city_name, coordinate, temp, pressure, humidity, main, description]
    return list_
  except:
    return "No City Matched"


@client.event 
async def on_ready():
   print('Welcome {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('$wtf'):
    txt = message.content
    words = txt.split(' ')

    city = words[1]
    stri = get_weather(city)
    if stri == "No City Matched":
      await message.channel.send('-------**No City Matched**------\n....... *try again*?')
    else:
      string_prod = "------- WEATHER REPORT IS READY --------\n"
      string_prod += "\n\n*City ka naam* :          "
      string_prod += stri[0]
      string_prod += "\n\n*City ka Temperature* :   "
      string_prod +=stri[2]
      string_prod += "\n\n*City ka pressure* :      "
      string_prod +=stri[3]
      string_prod += "\n\n*City ka humidity* :      "
      string_prod +=stri[4]
      string_prod += "\n\n*Skies ka Haal* : "
      string_prod +=stri[5]
      string_prod += "\n\n*Zabardasti ka gyaan* :   "
      string_prod +=stri[6]
      await message.channel.send(string_prod)
client.run(my_secret)