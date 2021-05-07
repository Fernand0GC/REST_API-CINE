from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)

#conexion a base de datos
conexion = psycopg2.connect(
    host = "127.0.0.1", 
    database = "Cine", 
    user = "postgres", 
    password = "73062466Fer")

# settings
app.secret_key='my secret key'

@app.route('/')
def index():
    return render_template('menu.html')

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
@app.route('/delete/<string:id>', methods = ['POST', 'GET'])
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
    query="SELECT id_empleado,nombre_empleado ,apellido_empleado, identidad_empleado, nombre_tipo_cargo, jefe, fecha_ingreso, salario FROM empleado INNER JOIN tipo_cargo ON empleado.id_cargo = tipo_cargo.id_tipo_cargo;"
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
        WHERE id_pelicula = %s
        """, (nombre_empleado, apellido_empleado, identidad_empleado,tipo_cargo,jefe,fecha_ingreso,salario, id))
        conexion.commit()
        flash('Employee Updated Successfully')
        return redirect(url_for('Empleados'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)