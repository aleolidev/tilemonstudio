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

from typing import List, Dict, Set, FrozenSet, Tuple
import random
import heapq as hq
from functools import reduce
from more_itertools import peekable


from params import LIMIT, MAX_DEPTH, OPTION, NUM_TILES



# class MinHeap(list):
#     def __init__(self, key=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if key is None:
#             self.key = lambda x: x
#         else:
#             self.key = key

#     def append(self, item):
#         if None in self:  # buscar el primer lugar desocupado, de haberlo. así se mantiene balanceado!
#             index = self.index(None)
#             self[index] = item
#         else:
#             super().append(item)
#             index = len(self) - 1
#         while self.key(self[index]) < self.key(self[index // 2]):
#             self[index], self[index // 2] = self[index // 2], self[index]
#             index = index // 2
#         print(self)
    
#     def pop(self, index):
#         item = self[index]
#         self[index] = None
#         while index * 2 + 1 < len(self):
#             print("comparando", self[index * 2 + 1], self[index * 2 + 2])
#             if self.key(self[index * 2 + 1]) <= self.key(self[index * 2 + 2]):
#                 self[index] = self[index * 2 + 1]
#                 index = index * 2 + 1
#                 self[index * 2 + 1] = None
#             else:
#                 self[index] = self[index * 2 + 2]
#                 index = index * 2 + 2
#                 self[index * 2 + 2] = None
#         return item



# a = MinHeap()
# print(a)
# a.append(1)
# a.append(2)
# a.append(4)
# a.append(3)
# print(a.pop(0))

# exit()


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



"""

    un camino es el conjunto de paletas que voy a seleccionar
    puedo llevar registro también de qué tiles ya tengo, así no lo recalculo constantemente

    1. los nodos no pueden tener un padre, tengo que guardar los caminos de otra forma.


    sí o sí, con n tiles, el camino más largo puede ser de largo n, pero esa restricción está
    implícita al descartar nodos que no te sirve mirar


    duda: voy a revisar en amplitud o en profundidad?
    lo suyo sería amplitud, quiero el clique más pequeño

    g = largo camino (todas las aristas pesan 1)
    h = el nodo más grande

    f = g +' h

    mira, si ya pasé por un nodo con un camino, puedo volver a pasar por él tomando otro camino,
    aunque el padre directo sea el mismo


    cuando inicio, tengo UN nodo en mi frontera (n0)
    voy a armar todos los caminos posibles y voy a guardar los caminos de c/u

    luego, para cada camino le calculo su frontera y expando


    var caminos_actual: list[list[tuple[int]]]  # camino = lista de nodos (nodos := tupla de ints (tiles ids))
    var caminos_proxim: list[list[tuple[int]]]  # lo mismo de arriba

    while len(caminos_actual) > 0:
        caminos_proxim = []
        for camino in caminos_actual:
            

    var caminos_actual: list[dict[tuple[int], set[tuple[int]]]]
    # guardo los que me quedan por ver


    {
        cam_1: nodos que ya he revisado al 100%
        cam_1 + un nodo: nodos que ya he revisado al 100%
        etc
    }
"""

def calcular_acumulados(camino):
    tengo = reduce(lambda x, y: x.union(y), camino, set())
    return tengo


def calcular_restantes(camino, espacio_total):
    tengo = calcular_acumulados(camino)
    return espacio_total.difference(tengo)


def node_bin_packing_solver(grafo: dict, nodo_inicio: Tuple[int], espacio_total: Set[int], return_first=False, use_max_depth=False, max_depth=MAX_DEPTH):
    caminos_actual = [[nodo_inicio]]
    soluciones = []
    largo = 0
    print(nodo_inicio)
    # encuentro una solución cuando no tengo frontera que expandir
    while len(caminos_actual) > 0 and len(soluciones) == 0:
        print("Estamos en largo...", largo)
        print("Espacio de búsqueda:", len(caminos_actual))
        caminos_proxim = []
        for camino in caminos_actual:
            if len(calcular_restantes(camino, espacio_total)) == 0:  # HAY SOLUCIÓN!
                if return_first:
                    return camino.copy(), largo
                else:
                    soluciones.append(camino.copy())
                    continue
            tengo = calcular_acumulados(camino)
            nodo_actual = camino[-1]
            for vecino in grafo[nodo_actual]["vecinos"]:
                if len(tengo.intersection(vecino)) == 0:  # si no hay "objetos" comunes entre mis acumulados y el propio vecino
                    caminos_proxim.append(camino + [vecino])
        caminos_actual = caminos_proxim
        largo += 1
    return soluciones, largo


def node_bin_packing_solver_aestrella_ish(grafo, nodo_inicio, espacio_total, return_first=False, use_max_depth=False, max_depth=MAX_DEPTH):
    soluciones = []
    mejor_largo = None
    
    
    camino_actual = [nodo_inicio]
    largo_actual = len(camino_actual)
    abiertos_no_explorados = list(filter(
        lambda x: len(calcular_acumulados(camino_actual).intersection(x)) == 0,
        grafo[nodo_inicio]["vecinos"]
    ))
    caminos_open = hq.heapify([
        (largo_actual, len(calcular_restantes(camino_actual, espacio_total)), camino_actual, abiertos_no_explorados)
    ])  # minheap de tuplas (largo, restantes, camino, abiertos-no-explorados)
    
    while len(caminos_open) > 0:
        largo_actual, restantes, caminos_open, abiertos_no_explorados = hq.heappop(caminos_open)
        
    
    
    # while True:  # FIXME
    #     # nodo_actual = camino_actual[-1]
    #     pass
        # vecinos_filtrados = filter(lambda x: len(tengo_actual.intersection(set)) == 0, grafo[nodo_actual]["vecinos"])
        # debería meter el primer vecino en el camino actual
        # y luego meter todos los demás en el heap de los open...  OPTION = 1
        # o debería meterlos todos en el heap del open y sacar mi camino actual
        # del tope del heap?...  OPTION = 2
        # if OPTION == 1:
        #     primer_vecino = next(vecinos_filtrados)
        #     for vecino in vecinos_filtrados:
                
            
            
        #     camino_actual.append(primer_vecino)
            
        #     pass
        # elif OPTION == 2:
        for vecino in vecinos_filtrados:
            largo_camino = len(camino_actual) + 1
            
        
        # actualizar camino actual!
            
    


def sacar_vecinos_filtrados(grafo, camino):
    tengo = calcular_acumulados(camino)
    return filter(lambda x: len(tengo.intersection(x)) == 0, grafo[camino[-1]]["vecinos"])



def node_bin_packing_solver_dfs(grafo, nodo_inicio, espacio_total, caminos_vistos: set=set(), return_first=False, keep_one=True, use_max_depth=False, max_depth=MAX_DEPTH):
    soluciones = []
    mejor_largo = None
    largo_objetivo = None
    

    # STACK de tuplas (largo, camino, abiertos-no-explorados)
    caminos_open = [(1, [nodo_inicio], sacar_vecinos_filtrados(grafo, [nodo_inicio]))]
    
    while len(caminos_open) > 0:
        """
            Aquí voy a continuar con el último que miré.
        """
        
        largo, camino, abiertos_no_explorados = caminos_open[-1]  # .pop()
        try:
            prox_nodo = next(abiertos_no_explorados)
        except StopIteration:
            # vacié esta ruta y tengo que volver!
            caminos_open.pop()
            continue
        # if len(abiertos_no_explorados) == 0:
        #     # vacié esta ruta y tengo que volver!
        #     caminos_open.pop()
        #     continue
        if largo_objetivo is not None and largo >= largo_objetivo:
            # me pasé del target
            caminos_open.pop()
            continue
        elif mejor_largo is not None and largo >= mejor_largo:
            # ya estoy pasado del largo óptimo que encontré antes
            caminos_open.pop()
            continue
        
        camino_nuevo = camino + [prox_nodo]  # Expando el camino en un nodo
        fs_camino_nuevo = frozenset(camino_nuevo)
        if fs_camino_nuevo in caminos_vistos:
            # este ya lo vi, no lo quiero, está viejo.
            continue
        caminos_vistos.add(fs_camino_nuevo)
        vecinos_filtrados = sacar_vecinos_filtrados(grafo, camino_nuevo)  # Filtro las posibles expansiones futuras
        
        if peekable(vecinos_filtrados):
            # Si no me puedo expandir eso quiere decir que ya tengo todos los nodos
            if return_first:
                # OJO! no es el mejor
                return [camino_nuevo], largo + 1
            
            # print("Encontré camino:", camino_nuevo)
            
            if mejor_largo is None:
                mejor_largo = largo + 1
                soluciones.append(camino_nuevo.copy())
                print("MEJOR LARGO:", mejor_largo)
            
            elif mejor_largo > largo + 1:
                mejor_largo = largo + 1
                soluciones = [camino_nuevo.copy()]
                print("ACTUALIZAMOS MEJOR LARGO:", mejor_largo)
            
            elif mejor_largo == largo + 1:
                soluciones.append(camino_nuevo.copy())
                
            else:  # mejor_largo es mejor que el actual
                continue
            largo_objetivo = largo
            print("Largo objetivo:", largo_objetivo)

        else:
            if mejor_largo is not None and largo + 1 >= mejor_largo:  # PODA!
                """
                    Poda: quito los que tendrán el mismo o mayor largo que el mejor hasta ahora porque
                            los con igual largo, al sacarlos, este automáticamente aumentará en uno, así
                            que no tiene mucho sentido dejarlos como candidatos.
                """
                # caminos_open.pop()
                continue
            caminos_open.append((largo + 1, camino_nuevo, vecinos_filtrados))
    return soluciones, mejor_largo

















# def buscar_menor_clique(grafo, nodo, totales):
#     vistos = grafo[nodo]["vecinos"].copy()
#     l_open = [nodo]
#     s_closed = set()
#     while vistos != totales:
#         pass
#     pass
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
    for _ in range(NUM_TILES):
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
    for nodo, data in grafo.items():
        data["vecinos"].sort(key=lambda x: len(x), reverse=True)
    
    print("Num nodos:", num_nodos)
    print("Num aristas:", cont_aristas)
    nodos_por_tamaño = sorted(grafo.keys(), key=lambda x: len(x), reverse=True)
    # print(nodos_por_tamaño[0], nodos_por_tamaño[-1])
    # print(grafo[nodos_por_tamaño[0]])
    # exit()
    for nodo in nodos_por_tamaño:
        grafo[nodo]["vecinos"].sort(key=lambda x: len(x), reverse=True)  # me ordena los vecinos para primero mirar los más grandes
    
    print("EMPEZAMOS LA BÚSQUEDA!")
    caminos_vistos = set()
    # print(set(range(len(tiles))))
    nodo = nodos_por_tamaño[0]
    caminos, largo = node_bin_packing_solver_dfs(grafo, nodo, set(range(len(tiles))), caminos_vistos, return_first=False)
    print(caminos)
    print(largo)
    print(len(caminos_vistos))
    
    
    
    
    exit()
    
    
    
    
    sols = []
    mejor_largo = None
    for nodo in nodos_por_tamaño:
        caminos, largo = node_bin_packing_solver(grafo, nodo, set(range(len(tiles))), return_first=True)
        if mejor_largo is None:
            mejor_largo = largo
            sols.append(camino)
            print("LARGO ES:", mejor_largo)
        elif mejor_largo == largo:
            sols.append(camino)
        elif mejor_largo > largo:
            mejor_largo = largo
            sols = [camino]
            print("MEJOR LARGO BAJA A:", mejor_largo)
    
    for sol in sols:
        print("N0:", sol[0])
        print("Paletas:", sol)
        print()
    
    # heurística: irme al nodo con más colores que me falten!
    
    # res = busqueda_generica(tiles, nodos_por_tamaño, grafo)
    # print(res)

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
