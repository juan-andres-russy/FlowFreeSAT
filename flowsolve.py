import Logica

def FlowRead(MAP_FILE):
	MAP_FILE = open(MAP_FILE,"r")
	MAP_MATRIX = [j.strip() for j in MAP_FILE]
	MAP_FILE.close()
	return MAP_MATRIX

def defineMap(matriz):
    dic = {}
    for y in range(len(matriz)):
        for x in range(len(matriz[y])):
            if matriz[y][x] in ['R','G','B','O']:
                dic[(x,y)] = matriz[y][x]
    return dic

def topico(tsei,intdict):
    M = []
    for claus in tsei:
        cl = []
        for kkk in claus:
            kkk = intdict[kkk]
            cl.append(kkk)
        M.append(cl)
    return M

def resolver(formula):
    S = Logica.tseitin(formula)
    pycosatset = S
    count = 1
    intdict = {}
    dictint = {}
    for cl in S:
        for kk in cl:
            if "-" not in kk:
                if kk not in intdict.keys():
                    intdict[kk] = count
                    dictint[count] = kk
                    count+=1
            else:
                if kk[1] not in intdict.keys():
                    intdict[kk[1]] = count
                    dictint[count] = kk[1]
                    count+=1
                intdict[kk] = -1 * intdict[kk[1]]
    pycosatset = topico(pycosatset,intdict)
    import pycosat
    solution = pycosat.solve(pycosatset)
    II = {}
    for innt in solution:
        num = -1*innt if innt < 0 else innt
        boole = True if innt > 0 else False
        II[dictint[num]] = boole
    lis = []
    for k in II:
        if (ord(k) >= OenCasilla.rango[0]) and (ord(k) <= OenCasilla.rango[1]) and II[k]:
            lis.append(k)
    return lis



mapa = FlowRead(input("mapa: "))

Nx = len(mapa[0])
Ny = len(mapa)
Nc = 4
Nd = 4
X = list(range(Nx))
Y = list(range(Ny))
C = list(range(Nc))
D = list(range(Nd))

NColores = {
	'R' : 0,
	'G' : 1,
	'B' : 2,
	'O' : 3
}

Colores = {
    0 : 'R',
    1 : 'G',
    2 : 'B',
    3 : 'O' 
}

Direcciones = {
	0 : 't',
	1 : 'b',
	2 : 'l',
	3 : 'r',
}


direcciones_posibles = {
    (0,1) : 'tb',
    (0,2) : 'tl',
    (0,3) : 'tr',
    (1,2) : 'bl',
    (1,3) : 'br',
    (2,3) : 'lr'
}

OenCasilla = Logica.Descriptor([Nx,Ny,Nc,Nd])
pos_t = defineMap(mapa)


def regla_1():
    Y_xy = []
    for x in X:
        for y in Y:
            if (x,y) not in pos_t:
                O_d = []
                for d in direcciones_posibles.keys():
                    pq = [Logica.Ytoria([OenCasilla.P([x,y,c,d[0]]),OenCasilla.P([x,y,c,d[1]])]) for c in C] 
                    pq = Logica.Otoria(pq)
                    O_d.append(pq)
                Y_xy.append(Logica.Otoria(O_d))
    return Logica.Ytoria(Y_xy)


def regla_2():
    Y_xy = []
    for x in X:
        for y in Y:
            if (x,y) not in pos_t:
                O_c = []
                for c in C:
                    nq = [OenCasilla.P([x,y,nc,d]) for nc in C if nc != c for d in D]
                    q = [OenCasilla.P([x,y,c,d]) for d in D]
                    formula = "("+Logica.Otoria(q)+"Y-"+Logica.Otoria(nq)+")"
                    O_c.append(formula)
                Y_xy.append(Logica.Otoria(O_c))
    return Logica.Ytoria(Y_xy)

M = resolver(Logica.Ytoria([regla_1(),regla_2()]))
for i in M:
    print(OenCasilla.inv(i))
