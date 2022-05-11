import Logica

Nx = 5
Ny = 5
Nc = 4
Nd = 7
X = list(range(Nx))
Y = list(range(Ny))
C = list(range(Nc))
D = list(range(Nd))
xypos = []
Colores = {
    0 : 'R',
    1 : 'G',
    2 : 'B',
    3 : 'O' 
}
Direcciones = {
    0 : "t",
    1 : "tb",
    2 : "tl",
    3 : "tr",
    4 : "lb",
    5 : "rb",
    6 : "lr"
}

reglas = []

OenCasilla = Logica.Descriptor([Nx,Ny,Nc,Nd])

#decodificacion caracter
def escribir(self,literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' no'
    else:
        atomo = literal
        neg = ''
        x, y, c, d = self.inv(atomo)
        return f"{neg}({X[x]},{Y[y]})/{Colores[c]}{Direcciones[d]}"

from types import MethodType
OenCasilla.escribir = MethodType(escribir, OenCasilla)

def decodificar(list):
    matriz = []
    m = []
    pos = {}
    t = {
        "Rt" : "R",
        "Rlr" : "r",
        "Rtb" : "Q",
        "Rtl" : "W",
        "Rtr" :    "E",
        "Rlb" : "T",
        "Rrb" : "Y",
        "Gt"  : "G",
        "Glr" : "g",
        "Gtb" : "q",
        "Gtl" : "w",
        "Gtr" : "e",
        "Glb" : "t",
        "Grb" : "y",
        "Bt" : "B",
        "Btb": "z",
        "Btl" : "x",
        "Btr" : "c",
        "Blb" : "v",
        "Brb" : "n",
        "Ot" : "O",
        "Olr" : "o",
        "Otb" : "Z",
        "Otl" : "X",
        "Otr" : "C",
        "Olb" : "V",
        "Orb" : "N"

    }
    for key in list:
        m.append(OenCasilla.escribir(key))
    for i in m:
        pos[(int(i[1]),int(i[3]))] = i.split("/")[1]
    for y in range(Ny):
        strr = ""
        for x in range(Nx):
            for key in pos.keys():
                if key[0] == x and key[1] == y:
                    strr+=t[pos[(x,y)]]
                else:
                    continue
        matriz.append(strr)
    return matriz

def asignarReglas(lista):
    reglas = []
    reglas.append(unCD())
    reglas.append(vecT())
    for i in lista:
        reglas.append(OenCasilla.P([i[0],i[1],i[2],i[3]]))
        xypos.append((i[0],i[1]))
    reglas.append(asignarCD())
    return resolver(Logica.Ytoria(reglas))

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
    return decodificar(lis)


#cada casilla debe tener un objeto
def asignarCD():
    Y_xy = []
    for x in X:
        for y in Y:
                Oc = []
                for c in C:
                    if (x,y) not in xypos:
                        cd = [OenCasilla.P([x,y,c,u]) for u in D if u != 0]
                        formula = Logica.Otoria(cd) #si no es terminal se le asigna color y direccion
                        Oc.append(formula)
                if len(Oc) != 0:
                    Y_xy.append(Logica.Otoria(Oc))
    return Logica.Ytoria(Y_xy)


#Cada casilla debe tener solo un color y solo una direccion
def unCD():
    Y_xy = []
    for x in X:
        for y in Y:
            Yd = []
            for d in D:
                Yc = []
                for c in C:
                    ocd = [OenCasilla.P([x,y,u,m]) for u in C for m in D if u != c or m != d] #casillas con diferente direccion o color
                    formula = "("+OenCasilla.P([x,y,c,d])+">-"+Logica.Otoria(ocd)+")"
                    Yc.append(formula)
                Yd.append(Logica.Ytoria(Yc))
            Y_xy.append(Logica.Ytoria(Yd))
    return Logica.Ytoria(Y_xy)

#Cada terminal tiene un solo vecino(un solo color adyacente a este)
def vecT():
    Y_xy = []
    for x in X:
        for y in Y:
            Y_c = []
            for c in C:
                vecinos = [OenCasilla.P([u,m,c,d]) for u in X for m in Y for d in D if ((u == x-1 and m == y) or (u == x+1 and m == y) or (m==y+1 and u == x) or (m==y-1 and u == x)) and d!=0 ]
                formula = "("+OenCasilla.P([x,y,c,0])+">"
                v = []
                for e in vecinos:
                    otros_vecinos = [n for n in vecinos if n != e]
                    form = "("+e+"Y-"+Logica.Otoria(otros_vecinos)+")"
                    v.append(form)
                vv = Logica.Otoria(v)
                formula+=vv+")"
                if len(vecinos) != 1:
                    Y_c.append(formula)
                else:
                    Y_c.append("("+OenCasilla.P([x,y,c,0])+">"+vecinos[0]+")")
            Y_xy.append(Logica.Ytoria(Y_c))
    return Logica.Ytoria(Y_xy)


                    


