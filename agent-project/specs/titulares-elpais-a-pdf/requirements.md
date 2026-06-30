# Requirements

## R1
CUANDO se proporciona la URL https://elpais.com/, el sistema DEBE extraer un listado de titulares principales del HTML publico de la pagina.

## R2
CUANDO se ejecuta el flujo de exportacion, el sistema DEBE generar un archivo PDF con los titulares extraidos en formato de lista legible.

## R3
CUANDO el usuario solicita informacion de dependencias, el sistema DEBE devolver el listado completo de librerias Python necesarias para scraping, parseo HTML y generacion del PDF.

## R4
SI la URL no es accesible, la estructura HTML no contiene titulares esperados o falla la escritura del PDF ENTONCES el sistema DEBE informar un error explicito y no devolver un PDF corrupto.

## R5
MIENTRAS se mantenga la implementacion de scraping y extraccion, el sistema DEBE estructurar el codigo con patron POM separando objetos de pagina de la logica de orquestacion.
