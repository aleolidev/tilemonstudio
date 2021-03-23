# grupo_stack = []

# usadas_grupo_stack = []  # closed
# stack = []  # sol parcial
# próximos = []  # open
# print("SALTOS EN WHILE: ", saltos, "| PIVOTE:", pivote)
# ## el default!!
# saltos[pivote - 1] += 1
# saltos[pivote] = saltos[pivote - 1] + 1
# if pivote == 0 and saltos[pivote] == len(elementos) - k:
#     # TERMINAMOS!
#     # raise StopIteration()
#     break
# elif pivote == 0 and saltos[pivote] == saltos[pivote + 1] - 1:
#     saltos[pivote] += 1
#     saltos[pivote + 1] += saltos[pivote] + 1
#     pivote += 1

#--------------------------------------------------------------------

import random


LIMIT = 16  # máx colores + 1


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


def encontrar_min_combinacion(paletas_candidatas):
    for k in range(1, len(paletas_candidatas) + 1):
        for gen_comb in combs_k_elementos(paletas_candidatas, k):
            comb_paletas = list(gen_comb)
            sirve = comprobar_paletas(comb_paletas, paletas)
            if sirve:
                return comb_paletas


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


def encontrar_nodos_faltantes(grafo: dict, nodo: tuple, totales: set) -> set:
    na = nodo
    vistos = set(na)
    while grafo[na]["padre"] is not None:
        vistos.update(grafo[na]["padre"])
        na = grafo[na]["padre"]
    return totales.difference(vistos)


def construir_camino(grafo: dict, nodo: tuple) -> list:
    camino = [nodo]
    na = nodo
    while grafo[na]["padre"] is not None:
        camino.append(grafo[na]["padre"])
        na = grafo[na]["padre"]
    return camino


# def mezcla(grafo, cola_open, set_closed, nodo):
#     for v in set(grafo[nodo]["vecinos"]).difference(cola_open).difference(set_closed):
#         cola_open.append(v)


# def busqueda_generica(tiles, nodos_por_tamaño, grafo):
#     ## IMPORTANTE, PARA NO REPETIR TODO EL RATO
#     total_colores = set([i for i in range(len(tiles))])
#     nodo_actual = nodos_por_tamaño[1]
#     cola_closed = set()
#     cola_open = list([nodo_actual])
#     print("nodo_actual", nodo_actual)
#     sol_optima = None
#     sol_actual = None
#     while len(cola_open) > 0:
#         u = cola_open.pop(0)
#         cola_closed.update([u])
#         for v in set(grafo[u]["vecinos"]).difference(cola_open).difference(cola_closed):
#             print("Viendo vecino:", v)
#             if len(encontrar_nodos_faltantes(grafo, v, total_colores).intersection(v)):
#                 # no tengo que crear una arista, sino continuar
#                 continue
#             # if grafo[v]["padre"] is not None:
#             #     pass  # tengo que ver cuál es mejor
#             # else:
#             print("Haciendo padre!")
#             grafo[v]["padre"] = u
#             if encontrar_nodos_faltantes(grafo, v, total_colores) == total_colores:
#                 return v
#         mezcla(grafo, cola_open, cola_closed, u)
#         print("nueva open:", cola_open)


def buscar_menor_clique(grafo, nodo, totales):
    vistos = grafo[nodo]["vecinos"].copy()
    l_open = [nodo]
    s_closed = set()
    while vistos != totales:
        pass
    pass
"""
# básicamente, lo que tengo que aprovechar es que el árbol de búsqueda se achica con cada nodo que agrego


un nodo = saco al primero de la open
me paro en un nodo
filtro a los vecinos que me interesan (acumulado inter vecino == vacío)
agrego a los que me quedan a la open



"""

if __name__ == "__main__":
    # def generar_paletas(num_tiles, max_colore)
    paletas = set()
    for _ in range(20):
        generado = [random.randint(0, 32) for _ in range(random.randint(1, 16))]
        generado = tuple(set(generado))
        paletas.add(generado)

    tiles = list(paletas)
    print("PALETAS TILES:", tiles)
    raw_combs = []
    for i in range(1, len(paletas) + 1):
        raw_combs.append(combs_k_elementos(list(paletas), i))
    combinaciones = []
    c = 0
    for row_k in raw_combs:
        for comb in row_k:
            c += 1
            if largo_paleta([tiles[i] for i in comb]) < LIMIT:
                # print(comb)
                combinaciones.append(comb)
    ## ---- integridad
    s = []
    for i in combinaciones:
        s += i
    print("ESTÁN TODOS LOS TILES: ", len(set(s)) == len(paletas))
    ## ---- fin integridad
    ## NUEVA ETAPA: grafo.
    grafo, num_nodos, cont_aristas = construir_grafo(combinaciones)
    print("Num nodos:", num_nodos)
    print("Num aristas:", cont_aristas)
    nodos_por_tamaño = sorted(grafo.keys(), key=lambda x: len(x), reverse=True)
    # heurística: irme al nodo con más colores que me falten!
    
    res = busqueda_generica(tiles, nodos_por_tamaño, grafo)
    print(res)

    # for nodo_final in busqueda_generica(tiles, nodos_por_tamaño, grafo):
    #     print(construir_camino(grafo, nodo_final))
    #     input()
        # if encontrar_nodos_faltantes(grafo, nodo_actual, total_colores) == total_colores:
        #     # ENCONTRÉ SOLUCIÓN! :D
        #     solucion_actual = construir_camino(grafo, nodo_actual)
        #     if sol_optima is None or len(solucion_actual) < len(sol_optima):
        #         sol_optima = sol_actual
        #     break
        # prox_prox = set()
        # for nodo_actual in proxima:
        #     for nodo in nodo_actual["vecinos"]:
        #         if nodo in vistos:
        #             continue
        #         if len(encontrar_nodos_faltantes(grafo, nodo_actual, total_colores).intersection(nodo)) != 0:
        #             grafo[nodo]["padre"] = nodo_actual
        #             vistos.update([nodo])
        #             continue
        #         else:
        #             prox_prox.update([nodo])
        # proxima = prox_prox
        







# paletas_candidatas = []
# for comb in combinaciones:
#     s = set()
#     for p in comb:
#         s.update(p)
#     paletas_candidatas.append(s)
# y ahora quiero el menor conjunto de paletas tal que todos los tiles puedan ser dibujados
# print("SIRVE:", comprobar_paletas([(1, 2, 3, 4, 5)], {(1, 2), (2, 3), (4, 5)}))
# print("RES:", encontrar_min_combinacion(paletas_candidatas))
