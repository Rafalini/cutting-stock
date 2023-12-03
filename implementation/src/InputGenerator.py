import json
import math
import random
import os, sys
from unittest import result
import argparse


parser=argparse.ArgumentParser()
parser.add_argument("--input-dir", help="Input directory", default="input")
parser.add_argument("--output-dir", help="Output directory", default="output")
parser.add_argument("--samples", help="Samples number", default=10, type=int)
parser.add_argument("--min-order", help="Min order", default=5, type=int)
parser.add_argument("--mode", help="Generation mode", choices=["random", "reverse"], default="reverse")
parser.add_argument("--batch", help="Amount in batch of given size", default=5, type=int)
args=parser.parse_args()

factor = 3

def clearInputsOutputs():

    if not os.path.exists(args.input_dir):
        os.makedirs(args.input_dir)
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for file in os.listdir(args.input_dir):
        os.remove(os.path.join(args.input_dir, file))

    # for file in os.listdir(args.output_dir):
    #     os.remove(os.path.join(args.output_dir,file))


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
        relaxation_length = 0
        relaxation_number = 0
        if length > 2 and relaxation:
            relaxation_number = random.randint(0, amount-1)
            relaxation_length = math.ceil(length * random.randint(1, max_percentage)/100)

        data.append({"rod_size": length, "rods_number": amount, "relaxation_length": relaxation_length, "relaxation_number": relaxation_number})

    return {"optimal_solution": order_size, "factory_rod_size": factory_rod_size, "order": data}


if __name__ == "__main__":
    clearInputsOutputs()

    minOrder = 1

    if len(sys.argv) == 3:
        minOrder = args.min_order

    for i in range(1, args.samples+1):
        name = f"{'out_'}{i:04}" + ".json"
        with open(os.path.join(args.input_dir, name), "w") as outfile:
            data = []

            for j in range(args.batch):
                match args.mode:
                    case "reverse":
                        data.append(reverseGenerator(relaxation=True, max_percentage = 20, factory_rod_size = 12, order_size=minOrder + i*factor))
                        # data.append(reverseGenerator(relaxation=False, max_percentage = 20, factory_rod_size = 12, order_size=minOrder + i*factor))
                    case "random":
                        data.append(generateData(relaxation=True, max_percentage = 20, factory_rod_size = 12, order_size=minOrder + i*factor))
                        # data.append(generateData(relaxation=False, max_percentage = 20, factory_rod_size = 12, order_size=minOrder + i*factor))

            outfile.write(json.dumps(data))
