import csv
from faker import Faker

fake = Faker()

# Generar 100 libros de metadatos
libros = []
for i in range(100):
    titulo = fake.sentence(nb_words=3, variable_nb_words=True)
    autor = fake.name()
    fecha = fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d')
    tema = fake.random_element(elements=('Datos Maestros', 'Metadatos', 'Gestión de datos', 'Programacion'))
    tipo_contenido = fake.random_element(elements=('Texto', 'Imagen', 'Audio', 'Video'))
    palabras_clave = '; '.join(fake.words(nb=3))
    descripcion = fake.paragraph(nb_sentences=2)
    idioma = fake.language_name()
    licencia = fake.random_element(elements=('CC BY', 'CC BY-NC', 'CC BY-SA', 'CC0', 'Todos los derechos reservados'))
    numero_paginas = fake.random_int(min=1, max=500)
    formato = fake.random_element(elements=('PDF', 'MP3', 'MP4'))
    
    libros.append((titulo, autor, fecha, tema, tipo_contenido, palabras_clave, descripcion, idioma, licencia, numero_paginas, formato))

# Escribir los libros en un archivo CSV
with open('libros.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # writer.writerow(['Titulo', 'Autor', 'Fecha de creacion', 'Tipo de contenido', 'Palabras Clave', 'Descripcion', 'Idioma', 'Tema', 'Licencia', 'Numero de Paginas', 'Formato'])
    for libro in libros:
        writer.writerow(libro)