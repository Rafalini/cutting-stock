import json
import math
import random
import os, sys

def clearInputsOutputs():

    inputDir = 'input'
    outputDir = 'output'

    if not os.path.exists(inputDir):
        os.makedirs(inputDir)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    for input in os.listdir(inputDir):
        os.remove(os.path.join(inputDir, input))

    for input in os.listdir(outputDir):
        os.remove(os.path.join(outputDir,input))


def generateData(relaxation=False, max_percentage=50, factory_rod_size=15, order_size=10):
    order = []
    while order_size > 0:
        rod_size = random.randint(1, factory_rod_size - 1)
        rods_number = random.randint(1, order_size)
        order_size -= rods_number
        if order_size < 0:
            rods_number += order_size

        relaxation_length = random.randint(0, math.ceil(rod_size*max_percentage/100)-1)
        relaxation_number = random.randint(0, rods_number)
        if not relaxation:
            relaxation_length = 0
            relaxation_number = 0

        order.append({"rod_size": rod_size, "rods_number": rods_number, "relaxation_length": relaxation_length, "relaxation_number": relaxation_number})

    return {"factory_rod_size": factory_rod_size, "order": order}

if __name__ == "__main__":
    clearInputsOutputs()
    for i in range(1, int(sys.argv[1])+1):
        name = str(i) + ".json"
        with open(os.path.join("input", name), "w") as outfile:
            if len(sys.argv) == 0:
                data = generateData(relaxation=True, max_percentage = 20, factory_rod_size = 20, order_size=5 + i)
            else:
                data = generateData(relaxation=True, max_percentage = 20, factory_rod_size = 20, order_size=5 + i)
            outfile.write(json.dumps(data))
