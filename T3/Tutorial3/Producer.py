import pika

#Conexión al servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

message = input("Ingrese su busqueda de wikipedia: ")
#Creación de la cola
channel.queue_declare(queue='WikipediaRes')
channel.queue_declare(queue='WikipediaView')

#Publicación del mensaje
channel.basic_publish(exchange='',
                      routing_key='WikipediaRes',
                      body=message)

channel.basic_publish(exchange='',
                      routing_key='WikipediaView',
                      body=message)

print(" [x] Sent " + message + " search to Wikipedia Consumers")

connection.close()