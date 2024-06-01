# WebScrapingFacebookGrupos
Programa Autónomo de Recolección de Datos de Publicaciones en Grupos de Facebook
Este programa se encarga de recolectar datos de publicaciones en grupos de Facebook. Los datos que recopila incluyen el nombre de la persona que publicó, la fecha de la publicación, el contenido de la publicación y los comentarios asociados. Además, el programa accede a los perfiles de los usuarios para obtener los enlaces de sus perfiles. Toda esta información se guarda en una base de datos.

El programa enfrenta varios problemas, entre ellos:

Cambio de clases HTML: Las clases de los elementos HTML cambian con cierta frecuencia, lo que hace que el programa deje de funcionar al no encontrar los elementos deseados. Este problema se resolvió parcialmente para la fecha de publicación, accediendo a una publicación fija y navegando con la tecla Tab hasta el elemento deseado para extraer su clase.

Texto diferente al visible en pantalla: El texto obtenido de los elementos HTML era distinto al que se muestra en pantalla. Aparecían caracteres no deseados mezclados con la fecha. Inicialmente, se intentó filtrar estos caracteres, pero se descartó esta idea ya que los caracteres aparecían mezclados. En su lugar, se decidió capturar una imagen del elemento.

Para resolver este problema, se utilizaron las librerías PIL y pytesseract. El programa toma una captura de pantalla, recorta la imagen en las coordenadas del elemento deseado y luego convierte esa imagen en texto.

