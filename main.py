import discord
from discord.ext import commands
import nltk
#nltk.download()
from neuralintents import GenericAssistant
from Recommandation import Prediction
from API_get import data_json

chatbot = GenericAssistant('intents.json')
chatbot.train_model()
chatbot.save_model()
on_command = False
#client = discord.Client()

bot = commands.Bot("!")

TOKEN = 'OTUwNDE0MjQxMzI2ODUwMDc5.YiYkPA.w5OqYkHWzcfATQHemvZ9NPQ7d-E'
async def display(ctx, i):

    await ctx.channel.send(i["images"])
    await ctx.channel.send(i["name"])
    await ctx.channel.send("***Aliases : ***")
    await ctx.channel.send(i["aliases"])
    await ctx.channel.send("***Power Stats : ***")
    await ctx.channel.send(i["powerstats"])
    await ctx.channel.send("***Group Affiliations : ***")
    await ctx.channel.send(i["groupAffiliation"])
    await ctx.channel.send("***Alignement : ***" + i["alignment"])
    await ctx.channel.send("***Publisher : ***" + i["publisher"])
    
@bot.command()
async def describe(ctx, *, hero):
    if (hero == "" or hero.lower() == "random"):
        line = data_json.sample().to_dict("records")
    else:
        line = data_json.loc[data_json["name"]== hero].to_dict('records')
        if (len(line) == 0):
            line = [i for i in data_json.iloc if hero in i["aliases"]]
    if (hero.lower() == "random"):
        await ctx.channel.send(f"Hope you will like : ")
    else:
        await ctx.channel.send(f"Number of {hero} : {len(line)}")
    for i in line:
        await display(ctx, i)
        
@bot.command()
async def guess(ctx):
    global on_command
    on_command = True
    line = data_json.sample().to_dict("records")
    await ctx.channel.send("Who is this !")
    await ctx.channel.send(line[0]["images"])
    mess = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel==ctx.channel)
    if(mess.content.lower() == line[0]["name"].lower()):
        await ctx.channel.send("You're right Congratulations !!")
    else:
        await ctx.channel.send("Wrong, it was " + line[0]["name"])
    on_command = False


@bot.command()
async def recommand(ctx):
    global on_command
    on_command = True
    ratings = []
    id_hero = []
    await ctx.channel.send("First rate those 5 heros between 1 and 10 !")
    heros = [data_json.sample().to_dict('records') for i in range(5)]
    for i in heros:
        await display(ctx, i[0])
        mess = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel==ctx.channel)
        ratings.append(float(mess.content))
        id_hero.append(i[0]["id"])
    result = Prediction(ratings, id_hero)
    await ctx.channel.send("You will probably like those 3 :")
    for i in result.to_dict('records'):
        await display(ctx, i)
    on_command = False

@bot.command()
async def helpme(ctx):
    await ctx.channel.send("!describe <*name of hero or random*> : I give you informations on a hero")
    await ctx.channel.send("!recommand : Let me recommand you 3 heros you may like")
    await ctx.channel.send("!guess : Try to guess the hero !")


@bot.event
async def on_message(message):
    if (message.author.bot == False):
        await bot.process_commands(message)
        if not message.content.startswith('!') and on_command == False:
            response = chatbot.request(message.content[1:])
            await message.channel.send(response)

@bot.event 
async def on_ready():
    print("Bot Ready !")

@describe.error
async def describe_error(ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
                await ctx.send("Put the name of a hero after !describe or just random !")

bot.run(TOKEN)  #The token might be expired 
