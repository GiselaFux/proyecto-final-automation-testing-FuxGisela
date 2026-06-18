import logging               # importa el módulo logging de Python
import os                    # importa el módulo para trabajar con rutas y carpetas

# Carpeta logs/ en la raíz del proyecto
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
#   os.path.dirname(__file__) → ruta de este archivo (utils/logger.py)
#   os.path.dirname(...) de nuevo → va arriba (utils → raíz del proyecto)
#   os.path.join(..., "logs") → añade "logs" al final
os.makedirs(LOGS_DIR, exist_ok=True)  
#   crea la carpeta logs/ si no existe; exist_ok=True = no error si ya existe

LOG_FILE = os.path.join(LOGS_DIR, "api_tests.log")
#   ruta completa del archivo de log: logs/api_tests.log


def get_logger(name: str) -> logging.Logger:
    # Función que devuelve un logger ya configurado.
    # name: usualmente __name__ del módulo que lo usa (ej. "test_usuario")

    logger = logging.getLogger(name)
    #   crea o recupera un Logger con ese nombre.
    #   Loggers se comparten por nombre entre todo el programa.

    if logger.handlers:
        return logger
    #   si este logger YA tiene handlers, no los añade de nuevo.
    #   evita que el mismo mensaje se imprima varias veces.

    logger.setLevel(logging.DEBUG)
    #   el logger acepta TODOS los mensajes desde DEBUG hasta ERROR.
    #   si fuera INFO, los DEBUG se descartan antes de llegar a los handlers.

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    #   define cómo se escribe cada línea de log:
    #   - asctime: fecha y hora
    #   - levelname: INFO, ERROR, DEBUG, etc.
    #   - name: nombre del logger (el que pasaste a get_logger)
    #   - message: el texto que escribiste (logger.info("xxx"))

    # ===== HANDLER: archivo (solo INFO y superiores) =====
    file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    #   FileHandler: escribe en un archivo.
    #   LOG_FILE: ruta del archivo (logs/api_tests.log)
    #   mode="a": append (añade al final, no sobrescribe)
    #   encoding="utf-8": permite tildes, caracteres especiales, JSON, etc.

    file_handler.setFormatter(formatter)
    #   le asigna el formato definido arriba.

    file_handler.setLevel(logging.INFO)
    #   este handler SOLO escribe INFO, WARNING, ERROR.
    #   DEBUG se filtra aquí y no va al archivo.

    # ===== HANDLER: consola (DEBUG y superiores) =====
    console_handler = logging.StreamHandler()
    #   StreamHandler: escribe en un stream.
    #   Por defecto usa sys.stderr (consola).

    console_handler.setFormatter(formatter)
    #   mismo formato que en el archivo.

    console_handler.setLevel(logging.DEBUG)
    #   este handler escribe DEBUG, INFO, WARNING, ERROR.
    #   aquí ves TODO en consola.

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    #   añade los dos handlers al logger.
    #   cuando el logger recibe un mensaje, lo pasa a ambos handlers.

    return logger