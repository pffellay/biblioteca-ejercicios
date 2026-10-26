#!/usr/bin/env python3
"""Convierte el HTML del artefacto "Biblioteca de ejercicios" en el index.html de esta página.

Uso:  python3 herramientas/sincronizar.py <artefacto.html> [carpeta_repo]

- Reemplaza cada /_blob/<id> por su archivo local (imagenes/eNN.jpg o videos/eNN.mp4)
  según herramientas/mapa_archivos.json.
- Si encuentra archivos nuevos (blobs que no están en el mapa), les asigna nombre según
  el número de ejercicio, los agrega al mapa y los lista en herramientas/pendientes.json
  para descargarlos del artefacto (Artifact read con path=<id>).
- Imprime un resumen en JSON.
"""
import json, re, sys, os

PREFIJO = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
           '<style>html,body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
           '</head>\n<body>\n')
SUFIJO = '\n</body>\n</html>\n'

def main():
    src = sys.argv[1]
    repo = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mapa_p = os.path.join(repo, 'herramientas', 'mapa_archivos.json')
    mapa = json.load(open(mapa_p))
    html = open(src, encoding='utf-8').read()
    # Si viene como documento completo, quedarse con el contenido del body
    m = re.search(r'<body[^>]*>(.*)</body>', html, re.S)
    if m and '<title>' not in html[:html.find('<body')]:
        html = m.group(1)
    html = html.strip()

    usados = set(mapa.values())
    pendientes = {}
    def nombre_nuevo(pos, es_video):
        prev = html[:pos]
        nums = re.findall(r'"n":\s*"(\d+)"', prev)
        n = nums[-1] if nums else 'xx'
        base = f"videos/e{n}.mp4" if es_video else f"imagenes/e{n}.jpg"
        cand, k = base, 2
        while cand in usados:
            cand = base.replace('.', f'-{k}.'); k += 1
        return cand

    def reemplazar(mm):
        blob = mm.group(0)
        if blob not in mapa:
            es_video = html[max(0, mm.start()-20):mm.start()].rstrip('\\"').endswith('data-video=')
            ruta = nombre_nuevo(mm.start(), es_video)
            mapa[blob] = ruta; usados.add(ruta); pendientes[blob.split('/')[-1]] = ruta
        return mapa[blob]

    salida = re.sub(r'/_blob/[0-9a-f]{32}', reemplazar, html)
    nuevo = PREFIJO + salida + SUFIJO
    idx = os.path.join(repo, 'index.html')
    viejo = open(idx, encoding='utf-8').read() if os.path.exists(idx) else ''
    cambio = viejo != nuevo
    if cambio:
        open(idx, 'w', encoding='utf-8').write(nuevo)
    json.dump(mapa, open(mapa_p, 'w'), indent=0, sort_keys=True)
    pend_p = os.path.join(repo, 'herramientas', 'pendientes.json')
    faltan = {b: r for b, r in mapa.items() if not os.path.exists(os.path.join(repo, r))}
    faltan = {b.split('/')[-1]: r for b, r in faltan.items()}
    faltan.update(pendientes)
    json.dump(faltan, open(pend_p, 'w'), indent=1)
    print(json.dumps({'index_cambio': cambio, 'archivos_a_descargar': faltan}, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
