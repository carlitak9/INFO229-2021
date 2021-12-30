import mysql.connector
import requests
import os, time
import pika
import create_gif_database

print("Start GIF Database manager...")
create_gif_database.main()

DATABASE = "gifbot"

DATABASE_IP = str(os.environ['DATABASE_IP'])

DATABASE_USER = "root"
DATABASE_USER_PASSWORD = "root"
DATABASE_PORT=3306

time.sleep(10)
########### CONNEXIÓN A RABBIT MQ #######################

HOST = os.environ['RABBITMQ_HOST']
print("rabbit:"+HOST)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channel = connection.channel()

#El consumidor utiliza el exchange 'cartero'
channel.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue="interaction", exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='cartero', queue=queue_name, routing_key="interaction")

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
	print(body.decode("UTF-8"))
	arguments = body.decode("UTF-8").split(" ")

	#if (arguments[0]=="!hug"): #https://tenor.com/view/toilet-bound-hanakokun-anime-anime-hug-gif-16831471

	#print("HUG buscando")
	a = arguments[0]	
	db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
	cursor = db_connection.cursor()
	cursor.execute(f"USE {DATABASE}")
	cursor.execute(f'''SELECT url,anime,action FROM gifs WHERE action="{a[1:]}" ORDER BY RAND() LIMIT 1;''')

        #caso sin usuario entregado
	result="no"
	for (url, anime, action) in cursor:
		result="{} ------ {} ------ {}".format(url,anime,action)
		print(result)
	print("URL gif de interaccion: "+result)

		########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
	print("send a new message to rabbitmq: "+result)
	channel.basic_publish(exchange='cartero',routing_key="discord_writer_int",body=result)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
