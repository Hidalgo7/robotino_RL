import sys
import numpy as np
import matplotlib.pyplot as plt

if __name__ =="__main__":
    if len(sys.argv) < 2:
        print("Se debe introducir la ruta del fichero para imprimir el grafico")
    else:
        grafico = sys.argv[1]
        file = open(grafico,'r')
        lines = file.readlines()
        x_axis = [i for i in range(1,len(lines)+1)]
        y_axis = []
        for line in lines:
            reward_value = float(line[8:])
            y_axis.append(reward_value)

        plt.plot(x_axis, y_axis)
        plt.show()