# Proyecto Final – Automatización de Pruebas de API

## 1. Descripción general

Este proyecto implementa una automatización de pruebas de API en Python,
utilizando `pytest` y `requests` para probar la API pública **JSONPlaceholder**  
(`https://jsonplaceholder.typicode.com`).

El objetivo es:

- Practicar los conceptos de Testing QA aplicados a APIs.
- Diseñar una arquitectura clara y mantenible (Page Object Model, pero aplicada a API mediante *clients*).
- Incorporar logging y reportes HTML para facilitar el análisis de resultados.

La solución se centra en los recursos `/posts` y `/users` de JSONPlaceholder. 


## 2. Tecnologías utilizadas

 ** Lenguaje: Python 3.x  
 ** Framework de testing: `pytest`  
 ** Cliente HTTP: `requests`  
 ** Reportes: `pytest-html`  
 ** Logging: módulo estándar `logging` de Python

Estas herramientas son estándar y recomendadas para testing de APIs en Python. 



## 3. Estructura del proyecto

proyecto-final-automation-testing-FuxGisela/
├── pages/                     # "POM" para API: clients por recurso
│   ├── __init__.py
│   ├── base_client.py         # BaseAPIClient (URL base, sesión, logging, métodos HTTP)
│   ├── posts_client.py        # PostsClient (acciones sobre /posts)
│   └── users_client.py        # UsersClient (acciones sobre /users)
├── tests/
│   └── api/
│       ├── test_posts_basic_api.py      # Tests básicos de /posts
│       ├── test_posts_lifecycle_api.py  # Ciclo completo: POST → GET → PATCH → GET → DELETE → GET
│       └── test_users_api.py           # Tests básicos de /users
├── utils/
│   ├── __init__.py
│   └── logger.py              # Configuración de logging (consola + archivo)
├── logs/                      # Archivos de log (api_tests.log)
├── reports/                   # Reportes HTML generados por pytest-html
├── conftest.py                # Fixtures de pytest (clients de API)
├── pytest.ini                 # Configuración global de pytest (paths, markers, opciones)
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Este archivo
```

### Carpeta `pages/` (arquitectura tipo POM para API)

- `base_client.py`:  
  - Define la clase `BaseAPIClient`.  
  - Contiene la URL base de JSONPlaceholder (`https://jsonplaceholder.typicode.com`).  
  - Usa una sesión de `requests.Session()` para reutilizar conexiones.  
  - Implementa métodos genéricos: `get`, `post`, `put`, `patch`, `delete`.  
  - Realiza **logging** de cada request y response (método HTTP, URL, parámetros y cuerpo). [web:120][web:132]

- `posts_client.py`:  
  - Hereda de `BaseAPIClient`.  
  - Expone métodos de alto nivel para `/posts`:  
    - `get_all_posts()`  
    - `get_post_by_id(post_id)`  
    - `create_post(payload)`  
    - `update_post_put(post_id, payload)`  
    - `update_post_patch(post_id, payload)`  
    - `delete_post(post_id)`

- `users_client.py`:  
  - Hereda de `BaseAPIClient`.  
  - Expone métodos para `/users`:  
    - `get_all_users()`  
    - `get_user_by_id(user_id)`

Esta capa es el equivalente al **Page Object Model**, pero aplicada a recursos de una API en lugar de páginas de UI. [web:126][web:123]

### Carpeta `tests/api/`

- `test_posts_basic_api.py`  
  - Valida operaciones básicas sobre `/posts`:
    - `GET /posts` devuelve lista con estructura correcta.  
    - `GET /posts/{id}` devuelve el post solicitado.  
    - `POST /posts` simula la creación de un post y valida el cuerpo de respuesta. [web:132][web:134]

- `test_posts_lifecycle_api.py`  
  - Demuestra un **ciclo completo** (encadenamiento de peticiones) sobre `/posts`:
    1. `POST /posts` → crear un post.
    2. `GET /posts/{id}` → intentar obtener el post creado.
    3. `PATCH /posts/{id}` → actualizar parcialmente el título.
    4. `GET /posts/{id}` → intentar verificar la actualización.
    5. `DELETE /posts/{id}` → borrar el post.
    6. `GET /posts/{id}` → comprobar el comportamiento después del borrado.

  - JSONPlaceholder es una API **fake** de prueba: simula operaciones y no siempre refleja los cambios como lo haría un backend real.  
    Por eso los asserts aceptan códigos como `200` o `404` en algunos `GET`, y se explica en los comentarios del test. [web:132][web:134]

- `test_users_api.py`  
  - Valida `/users`:
    - `GET /users` devuelve una lista de usuarios.  
    - Cada elemento contiene al menos `id`, `name` y `email`. [web:132]

### Carpeta `utils/`

- `logger.py`  
  - Configura un logger central para el proyecto.  
  - Escribe en:
    - Consola.
    - Archivo `logs/api_tests.log`.  
  - Formato del log: fecha/hora, nivel, nombre del logger y mensaje. [web:129]

### archivo `conftest.py`

- Define fixtures de pytest:

  - `posts_client()` → instancia de `PostsClient`, reutilizada en todos los tests de posts.  
  - `users_client()` → instancia de `UsersClient`, reutilizada en todos los tests de users.

- `scope="session"`: las instancias se crean una sola vez por ejecución de pytest. [web:133][web:135]

### archivo `pytest.ini`

- Configura:

  - `testpaths = tests` → pytest busca tests en la carpeta `tests`.  
  - `python_files = test_*.py` → solo considera archivos que empiezan con `test_`.  
  - `addopts = -v --tb=short` → salida más detallada y tracebacks cortos.  
  - markers:
    - `api`, `smoke`, `regression`, `critical`.

Esto sigue las buenas prácticas recomendadas para proyectos de API testing con pytest. [web:120][web:131]

---

## 4. Instalación y configuración

### 4.1. Clonar o copiar el proyecto

Descargar o copiar la estructura del proyecto en una carpeta local, por ejemplo:

```text
~/proyecto-final-automation-testing-[nombre-apellido]/
```

### 4.2. Crear y activar entorno virtual (opcional pero recomendado)

En Linux/Mac:

```bash
python -m venv venv
source venv/bin/activate
```

En Windows (PowerShell):

```bash
python -m venv venv
venv\Scripts\activate
```

### 4.3. Instalar dependencias

Desde la raíz del proyecto:

```bash
pip freeze > requirements.txt
---

pip freeze > requirements.txt crea un archivo requirements.txt con la lista de paquetes instalados en tu entorno actual, junto con sus versiones.

Qué hace exactamente   pip freeze muestra las dependencias instaladas en formato compatible con requirements.txt.
Importante
pip freeze no adivina cuáles librerías usa tu proyecto; solo muestra todo lo que está instalado en ese entorno. Por eso conviene usarlo dentro de un entorno virtual limpio, así el archivo no queda lleno de paquetes que no necesitás.

Resumen corto
pip freeze = lista dependencias instaladas.


requirements.txt = archivo para reproducir el entorno.


> redirige esa salida a un archivo llamado requirements.txt, en vez de mostrarla en pantalla.

Ojo con esto
pip freeze lista lo que está instalado en el entorno, no solo lo que tu proyecto usa directamente. Por eso conviene hacerlo dentro de un entorno virtual limpio



Esto instala `pytest`, `requests` y `pytest-html`. 

---

## 5. Cómo ejecutar las pruebas

### 5.1. Ejecutar todos los tests de API

```bash
pytest -m api -v
```

- `-m api` → ejecuta solo los tests marcados con `@pytest.mark.api`.  
- `-v` → muestra el nombre de cada test (modo “verbose”).

### 5.2. Ejecutar tests específicos

Solo los tests de `/posts` básicos:

```bash
pytest tests/api/test_posts_basic_api.py -v
```

Solo el test de ciclo completo:

```bash
pytest tests/api/test_posts_lifecycle_api.py -v
```

Solo los tests de `/users`:

```bash
pytest tests/api/test_users_api.py -v
```

### 5.3. Generar reporte HTML

```bash
pytest -m api -v --html=reports/api_report.html --self-contained-html
```

- Crea un archivo `reports/api_report.html` con el detalle de la ejecución.  
- La opción `--self-contained-html` hace que el reporte sea un archivo único, fácil de compartir.

---

## 6. Diseño y buenas prácticas aplicadas

### 6.1. Arquitectura tipo POM para API

En lugar de tener llamadas HTTP sueltas en cada test, se utiliza una capa de **API Clients**:

- `BaseAPIClient` concentra:
  - URL base de la API.
  - Construcción de URLs.
  - Manejo de la sesión Requests.
  - Logging uniforme de requests y responses.

- `PostsClient`, `UsersClient` representan “objetos” de la API:  
  cada método refleja una acción de negocio (obtener posts, crear, actualizar, etc.).

Esto hace que los tests sean más legibles y fáciles de mantener.

### 6.2. Fixtures reutilizables

Las fixtures de `conftest.py`:

- Evitan repetir la creación de clients en cada archivo de test.  
- Se integran con la filosofía de pytest de escribir tests claros, cortos y con poco setup explícito. 

### 6.3. Logging

El logging está centralizado en `utils/logger.py` y aplicado en `BaseAPIClient`:

- Cada request se registra con método, URL y parámetros.  
- Cada response se registra con status code, URL y cuerpo (JSON o texto).

Esto ayuda a:

- Entender qué pasó cuando un test falla.  
- Usar el log como evidencia en la entrega del proyecto.

### 6.4. Manejo de la naturaleza “fake” de JSONPlaceholder

JSONPlaceholder es una API de prueba que **no persiste datos de manera real**:

- Un `POST` simula crear un recurso y devuelve un objeto con `id`, pero ese recurso puede no estar realmente disponible en futuras consultas `GET`.  

En los tests de ciclo completo:

- Se documenta este comportamiento en los comentarios.  
- Se permiten códigos como `200` o `404` en algunos `GET` posteriores, explicando que en una API real esperaríamos `404` después del borrado.

---

## 7. Posibles mejoras futuras

Algunas ideas para extender el framework:

- Añadir más recursos de JSONPlaceholder (por ejemplo `/comments`, `/albums`).  
- Leer la URL base desde una variable de entorno o archivo de configuración.  
- Integrar herramientas de coverage o CI (GitHub Actions, GitLab CI).  
- Añadir tests negativos (por ejemplo, usar IDs inexistentes y validar códigos de error). 

---

## 8. Autor

- Alumno/a: **[Tu nombre y apellido]**  
- Curso: Testing QA – Proyecto Final  
- Plataforma de práctica: JSONPlaceholder (API pública de prueba). [
  