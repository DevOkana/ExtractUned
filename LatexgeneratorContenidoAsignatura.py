import os.path

import requests
from bs4 import BeautifulSoup
import datetime
import calendar

# URL de la página web que deseas analizar



mylist =[]
asignatura = ["71013012","71013029", "71013035","71013041","71013130"]

def addAsginatura(x):
    global mylist
    url = f"http://portal.uned.es/portal/page?_pageid=93,71763119&_dad=portal&_schema=PORTAL&idAsignatura={x}&idContenido=7&idTitulacion=7101"
    mylist.append(url)
for x in asignatura:
    addAsginatura(x)

#mylist = ["http://portal.uned.es/portal/page?_pageid=93,71763119&_dad=portal&_schema=PORTAL&idAsignatura=71013012&idContenido=7&idTitulacion=7101","http://portal.uned.es/portal/page?_pageid=93,71763119&_dad=portal&_schema=PORTAL&idAsignatura=71012024&idContenido=7&idTitulacion=7101","http://portal.uned.es/portal/page?_pageid=93,71763119&_dad=portal&_schema=PORTAL&idAsignatura=71902060&idContenido=7&idTitulacion=7101","http://portal.uned.es/portal/page?_pageid=93,71763119&_dad=portal&_schema=PORTAL&idAsignatura=71902077&idContenido=7&idTitulacion=7101","http://portal.uned.es/portal/page?_pageid=93,71763119&_dad=portal&_schema=PORTAL&idAsignatura=71902083&idContenido=7&idTitulacion=7101"]
# Realiza una solicitud HTTP a la URL
#mylist = ["https://www.uned.es/universidad/inicio/estudios/grados/grado-en-ingenieria-informatica/asignaturas.html?codTitulacion=7101&codAsignatura=71013012&idContenido=1"]
for x in mylist:
    url = x
    response = requests.get(url)
    fecha_actual = datetime.date.today()
    anno = fecha_actual.year
    mes = fecha_actual.month
    nombre_mes = calendar.month_name[mes]

    # Comprueba si la solicitud fue exitosa
    if response.status_code == 200:
        # Crea un objeto BeautifulSoup para analizar el contenido HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encuentra todos los elementos con la clase específica (reemplaza 'contenido_texto' con la clase real)
        elements_with_specific_class = soup.find_all(class_='contenido_texto')

        h1_element = soup.find('h1', class_='contenido_titulo')
        ruta_carpeta = "asignaturalatex"
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
        ruta_archivo = os.path.join(ruta_carpeta,h1_element.text+".tex")
        # Abre un archivo .tex en modo escritura
        with open(ruta_archivo, 'w', encoding='utf-8') as tex_file:
            tex_file.write("\\documentclass{article}\n")
            tex_file.write("\\usepackage{graphicx}\n")  # Required for inserting images
            tex_file.write("\\title{" + h1_element.text + "}\n")
            tex_file.write("\\date{" + str(nombre_mes) + " " + str(anno) + "}\n")
            tex_file.write("\\begin{document}\n")
            tex_file.write("\\maketitle\n")

            # Inicializa un contador para los subíndices de los elementos <h4>
            subindice_h4 = 1
            # Inicializa un contador para los subíndices de los elementos <li>
            subindice_li = 1

            # Inicializa una variable para rastrear la sección actual
            seccion_actual = None

            # Itera a través de los elementos encontrados
            for element in elements_with_specific_class:
                # Busca todos los elementos <h4> dentro de cada elemento con la clase específica
                h4_elements = element.find_all('h4')
                li_elements = element.find_all('li')

                # Itera a través de los elementos <h4> encontrados dentro de este elemento
                for h4 in h4_elements:
                    # Si la sección cambia, reinicia el contador de elementos <li>
                    if seccion_actual != h4.text:
                        seccion_actual = h4.text
                        subindice_li = 1

                    # Escribe el contenido del elemento <h4> con subíndice en formato LaTeX
                    tex_file.write(f"\\section*{{{subindice_h4}. {h4.text}}}\n")

                    # Encuentra los elementos <li> asociados a este <h4> (que están en el mismo elemento 'element')
                    related_li_elements = [li for li in li_elements if li.find_previous('h4') == h4]

                    # Itera a través de los elementos <li> relacionados
                    for li in related_li_elements:
                        # Escribe el contenido del elemento <li> con subíndice en formato LaTeX
                        tex_file.write(f"\\begin{{enumerate}}\n")
                        tex_file.write(f"  \\item[] {li.text}\n")
                        tex_file.write(f"\\end{{enumerate}}\n")
                        subindice_li += 1

                    subindice_h4 += 1

            tex_file.write("\\end{document}\n")

        print("El archivo output.tex ha sido generado con éxito.")
    else:
        print(f'Error al hacer la solicitud HTTP. Código de estado: {response.status_code}')
