import random

from more_itertools import peekable

from aux_funcs import (
    sacar_vecinos_filtrados, combs_k_elementos, construir_grafo,
    es_mochila_valida
)

from params import (MAX_DEPTH, NUM_TILES, LIMIT, NODO_INICIAL)



def node_bin_packing_solver_dfs(grafo, nodo_inicio, caminos_vistos: set=None, largo_objetivo: int=None, return_first=False):
    soluciones = []
    mejor_largo = None
    largo_objetivo = largo_objetivo
    num_caminos_vistos = 0

    # STACK de tuplas (largo, camino, abiertos-no-explorados)
    caminos_open = [(1, [nodo_inicio], sacar_vecinos_filtrados(grafo, [nodo_inicio]))]
    
    while len(caminos_open) > 0:
        """
            Aquí voy a continuar con el último que miré.
        """
        # input("...")
        # print(largo_objetivo, mejor_largo)
        
        largo, camino, abiertos_no_explorados = caminos_open[-1]  # .pop()
        # print("MIRANDO:", camino)
        try:
            prox_nodo = abiertos_no_explorados.pop(0) 
            # prox_nodo = next(abiertos_no_explorados)
        except StopIteration:
            # vacié esta ruta y tengo que volver!
            caminos_open.pop()
            # print("RUTA VACIADA!", camino)
            continue
            
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
        
        if caminos_vistos is not None:  # voy a gastar muuuucha ram.
            fs_camino_nuevo = frozenset(camino_nuevo)
            # print("camino nuevo", fs_camino_nuevo)
            if fs_camino_nuevo in caminos_vistos:
                # este ya lo vi, no lo quiero, está viejo.
                # print("DESCARTA3")
                continue
            caminos_vistos.add(fs_camino_nuevo)
            if len(caminos_vistos) % 100_000 == 0:
                print("Vistos:", len(caminos_vistos))
        else:
            num_caminos_vistos = num_caminos_vistos + 1
            if num_caminos_vistos % 100_000 == 0:
                print("Vistos:", num_caminos_vistos)
        
        vecinos_filtrados = sacar_vecinos_filtrados(grafo, camino_nuevo)  # Filtro las posibles expansiones futuras
        peekable_vecinos_filtrados = peekable(vecinos_filtrados)
        # print(bool(peekable_vecinos_filtrados))
        # print("VECINOS:", vecinos_filtrados)
        # if peekable_vecinos_filtrados:
        #     print("PEEKABLE")
        # else:
        #     print("NO PEEKABLE!")
        if not peekable_vecinos_filtrados:
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
    tiles = set()
    for _ in range(NUM_TILES):
        generado = [random.randint(0, 32) for _ in range(random.randint(1, 16))]
        generado = tuple(sorted(set(generado)))
        tiles.add(generado)
    paletas_por_tile = list(tiles)
    print("PALETAS TILES:", paletas_por_tile)
    
    mochilas = []
    for i in range(1, len(paletas_por_tile) + 1):
        for ids_mochila in combs_k_elementos(paletas_por_tile, i):
            mochila = [paletas_por_tile[id_] for id_ in ids_mochila]
            if es_mochila_valida(mochila):
                mochilas.append(ids_mochila)
    grafo, num_nodos, num_aristas = construir_grafo(mochilas)
    
    print("N° nodos:", num_nodos)
    print("N° aristas:", num_aristas)
    print(grafo[0])
    print(grafo[1])
    
    
    print("EMPEZAMOS LA BÚSQUEDA!")
    caminos_vistos = set()  # Lo defino acá para poder reutilizarlo entre distintos nodos de inicio
    nodo_inicial = NODO_INICIAL
    caminos, largo = node_bin_packing_solver_dfs(grafo, nodo_inicial, caminos_vistos, return_first=False)
    print(caminos)
    print(largo)
    print(len(caminos_vistos))

