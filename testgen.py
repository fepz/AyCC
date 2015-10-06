import math
import random as rnd
import sys

def density(n, m):
    return math.ceil(10 * (2*m) / (n * (n-1))) / 10

def save_graph_to_file(g, n, ne, path=''):
    # Calcula la densidad
    d = density(n, ne)

    # Almacena en archivo
    fp = open(path + 'graph_'+str(ne)+'_'+"{:.1f}".format(d)+'.edgelist', 'w')
    fp.write('# Numero de nodos: ' + str(n) + '\n')
    fp.write('# Numero de arcos: ' + str(ne) + '\n')
    fp.write('# Densidad: ' + "{:.1f}".format(d) + '\n')
    fp.write('\n'.join('{} {} {}'.format(x[0],x[1],x[2]) for x in g))
    fp.close()

# n (numero de nodos) dado m (numero de arco) y d (densidad).
def cant_nodos(m, d):
    disc = 1 + ((8*m) / d)
    n = (1 + math.sqrt(disc)) / 2
    return math.ceil(n)

def gen_complete_graph(n):
    rs = []
    for i in range(1, n):
        for j in range(i+1, n+1):
            w = rnd.randint(1, 10)
            rs.append((i, j, w))
    return rs

# Genera una secuencia de grafos para un m (cant. arcos) fija
# y una d (densidad) variable cada ds=0.1 pasos.
def gen_graph_seq(m):
    d = [round(x/10,1) for x in range(10, 2, -1)]
    n = list(map(cant_nodos, [m]*len(d), d))
    mt = len(n)

    p = n[0] # Cantidad de nodos del grafo
    g = gen_complete_graph(p) # Genera un grafo completo con la menor cantidad de nodos.

    t = 0
    while t < mt:

        if p == n[t]:
            # Almacena los grafos intermedios segun criterio.
            save_graph_to_file(g, p, m, path='./test/')
            t += 1

        e = g[p - 1]
        g[p - 1] = (e[0], p + 1, e[2])
        p += 1

    return g

if __name__ == '__main__':

    if(len(sys.argv) != 2):
        print('Uso: python testgen.py m')
        print('donde m es el número de arcos a generar')
        exit(1)

    print("Generando...")
    gen_graph_seq(int(sys.argv[1]))    # SE LE PASA LA CANT DE NODOS POR LINEA DE COMANDO
    print("Generación finalizada.")
