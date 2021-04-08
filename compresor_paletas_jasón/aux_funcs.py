from functools import reduce

from params import LIMIT


def es_mochila_valida(mochila):
    """
        Entra una mochila cruda, sólo su contenido.
    """
    return len(reduce(lambda x, y: x.union(y), mochila, set())) < LIMIT



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
            while pivote < k:  # me muevo hacia la izquierda y después derecha!
                if pivote != 0 and saltos[pivote - 1] == saltos[pivote] - 1:
                    pivote -= 1
                else:
                    saltos[pivote - 1] += 1
                    saltos[pivote] = saltos[pivote - 1] + 1
                    pivote += 1
        if saltos[-1] >= len(elementos):
            break
        yield saltos.copy()
        saltos[-1] += 1


def construir_grafo(combinaciones):
    grafo: list = [{"contenido": tuple(sorted(nodo)), "vecinos": []} for nodo in combinaciones]
    grafo.sort(key=lambda x: len((x["contenido"])), reverse=True)  # ordenamos los nodos de más grandes a más pequeños
    n_aristas = 0
    for i in range(len(grafo)):
        for k in range(i+1, len(grafo)):
            n1 = grafo[i]
            n2 = grafo[k]
            if len(set(n1["contenido"]).intersection(n2["contenido"])) == 0:
                n1["vecinos"].append(k)
                n2["vecinos"].append(i)
                n_aristas = n_aristas + 1
    return grafo, len(grafo), n_aristas


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


def calcular_acumulados(grafo, camino):
    tengo = reduce(lambda x, y: x.union(grafo[y]["contenido"]), camino, set())
    return tengo


def sacar_vecinos_filtrados(grafo, camino):
    tengo = calcular_acumulados(grafo, camino)
    query = filter(lambda x: len(tengo.intersection(grafo[x]["contenido"])) == 0, grafo[camino[-1]]["vecinos"])
    return list(query)




