from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)

#conexion a base de datos
conexion = psycopg2.connect(
    host = "ec2-18-214-140-149.compute-1.amazonaws.com", 
    database = "d7oi4tej1b57ta", 
    user = "xnwwboulwuegts", 
    password = "6b94116a31888bd953eff4eacec821a90d6dd403413a2a65207b3ebedbf0d9e4")

# settings
app.secret_key='my secret key'

@app.route('/')
def index():
    cursor = conexion.cursor()
    cursor.execute(" select count (*) from sala")
    cantsalas = cursor.fetchall()
    cursor.execute(" select count (*) from cliente")
    cantcliente = cursor.fetchall()
    cursor.execute(" select count (*) from empleado")
    cantempleado = cursor.fetchall()
    cursor.execute(" select count (*) from pelicula")
    cantpelicula = cursor.fetchall()
    cursor.close
    return render_template('menu.html',salas=cantsalas, clientes=cantcliente, empleado=cantempleado, pelicula=cantpelicula)

@app.route('/info')
def info():
    return render_template('info.html')
    
@app.route('/tablas')
def tablas():
    return render_template('tablas.html')

#TABLA CLIENTE
@app.route('/Cliente')
def Clientes():#MOSTRAR CLIENTES
    cursor = conexion.cursor()
    query = "select * from cliente"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return render_template('Cliente.html', clientes = data)
@app.route("/add_cliente", methods = ['POST'])
def add_CLientes():#AÑADIR CLIENTES
    nombre_cliente = request.form['nombre_cliente']
    identidad_cliente = request.form['identidad_cliente']
    Email=request.form['Email']
    cur = conexion.cursor()
    cur.execute('INSERT INTO cliente (nombre_cliente, identificacion_cliente, email) VALUES(%s, %s, %s)', (nombre_cliente, identidad_cliente, Email))
    conexion.commit()
    flash('Client added successfully...')
    return redirect(url_for("Clientes"))
@app.route('/edit_cliente/<id>', methods = ['POST', 'GET'])
def get_Clientes(id):#OBTENER ID CLIENTE
    cur=conexion.cursor()
    cur.execute('SELECT * FROM cliente WHERE id_cliente = %s', (id))
    data = cur.fetchall()
    return render_template('edit-client.html',client=data[0] )
@app.route('/update_cliente/<id>', methods=['POST'])
def update_client(id):#ACTUALIZAR CLIENTE
    if request.method=='POST':
        nombre_cliente=request.form['nombre_cliente']
        identidad_cliente=request.form['identidad_cliente']
        Email=request.form['Email']
        cur=conexion.cursor()
        cur.execute("""
        UPDATE cliente
        SET nombre_cliente=%s,
            identificacion_cliente=%s,
            Email=%s
        WHERE id_cliente = %s
        """, (nombre_cliente, identidad_cliente, Email, id))
        conexion.commit()
        flash('Client Updated Successfully')
        return redirect(url_for('Clientes'))
@app.route('/delete_cliente/<string:id>', methods = ['POST', 'GET'])
def delete_cliente(id):#ELIMINAR CLIENTE
    cur=conexion.cursor()
    cur.execute('DELETE FROM cliente WHERE id_cliente = {0}'.format(id))
    conexion.commit()
    flash('Client Removed Successfully...')
    return redirect(url_for('Clientes'))
#FIN TABLA CLIENTE

#TABLA PELICULA
@app.route('/Pelicula')
def Peliculas():#MOSTRAR PELICULAS
    cursor=conexion.cursor()
    query="SELECT id_pelicula,nombre_pelicula ,genero, descripcion_pelicula  FROM pelicula INNER JOIN tipo_pelicula ON pelicula.id_tipo = tipo_pelicula.id_tipo;"
    cursor.execute(query)
    data=cursor.fetchall()
    cursor.close
    return render_template('Pelicula.html', peliculas = data)
@app.route("/add_pelicula", methods = ['POST'])
def add_Pelicula():
    nombre_pelicula = request.form['nombre_pelicula']
    descripcion = request.form['descripcion']
    tipo_de_pelicula=request.form['tipo_de_pelicula']
    cur = conexion.cursor()
    cur.execute('INSERT INTO pelicula (nombre_pelicula, descripcion_pelicula, id_tipo) VALUES(%s, %s, %s)', (nombre_pelicula, descripcion, tipo_de_pelicula))

    conexion.commit()
    flash('Movie added successfully...')

    return redirect(url_for("Peliculas"))
@app.route('/edit_pelicula/<id>', methods = ['POST', 'GET'])
def get_Peliculas(id):
    cur=conexion.cursor()
    cur.execute('SELECT * FROM pelicula WHERE id_pelicula = %s', (id))
    data = cur.fetchall()
    return render_template('edit-pelicula.html',pelicula=data[0] )
@app.route('/update_pelicula/<id>', methods=['POST'])
def update_pelicula(id):
    if request.method=='POST':
        nombre_pelicula=request.form['nombre_pelicula']
        descripcion=request.form['descripcion']
        tipo_de_pelicula=request.form['tipo_de_pelicula']
        cur=conexion.cursor()
        cur.execute("""
        UPDATE pelicula
        SET nombre_pelicula=%s,
            descripcion_pelicula=%s,
            id_tipo=%s
        WHERE id_pelicula = %s
        """, (nombre_pelicula, descripcion, tipo_de_pelicula, id))
        conexion.commit()
        flash('Movie Updated Successfully')
        return redirect(url_for('Peliculas'))
@app.route('/delete_pelicula/<string:id>', methods = ['POST', 'GET'])
def delete_pelicula(id):
    cur=conexion.cursor()
    cur.execute('DELETE FROM pelicula WHERE id_pelicula = {0}'.format(id))
    conexion.commit()
    flash('Movie Removed Successfully...')
    return redirect(url_for('Peliculas'))
#FIN TABLA PELICULA

#TABLA EMPLEADO
@app.route('/Empleado')
def Empleados():
    cursor=conexion.cursor()
    query="SELECT e2.id_empleado, e2.nombre_empleado ,e2.apellido_empleado, e2.identidad_empleado,e3.nombre_tipo_cargo, e2.jefe as id_jefe, e1.nombre_empleado as nombre_jefe, e2.fecha_ingreso, e2.salario FROM empleado e1 FULL OUTER  join empleado e2 on (e2.jefe = e1.id_empleado)inner join tipo_cargo e3 ON (e3.id_tipo_cargo =e2.id_cargo);"
    cursor.execute(query)
    data=cursor.fetchall()
    cursor.close
    return render_template('Empleado.html', empleados = data)
@app.route('/add_empleado', methods = ['POST'])
def add_Empleado():
    nombre = request.form['nombre_empleado']
    apellido = request.form['apellido_empleado']
    CI=request.form['identidad_empleado']
    cargo=request.form['tipo_cargo']
    jefe=request.form['jefe']
    ingreso=request.form['fecha_ingreso']
    salario=request.form['salario']
    cur = conexion.cursor()
    cur.execute('INSERT INTO empleado (nombre_empleado, apellido_empleado, identidad_empleado, id_cargo, jefe, fecha_ingreso , salario ) VALUES(%s, %s, %s,%s, %s, %s, %s)', (nombre, apellido, CI, cargo, jefe, ingreso, salario))
    conexion.commit()
    flash('employee added successfully...')
    return redirect(url_for("Empleados"))
@app.route('/edit_empleado/<id>', methods = ['POST', 'GET'])
def get_Empleados(id):
    cur=conexion.cursor()
    cur.execute('SELECT * FROM empleado WHERE id_empleado = %s', (id))
    data = cur.fetchall()
    return render_template('edit-empleado.html',empleado=data[0] )
@app.route('/update_empleado/<id>', methods=['POST'])
def update_empleado(id):
   if request.method=='POST':
        nombre_empleado=request.form['nombre_empleado']
        apellido_empleado=request.form['apellido_empleado']
        identidad_empleado=request.form['identidad_empleado']
        tipo_cargo=request.form['tipo_cargo']
        jefe=request.form['jefe']
        fecha_ingreso=request.form['fecha_ingreso']
        salario=request.form['salario']
        cur=conexion.cursor()
        cur.execute("""
        UPDATE empleado
        SET nombre_empleado=%s,
            apellido_empleado=%s,
            identidad_empleado=%s,
            id_cargo=%s,
            jefe=%s,
            fecha_ingreso=%s,
            salario=%s
        WHERE id_empleado = %s
        """, (nombre_empleado, apellido_empleado, identidad_empleado,tipo_cargo,jefe,fecha_ingreso,salario, id))
        conexion.commit()
        flash('Employee Updated Successfully')
        return redirect(url_for('Empleados'))
@app.route('/delete_empleado/<string:id>', methods = ['POST', 'GET'])
def delete_empleado(id):
    cur=conexion.cursor()
    cur.execute('DELETE FROM empleado WHERE id_emplado = {0}'.format(id))
    conexion.commit()
    flash('Employee Removed Successfully...')
    return redirect(url_for('Empleados'))
#FIN TABLA EMPLEADO

#TABLA SALA
@app.route('/Sala')
def Salas():
    cursor=conexion.cursor()
    query="SELECT id_sala, nombre_sala, nombre_tipo from sala INNER JOIN  tipo_sala on tipo_sala.id_tipo=id_tipo_sala;"
    cursor.execute(query)
    data=cursor.fetchall()
    cursor.close
    return render_template('Sala.html', salas = data)
@app.route('/add_sala', methods = ['POST'])
def add_sala():

    nombre_sala = request.form['nombre_sala']
    id_tipo_sala=request.form['id_tipo_sala']
    cur = conexion.cursor()
    cur.execute('INSERT INTO sala (nombre_sala, id_tipo_sala ) VALUES( %s, %s)', (nombre_sala, id_tipo_sala))
    conexion.commit()
    flash('Theater added successfully...')
    return redirect(url_for("Salas")
    )
@app.route('/edit_sala/<string:id>', methods = ['POST', 'GET'])
def get_salas(id):
    cur=conexion.cursor()
    cur.execute("SELECT * from sala where id_sala = {0}".format(id))
    data = cur.fetchall()
    return render_template('edit-sala.html',sala=data[0] )
@app.route('/update_sala/<id>', methods=['POST'])
def update_sala(id):
    if request.method=='POST':
        nombre_sala=request.form['nombre_sala']
        id_tipo_sala=request.form['id_tipo_sala']
        cur=conexion.cursor()
        cur.execute("""
        UPDATE sala
        SET nombre_sala=%s,
            id_tipo_sala=%s
        WHERE id_sala = %s
        """, (nombre_sala, id_tipo_sala, id))
        conexion.commit()
        flash('Theater Updated Successfully')
        return redirect(url_for('Salas'))
@app.route('/delete_sala/<string:id>', methods = ['POST', 'GET'])
def delete_sala(id):
    cur=conexion.cursor()
    cur.execute('DELETE FROM sala WHERE id_sala = {0}'.format(id))
    conexion.commit()
    flash('Theater Removed Successfully...')
    return redirect(url_for('Salas'))
#FIN TABLA SALA

#TABLA FUNCION
@app.route('/Funcion')
def Funciones():
    cursor=conexion.cursor()
    query="select id_funcion, nombre_sala, nombre_pelicula, horario from funcion INNER JOIN sala on (funcion.id_sala=sala.id_sala)INNER JOIN pelicula on (funcion.id_pelicula=pelicula.id_pelicula);"
    cursor.execute(query)
    data=cursor.fetchall()
    cursor.close
    cursor=conexion.cursor()
    cursor.execute('select id_pelicula, nombre_pelicula from pelicula')
    datapelicula=cursor.fetchall()
    cursor.close
    return render_template('Funcion.html', funciones = data, peliculas = datapelicula)
@app.route("/add_funcion", methods = ["POST"])
def add_funcion():
    id_pelicula = request.form['id_pelicula']
    id_sala=request.form['id_sala']
    horario=request.form['horario']
    cur = conexion.cursor()
    cur.execute('INSERT INTO funcion (id_pelicula, id_sala, horario ) VALUES( %s, %s, %s)', (id_pelicula, id_sala, horario))
    conexion.commit()
    flash('Show added successfully...')
    return redirect(url_for("Funciones"))
@app.route('/edit_funcion/<string:id>', methods = ['POST', 'GET'])
def get_funcion(id):
    cur=conexion.cursor()
    cur.execute('SELECT * FROM funcion WHERE id_funcion = %s', (id))
    data = cur.fetchall()
    cursor=conexion.cursor()
    cursor.execute('SELECT id_pelicula, nombre_pelicula from pelicula')
    datapelicula=cursor.fetchall()
    cursor.close
    return render_template('edit-funcion.html',funcion=data[0], peliculas = datapelicula )
@app.route('/update_funcion/<id>', methods=['POST'])
def update_funcion(id):
    if request.method=='POST':
        id_pelicula=request.form['id_pelicula']
        id_sala=request.form['id_sala']
        horario=request.form['horario']
        cur=conexion.cursor()
        cur.execute("""
        UPDATE funcion
        SET id_pelicula=%s,
            id_sala=%s,
            horario=%s
        WHERE id_funcion = %s
        """, (id_pelicula, id_sala, horario, id))
        conexion.commit()
        flash('Show Updated Successfully')
        return redirect(url_for('Funciones'))
@app.route('/delete_funcion/<string:id>', methods = ['POST', 'GET'])
def delete_funcion(id):
    cur=conexion.cursor()
    cur.execute('DELETE FROM funcion WHERE id_funcion = {0}'.format(id))
    conexion.commit()
    flash('Theater Removed Successfully...')
    return redirect(url_for('Funciones'))
#FIN TABLA FUNCION

#TABLA TICKET
@app.route('/Ticket')
def ticket():
    pass


if __name__ == '__main__':
    app.run(port=3000, debug=True)