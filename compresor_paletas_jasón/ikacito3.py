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
from functools import reduce
from more_itertools import peekable


from params import LIMIT, MAX_DEPTH, OPTION, NUM_TILES




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


def sacar_vecinos_filtrados(grafo, camino):
    tengo = calcular_acumulados(camino)
    return (filter(lambda x: len(tengo.intersection(x)) == 0, grafo[camino[-1]]["vecinos"]))
    # si lo quiero como lista:
    # return list(filter(lambda x: len(tengo.intersection(x)) == 0, grafo[camino[-1]]["vecinos"]))[::-1]


# def comprobar_solucion()


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
    
    
    
    
