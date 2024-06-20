
## Scraper Web para histórico de precios

Conjunto de scrapers para guardar precios de diferentes webs y guardar históricamente los datos, puede servir para luego de obtener muchos datos trabajar con análisis de datos, graficas, etc.

> **Pagina principal:** [flask.aleliz.xyz](https://flask.aleliz.xyz)

## Instalación

Descargar el repo de forma local

    git clone https://github.com/jata-imk/flaskrap.git
    cd flaskrap

Instalamos las dependencias de Flask *(Necesario uso de pipenv)*

    python -m pipenv install
    python -m pipenv shell
    
 Instalamos las dependencias de NPM *(frontend)*

    cd ./react-frontend/
    npm install
    
Nos posicionamos nuevamente en la carpeta raíz del proyecto e iniciamos el servidor de flask:

    cd ..
    flask run --debug

Ahora en otra terminal iniciamos el servidor de VITE

    cd ./react-frontend/
    npm run dev

Si todo salió bien ahora deberíamos tener dos servidores, uno en el puerto 5000 (Flask) y el otro en el puerto 5147 (Vite), entramos desde nuestro navegador a la dirección [http://localhost:5173](http://localhost:5000) y listo.

## Variables de entorno

Para poder ejecutar este proyecto necesitas solicitar las variables de entorno con los demás integrantes del proyecto, ya que por razones de seguridad no se suben al repositorio

## Principales tecnologías

 - Python v3.10.6
 - NodeJS v18.18.0
 - Flask
 - InertiaJS
 - ReactJS
 - Vite
 - TailwindCSS
