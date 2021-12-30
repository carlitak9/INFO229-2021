import os
from typing import Text

import discord
from dotenv import load_dotenv
from discord.ext import commands
import threading
import pika
import builtins


############ CONEXION RABBITMQ ##############

HOST = os.environ['RABBITMQ_HOST']
print("rabbit:"+HOST)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channelMQ = connection.channel()

#Creamos el exchange 'cartero' de tipo 'fanout'
channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

#channelMQ.exchange_declare(exchange='gifs', exchange_type='topic', durable=True)


#############################################

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')
builtins.bot = bot


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    for channel in bot.get_all_channels():
        print(channel)
        print(channel.id)

    channel = bot.get_channel(913706828502814760) 
    await channel.send('¡Hola!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'pizza' or message.content == 'cerveza' or message.content == 'donuts':
        response = "!mmm..."+message.content+"!"
        await message.channel.send(response)

    await bot.process_commands(message)

@bot.command(name='birthday', help='Muestra la fecha de cumpleaño del miembro de la GUILD que se pasa en parámetro. Ejemplo: !birthday MatthieuVernier')
async def cumpleaños(ctx):
    message =  ctx.message.content
    print("send a new mesage to rabbitmq: "+message)

    channelMQ.basic_publish(exchange='cartero', routing_key="birthday", body=message)

@bot.command(name='add-birthday', help='Permite añadir el cumpleaño de un nuevo miembro de la GUILD que se pasa en parámetro. Ejemplo: !birthday MatthieuVernier 1985-02-13')
async def cumpleaños(ctx):
    message =  ctx.message.content
    print("send a new mesage to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="birthday", body=message)

#GIF SYSTEM

@bot.command(name='gif', help='Muestra un gif de lo solicitado. !gif Legoshi')
async def gifs(ctx):
    message = ctx.message.content
    print("send a new gif message to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="searchgif", body=message)

@bot.command(name='egif', help='Entrega un embed con el gif solicitado. !egif Legoshi')
async def gifs(ctx):
    message = ctx.message.content
    print("send a new gif message to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="searchgif", body=message)


#Interacciones

@bot.command(name='hug', help='Muestra una interaccion con gif')
async def gifs(ctx):
    message = ctx.message.content
    print("send a new gif message to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="interaction", body=message)

@bot.command(name='angry', help='Muestra una interaccion con gif')
async def gifs(ctx):
    message = ctx.message.content
    print("send a new gif message to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="interaction", body=message)

@bot.command(name='dance', help='Muestra una interaccion con gif')
async def gifs(ctx):
    message = ctx.message.content
    print("send a new gif message to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="interaction", body=message)

@bot.command(name='sleep', help='Muestra una interaccion con gif')
async def gifs(ctx):
    message = ctx.message.content
    print("send a new gif message to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="interaction", body=message)

@bot.command(name='pat', help='Muestra una interaccion con gif')
async def gifs(ctx):
    message = ctx.message.content
    print("send a new gif message to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="interaction", body=message)

@bot.command(name='kiss', help='Muestra una interaccion con gif')
async def gifs(ctx):
    message = ctx.message.content
    print("send a new gif message to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="interaction", body=message)

@bot.command(name='slap', help='Muestra una interaccion con gif')
async def gifs(ctx):
    message = ctx.message.content
    print("send a new gif message to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="interaction", body=message)


############ CONSUMER ###############

import threading
import asyncio

def writer(bot):
    """thread worker function"""
    print('Worker')

    HOST = os.environ['RABBITMQ_HOST']

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST))
    channelMQ = connection.channel()

    #Creamos el exchange 'cartero' de tipo 'fanout'
    channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

    #Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
    result = channelMQ.queue_declare(queue="discord_writer", exclusive=True, durable=True)
    queue_name = result.method.queue

    #La cola se asigna a un 'exchange'
    channelMQ.queue_bind(exchange='cartero', queue=queue_name, routing_key="discord_writer")
    

    print(' [*] Waiting for messages. To exit press CTRL+C')

    async def write(message):
        channel = bot.get_channel(908505071887732768)#913706828502814760 #908505071887732768
        if(message.split(" ")[0] == "embedgif"): # ------ 
            embed = discord.Embed()
            embed.set_image(url=message.split(" ")[1])
            await channel.send(embed=embed)

        elif(message.split(" ------ ")[0] == "embed"):
            user = message.split(" ------ ")[1]
            embed = discord.Embed(title=user)
            print(user)
            embed.set_image(url="https://c.tenor.com/tisW_l-jKW4AAAAC/anime-birthday-hat.gif")
            text = "Anime : Suzumiya Haruhi no Yūutsu"
            embed.set_footer(text=text)
            await channel.send(embed=embed)

        else:
            
            await channel.send(message)
    

    def callback(ch, method, properties, body):
        message=body.decode("UTF-8")
        #print(message)

        bot.loop.create_task(write(message))

    channelMQ.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channelMQ.start_consuming()

t = threading.Thread(target=writer, args=[bot])
t.start()


############ CONSUMER Interacciones ###############

import threading
import asyncio

def writerInt(bot):
    """thread worker function"""
    print('Worker')

    HOST = os.environ['RABBITMQ_HOST']

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST))
    channelMQ = connection.channel()

    #Creamos el exchange 'cartero' de tipo 'fanout'
    channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

    #Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
    result = channelMQ.queue_declare(queue="discord_writer_int", exclusive=True, durable=True)
    queue_name = result.method.queue

    #La cola se asigna a un 'exchange'
    channelMQ.queue_bind(exchange='cartero', queue=queue_name, routing_key="discord_writer_int")
    

    print(' [*] Waiting for messages. To exit press CTRL+C')

    async def write(message):
        channel = bot.get_channel(908505071887732768)#913706828502814760 #908505071887732768
        #if(message.split(" ------ ")[2] == "hug"):
        url = message.split(" ------ ")[0]
        

        user = "Se a enviado un {}".format(message.split(" ------ ")[2])
        embed = discord.Embed(title=user)
        print(user)
        embed.set_image(url=str(url))
        text = "Anime : " + message.split(" ------ ")[1]
        embed.set_footer(text=text)
        await channel.send(embed=embed)


    

    def callback(ch, method, properties, body):
        message=body.decode("UTF-8")
        #print(message)

        bot.loop.create_task(write(message))

    channelMQ.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channelMQ.start_consuming()

t = threading.Thread(target=writerInt, args=[bot])
t.start()

########################################
bot.run(TOKEN)
