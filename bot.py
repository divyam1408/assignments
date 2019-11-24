# Work with Python 3.6
import discord
from googlesearch import search
from os import path
from collections import defaultdict
import json

TOKEN = 'NjQ3Nzg2ODk5OTIyMjIzMTQ1.XdmI5Q.EwQCeRscY4AkrKrHoUsb44-ciZw'
GUILD = 'live_bird'





client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if(guild.name == GUILD):
            break
    print(f'{client.user} has connected to following gluid:\n'
            f'{guild.name}(id:{guild.id} )')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    if(path.exists('user_search_history.txt') == False):
        data = {}
        with open('user_search_history.txt','w') as outfile:
            json.dump(data,outfile)
            print('Search history file created')
        outfile.close()



@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    what_to_search = message.content.split()



    if message.content == 'hi':
            await message.channel.send('hey')

    #implementing google search
    elif(what_to_search[0] == '!google'):

        if(len(what_to_search) == 1):
            err_message = "Nothing to Search For!!!!  Try using '!google your content to search'"
            await message.channel.send(err_message)
        else:
            await message.channel.send('Please Wait Fetching your results........')

            content_to_search = what_to_search[1]
            for j in range(2,len(what_to_search)):
                content_to_search = content_to_search + " " + what_to_search[j]

            #storing user search

            #load the data
            message_user = str(message.author)
            with open('user_search_history.txt') as json_file:
                data = json.load(json_file)
                if message_user not in data:
                    data[message_user] = []
                    data[message_user].append(content_to_search)
                else:
                    data[message_user].append(content_to_search)

            json_file.close()

            #writing back to file

            with open('user_search_history.txt','w') as outfile:
                json.dump(data,outfile)

            outfile.close()

            search_iter = search(content_to_search,tld='com',lang='en',start=0,stop=5)

            top_5_links = []
            for link in search_iter:
                top_5_links.append(link)

            await message.channel.send('Top 5 links for your results are:')
            for link in top_5_links:
                await message.channel.send(link)

    #search from history
    elif(what_to_search[0] == '!recent'):
        message_user = str(message.author)
        with open('user_search_history.txt') as json_file:
            data = json.load(json_file)

        json_file.close()

        content_to_search = what_to_search[1]
        for j in range(2,len(what_to_search)):
            content_to_search = content_to_search + " " + what_to_search[j]

        if(message_user not in data):
            await message.channel.send('ooops You have not searched anything yet!!!!!')
        else:
            history = data[message_user]
            prev_searches = list(filter(lambda item:content_to_search in item,history))
            if(len(prev_searches) == 0):
                await message.channel.send('Nothing matching in search history!!!')
            else:
                await message.channel.send('Following searches found:')
                for temp in prev_searches:
                    await message.channel.send(temp)





client.run(TOKEN)
