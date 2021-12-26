import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="my-api",
  password="my-api-password"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE sun")

#Insertar datos en Database para prueba de app
mycursor.execute("USE sun")

mycursor.execute('''CREATE TABLE news (
		id_news INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
		url TEXT,
		title TEXT, 
		date TEXT,
		media_outlet VARCHAR(50),
		category VARCHAR(100)
        );''')

mycursor.execute('''INSERT INTO news (url,title,date,media_outlet,category) VALUES
    ('https://www.biobiochile.cl/noticias/futbol-internacional/chilenos-en-el-exterior/2021/10/21/carlos-palacios-ingreso-en-el-segundo-tiempo-en-empate-de-inter-ante-bragantino.shtml
','Carlos Palacios ingresó en el segundo tiempo en empate de Inter ante Bragantino 
','2021-10-21','biobiochile','deportes'),
    ('https://www.biobiochile.cl/noticias/economia/actualidad-economica/2021/10/20/por-sexta-semana-consecutiva-suben-todas-las-bencinas-en-63-pesos-por-litros.shtml
','Por sexta semana consecutiva suben todas las bencinas en 6,3 pesos por litro
','2021-10-20','biobiochile','economia'),
    ('https://www.biobiochile.cl/biobiotv/programas/podria-ser-peor/2021/10/21/vicepdte-colegio-medico-si-aumenta-rapido-la-demanda-covid-19-no-alcanzaremos-a-responder.shtml
','Vicepdte. Colegio Médico: "Si aumenta rápido la demanda Covid-19, no alcanzaremos a responder"
','2021-10-21','biobiochile','salud');
    ''')
mycursor.execute("COMMIT;") 