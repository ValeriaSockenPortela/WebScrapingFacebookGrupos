from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import mysql.connector
from time import sleep
from PIL import Image
import pytesseract
import funciones
import re

def guardarEnBaseDatos(driver1, driver2, driver3):
    ajustarY = -55
    nombreAnonimo = "Miembro anónimo"
    nombreAnonimo2 = "Participante anónimo"
    publicacionNoDisponibleTexto = "Este producto no está disponible ahora."
    #Clases para eliminar
    clasesVerComentarios = ["x1i10hfl", "xjbqb8w", "xjqpnuy", "xa49m3k", "xqeqjp1", "x2hbi6w", "x13fuv20", "xu3j5b3", "x1q0q8m5", "x26u7qi", "x972fbf", 
                                "xcfux6l", "x1qhh985", "xm0m39n", "x9f619", "x1ypdohk", "xdl72j9", "xe8uvvx", "xdj266r", "x11i5rnm", "xat24cr", "x1mh8g0r", 
                                "x2lwn1j", "xeuugli", "xexx8yu", "x18d9i69", "xkhd6sd", "x1n2onr6", "x16tdsg8", "x1hl2dhg", "xggy1nq", "x1ja2u2z", "x1t137rt", 
                                "x1o1ewxj", "x3x9cwd", "x1e5q0jg", "x13rtm0m", "x3nfvp2", "x1q0g3np", "x87ps6o", "x1a2a7pz", "x6s0dn4", "xi81zsa", "x1iyjqo2", 
                                "xs83m0k", "xsyo7zv", "xt0b8zv"]
    #Clase para ver los comentarios
    clasesComentarios = ["x1n2onr6", "x1swvt13", "x1iorvi4", "x78zum5", "x1q0g3np", "x1a2a7pz"]
    #Clase para ver los usuarios de los comentarios
    clasesLinkComentariosUsuarios = ["xt0psk2"]
    #Clases para el proceso de eliminado
    clasesPublicaciones = ["x1yztbdb", "xh8yej3"]
    #clase para eliminar las publicaciones ya eliminadas
    clasesPubliacionesELiminadas = ["x1lliihq", "x6ikm8r", "x10wlt62", "x1n2onr6"]
    def comentarios(idPermalinkPublicacion, usuarioPublicacion):
        
        print("-----COMENTARIOS-----")
        try:
            elementosComentarios = driver2.find_elements(By.XPATH, f"//*[contains(@class, '{' '.join(clasesComentarios)}')]")
        except NoSuchElementException:
            print("Puede que cambiarion las clases clasesComentarios")
            #Aqui hay que llamar el metodo de reparacion
            return
        comentarioTexto = [elementosTexto.text for elementosTexto in elementosComentarios]
        if comentarioTexto:
            try:
                try:
                    elementos = driver2.find_elements(By.XPATH, f"//*[contains(@class, '{' '.join(clasesVerComentarios)}')]")
                except NoSuchElementException:
                    print("Puede que las clases hayan cambiado, clasesVerComentarios")
                for elemento in elementos:
                    elemento.click()
                sleep(5)
            except Exception as e:
                print("Error3: ",e)
            try:
                elementosLinkUsuario = driver2.find_elements(By.XPATH, f"//*[contains(@class, '{' '.join(clasesLinkComentariosUsuarios)}')]")
            except NoSuchElementException:
                print("Puede que las clases hayan cambiado, clasesLinkComentariosUsuarios")
            elementoTexto = [elemento.get_attribute("href") for elemento in elementosLinkUsuario]
            linksFiltrados = [enlace for enlace in elementoTexto if enlace is not None and '/user/' in enlace]
            if usuarioPublicacion != nombreAnonimo or usuarioPublicacion != nombreAnonimo2:
                linksFiltrados.pop(0)
                linksFiltrados.pop(0)
            elementosComentarios = driver2.find_elements(By.XPATH, f"//*[contains(@class, '{' '.join(clasesComentarios)}')]")
            comentarioTexto = [elementosTexto.text for elementosTexto in elementosComentarios]
            for comentario, link in zip(comentarioTexto, linksFiltrados):
                partes = comentario.split('\n')
                #print(partes)
                nombre = partes[0]
                comentario = partes[1]
                if comentario == "Colaborador destacado" or comentario == "Autor":
                    comentario = partes[2]
                    if comentario == "  ·" and partes[3] == "Seguir":
                        comentario = partes[4]
                print("==========================================================================")
                print("Usuario: ", nombre)
                print("Comentario: ", comentario)
                if nombre != nombreAnonimo:
                    driver3.get(link)
                    sleep(10)
                    pattern = r"/user/(\d+)/"
                    match = re.search(pattern, link)
                    Permalink = match.group(1)
                    print(Permalink)
                    driver3.find_element(By.LINK_TEXT, 'Ver perfil').click()
                    sleep(5)
                    link = driver3.current_url
                    print(link)
                    mydb = mysql.connector.connect(host="localhost", user="root", password="Arturit0tsuru.,", database="itverTroll")
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM usuarios WHERE permalink = %s"
                    mycursor.execute(sql,(Permalink, ))
                    resultados = mycursor.fetchall()
                    if not resultados:
                        sql = "INSERT INTO usuarios (link, permalink, nombre) VALUES (%s, %s, %s)"
                        mycursor.execute(sql, (link, Permalink, nombre, ))
                        mydb.commit()     
                    sql = "SELECT * FROM comentarios WHERE idPublicacion = %s AND idUsuario = %s AND comentario LIKE %s"
                    mycursor.execute(sql, (idPermalinkPublicacion, Permalink, comentario, ))
                    resultados = mycursor.fetchall()
                    if not resultados:
                        sql = "INSERT INTO comentarios (idPublicacion, idUsuario, comentario) VALUES (%s, %s, %s)"
                        mycursor.execute(sql, (idPermalinkPublicacion, Permalink, comentario, ))
                        mydb.commit()
                    mycursor.close()
                    mydb.close()
                else:
                    print("Usuario Anonimo no se busca su perfil")
                    Permalink = 1
                    mydb = mysql.connector.connect(host="localhost", user="root", password="Arturit0tsuru.,", database="itverTroll")
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM comentarios WHERE idPublicacion = %s AND idUsuario = %s AND comentario LIKE %s"
                    mycursor.execute(sql, (idPermalinkPublicacion, Permalink, comentario, ))
                    resultados = mycursor.fetchall()
                    if not resultados:
                        sql = "INSERT INTO comentarios (idPublicacion, idUsuario, comentario) VALUES (%s, %s, %s)"
                        mycursor.execute(sql, (idPermalinkPublicacion, Permalink, comentario, ))
                        mydb.commit()
                        mycursor.close()
                        mydb.close()
        else:
            print('\033[96m'+"No hay comentarios"+'\033[0m')

    def publicaciones():
        driver1.switch_to.active_element.send_keys(Keys.TAB)
        elementoActivo = driver1.switch_to.active_element
        while not all(clase in elementoActivo.get_attribute("class").split() for clase in clasesVerificar):
            posicionNueva = elementoActivo.location['y']
            elementoActivo = driver1.switch_to.active_element
            elementoActivo.send_keys(Keys.TAB)
            elementoActivo = driver1.switch_to.active_element
            if posicionNueva == 0:
                print('\033[90m' + "Regreso al inicio" + '\033[0m')
                driver1.refresh()
                """
                elementosPublicacionesEliminadas = driver1.find_elements(By.XPATH, f"//*[contains(text(), '{publicacionNoDisponibleTexto}')]")
                cantidad2 = len(elementosPublicacionesEliminadas)
                elementos = driver1.find_elements(By.XPATH, f"//*[contains(@class, '{' '.join(clasesPublicaciones)}')]")
                cantidad = len(elementos)
                if cantidad == cantidad2:
                    print("Entro en eliminar publicaciones ya no disponibles")
                    driver1.refresh()
                    sleep(5)
                    driver1.switch_to.active_element.send_keys(Keys.TAB * 17)
                    sleep(2)
                    driver1.switch_to.active_element.send_keys(Keys.ENTER)
                    sleep(2)
                    driver1.switch_to.active_element.send_keys(Keys.ENTER)
                    publicaciones()
                if cantidad != 0:
                    driver1.switch_to.active_element.send_keys(Keys.TAB*10)
                    publicaciones()"""
        elementoActivo.send_keys(Keys.TAB)
        publicacion = driver1.switch_to.active_element.text
        print("==PUBLICACION==")
        print(publicacion)#Publicacion
        linkPublicacion = driver1.switch_to.active_element.get_attribute("href")
        print(linkPublicacion)#url de la publiacion
        patron = r'\d+' 
        id = re.findall(patron, linkPublicacion)
        idPermalink = id[-1]
        print(idPermalink)#Permalink Publicacion de usuario
        mydb = mysql.connector.connect(host="localhost",user="root",password="Arturit0tsuru.,",database="itverTroll")
        mycursor = mydb.cursor()
        sql = "SELECT * FROM publicaciones WHERE permalink = %s"
        mycursor.execute(sql,(idPermalink, ))
        resultados = mycursor.fetchall()
        if resultados:
            print('\033[91m'+"Publicaciones ya guardada"+'\033[0m')
            driver1.switch_to.active_element.send_keys(Keys.TAB)
            driver1.switch_to.active_element.send_keys(Keys.ENTER)
            sleep(2)
            if driver1.switch_to.active_element.text == "Compartir":
                driver1.switch_to.active_element.send_keys(Keys.ARROW_DOWN)
            sleep(2)
            driver1.switch_to.active_element.send_keys(Keys.ENTER)
            sleep(2)
            driver1.switch_to.active_element.send_keys(Keys.TAB*10)
            publicaciones()
        if not resultados:
            driver2.get(linkPublicacion)
            sleep(5)
            driver2.switch_to.active_element.send_keys(Keys.TAB*28)
            elementoNombreUsuario = driver2.switch_to.active_element
            textoNombre = elementoNombreUsuario.text
            driver2.switch_to.active_element.send_keys(Keys.TAB)
            elementoFecha = driver2.switch_to.active_element
            driver2.switch_to.active_element.send_keys(Keys.TAB)
            location = elementoFecha.location
            size = elementoFecha.size
            driver2.save_screenshot('full_screenshot.png')
            full_image = Image.open('full_screenshot.png')
            left = location['x']
            top = location['y'] + ajustarY
            right = left + size['width']
            bottom = top + size['height']
            cropped_image = full_image.crop((left, top, right, bottom))
            cropped_image.save('cropped_screenshot.png')
            text = pytesseract.image_to_string(cropped_image)
            print(text)
            fecha = funciones.fecha(text)
            print("fecha: ",fecha)
            print("-----Usuario")
            print(textoNombre)
            if textoNombre == nombreAnonimo or textoNombre == nombreAnonimo2:
                #print(textoNombre)
                idPermalinkUsuario = 1
            else:
                driver2.refresh()
                sleep(5)
                driver2.switch_to.active_element.send_keys(Keys.TAB*28)
                driver2.switch_to.active_element.send_keys(Keys.ENTER*2)
                sleep(5)
                linkUsuario = driver2.current_url
                driver2.back()
                driver3.get(linkUsuario)
                sleep(10)
                pattern = r"/user/(\d+)/"
                match = re.search(pattern, linkUsuario)
                idPermalinkUsuario = match.group(1)
                print(idPermalinkUsuario)
                mydb = mysql.connector.connect(host="localhost",user="root",password="Arturit0tsuru.,",database="itverTroll")
                mycursor = mydb.cursor()
                sql = "SELECT * FROM usuarios WHERE permalink = %s"
                mycursor.execute(sql,(idPermalinkUsuario, ))
                resultados = mycursor.fetchall()
                if not resultados:
                    print('\033[92m'+"El usuario no esta guardado"+'\033[0m')
                    driver3.find_element(By.LINK_TEXT, 'Ver perfil').click()
                    sleep(5)
                    link = driver3.current_url
                    print(link)
                    #Comprueba que el usuario no este guardado en la base de datos
                    sql = "INSERT INTO usuarios (link, permalink, nombre) VALUES (%s, %s, %s)"
                    mycursor.execute(sql, (link, idPermalinkUsuario, textoNombre, ))
                    mydb.commit()
                    mycursor.close()
                    mydb.close()
                mycursor.close()
                mydb.close()
            mydb = mysql.connector.connect(host="localhost",user="root",password="Arturit0tsuru.,",database="itverTroll")
            mycursor = mydb.cursor()
            sql = "INSERT INTO publicaciones (idUsuario, publicacion, link, fecha, permalink) VALUES (%s, %s, %s, %s, %s)"
            mycursor.execute(sql, (idPermalinkUsuario, publicacion, linkPublicacion, fecha, idPermalink, ))
            mydb.commit()
            mycursor.close()
            mydb.close()
            sleep(2)
            comentarios(idPermalink, textoNombre)
            publicaciones()
    
    driver1.get("https://www.facebook.com/saved/?list_id=122117340248260572&referrer=SAVE_DASHBOARD_NAVIGATION_PANEL")
    sleep(2)
    driver1.switch_to.active_element.send_keys(Keys.TAB*18)
    clasesVerificar = driver1.switch_to.active_element.get_attribute("class").split()
    driver1.refresh()
    sleep(5)
    driver1.switch_to.active_element.send_keys(Keys.TAB)
    publicaciones()