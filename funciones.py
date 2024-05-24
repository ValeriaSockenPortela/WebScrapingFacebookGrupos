from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime, timedelta
import re
diccionario = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12"
}
def inicioSeccion(driver, correo, contraseña):
    celda0 = driver.find_element(By.ID, 'email')
    celda0.send_keys(correo)
    sleep(2)
    celda0 = driver.find_element(By.ID, 'pass')
    celda0.send_keys(contraseña)
    elementoActivo = driver.switch_to.active_element
    elementoActivo.send_keys(Keys.ENTER)
    sleep(5)

def cerrarSeccion(driver):
    driver.refresh()
    sleep(5)
    elementoActivo = driver.switch_to.active_element
    elementoActivo.send_keys(Keys.TAB*10)
    elementoActivo = driver.switch_to.active_element
    elementoActivo.click()
    elementoActivo = driver.switch_to.active_element
    sleep(2)
    elementoActivo = driver.switch_to.active_element
    elementoActivo.send_keys(Keys.TAB*6)
    elementoActivo = driver.switch_to.active_element
    elementoActivo.click()
    sleep(5)

def fecha(texto):
    fechaTexto = texto.replace(" ", "")
    fechaActual = datetime.now()
    if len(fechaTexto) == 3 or len(fechaTexto) == 4:
        digitos = list(filter(str.isdigit, fechaTexto))
        cadena = ''.join(digitos)
        numeros = int(cadena)
        print(fechaTexto[1])
        if fechaTexto[1] == "h":
            print("Entro en horas")
            fechaHora = fechaActual - timedelta(hours=numeros)
            fecha = fechaHora.strftime('%Y-%m-%d')
            return fecha
        if fechaTexto[1] == "d":
            print("Entro en dias")
            fechaHora = fechaActual - timedelta(days=numeros)
            fecha = fechaHora.strftime('%Y-%m-%d')
            return fecha
    if len(fechaTexto) == 5 or len(fechaTexto) == 6:
        digitos = list(filter(str.isdigit, fechaTexto))
        cadena = ''.join(digitos)
        numeros = int(cadena)
        fechaHora = fechaActual - timedelta(minutes=numeros)
        fecha = fechaHora.strftime('%Y-%m-%d')
        return fecha
    if len(fechaTexto) == 18 and fechaTexto[0] == "A":
        #Listo
        fechaHora = fechaActual - timedelta(days=1)
        fecha = fechaHora.strftime('%Y-%m-%d')
        return fecha
    if len(fechaTexto) == 18 and fechaTexto[0] != "A":
        texto2 = texto.split()
        dia = texto2[0]
        mes = diccionario[texto2[2]]
        año = texto2[4]
        fecha = f"{año}-{mes}-{dia}"
        return fecha
    if len(fechaTexto) >= 20:
        #listo
        texto2 = texto.split()
        dia = texto2[0]
        mes = diccionario[texto2[2]]
        año = datetime.now().year
        fecha = f"{año}-{mes}-{dia}"
        return fecha