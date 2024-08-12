from math import sqrt
from data_loader.models import *

def get_graph():
    ubicaciones = {ubicacion.nombre: (ubicacion.posX, ubicacion.posY) for ubicacion in Ubicacion.objects.all()}
    conexiones = Conexion.objects.all()
    
    graph = {loc: {} for loc in ubicaciones}
    
    for conexion in conexiones:
        ubicacion1 = conexion.ubicacion1.nombre
        ubicacion2 = conexion.ubicacion2.nombre
        peso = conexion.peso
        
        graph[ubicacion1][ubicacion2] = peso
        graph[ubicacion2][ubicacion1] = peso
        
    return graph

def dijkstra(graph, start, end):
    distancias = {nodo: float('infinity') for nodo in graph}
    nodo_anterior = {nodo: None for nodo in graph}
    distancias[start] = 0
    nodos = list(graph.keys())
    
    while nodos:
        nodo_actual = min(nodos, key=lambda nodo: distancias[nodo])
        nodos.remove(nodo_actual)
        
        if distancias[nodo_actual] == float('infinity'):
            break
        
        for vecino, peso in graph[nodo_actual].items():
            ruta_alternativa = distancias[nodo_actual] + peso
            if ruta_alternativa < distancias[vecino]:
                distancias[vecino] = ruta_alternativa
                nodo_anterior[vecino] = nodo_actual
                
        if nodo_actual == end:
            break
        
    ruta, nodo_actual = [], end
    while nodo_anterior[nodo_actual] is not None:
        ruta.insert(0, nodo_actual)
        nodo_actual = nodo_anterior[nodo_actual]
    if ruta:
        ruta.insert(0, nodo_actual)
        
    return ruta, distancias[end]