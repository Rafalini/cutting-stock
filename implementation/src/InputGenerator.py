import json
import math
import random
import os, sys
from unittest import result

def clearInputsOutputs():

    inputDir = 'input'
    outputDir = 'output'

    if not os.path.exists(inputDir):
        os.makedirs(inputDir)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    for file in os.listdir(inputDir):
        os.remove(os.path.join(inputDir, file))

    for file in os.listdir(outputDir):
        os.remove(os.path.join(outputDir,file))


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

def reverseGenerator(relaxation=False, max_percentage=50, factory_rod_size=15, order_size=10):
    order={}

    for _ in range(order_size):

        remaining_length = factory_rod_size

        while remaining_length > 0:
            # Generate a random number between 1 and the remaining sum
            random_num = random.randint(1, remaining_length)
            
                # If the remaining sum is greater than the random number, append the random number
            if remaining_length > random_num:
                order[random_num] = order.get(random_num, 0) + 1
                remaining_length -= random_num
            else:
                # If the remaining sum is less than or equal to the random number, append the remaining sum
                order[random_num] = order.get(remaining_length, 0) + 1
                break

    data = []
    for length, amount in order.items():

        relaxation_length = random.randint(0, math.ceil(length*max_percentage/100)-1)
        relaxation_number = random.randint(0, amount-1)
        if not relaxation:
            relaxation_length = 0
            relaxation_number = 0

        data.append({"rod_size": length, "rods_number": amount, "relaxation_length": relaxation_length, "relaxation_number": relaxation_number})

    return {"optimal_solution": order_size, "factory_rod_size": factory_rod_size, "order": data}

if __name__ == "__main__":
    clearInputsOutputs()

    minOrder = 10

    if len(sys.argv) == 3:
        minOrder = sys.argv[2]

    for i in range(1, int(sys.argv[1])+1):
        name = str(i) + ".json"
        with open(os.path.join("input", name), "w") as outfile:
            data = reverseGenerator(relaxation=True, max_percentage = 20, factory_rod_size = 12, order_size=minOrder + i*10)
            outfile.write(json.dumps(data))
