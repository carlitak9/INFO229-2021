import mysql.connector
import os, time

def create_gif_database(db_connection,db_name,cursor):
	cursor.execute(f"CREATE DATABASE {db_name};")
	cursor.execute(f"COMMIT;")
	cursor.execute(f"USE {db_name};")
	
	# Tabla news
	cursor.execute('''CREATE TABLE gifs (
		id_gif INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
		url VARCHAR(500),
		anime VARCHAR(500),
        action VARCHAR(50)
		);''')


	cursor.execute("SET GLOBAL time_zone = 'UTC';")
	cursor.execute("SET SESSION time_zone = 'UTC';")

	cursor.execute("COMMIT;") 

def insert_data(cursor):
    print("insert")
    cursor.execute('''INSERT INTO gifs (url,anime,action) VALUES
    ('https://c.tenor.com/xIuXbMtA38sAAAAd/toilet-bound-hanakokun.gif','Hanako-kun','hug'),
	('https://c.tenor.com/ikKAd57zDEwAAAAd/anime-mad.gif', 'Love is War', 'angry'),
	('https://c.tenor.com/4iTun5cu2uwAAAAC/dance-anime.gif','Mikakunin de Shinkoukei','dance'),
	('https://c.tenor.com/0i6HB03LuE4AAAAC/anime-sleeping.gif','Yuru Camp','sleep'),
	('https://c.tenor.com/3PjRNS8paykAAAAC/pat-pat-head.gif','Acchi kocchi','pat'),
	('https://c.tenor.com/vberBgo__S4AAAAC/naruko-anime.gif','Haiyore! Nyaruko-san','kiss'),
	('https://c.tenor.com/DVOTqLcB2jUAAAAC/anime-hug-love.gif', 'Tate no Yuusha', 'hug'),
	('https://c.tenor.com/jY84qSwONRwAAAAC/anime-happy.gif','Show by Rock!!','dance'),
	('https://c.tenor.com/HItBOocy6ikAAAAC/umaru-sleeping.gif','Himouto Umaru-Chan','sleep'),
	('https://c.tenor.com/N41zKEDABuUAAAAC/anime-head-pat-anime-pat.gif','Senpai ga Uzai Kōhai no Hanashi','pat'),
	('https://c.tenor.com/h9A4bnxJys8AAAAC/cheek-kiss.gif','Sakurasou no pet na kanojo','kiss'),
	('https://c.tenor.com/XiYuU9h44-AAAAAC/anime-slap-mad.gif','Toradora!','slap'),
	('https://c.tenor.com/PeJyQRCSHHkAAAAC/saki-saki-mukai-naoya.gif','Kanojo mo Kanojo','slap'),
	('https://c.tenor.com/X3x3Y2mp2W8AAAAC/anime-angry.gif','Kobayashi-san Chi No Maid Dragon','angry')
	;
    ''')
    cursor.execute("COMMIT;") 

#######################

def main():
	print("start creating database...")

	DATABASE = "gifbot"

	DATABASE_IP = str(os.environ['DATABASE_IP'])

	DATABASE_USER = "root"
	DATABASE_USER_PASSWORD = "root"
	DATABASE_PORT=3306

	not_connected = True

	while(not_connected):
		try:
			print(DATABASE_IP,"IP")
			db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
			not_connected = False

		except Exception as e:
			time.sleep(3)
			print(e, "error!!!")
			print("can't connect to mysql server, might be intializing")
			
	cursor = db_connection.cursor()

	try:
		cursor.execute(f"USE {DATABASE}")
		print(f"Database: {DATABASE} already exists")
	except Exception as e:
		create_gif_database(db_connection,DATABASE,cursor)
		insert_data(cursor)
		print(f"Succesfully created: {DATABASE}")
