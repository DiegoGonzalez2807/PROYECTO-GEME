import csv
from faker import Faker

fake = Faker()

# Generar 100 libros de historia
libros = []
for i in range(100):
    titulo = fake.sentence(nb_words=4)
    autor = fake.name()
    fecha = fake.year()
    tema = 'Historia'
    libros.append((titulo, autor, fecha, tema))

# Escribir los libros en un archivo CSV
with open('libros.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Título', 'Autor', 'Fecha', 'Tema'])
    for libro in libros:
        writer.writerow(libro)
