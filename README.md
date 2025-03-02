<h1 align="center">Proyecto Final</h1>
<p align="center" style="font-size: 22px"><b>Tokio School</b></p>
<p align="center">Aplicacion web de gestion de productos y proveedores</p>

<p align="center"><i>Erik Vives Von Heyne</i></p>

<p align="center"><img alt="banner" src="/src/static/images/banner.png"></p>

# Indice
- [Descripción](#descripción)
- [Funciones Clave](#funciones-clave)
- [Tecnologias](#tecnologias)
  - [Dependencias](#dependencias)
- [Instalación y Ejecución](#instalación-y-ejecución)
  - [Comprobaciones](#comprobaciones)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Aplicaciones de Trabajo Recomendadas](#apliaciones-de-trabajo-recomendadas)

# Descripción

Este proyecto web se trata de un **gestor web** diseñado para la gestion de usuarios, gestion de inventario, funcionalidades de administrador y sistemas de monitorización y reserva.

Utiliza un framework Flask con SQLAlchemy y varias otras dependencias.

# Funciones Clave

- Sistema de Login/Registro
- Contraseñas encriptadas
- Control de registro
- Union con Base de Datos SQLAlchemy
- Monitorización en web de base de datos
- Visualizador de estadisticas con graficas (Chart.JS)
- Acceso a la Base de Datos mediante UI (HTML)
...

# Tecnologias

| Technology       	| Version 	|
|------------------	|---------	|
| Python           	| 3.12.6  	|
| Flask            	| 3.0.3   	|
| Flask-Session    	| 0.8.0   	|
| Flask-SQLAlchemy 	| 3.1.1   	|
| SQLAlchemy       	| 2.0.36  	|
| Jinja2           	| 3.1.5   	|
| Werkzeug         	| 3.1.3   	|
| pathlib         	| 1.0.1   	|

## Dependencias

Todas las dependencias que **dependan de python** estan definidas en el archivo [requirements](https://github.com/ElHeyne/ProyectoFinalTS/blob/main/requirements.txt)

Tambien se requiere la instalación de npm y nvm para la instalación de **ChartJS**, que es el responsable de mostrar las gráficas.

# Instalación y Ejecución

```
# Clonar el repositorio
git clone https://github.com/ElHeyne/ProyectoFinalTS

# Entrar en el directorio
cd ProyectoFinalTS

# Crear un entorno virtual
python -m venv venv
source venv/bin/activate  
# En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Comprobar NPM y ChartsJS
node -v
npm -v

# Ejecutar el gestor
python ./src/app.py
```

## Comprobaciones

Es recomendable revisar que las versiones de los componentes dentro del .venv o del sistema que ejecuta el proyecto tenga las versiones correctas.

```
# Revisar Python
python -V

# Revisar PIP
pip --version
pip list

# Revisar NPM y ChartsJS
node -v
npm -v
```

# Estructura del Proyecto
```
ProyectoFinalTS
├───src
│   ├───database
│   │   └───.db
│   ├───static
│   │   ├───.js
│   │   ├───.css
│   │   └───images
│   └───templates
│       └───.html
├───.gitignore
├───README.md
├───requirements.txt
└───.py
```

# Apliaciones de Trabajo Recomendadas
| App              	    | Motivo                  |
|---------------------  |-----------------------  |
| Visual Studio Code	| Edición de Codigo       |
| PyCharm C.E.      	| Edición de Codigo       |
| Beekeeper Studio     	| Manejo de Base de Datos |