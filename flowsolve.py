import Logica

def FlowRead(MAP_FILE):
	MAP_FILE = open(MAP_FILE,"r")
	MAP_MATRIX = [j.strip() for j in MAP_FILE]
	MAP_FILE.close()
	return MAP_MATRIX

def asignarTerminales(mapa):
	M = []
	for y in range(len(mapa)):
		for x in range(len(mapa[y])):
			if mapa[y][x] in ['R','G','B','O']:
				M.append(TenCasilla.P([x,y,NColores[mapa[y][x]]]))
	return M

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

TenCasilla = Logica.Descriptor([Nx,Ny,Nc])
OenCasilla = Logica.Descriptor([Nx,Ny,Nc,Nd])

terminales = asignarTerminales(mapa)
print(terminales)