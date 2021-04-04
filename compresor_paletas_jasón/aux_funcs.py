from functools import reduce


def largo_paleta(paletas: list):
    p = set()
    for paleta in paletas:
        p = p.union(paleta)
    return len(p)


def comprobar_paletas(paletas, tiles):
    for tile in tiles:
        for paleta in paletas:
            if set(tile) == set(paleta).intersection(tile):
                break
        else:
            return False
    return True


def combs_k_elementos(elementos: list, k: int):
    if len(elementos) < k:
        raise Exception("No hay suficientes elementos en la lista.")
    saltos = [i for i in range(k)]
    while True:
        if saltos[-1] >= len(elementos):
            pivote = k - 1
            while pivote < k:  ## me muevo hacia la izquierda y después derecha!
                if pivote != 0 and saltos[pivote - 1] == saltos[pivote] - 1:
                    pivote -= 1
                else:
                    saltos[pivote - 1] += 1
                    saltos[pivote] = saltos[pivote - 1] + 1
                    pivote += 1
        if saltos[-1] >= len(elementos):
            break
        yield saltos.copy()
        # yield [elementos[i] for i in saltos]
        saltos[-1] += 1




def construir_grafo(combinaciones):
    grafo = {}
    for nodo in combinaciones:
        grafo[tuple(nodo)] = {
            "vecinos": [],
            "padre": None,
        }
    cont_aristas = 0
    for nodo in grafo.keys():
        for nodo_2 in grafo.keys():
            if nodo != nodo_2 and len(set(nodo).intersection(nodo_2)) == 0:
                grafo[nodo]["vecinos"].append(nodo_2)
                grafo[nodo_2]["vecinos"].append(nodo)
                cont_aristas += 1
    return grafo, len(combinaciones), cont_aristas


def es_solucion(sol_actual, k):
    """ 
        sol_actual: lista de tuplas (c/u es un nodo)
        k: número total de tiles
    """
    u = set()
    for nod in sol_actual:
        u.update(nod)
    return len(u) == k


def actualizar_caminos_vistos(caminos_vistos, mejor_largo):
    return set(filter(lambda x: len(x) < mejor_largo, caminos_vistos))


def calcular_acumulados(camino):
    tengo = reduce(lambda x, y: x.union(y), camino, set())
    return tengo

def sacar_vecinos_filtrados(grafo, camino):
    tengo = calcular_acumulados(camino)
    return (filter(lambda x: len(tengo.intersection(x)) == 0, grafo[camino[-1]]["vecinos"]))




