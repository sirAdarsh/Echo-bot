from sqlite3.dbapi2 import connect
import discord
import json
import urllib.request

from discord import channel
from discord import user
import key
import songs_db
import sqlite3

# 649595574407921664


my_secret = key.bot_key
my_api = key.api_key

client = discord.Client()

def create_new_table(user_id):
  con = sqlite3.connect('song_DB.db')
  cur = con.cursor()
  cur.execute("CREATE TABLE a_"+str(user_id)+"(SONG TEXT, id INTEGER);")
  cur.close

def check_if_user_has_a_song_table(user_id):
  con = sqlite3.connect('song_DB.db')
  cur = con.cursor()
  listOfTables = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='a_"+user_id+"'"+";" ).fetchall()
  cur.close()
  if listOfTables == []:
    return False
  return True

def get_rows_count(user_id):
  con = sqlite3.connect('song_DB.db')
  cur = con.cursor()
  cur.execute("SELECT * FROM a_"+user_id)
  song_list = cur.fetchall()
  cur.close()
  con.close()
  return song_list
  

def display_list(user_id):
  song_list = get_rows_count(user_id)
  song_list_formatted = []
  for song in song_list:
    song_list_formatted.append(song[0])
  return song_list_formatted

def add_song(user_id, song_name):
  con = sqlite3.connect('song_DB.db')
  cur = con.cursor()
  cur.execute("SELECT * from a_"+str(user_id))
  results = cur.fetchall()
  last_id = len(results)
    
  cur.execute("INSERT INTO a_"+user_id+" VALUES ('"+song_name+"','"+str(last_id+1)+"')")
  con.commit()
  cur.close()

def del_song(user_id, song_id):
  con = sqlite3.connect('song_DB.db')
  cur = con.cursor()
  cur.execute("DELETE FROM a_"+user_id+" WHERE id = "+song_id)
  con.commit()
  cur.close()
  con.close()
  
  # Update the song_id of all other songs (post-deleted)
  con = sqlite3.connect('song_DB.db')
  cur = con.cursor()
  cur.execute("UPDATE a_"+user_id+" SET id = id-1 WHERE id>"+str(song_id))
  con.commit()
  cur.close()
  con.close()

def del_all_song(user_id):
  con = sqlite3.connect('song_DB.db')
  cur = con.cursor()
  cur.execute("DELETE FROM a_"+user_id)
  con.commit()
  cur.close()
  con.close()

def update_song(user_id, song_id, song_name):
  con = sqlite3.connect('song_DB.db')
  cur = con.cursor()
  cur.execute("UPDATE a_"+user_id+" SET SONG = '"+song_name+"' WHERE id = "+str(song_id))
  con.commit()
  cur.close()
  con.close()

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
    string_prod += stri[0].upper()
    string_prod += "\n\n*City ka Temperature* :   "
    string_prod += '**'+stri[2]+'**'
    string_prod += "\n\n*City ka pressure* :      "
    string_prod += '**'+stri[3]+'**'
    string_prod += "\n\n*City ka humidity* :      "
    string_prod += '**'+stri[4]+'**'
    string_prod += "\n\n*Skies ka Haal* : "
    string_prod += '**'+stri[5]+'**'
    string_prod += "\n\n*Zabardasti ka gyaan* :   "
    string_prod += '**'+stri[6]+'**'
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
    myid = "<@"+user_id+">"
    
    client.fetch_guild
    txt = message.content
    words = txt.split(' ')

    keyword = words[1]

    if keyword == 'weather':
      city = ""
      for i in range(2,len(words)):
        city = city + words[i] + '+'
      
      await message.channel.send("Hey %s! Here's your weather report :partly_sunny: \n\n"%myid)
      await message.channel.send(handle_weather(city))
    
    if keyword == 'song':

      # DISPLAY, ADD, DELETE, PLAY
      func = words[2]
      if func == 'display' or func == 'show' or func == 'all':
        if check_if_user_has_a_song_table(user_id):
          msg = 'Databse found\n'
          await message.channel.send(msg)
          song_list = display_list(user_id)

          #Show how many songs are enlisted
          count = len(get_rows_count(user_id))
          await message.channel.send("You have a total of ***"+str(count)+"*** songs! :notes: \n\n")

          song_string = '\n'
          for i in range(len(song_list)):
            song_string += ' **'+str(i+1)+'.**  '
            song_string += str(song_list[i])
            song_string += '\n'

          await message.channel.send(song_string)
        else:
           msg = 'No database\n\n  Lets create one! \n  *Hang on there..*\n\n'
           await message.channel.send(msg)
           try:
             create_new_table(user_id)
             await message.channel.send('Created your database ✅, happy adding songs! :)')
           except:
             await message.channel.send('Could not create your database :(')

      if func == 'add' or func == 'PUSH':
        song_name = ""
        msg = ' .'
        for i in range(3, len(words)):
          song_name += words[i]+" "
        if song_name == "":
          msg = 'Song cant be empty! :x: '
        else:
          try:
           add_song(user_id, str(song_name))
           msg = 'Cool! *Song added*  ✅ '
          except:
            msg = "Some **Error** occured :'(" 
        await message.channel.send(msg)

      if func == 'del' or func == 'delete':
        song_id = words[3]
        try:
          if song_id == 'all':
            del_all_song(user_id)
            await message.channel.send('Deleted all your tracks. ✅')
          else:
            del_song(user_id, song_id)
            await message.channel.send('Deleted your track. ✅')
        except:
          await message.channel.send('Some **ERROR** occured :(')

      if func == 'u' or func == 'upd' or func == 'update':
        if len(words)<4:
          await message.channel.send("To update, use this format after 'update' : {song_id} {updated_song}")
        else:
          song_id = words[3]
          song_name = ''
          for i in range(4, len(words)):
            song_name += words[i] + ' '
          try:
            update_song(user_id, song_id, song_name)
            await message.channel.send("Song updated ✅")
          except:
            await message.channel.send("Coudn't update :x:")
            


client.run(my_secret)