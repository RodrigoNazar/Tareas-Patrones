# Tarea 02: Reconocedor de Paredes Rayadas

Esta tarea consiste en desarrollar un reconocedor automático de paredes rayadas usando características de texturas, un seleccionador de características y knn.

## Empezando

Estas instrucciones le proporcionarán las instrucciones para poder ejecutar de manera correcta en su máquina local la tarea.

### Prerrequisitos

Las cosas más importantes a tener en consideración, son:

* La tarea fue implementada usando un ambiente virtual en Python3.6, por lo que se recomienda fuertemente hacer lo mismo.

  A continuación proveeré unos links para su instalación y uso:

  [Instalación y uso en Ubuntu](https://www.digitalocean.com/community/tutorials/como-instalar-python-3-y-configurar-un-entorno-de-programacion-en-ubuntu-18-04-guia-de-inicio-rapido-es)

  [Instalación y uso en Mac](https://sourabhbajaj.com/mac-setup/Python/virtualenv.html)

  [Instalación y uso en Windows](https://programwithus.com/learn-to-code/Pip-and-virtualenv-on-Windows/)

  Luego de tener el ambiente virtual, es necesario ingresar a el para los pasos que vienen.

* Poder ejecutar el comando ```make``` dentro del directorio, al igual que ```make clean```.

### Instalación

Lo primero es instalar el ambiente virtual de python 3 en el directorio con:

```
virtualenv -p python3 venv
```

Para luego ingresar a el con:

```
source venv/bin/activate
```

Una vez ya dentro del ambiente virtual se recomienda ejecutar los siguientes comandos:

Instalar las librerías utilizadas en la tarea vía pip:
```
pip install -r requirements.txt
```

Luego ejecutar:

```
make clean
make
```

Esto hace que se eliminen los archivos compilados de python ```.pyc``` y que se ejecute el arhivo ```setup.py``` que ordena las dependencias de las rutas del proyecto.

Si no puedes ejecutar el comando ```make```, puedes ejecutar el siguiente comando que lo reemplaza:
```
python setup.py develop
```


Finalmente ejecutar:

```
python main.py
```

Para ejecutar el código de main de la tarea.

## Corriendo e importando el reconocedor

En el enunciado de la tarea se pide implementar una función ```reconocedor.py``` con una función ```reconocedor``` dentro.

Para importar esta función en un módulo aparte (como me imagino que corregirán), es necesario hacer todos los pasos anteriores, para que las rutas entre módulos estén bien definidas y no haya errores del tipo "Cannot import module..."

Entonces se debe copiar el archivo ```.py``` con el que se testeará la función ```reconocedor.py``` en el directorio ```T1-Patrones``` y desde ese módulo importar el reconocedor como:

```
from reconocedor import reconocedor
```

Así, se podrá usar la función de correcta manera

### Módulos y Directorios

* ```apps```: Se encuentran las distintas aplicaciones desarrolladas para cada uno de los requerimientos de la tarea.

  * ```feature_extraction.py```: Procesa las imágenes de la ruta ```img``` y obtiene sus características (tanto como de training, como testing), para guardarlas en ```data```.

  * ```feature_selection.py```: Contiene el código del algoritmo SFS para la selección de características.

  * ```classifier_performance.py```: Módulo que muestra estadísticas de desempeño del clasificador utilizado.

* ```data```: Directorio en el que se guardan datos del programa, para no tener que calcularlos todo el tiempo.
  * ```paredes_data.json```: Características de los datos de testing y training.

  * ```sfs_cache.json```: Datos de las características seleccionadas por sfs.

  * ```reconocedor.json```: Datos para el módulo ```reconocedor.py```.

* ```img```: Directorio en el que se encuentran las imágenes.

* ```utils```: Directorio de útiles desarrollados para la tarea.

  * ```lbp.py```: Extracción de características de LBP.

  * ```haralick.py```: Extracción de características de Haralick.

  * ```gabor.py```: Extracción de características de Gabor.

  * ```utils.py```: útiles generales para el procesamiento de imágenes


## Autor

* **Rodrigo Nazar** - *Ingeniería Eléctrica UC* - [RodrigoNazar](https://github.com/RodrigoNazar)
