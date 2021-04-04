import random

from more_itertools import peekable

from aux_funcs import (
    sacar_vecinos_filtrados, combs_k_elementos, largo_paleta, construir_grafo)
from params import (MAX_DEPTH, NUM_TILES, LIMIT)



def node_bin_packing_solver_dfs(grafo, nodo_inicio, espacio_total, caminos_vistos: set=set(), return_first=False, keep_one=True, use_max_depth=False, max_depth=MAX_DEPTH):
    soluciones = []
    mejor_largo = None
    largo_objetivo = None
    num_caminos_vistos = 0

    # STACK de tuplas (largo, camino, abiertos-no-explorados)
    caminos_open = [(1, [nodo_inicio], sacar_vecinos_filtrados(grafo, [nodo_inicio]))]
    
    while len(caminos_open) > 0:
        """
            Aquí voy a continuar con el último que miré.
        """
        # print(largo_objetivo, mejor_largo)
        
        largo, camino, abiertos_no_explorados = caminos_open[-1]  # .pop()
        # print("MIRANDO:", camino)
        try:
            # prox_nodo = abiertos_no_explorados.pop() 
            prox_nodo = next(abiertos_no_explorados)
        except StopIteration:
            # vacié esta ruta y tengo que volver!
            caminos_open.pop()
            # print("RUTA VACIADA!", camino)
            
        except IndexError:
            # vacié esta ruta y tengo que volver!
            caminos_open.pop()
            # print("RUTA VACIADA!", camino)
            continue
        if largo_objetivo is not None and largo >= largo_objetivo:
            # me pasé del target
            caminos_open.pop()
            continue
        elif mejor_largo is not None and largo >= mejor_largo:
            # ya estoy pasado del largo óptimo que encontré antes
            caminos_open.pop()
            continue
        
        camino_nuevo = camino + [prox_nodo]  # Expando el camino en un nodo
        num_caminos_vistos = num_caminos_vistos + 1
        if num_caminos_vistos % 100_000 == 0:
            print(num_caminos_vistos)
        # fs_camino_nuevo = frozenset(camino_nuevo)
        # if fs_camino_nuevo in caminos_vistos:
        #     # este ya lo vi, no lo quiero, está viejo.
        #     continue
        # caminos_vistos.add(fs_camino_nuevo)
        # if len(caminos_vistos) % 100000 == 0:
        #     print(len(caminos_vistos))
        vecinos_filtrados = sacar_vecinos_filtrados(grafo, camino_nuevo)  # Filtro las posibles expansiones futuras
        
        if not peekable(vecinos_filtrados):
            # Si no me puedo expandir eso quiere decir que ya tengo todos los nodos
            if return_first:
                # OJO! no es el mejor
                return [camino_nuevo], largo + 1
            
            # print("Encontré camino:", camino_nuevo)
            
            if mejor_largo is None:
                mejor_largo = largo + 1
                soluciones.append(camino_nuevo.copy())
                print("MEJOR LARGO:", mejor_largo)
                # caminos_vistos = actualizar_caminos_vistos(caminos_vistos, mejor_largo)
                largo_objetivo = largo
                print("Largo objetivo:", largo_objetivo)
            
            elif mejor_largo > largo + 1:
                mejor_largo = largo + 1
                soluciones = [camino_nuevo.copy()]
                print("ACTUALIZAMOS MEJOR LARGO:", mejor_largo)
                # caminos_vistos = actualizar_caminos_vistos(caminos_vistos, mejor_largo)
                largo_objetivo = largo
                print("Largo objetivo:", largo_objetivo)
            
            elif mejor_largo == largo + 1:
                soluciones.append(camino_nuevo.copy())
                
            else:  # mejor_largo es mejor que el actual
                continue

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


if __name__ == "__main__":
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
    grafo, num_nodos, cont_aristas = construir_grafo(combinaciones)
    for nodo, data in grafo.items():
        data["vecinos"].sort(key=lambda x: len(x), reverse=True)
    
    print("Num nodos:", num_nodos)
    print("Num aristas:", cont_aristas)
    nodos_por_tamaño = sorted(grafo.keys(), key=lambda x: len(x), reverse=True)

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

