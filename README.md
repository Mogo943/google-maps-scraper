# Google Maps Leads Scraper

Script en **python** diseñado para automatizar la extracción de prospectos comerciales (leads) desde **Google Maps** utilizando coordenadas geográficas precisas. Filtra automáticamente los resultados para identificar comercios que no poseen un sitio web corporativo o que únicamente utilizan **Instagram** como canal digital.

---

<p align="center">
  <p>Tecnologias</p>
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py" />
  </a>
</p>

## 🚀 Requisitos e Instalación

1. Asegurarse de tener instalado **python** (versión 3.8 o superior).
2. Clonar este repositorio en tu entorno local.
3. Instalar la librería de automatización **playwright** y sus binarios ejecutando los siguientes comandos en la terminal:

```bash
pip install playwright
playwright install chromium
```

---

## ⚙️ Configuración y Uso

El script utiliza geolocalización forzada mediante URL para escanear cuadrantes específicos sin depender del buscador global broad de Google.

1. Abrir el archivo del script (ej: `scraper.py`).
2. Modificar los parámetros de la función `scraping_localizado` al final del archivo:

*   **busqueda**: El nicho o rubro comercial a extraer (ej: `"padel"`, `"crossfit"`).
*   **lat**: Latitud exacta obtenida mediante clic derecho en Google Maps.
*   **lng**: Longitud exacta obtenida mediante clic derecho en Google Maps.
*   **zoom**: Escala de visualización del mapa (valor predeterminado: `15` para nivel barrio).

3. Ejecutar el script desde la terminal:

```bash
python scraper.py
```

---

## 📊 Formato de Salida

Al finalizar el proceso de scroll y filtrado, el script exporta un archivo estructurado denominado **leads_filtrados.csv** con las siguientes columnas optimizadas para preventa:

*   **Nombre**: Nombre comercial registrado en la ficha.
*   **Direccion**: Ubicación física del local.
*   **Telefono**: Número de contacto (extraído mediante identificadores internos limpios).
*   **Instagram**: URL del perfil de Instagram si se detecta en lugar de un sitio web tradicional.
*   **URL_Maps**: Enlace directo a la ficha del negocio para relevamiento visual de fotos.
