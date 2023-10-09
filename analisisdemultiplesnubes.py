import numpy as np
import open3d as o3d
import os  

def cargar_ply(nombre_archivo):
    pcd = o3d.io.read_point_cloud(nombre_archivo)
    return pcd

def eliminar_outliers(pcd, nb_neighbors=1002, std_ratio=0.9):
    pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    return pcd

def procesar_ply(nombre_archivo):
    pcd = cargar_ply(nombre_archivo)
    pcd = eliminar_outliers(pcd)

    superficie_fija = 0.95 # Unidades 
    puntos = np.asarray(pcd.points)
    idx_punto_mas_profundo = np.argmin(puntos[:, 2])
    superficie_estimada = np.median(puntos[:, 2])  
    
    print(f"\nArchivo: {nombre_archivo}")
    print(f"Superficie estimada: {superficie_estimada:.4f} unidades")
    
    profundidad_agujero = puntos[idx_punto_mas_profundo, 2] + superficie_fija
    
    print(f"Profundidad del agujero desde la superficie fija: {profundidad_agujero:.4f} unidades")
    print(f"Valor mínimo de Z: {np.min(puntos[:, 2]):.4f}, Valor máximo de Z: {np.max(puntos[:,2]):.4f}")
    
    # Retornar los resultados como un diccionario
    return {
        "archivo": nombre_archivo,
        "superficie_estimada": superficie_estimada,
        "profundidad_agujero": profundidad_agujero
    }

if __name__ == "__main__":
    carpeta_ply = "95cm bag"
    archivos_ply = [f for f in os.listdir(carpeta_ply) if f.endswith('.ply')]
    
    # Lista para almacenar los resultados
    resultados = []

    #outlier

    
    for archivo in archivos_ply:
        ruta_completa = os.path.join(carpeta_ply, archivo)
        resultado = procesar_ply(ruta_completa)
        resultados.append(resultado)
    
    # Imprimir todos los resultados al final
    print("\nResumen de resultados:")
    for res in resultados:
        print(f"\nArchivo: {res['archivo']}")
        print(f"Superficie estimada: {res['superficie_estimada']:.4f} unidades")
        print(f"Profundidad del agujero desde la superficie fija: {res['profundidad_agujero']:.4f} unidades")
