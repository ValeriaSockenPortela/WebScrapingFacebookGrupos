from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from time import sleep

textoGuardar = """Guardar publicación
Agregar a tus elementos guardados."""#Textos que se comparan para sabes si la publicacion ya esta guardada
textoEliminar = """Eliminar publicación
Eliminar de tus elementos guardados"""
textoEnlace = """Guardar enlace
Agregar a tus elementos guardados."""
textoVideo = """Guardar video
Agregar a tus elementos guardados."""

def guardarPublicaciones2(driver, llave):
    def guardarPublicaciones(clasesV):
        try:
            elementoActivo = driver.switch_to.active_element
            while not all(clase in elementoActivo.get_attribute("class").split() for clase in clasesV):
                elementoActivo.send_keys(Keys.TAB)
                elementoActivo = driver.switch_to.active_element
                posicionNueva = elementoActivo.location['y']
                if posicionNueva == 0:
                    print("Regreso al inicio")
                    return
            print("======Encontró el elemento======")
            textoC = driver.switch_to.active_element.text
            print('\033[95m'+"Texto1:  ", textoC + '\033[0m')
            listaCon = [caracter for caracter in textoC if caracter != '\n']
            digitos = any(caracter.isdigit() for caracter in listaCon)
            print(len(listaCon))
            sleep(5)
            if (digitos and len(listaCon) > 30) or len(listaCon) == 0:
                driver.switch_to.active_element.send_keys(Keys.TAB)
                sleep(2)
                texto = driver.switch_to.active_element.text
                print('\033[91m'+"Texto2:   ", texto + '\033[0m')
                if texto == "Me gusta" or texto == "Ver más":
                    for _ in range(10):
                        driver.switch_to.active_element.send_keys(Keys.TAB)
                    guardarPublicaciones(clasesV)
                else:
                    driver.switch_to.active_element.send_keys(Keys.ENTER)
                    sleep(1)
                    elementoActivo = driver.switch_to.active_element
                    textoElementoActivo = elementoActivo.text
                    print('\033[92m'+"Texto3:  ", textoElementoActivo + '\033[0m')
                    if textoElementoActivo == textoGuardar or textoElementoActivo == textoEliminar:
                        if textoElementoActivo == textoGuardar:
                            elementoActivo.send_keys(Keys.ENTER)
                            sleep(2)
                            for _ in range(5):
                                driver.switch_to.active_element.send_keys(Keys.TAB)
                            sleep(2)
                            driver.switch_to.active_element.send_keys(Keys.ENTER)
                            sleep(2)
                            guardarPublicaciones(clasesV)
                        elif textoElementoActivo == textoEliminar:
                            if llave == 1:
                                print("Fin")
                                return
                            elif llave == 2:
                                guardarPublicaciones(clasesV)
                    else:
                        if textoElementoActivo == "Todas":
                            driver.switch_to.active_element.send_keys(Keys.TAB)
                            driver.switch_to.active_element.send_keys(Keys.ENTER)
                            guardarPublicaciones(clasesV)
                        else:
                            print('\033[95m', "No coincide",'\033[0m') 
                            guardarPublicaciones(clasesV)
            else:
                for _ in range(5):
                    driver.switch_to.active_element.send_keys(Keys.TAB)
                guardarPublicaciones(clasesV)
        except StaleElementReferenceException:
            print("Elemento obsoleto, reintentando...")
            guardarPublicaciones(clasesV)
        except Exception as e:
            print(f"Error inesperado: {e}")

    driver.get("https://www.facebook.com/groups/1591990424985025")
    sleep(5)
    driver.switch_to.active_element.send_keys(Keys.TAB*32)
    clasesV=driver.switch_to.active_element.get_attribute("class").split()
    driver.get("https://www.facebook.com/groups/ItverTroll.Bergas/?sorting_setting=CHRONOLOGICAL")
    sleep(5)
    driver.switch_to.active_element.send_keys(Keys.TAB*30)
    sleep(1)
    guardarPublicaciones(clasesV)