import pandas as pd
from solutions import BinPack
from solutions import StockCutter
import DataLoader
import os

IN_DIR = "input"
OUT_DIR = "output"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    GREEN = "\033[96m"
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

standardBinPack = BinPack.StandardBinPackSolver()
optimalCutter = StockCutter.StockCutter() 
opt = []
std = []
rel = []

for idx, input in enumerate(os.listdir(IN_DIR)):

    print(bcolors.WARNING + "Progress: " + str(round(100 * (idx+1)/len(os.listdir(IN_DIR)),2))+"%   " + input)

    jsonData = DataLoader.loadData(os.path.join(IN_DIR, input))

    # name = "optimal_" + input.split(".")[0]

    # with open(os.path.join(OUT_DIR, name), "w") as outfile:
    #     jsonData["fileName"] = name
    #     opt.append(optimalCutter.solve(jsonData, jsonData["factory_rod_size"]))
    #     outfile.write(str(opt[-1]))

    # name = "standard_binpack_" + input.split(".")[0]

    # with open(os.path.join(OUT_DIR, name), "w") as outfile:
    #     std.append(standardBinPack.solve(jsonData, jsonData["factory_rod_size"], False))
    #     outfile.write(str(std[-1]))

    
    # name = "relaxed_binpack_" + input.split(".")[0]

    # with open(os.path.join(OUT_DIR, name), "w") as outfile:
    #     rel.append(standardBinPack.solve(jsonData, jsonData["factory_rod_size"], True))
    #     outfile.write(str(rel[-1]))

    std.append(standardBinPack.solve(jsonData, jsonData["factory_rod_size"], False))
    # opt.append(optimalCutter.solve(jsonData, jsonData["factory_rod_size"]))
    opt.append(jsonData["optimal_solution"])
    rel.append(standardBinPack.solve(jsonData, jsonData["factory_rod_size"], True))


data = {
  "optimal": opt,
  "backpack": std,
  "backpack_relaxed" : rel
}

#load data into a DataFrame object:
df = pd.DataFrame(data)
df.to_csv(os.path.join(OUT_DIR, "summary.csv"))

