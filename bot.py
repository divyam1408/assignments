# Prequistes
#install beautifulsoup4 and google on the system
# using pip install beautifulsoup4 , pip install google
import discord
from googlesearch import search
from os import path
import json
import psycopg2

TOKEN = 'NjQ3Nzg2ODk5OTIyMjIzMTQ1.Xd5WwA.3rdnDjf-SYlgmTezCx9eK1J3uH4' #bot token
GUILD = 'divyam'
conn = psycopg2.connect(database="d526bgeke1bq", user = "fvdvxqancirhos", password = "d7cc600f1e4ac67d8f1286af93e0fe99c421c20278b01e737f0bd799c6aabce3", host = "ec2-174-129-214-193.compute-1.amazonaws.com", port = "5432")
print('connected successfully!!!!')

#connecting to heroku database





client = discord.Client()



@client.event
async def on_ready():
    owners=[]
    for guild in client.guilds:
        if(guild.owner not in owners):
            table_name = str(guild.owner).split('#')[0]
            print(table_name,guild)
            cur = conn.cursor()
            cur.execute('''CREATE TABLE '''+table_name+'''_history
              (SEARCH        TEXT    NOT NULL);''')

            conn.commit()
            owners.append(guild.owner)

    print(f'{client.user} has been connected to your gluid\n')

    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')

    # if(path.exists('user_search_history.txt') == False):
    #     data = {}
    #     with open('user_search_history.txt','w') as outfile:
    #         json.dump(data,outfile)
    #         print('Search history file created')
    #     outfile.close()



@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

    cur = conn.cursor()
    cur.execute('''CREATE TABLE '''+str(member.name)+'''_history
          (SEARCH        TEXT    NOT NULL);''')

    conn.commit()


    print('Search Table Created')



@client.event
async def on_message(message):
    #print(message.author,client.user)
    if (message.author == client.user):
        return

    # print(message.content)
    what_to_search = message.content.split()
    if(what_to_search == []):
        return
    #print(what_to_search)



    if (message.content == 'hi'):
            await message.channel.send('hey')

    #implementing google search
    elif(what_to_search[0] == '!google'):

        if(len(what_to_search) == 1):
            err_message = "Nothing to Search For!!!!  Try using '!google your content to search'"
            await message.channel.send(err_message)
        else:
            await message.channel.send('Please Wait Fetching your results........')

            content_to_search = str(what_to_search[1])
            for j in range(2,len(what_to_search)):
                content_to_search = content_to_search + " " + str(what_to_search[j])

            #storing user search

            cur = conn.cursor()
            table_name = str(message.author).split('#')[0]
            cur.execute("INSERT INTO "+table_name+"_history (SEARCH) VALUES ('"+content_to_search+"')")
            conn.commit()

            #load the data
            # message_user = str(message.author)
            # with open('user_search_history.txt') as json_file:
            #     data = json.load(json_file)
            #     if message_user not in data:
            #         data[message_user] = []
            #         data[message_user].append(content_to_search)
            #     else:
            #         data[message_user].append(content_to_search)
            #
            # json_file.close()
            #
            # #writing back to file
            #
            # with open('user_search_history.txt','w') as outfile:
            #     json.dump(data,outfile)
            #
            # outfile.close()

            content = search(content_to_search,tld='com',lang='en',start=0,stop=5)

            top_5_links = []
            for link in content:
                top_5_links.append(link)

            await message.channel.send('Top 5 links for your results are:')
            for link in top_5_links:
                await message.channel.send(link)

    #search from history
    elif(what_to_search[0] == '!recent'):
        message_user = str(message.author)
        table_name = message_user.split('#')[0]
        content_to_search = what_to_search[1]
        for j in range(2,len(what_to_search)):
            content_to_search = content_to_search + " " + what_to_search[j]


        cur = conn.cursor()
        cur.execute("select * from "+table_name+"_history")
        rows = cur.fetchall()

        if(rows == []):
            await message.channel.send('ooops You have not searched anything yet!!!!!')

        else:
            filtered_search = list(filter(lambda x:content_to_search in str(x[0]),rows))
            if(filtered_search == []):
                await message.channel.send('Nothing matching in search history!!!')
            else:
                await message.channel.send('Following searches found:')
                for temp in filtered_search:
                    await message.channel.send(temp)





        # message_user = str(message.author)
        # with open('user_search_history.txt') as json_file:
        #     data = json.load(json_file)
        #
        # json_file.close()
        #
        # content_to_search = what_to_search[1]
        # for j in range(2,len(what_to_search)):
        #     content_to_search = content_to_search + " " + what_to_search[j]
        #
        # if(message_user not in data):
        #     await message.channel.send('ooops You have not searched anything yet!!!!!')
        # else:
        #     history = data[message_user]
        #     prev_searches = list(filter(lambda item:content_to_search in item,history))
        #     if(len(prev_searches) == 0):
        #         await message.channel.send('Nothing matching in search history!!!')
        #     else:
        #         await message.channel.send('Following searches found:')
        #         for temp in prev_searches:
        #             await message.channel.send(temp)





client.run(TOKEN)
