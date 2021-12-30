import requests
import os, time
import pika
import discord, asyncio
#import os
#DiscordToken = os.getenv('DISCORD_TOKEN')
#TenorToken = os.getenv('TENOR_TOKEN')




embedColour = 0xff0000
CommandKey = '!'

########### CONNEXIÓN A RABBIT MQ #######################

HOST = os.environ['RABBITMQ_HOST']
print("rabbit:"+HOST)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channel = connection.channel()

#El consumidor utiliza el exchange 'cartero'
channel.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue="searchgif", exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='cartero', queue=queue_name, routing_key="searchgif")


##########################################################

# --- functions ---

#Retrieves GIF from site
def get_gif(searchTerm):  # PEP8: lower_case_names for functions
    response = requests.get("https://g.tenor.com/v1/search?q={}&key=0J42BFGZCYOO&limit=1".format(searchTerm))
    data = response.json()
    
    ''' 
    # see urls for all GIFs
    
    for result in data['results']:
        print('- result -')
        #print(result)
        
        for media in result['media']:
            print('- media -')
            print(media)
            print(media['gif'])
            print('url:', media['gif']['url'])
    '''
    return data['results'][0]['media'][0]['gif']['url']
    
########## ESPERA Y HACE ALGO CUANDO RECIBE UN MENSAJE ####

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(body.decode("UTF-8"))
	arguments = body.decode("UTF-8").split(" ")

	if (arguments[0]=="!gif"):

		search = body[5:].decode()
		print("termino a buscar: " + search)
		result = get_gif(search)
		print("URL gif encontrada: "+result)

		########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
		print("send a new message to rabbitmq: "+result)
		channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=result)

	if (arguments[0]=="!egif"):

		search = body[5:].decode()
		print("termino a buscar: " + search)
		result = get_gif(search)
		print("URL gif encontrada: "+result)
		result = "embedgif " + result

		########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
		print("send a new message to rabbitmq: "+result)
		channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=result)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()



#######################