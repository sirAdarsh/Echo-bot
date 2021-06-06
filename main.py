import discord
import json
import urllib.request

from discord import channel
import key
import songs_db
import sqlite3

my_secret = key.bot_key
my_api = key.api_key

def create_new_table(user_id):
  con = sqlite3.connect('song_DB.db')
  cur = con.cursor()
  cur.execute("CREATE TABLE a_"+str(user_id)+"(SONG text);")
  cur.close

def check_if_user_has_a_song_table(user_id):
  con = sqlite3.connect('song_DB.db')
  cur = con.cursor()
  listOfTables = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='a_"+user_id+"'"+";" ).fetchall()
  if listOfTables == []:
    return False
  return True


client = discord.Client()

def get_weather(city):

  try:
    source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&appid='+str(my_api)).read()

    list_of_data = json.loads(source)
    city_name = ''
    for i in city:
      if i!='+':
        city_name += i
      else:
        city_name += ' '

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


def handle_weather(keyword):

  stri = get_weather(keyword)
  if stri == "No City Matched":
    return '-------**No City Matched**------\n....... *try again*?'
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
    return string_prod

@client.event 
async def on_ready():
   print('Welcome {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('$wtf'):

    user_id = str(message.author.id)

    txt = message.content
    words = txt.split(' ')

    keyword = words[1]

    if keyword == 'weather':
      city = ""
      for i in range(2,len(words)):
        city = city + words[i] + '+'
      await message.channel.send(message.author.id)
      await message.channel.send(handle_weather(city))
    
    if keyword == 'song':
      # DISPLAY, ADD, DELETE, PLAY
      func = words[2]
      if func == 'display' or func == 'show' or func == 'all':
        if check_if_user_has_a_song_table(user_id):
          msg = 'Databse found'
          await message.channel.send(msg)
        else:
           msg = 'No database\n\n Lets create one! \n  *Hang on there..*\n\n'
           await message.channel.send(msg)
           try:
             create_new_table(user_id)
             await message.channel.send('Created your database, happy adding songs! :)')
           except:
             await message.channel.send('Could not create your database :(')

    
client.run(my_secret)