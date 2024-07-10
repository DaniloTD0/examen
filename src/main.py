from flask import Flask, render_template, request, redirect, url_for, session, flash
import database as db

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('aprendices.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']

        cursor = db.db.cursor(dictionary=True)  # Utilizamos db.db para obtener la conexión

        if rol == 'maestro':
            cursor.execute('SELECT * FROM maestros WHERE nombre = %s AND contraseña = %s', (username, password))
        else:
            cursor.execute('SELECT * FROM aprendiz WHERE nombre_aprendiz = %s AND cedula = %s', (username, password))

        user = cursor.fetchone()

        if user:
            session['nombre'] = user['nombre'] if rol == 'maestro' else user['nombre_aprendiz']
            if rol == 'maestro':
                return redirect(url_for('aprendices'))
            else:
                return 'Aun no esta listo'

        flash('Invalid username or password')
        return redirect(url_for('index'))

@app.route('/aprendices')
def aprendices():
    cursor = db.db.cursor()
    cursor.execute("SELECT * FROM aprendiz")
    myresult = cursor.fetchall()

    # Convertir datos a diccionarios
    insertObject = []
    columNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columNames, record)))
    cursor.close()
    return render_template('aprendices.html', data=insertObject)

@app.route('/addApr', methods=['POST'])
def addApr():
    nombre_aprendiz = request.form['nombre_aprendiz']
    edad = request.form['edad']
    telefono = request.form['telefono']
    gmail = request.form['gmail']
    cedula = request.form['cedula']

    if nombre_aprendiz and edad and telefono and gmail and cedula:
        cursor = db.db.cursor()
        sql = "INSERT INTO aprendiz (nombre_aprendiz, edad, telefono, gmail, cedula) VALUES (%s, %s, %s, %s, %s)"
        data = (nombre_aprendiz, edad, telefono, gmail, cedula)
        cursor.execute(sql, data)
        db.db.commit()
        cursor.close()
    return redirect(url_for('aprendices'))

@app.route('/delete/<string:id_aprendiz>')
def deleteApr(id_aprendiz):
    cursor = db.db.cursor()
    sql = "DELETE FROM aprendiz WHERE id_aprendiz=%s"
    data = (id_aprendiz,)
    cursor.execute(sql, data)
    db.db.commit()
    cursor.close()
    return redirect(url_for('aprendices'))

@app.route('/edit/<string:id_aprendiz>', methods=['POST'])
def editApr(id_aprendiz):
    # Verificar que todos los campos están presentes en el formulario
    required_fields = ['nombre_aprendiz', 'edad', 'telefono', 'gmail', 'cedula']
    for field in required_fields:
        if field not in request.form:
            return f"Missing form field: {field}", 400

    # Si todos los campos están presentes, proceder con la actualización
    nombre_aprendiz = request.form['nombre_aprendiz']
    edad = request.form['edad']
    telefono = request.form['telefono']
    gmail = request.form['gmail']
    cedula = request.form['cedula']

    if nombre_aprendiz and edad and telefono and gmail and cedula:
        cursor = db.db.cursor()
        sql = "UPDATE aprendiz SET nombre_aprendiz = %s, edad = %s, telefono = %s, gmail = %s, cedula = %s WHERE id_aprendiz = %s"
        data = (nombre_aprendiz, edad, telefono, gmail, cedula, id_aprendiz)
        cursor.execute(sql, data)
        db.db.commit()
        cursor.close()
    return redirect(url_for('aprendices'))

# Materia

@app.route('/materias')
def materias():
    cursor = db.db.cursor()
    cursor.execute("SELECT * FROM materias")
    myresult = cursor.fetchall()

    # Convertir datos a diccionarios
    insertObject = []
    columNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columNames, record)))
    cursor.close()
    return render_template('materias.html', data=insertObject)

@app.route('/addMat', methods=['POST'])
def addMat():
    nombre_materia = request.form['nombre_materia']

    if nombre_materia:
        cursor = db.db.cursor()
        sql = "INSERT INTO materias (nombre_materia) VALUES (%s)"
        data = (nombre_materia,)
        cursor.execute(sql, data)
        db.db.commit()
        cursor.close()
    return redirect(url_for('materias'))

@app.route('/deleteMat/<string:id_materia>')
def deleteMat(id_materia):
    cursor = db.db.cursor()
    sql = "DELETE FROM materias WHERE id_materia=%s"
    data = (id_materia,)
    cursor.execute(sql, data)
    db.db.commit()
    cursor.close()
    return redirect(url_for('materias'))

@app.route('/editMat/<string:id_materia>', methods=['POST'])
def editMat(id_materia):
    # Verificar que todos los campos están presentes en el formulario
    required_fields = ['nombre_materia']
    for field in required_fields:
        if field not in request.form:
            return f"Missing form field: {field}", 400

    # Si todos los campos están presentes, proceder con la actualización
    nombre_materia = request.form['nombre_materia']

    if nombre_materia:
        cursor = db.db.cursor()
        sql = "UPDATE materias SET nombre_materia = %s WHERE id_materia = %s"
        data = (nombre_materia, id_materia)
        cursor.execute(sql, data)
        db.db.commit()
        cursor.close()
    return redirect(url_for('materias'))

if __name__ == '__main__':
    app.run(debug=True, port=3001)
