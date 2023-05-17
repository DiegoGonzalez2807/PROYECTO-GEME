import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
    if titulo:
        metadatos = [row for row in metadatos if titulo.lower() in row[0].lower()]
    if autor:
        metadatos = [row for row in metadatos if autor.lower() in row[1].lower()]
    if fecha:
        metadatos = [row for row in metadatos if fecha.lower() in row[2].lower()]
    if tema:
        metadatos = [row for row in metadatos if tema.lower() in row[3].lower()]
    # Mostrar solo los primeros 10 metadatos
    metadatos = metadatos[:10]
    # Renderizar la plantilla index.html con los metadatos filtrados y los tags correspondientes
    return render_template('index.html', metadatos=metadatos, titulo=titulo, autor=autor, fecha=fecha, tema=tema)

# Ruta de la página para agregar metadatos
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        # Leer los datos del formulario
        titulo = request.form['titulo']
        autor = request.form['autor']
        fecha = request.form['fecha']
        tema = request.form['tema']
        # Agregar los datos al archivo CSV
        with open('libros.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([titulo, autor, fecha, tema])
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
        # Actualizar los datos en el archivo CSV
        with open('libros.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            metadatos = [row for row in reader]
        metadatos[id] = [titulo, autor, fecha, tema]
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
    app.run(debug=True)
