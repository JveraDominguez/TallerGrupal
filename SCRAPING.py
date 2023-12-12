import locale
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
driver = webdriver.Chrome()

fechas = []
precios_eur = []
Var_pib = []

driver.get('https://datosmacro.expansion.com/pib/ecuador')

# Agrega un tiempo de espera para asegurarte de que la página se cargue completamente
driver.implicitly_wait(10)  # 10 segundos de espera

contenido = driver.page_source

soup = BeautifulSoup(contenido, 'html.parser')

# Encuentra la tabla específica con la clase 'tabledat'
tabla = soup.find('table', class_='tabledat')

# Encuentra las filas de la tabla
filas = tabla.find_all('tr')

for fila in filas[1:]:  # Comienza desde la segunda fila para evitar la cabecera
    # Encuentra las celdas en cada fila
    celdas = fila.find_all(['th', 'td'])

    # Si hay celdas, extrae los datos
    if celdas:
        # Excluye las filas que contienen el año 1960
        if '1960' not in fila.text:
            fechas.append(celdas[0].text.strip())
            precios_eur.append(celdas[1].text.strip())

            # Extrae el valor del porcentaje de la cuarta celda y conviértelo a un número decimal
            var_pib_text = celdas[3].text.strip().replace(',', '.').rstrip('%')
            var_pib_decimal = float(var_pib_text) if var_pib_text else None

            Var_pib.append(f"{var_pib_decimal}%")  # Agrega el símbolo "%" aquí

# Crear un DataFrame de pandas
df = pd.DataFrame({
    'fechas': fechas,
    'precios_eur': precios_eur,
    'Var. PIB (%)': Var_pib
})

# Imprimir el DataFrame
with pd.option_context('display.colheader_justify', 'center'):
    print(df)

# Guardar el DataFrame en un archivo CSV sin la columna de precios en dólares
df.to_csv('ECUADOR.csv', index=False, encoding='utf-8-sig')  # Utiliza 'utf-8-sig'

# Cerrar el navegador
driver.quit()

#integrantes
#Bravo Bailon Kennya Maria
#Baque Carrera Xiomara Andrea
#Vera Dominguez Jesus Gonzalo