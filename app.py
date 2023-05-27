import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Base de datos de usuarios quemados
users = {'usuario1': 'contrasena1', 'usuario2': 'contraseña2', 'usuario3': 'contraseña3', 'usuario4': 'contraseña4', 'usuario5': 'contraseña5'}
usersInfo = {'usuario1': {'nombre': 'Usuario 1', 'edad': 25, 'nacionalidad': 'México'},
            'usuario2': {'nombre': 'Usuario 2', 'edad': 30, 'nacionalidad': 'España'},
            'usuario3': {'nombre': 'Usuario 3', 'edad': 28, 'nacionalidad': 'Estados Unidos'},
            'usuario4': {'nombre': 'Usuario 4', 'edad': 32, 'nacionalidad': 'Argentina'},
            'usuario5': {'nombre': 'Usuario 5', 'edad': 27, 'nacionalidad': 'Brasil'}}

# Arreglo para almacenar las búsquedas realizadas
busquedas = []

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener el nombre de usuario y la contraseña ingresados por el usuario
        username = request.form['username']
        password = request.form['password']
        # Verificar si el usuario y la contraseña coinciden
        if username in users and password == users[username]:
            # Inicio de sesión exitoso, redirigir a la página principal
            return redirect(url_for('index'))
        else:
            # Nombre de usuario o contraseña incorrectos, mostrar mensaje de error
            return render_template('login.html', error_message='Nombre de usuario o contraseña incorrectos.')
    else:
        # Mostrar la página de inicio de sesión
        return render_template('login.html')

# Ruta de la página de inicio
@app.route('/')
def index():
    # Leer los metadatos del archivo CSV
    with open('libros.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        metadatos = [row for row in reader]
    # Filtrar los metadatos según los criterios de búsqueda
    titulo = request.args.get('titulo', '')
    autor = request.args.get('autor', '')
    fecha = request.args.get('fecha', '')
    tema = request.args.get('tema', '')
    tipo_contenido = request.args.get('tipo_contenido', '')
    palabras_clave = request.args.get('palabras_clave', '')
    descripcion = request.args.get('descripcion', '')
    idioma = request.args.get('idioma', '')
    licencia = request.args.get('licencia', '')
    num_paginas = request.args.get('num_paginas', '')
    formato = request.args.get('formato', '')

    # Crear un diccionario con los valores de búsqueda
    busqueda = {
        'titulo': titulo,
        'autor': autor,
        'fecha': fecha,
        'tema': tema,
        'tipo_contenido': tipo_contenido,
        'palabras_clave': palabras_clave,
        'descripcion': descripcion,
        'idioma': idioma,
        'licencia': licencia,
        'num_paginas': num_paginas,
        'formato': formato
    }

    # Guardar la búsqueda en el arreglo
    busquedas.append(busqueda)

    if titulo:
        metadatos = [row for row in metadatos if titulo.lower() in row[0].lower()]
    if autor:
        metadatos = [row for row in metadatos if autor.lower() in row[1].lower()]
    if fecha:
        metadatos = [row for row in metadatos if fecha.lower() in row[2].lower()]
    if tema:
        metadatos = [row for row in metadatos if tema.lower() in row[3].lower()]
    if tipo_contenido:
        metadatos = [row for row in metadatos if tipo_contenido.lower() in row[4].lower()]
    if palabras_clave:
        metadatos = [row for row in metadatos if palabras_clave.lower() in row[5].lower()]
    if descripcion:
        metadatos = [row for row in metadatos if descripcion.lower() in row[6].lower()]
    if idioma:
        metadatos = [row for row in metadatos if idioma.lower() in row[7].lower()]
    if licencia:
        metadatos = [row for row in metadatos if licencia.lower() in row[8].lower()]
    if num_paginas:
        metadatos = [row for row in metadatos if num_paginas.lower() in row[9].lower()]
    if formato:
        metadatos = [row for row in metadatos if formato.lower() in row[10].lower()]

    # Mostrar solo los primeros 10 metadatos
    metadatos = metadatos[:10]

    # Obtener los temas más buscados
    temas_buscados = {}

    # Contar la frecuencia de cada tema en las búsquedas
    for busqueda in busquedas:
        tema = busqueda.get('tema')
        if tema in temas_buscados:
            temas_buscados[tema] += 1
        else:
            temas_buscados[tema] = 1

    # Ordenar los temas por su frecuencia en orden descendente
    temas_ordenados = sorted(temas_buscados.items(), key=lambda x: x[1], reverse=True)

    # Obtener los dos temas más buscados
    if len(temas_ordenados) >= 2:
        tema_mas_buscado = temas_ordenados[0][0]
        segundo_tema_mas_buscado = temas_ordenados[1][0]
    else:
        tema_mas_buscado = ""
        segundo_tema_mas_buscado = ""

    # Renderizar la plantilla index.html con los metadatos filtrados, los temas más buscados y los tags correspondientes
    return render_template('index.html', metadatos=metadatos, titulo=titulo, autor=autor, fecha=fecha, tema=tema,
                           tipo_contenido=tipo_contenido, palabras_clave=palabras_clave, descripcion=descripcion,
                           idioma=idioma, licencia=licencia, num_paginas=num_paginas, formato=formato,
                           tema_mas_buscado=tema_mas_buscado, segundo_tema_mas_buscado=segundo_tema_mas_buscado)

# Ruta de la página para agregar metadatos
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        # Leer los datos del formulario
        titulo = request.form['titulo']
        autor = request.form['autor']
        fecha = request.form['fecha']
        tema = request.form['tema']
        tipo_contenido = request.form['tipo_contenido']
        palabras_clave = request.form['palabras_clave']
        descripcion = request.form['descripcion']
        idioma = request.form['idioma']
        licencia = request.form['licencia']
        num_paginas = request.form['num_paginas']
        formato = request.form['formato']
        # Agregar los datos al archivo CSV
        with open('libros.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([titulo, autor, fecha, tema, tipo_contenido, palabras_clave, descripcion, idioma,
                             licencia, num_paginas, formato])
        # Redirigir a la página de inicio
        return redirect(url_for('index'))
    else:
        # Renderizar la plantilla agregar.html
        return render_template('agregar.html')

# Ruta de la página para editar metadatos
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        # Leer los datos del formulario
        titulo = request.form['titulo']
        autor = request.form['autor']
        fecha = request.form['fecha']
        tema = request.form['tema']
        tipo_contenido = request.form['tipo_contenido']
        palabras_clave = request.form['palabras_clave']
        descripcion = request.form['descripcion']
        idioma = request.form['idioma']
        licencia = request.form['licencia']
        num_paginas = request.form['num_paginas']
        formato = request.form['formato']
        # Actualizar los datos en el archivo CSV
        with open('libros.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            metadatos = [row for row in reader]
        metadatos[id] = [titulo, autor, fecha, tema, tipo_contenido, palabras_clave, descripcion, idioma,
                         licencia, num_paginas, formato]
        with open('libros.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for metadato in metadatos:
                writer.writerow(metadato)
        # Redirigir a la página de inicio
        return redirect(url_for('index'))
    else:
        # Leer los metadatos del archivo CSV
        with open('libros.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            metadato = [row for i, row in enumerate(reader) if i == id][0]
        # Renderizar la plantilla editar.html con los metadatos
        return render_template('editar.html', metadato=metadato)

# Ruta para eliminar metadatos
@app.route('/eliminar/<int:id>')
def eliminar(id):
    # Eliminar los datos del archivo CSV
    with open('libros.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        metadatos = [row for row in reader]
    del metadatos[id]
    with open('libros.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for metadato in metadatos:
            writer.writerow(metadato)
    # Redirigir a la página de inicio
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
