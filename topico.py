from bagpy import bagreader

# Nombre del archivo .bag
nombre_archivo_bag = "20230920_085112.bag"

# Abrir el archivo .bag
br = bagreader(nombre_archivo_bag)

# Obtener la lista de nombres de tópicos
topic_names = br.topics

# Mostrar los nombres de los tópicos
for name in topic_names:
    print(name)

br.close()