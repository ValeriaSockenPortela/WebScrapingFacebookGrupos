from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep
import funciones
from selenium.webdriver.common.keys import Keys
import guardarPublicaciones
import guardarEnBaseDatos

chrome_options = Options()
chrome_options.add_argument("--incognito")
s = Service("/usr/local/bin/chromedriver")
d1 = True
d2 = True
d3 = True
while True:
    print("Escoja un numero")
    print("1.-Guardar publicaciones en la seccion de guardados")
    print("2.-Guardar en la base de datos")
    print("3.-Salir")
    respuesta = int(input("Ingrese un numero:", ))
    if respuesta == 1:
        print("Que quiere hacer? ")
        print("1.-Finalizar cuando encuentre la primera opcion ya guardada")
        print("2.-Seguir guardando")
        llave = int(input("Ingrese un numero: ", ))
        if d1:
            driver1 = webdriver.Chrome(service=s, options=chrome_options)
            driver1.get("https://www.facebook.com/")
            driver1.maximize_window()
            funciones.inicioSeccion(driver1,'PaolaHernandez123572@outlook.com','')
            sleep(5)
            d1 = False
        guardarPublicaciones.guardarPublicaciones2(driver1, llave)

    if respuesta == 2:
        if d1:
            driver1 = webdriver.Chrome(service=s, options=chrome_options)
            driver1.get("https://www.facebook.com/")
            driver1.maximize_window()
            funciones.inicioSeccion(driver1,'PaolaHernandez123572@outlook.com','')
            sleep(5)
            d1 = False
        if d2:
            driver2 = webdriver.Chrome(service=s, options=chrome_options)
            driver2.get("https://www.facebook.com/")
            driver2.maximize_window()
            funciones.inicioSeccion(driver2,'PaolaHernandez123572@outlook.com', '')
            sleep(5)
            d2 = False
        if d3:
            driver3 = webdriver.Chrome(service=s, options=chrome_options)
            driver3.get("https://www.facebook.com/")
            driver3.maximize_window()
            funciones.inicioSeccion(driver3, 'karlaPerez43223@outlook.com','')
            sleep(5)
            d3 = False
        guardarEnBaseDatos.guardarEnBaseDatos(driver1, driver2, driver3)
    if respuesta == 3:
        if not d1:
            funciones.cerrarSeccion(driver1)
        if not d2:
            funciones.cerrarSeccion(driver2)
        if not d3:
            funciones.cerrarSeccion(driver3)
        break