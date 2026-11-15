# Notas Docker - PulseBoard

## Nivel 1 - Fundamentos

### Desiciones

* **Imagen slim en lugar de completa**
  * Por qué: FastAPI y sus dependencias se instalan mediante paquetes precompilados, por lo que solo es necesario el interprete de Python, sin herramientas de compilación ni librerías de desarrollo.
  * Coste: si una dependencia futura necesita compilarse, se tendrá que instalar herramientas extra.

* **Tag flotante `python:3.14-slim-trixie` (versión menor + sistema operativo)**
  * Por qué: recibe parches de seguridad y corrección de errores en cada build sin necesidad de editar el Dockerfile, y fijar el sistema operativo evita saltos inesperados de distribución.
  * Coste: 2 builds en fechas distintas pueden producir imágenes distintas.

* **Instalar dependencias antes de copiar código**
  * Por qué: la caché de capas es secuencial; si una capa cambia, se reconstruyen todas las posteriores. El código cambia a menudo y las dependencias casi nunca, así que va después.
  * Resultado: al editar solo código, el `pip install` sale de la caché.

* **`fastapi run` en lugar de `fastapi dev`** 
  * Por qué: `dev` escucha en 127.0.0.1 y activa recarga automática. El mapeo de puertos entrega el tráfico a la interfaz de red del contenedor, no a su loopback, así que con `dev` el servidor sería inalcanzable desde fuera. `run` escucha en 0.0.0.0 por defecto y está pensado para ejecución normal.

### Comandos

* `docker build`: Construye una imagen Docker a partir de un Dockerfile.
* `docker run <imagen>`: Crea e inicia un contenedor a partir de una imagen concreta.
* `docker stop <contenedor>`: Detiene un contenedor actualmente en ejecución-
* `docker start <contenedor>`: Inicia un contenedor detenido.
* `docker ps -a`: Lista todos los contenedor, incluidos los detenidos.
* `docker logs -f <contenedor>`: Muestra la salida producida por un contenedor en vivo.
* `docker exec -it <contenedor> sh`: Abre una shell dentro de un contenedor en ejecución.
* `docker top <contenedor>`: Muestra los procesos del contenedor vistos desde el host.
* `docker inspect <nombre>`: Muestra información detallada y de bajo nivel sobre los objetos Docker.

### Experimentos y observaciones

* **PID 1**: El proceso del servidor figura como 1025 en el host (`docker top`). Dentro del contenedor, por el aislamiento del namespace de procesos, figura como 1 al ser FastAPI el primer proceso que arrancó dentro del contenedor.

* **Imagen vs. contenedor**: Al eliminar el contenedor la imagen sigue existiendo. La imagen es una plantilla de capas de solo lectura; cada contenedor añade su propia capa de escritura.

* **Efimeridad**: Se creó un archivo dentro de un contenedor que posteriormente fue eliminado. Al levantar un nuevo contenedor a partir de la misma imagen se pudo observar que el archivo ya no se encontraba presente. Los cambios viven en la capa de escritura del contenedor, sobreviven a stop/start, pero se pierden al eliminarlo. Un contenedor nuevo siempre parte de la imagen limpia.

### Errores y soluciones

* **`ps` no existe dentro del contenedor**
  * Causa: la imagen `slim` no incluye `procps`.
  * Solución: usar `docker top` desde el host o inspeccionar `/proc/1/cmdline`, sin instalar nada.