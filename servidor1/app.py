from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb
import os

app = Flask(__name__)

# Conexión a la base principal (mysql)
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST", "mysql")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER", "root")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD", "root")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB", "db_informacion")
app.config['MYSQL_PORT'] = int(os.getenv("MYSQL_PORT", 3306))

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        experiencia = request.form.get('experiencia')
        formacion = request.form.get('formacion')

        # Guardar en base principal
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO datos (nombre, correo, experiencia, formacion) VALUES (%s, %s, %s, %s)",
                        (nombre, correo, experiencia, formacion))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            print("Error guardando en DB principal:", e)

        # Guardar en base réplica (conexión manual)
        try:
            conn = MySQLdb.connect(
                host="mysql_replica",
                user="root",
                passwd="root",
                db="db_informacion",
                port=3306
            )
            cur2 = conn.cursor()
            cur2.execute("INSERT INTO datos (nombre, correo, experiencia, formacion) VALUES (%s, %s, %s, %s)",
                         (nombre, correo, experiencia, formacion))
            conn.commit()
            cur2.close()
            conn.close()
        except Exception as e:
            print("Error guardando en DB réplica:", e)

        return redirect(url_for('formulario'))

    return render_template('index.html') 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
