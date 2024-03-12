import json
import math
import random
import os, sys
from unittest import result
import argparse

maxPercentageRelax=0.2
maxPercentageAmount=0.5

parser=argparse.ArgumentParser()
parser.add_argument("--input-dir", help="Input directory", default="input")
parser.add_argument("--output-dir", help="Output directory", default="output")
parser.add_argument("--factory-rod-size", help="Factory base rod length", default=1200, type=int)
parser.add_argument("--widths-gap", help="Minimal difference in lengths between generated widths", default=50, type=int)
parser.add_argument("--samples", help="Samples number", default=20, type=int)
parser.add_argument("--min-order", help="Min order", default=500, type=int)
parser.add_argument("--step", help="Min order + step on every interation", default=250, type=int)
parser.add_argument("--batch", help="Amount in batch of given size", default=10, type=int)
parser.add_argument("--increase-length", help="Should widhts be increased during relaxation", default=0, type=int)
args=parser.parse_args()

def clearInputsOutputs():

    if not os.path.exists(args.input_dir):
        os.makedirs(args.input_dir)
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    for file in os.listdir(args.input_dir):
        os.remove(os.path.join(args.input_dir, file))
    # for file in os.listdir(args.output_dir):
    #     os.remove(os.path.join(args.output_dir,file))


def reverseGenerator(factory_rod_size, order_size):
    order={}
    sumLen = 0
    for _ in range(order_size):

        remaining_length = factory_rod_size

        while remaining_length > 0:
            # Generate a random number between 0 and the remaining sum and ceil it to widths_gap
            random_num = random.randint(0, remaining_length - 1)
            random_num += args.widths_gap - (random_num % args.widths_gap)
            
                # If the remaining sum is greater than the random number, append the random number
            if remaining_length > random_num:
                order[random_num] = order.get(random_num, 0) + 1
                remaining_length -= random_num
                sumLen += random_num
            else:
                # If the remaining sum is less than or equal to the random number, append the remaining sum
                order[random_num] = order.get(remaining_length, 0) + 1
                sumLen += remaining_length
                break

    data = []
    for length, amount in order.items():
        # if length-5 > 0:
        #     length -= 1
        data.append({"rod_size": length, "rods_number": amount, "relaxation_length": 0, "relaxation_number": 0})

    return {"data": data, "sumLen":sumLen}


def relaxeOrder(factory_rod_size, order):
    relaxedOrder=[]
    maxRelax = 0
    random.shuffle(order)

    for entry in order:

        relaxation_number = random.randint(0, max(1, int(entry["rods_number"]*maxPercentageAmount)))

        relax_range = entry["rod_size"] * maxPercentageRelax;
        if relax_range + entry["rod_size"] > factory_rod_size:
            relax_range = factory_rod_size - entry["rod_size"];
        
        relaxation_length = random.randint(0, int(relax_range));
        if args.increase_length:
            length_increase = relaxation_length
        else:
            length_increase = 0

        if relaxation_number == 0 or relaxation_length == 0:
            relaxedOrder.append({"rod_size": entry["rod_size"], "rods_number": entry["rods_number"], "relaxation_length": 0, "relaxation_number": 0})
        elif relaxation_number == entry["rods_number"]:    
            relaxedOrder.append({"rod_size": entry["rod_size"]+length_increase, "rods_number": relaxation_number, "relaxation_length": relaxation_length, "relaxation_number": relaxation_number})
            maxRelax += relaxation_length * relaxation_number
        else:
            relaxedOrder.append({"rod_size": entry["rod_size"], "rods_number": entry["rods_number"]-relaxation_number, "relaxation_length": 0, "relaxation_number": 0})
            relaxedOrder.append({"rod_size": entry["rod_size"]+length_increase, "rods_number": relaxation_number, "relaxation_length": relaxation_length, "relaxation_number": relaxation_number})
            maxRelax += relaxation_length * relaxation_number
    return {"relaxed":relaxedOrder, "maxRelax":maxRelax}


if __name__ == "__main__":
    clearInputsOutputs()

    minOrder = args.min_order

    for i in range(0, args.samples):
        name = f"{'out_'}{i:04}" + ".json"
        with open(os.path.join(args.input_dir, name), "w") as outfile:
            data = []

            for j in range(args.batch):
                order_size = minOrder + i*args.step
                order = reverseGenerator(factory_rod_size = args.factory_rod_size, order_size=order_size)
                relaxedOrder = relaxeOrder(factory_rod_size=args.factory_rod_size, order=order["data"])
                data.append({"optimal_solution": order_size, "factory_rod_size": args.factory_rod_size, "orderSum":order["sumLen"], "maxRelax": relaxedOrder["maxRelax"],"order": order["data"], "relaxedOrder": relaxedOrder["relaxed"]})


            outfile.write(json.dumps(data))
