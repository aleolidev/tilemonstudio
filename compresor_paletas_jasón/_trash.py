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


def calcular_restantes(camino, espacio_total):
    tengo = calcular_acumulados(camino)
    return espacio_total.difference(tengo)

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
def construir_camino(grafo: dict, nodo: tuple) -> list:
    camino = [nodo]
    na = nodo
    while grafo[na]["padre"] is not None:
        camino.append(grafo[na]["padre"])
        na = grafo[na]["padre"]
    return camino


def encontrar_nodos_faltantes(grafo: dict, nodo: tuple, totales: set) -> set:
    na = nodo
    vistos = set(na)
    while grafo[na]["padre"] is not None:
        vistos.update(grafo[na]["padre"])
        na = grafo[na]["padre"]
    return totales.difference(vistos)
def encontrar_min_combinacion(paletas_candidatas):
    for k in range(1, len(paletas_candidatas) + 1):
        for gen_comb in combs_k_elementos(paletas_candidatas, k):
            comb_paletas = list(gen_comb)
            sirve = comprobar_paletas(comb_paletas, paletas)
            if sirve:
                return comb_paletas


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