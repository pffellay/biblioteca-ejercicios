# Sincronización artefacto → página

La biblioteca se edita en el artefacto de Claude "Biblioteca de ejercicios"
(https://claude.ai/artifact/MPB7H7cXo3tZoTXp3aju7k). Esta página es una copia publicada.

Pasos para sincronizar:
1. Leer el artefacto (Artifact read) y guardar su HTML.
2. `python3 herramientas/sincronizar.py <html_del_artefacto>`
   - Reescribe index.html cambiando /_blob/<id> por imagenes/eNN.jpg o videos/eNN.mp4.
   - Lista en herramientas/pendientes.json los archivos nuevos que hay que descargar
     del artefacto (Artifact read con path=<id>) y guardar con ese nombre.
3. Videos: máximo 90 segundos y menos de 25 MB.
4. Commit y push a main. GitHub Pages actualiza la página en unos minutos.
