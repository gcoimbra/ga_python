from funcoes_auxiliares import *

intervaloMin = 0; intervaloMax = 1

x1 = 0.788586; x2 = 0.408500

print("Treliça")
print("X1 = %.6f, X2 = %.6f" % (x1, x2))
print("f = %.6f" % funcaoTrelica(x1, x2))
print("Intervalo válido? R = %s" % validaTresRestricoesTrelica(x1, x2, intervaloMin, intervaloMax))
print("g1(x) = %.6f" % (((((math.sqrt(2)*x1) + x2)/((math.sqrt(2)*(x1**2)) + 2*x1*x2)) * P) - sigma))
print("g2(x) = %.6f" % ((((x2)/((math.sqrt(2)*(x1**2)) + 2*x1*x2)) * P) - sigma))
print("g3(x) = %.6f" % (((1)/((math.sqrt(2)*x2) + x1) * P) - sigma))

intervaloX1X2Min = 0; intervaloX1X2Max = 100
intervaloX3X4Min = 10; intervaloX3X4Max = 200

x1 = 14; x2 = 7; x3 = 44.766421; x4 = 146.422644

print("\nVaso de pressão")
print("X1 = (%d * %f) = %.6f, X2 = (%d * %f) = %.6f, X3 = %.6f e X4 = %.6f" % (x1, multiploVasoPressao, x1*multiploVasoPressao, x2, multiploVasoPressao, x2*multiploVasoPressao, x3, x4))
print("f = %.6f" % funcaoVasoPressao(x1, x2, x3, x4))
print("Intervalo válido? R = %s" % validaQuatroRestricoesVasoPressao(x1, x2, x3, x4, intervaloX1X2Min, intervaloX1X2Max, intervaloX3X4Min, intervaloX3X4Max))
print("g1(x) = %.6f" % (-(x1*multiploVasoPressao) + 0.0193*x3))
print("g2(x) = %.6f" % (-(x2*multiploVasoPressao) + 0.00954*x3))
print("g3(x) = %.6f" % ((-math.pi*(x3**2)*x4) - ((4/3)*math.pi*(x3**3)) + 1296000))
print("g4(x) = %.6f" % (x4 - 240))