from PIL import Image # type: ignore
import os

def divir_guardar_imagen(ruta_imagen, carpeta_destino, division_por_columna):
    # cargar imagen
    with Image.open(ruta_imagen) as img:
        ancho, alto = img.size
    
    # calcular numero de divisiones
    tamano_cuadrado = ancho // division_por_columna
    division_por_fila = alto // tamano_cuadrado

    os.makedirs(carpeta_destino, exist_ok=True)

    # dividir y guardar
    contador = 0
    for i in range(division_por_fila):
        for j in range(division_por_columna):
            # calcular coordenadas
            izquierda = j * tamano_cuadrado
            superior = i * tamano_cuadrado
            derecha = izquierda + tamano_cuadrado
            inferior = superior + tamano_cuadrado

            # recortar y guardar
            cuadrado = img.crop((izquierda, superior, derecha, inferior))
            nombre_archivo = f"title ({contador + 1}).png"
            cuadrado.save(os.path.join(carpeta_destino, nombre_archivo))

divir_guardar_imagen("assets\\tiles\\mainlevbuild.png", "assets\\tiles", 62)