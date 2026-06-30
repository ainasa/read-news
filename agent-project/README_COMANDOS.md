# README_COMANDOS

Comandos basicos para ejecutar la extraccion de titulares y generar PDFs.

## 1) Una sola URL

Ejemplo:

```powershell
c:/agent-project/.venv/Scripts/python.exe -m app.main --url https://elpais.com/ --output output/titulares_elpais.pdf --max-headlines 20
```

Resultado:

- Genera un PDF con nombre dinamico por fecha.
- Lo guarda en `output/<dominio>/`.
- Ejemplo para hoy: `output/elpais/titulares_elpais_30Junio.pdf`.

## 2) Array de URLs

Ejemplo:

```powershell
c:/agent-project/.venv/Scripts/python.exe -m app.main --url '["https://okdiario.com","https://elpais.com/", "https://www.elespanol.com/", "https://www.20minutos.es/"]' --output output/titulares_elpais.pdf --max-headlines 20
```

Resultado:

- Procesa cada URL en la misma ejecucion.
- Crea carpeta por dominio si no existe (`okdiario`, `elpais`, `20minutos`).
- Genera un PDF por cada URL dentro de su carpeta.

## 3) Traducir titulares al castellano con --ES

URL unica:

```powershell
c:/agent-project/.venv/Scripts/python.exe -m app.main --url https://www.bbcearth.com --output output/titulares_elpais.pdf --max-headlines 20 --ES
```

Array de URLs:

```powershell
c:/agent-project/.venv/Scripts/python.exe -m app.main --url '["https://okdiario.com","https://elpais.com/","https://www.20minutos.es/"]' --output output/titulares_elpais.pdf --max-headlines 20 --ES
```

Resultado:

- Traduce al castellano los titulares extraidos antes de escribir cada PDF.
- Mantiene la misma estructura de salida por carpeta de dominio.

Nota:

- En PowerShell se recomienda envolver el array en comillas simples para que llegue correctamente como un solo argumento.
