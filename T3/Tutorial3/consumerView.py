import pika, sys, os, wikipedia, pageviewapi.period

def main():

    #Conexión al servidor RabbitMQ   
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    #Nos aseguramos que existe una cola 'hello'
    channel.queue_declare(queue='WikipediaView')

    def callback(ch, method, properties, body):
        count = pageviewapi.period.sum_last("en.wikipedia", body.decode(), last=365, access='all-access', agent='all-agents')
        #count = pageviewapi.period.sum_last('es.wikipedia', "sword", last=30,
        #                    access='all-access', agent='all-agents')
        #count = 1 # limpieza de cola
        print(" [x] Received %r" % body +". las consultas para este termino en los ultimos dias son: " + str(count))

    channel.basic_consume(queue='WikipediaView', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


        #Bocle infinita
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
