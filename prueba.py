import numpy as np
import random

arreglo = [-1.0, 4.345415, -5.5565, 6.155646]
#print(sum(arreglo))
#print(np.absolute(arreglo))
#print([n**2 for n in arreglo])
print(sum([n**2 for n in np.absolute(arreglo)]))


#arreglo2 = [3, - 4, 5, -5, 0, -1]
#ordenado = sorted(arreglo2, key=lambda item: item, reverse=True)[:1]
#print(ordenado)


#for x in range(10):
#    print(x)

#print(random.randint(0, 4))


#print("--------------------")
#for indice in xrange(0, 5):
#    print(indice)