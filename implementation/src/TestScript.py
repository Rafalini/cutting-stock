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

for idx, input in enumerate(os.listdir(IN_DIR)):

    print(bcolors.WARNING + "Progress: " + str(round(100 * (idx+1)/len(os.listdir(IN_DIR)),2))+"%   " + input)

    jsonData = DataLoader.loadData(os.path.join(IN_DIR, input))
    opt = 0
    std = 0
    rel = 0

    name = "optimal_" + input.split(".")[0]

    with open(os.path.join(OUT_DIR, name), "w") as outfile:
        jsonData["fileName"] = name
        opt = optimalCutter.solve(jsonData, jsonData["factory_rod_size"])
        outfile.write(str(opt))

    name = "standard_binpack_" + input.split(".")[0]

    with open(os.path.join(OUT_DIR, name), "w") as outfile:
        std = standardBinPack.solve(jsonData, jsonData["factory_rod_size"], False)
        outfile.write(str(std))

    
    name = "relaxed_binpack_" + input.split(".")[0]

    with open(os.path.join(OUT_DIR, name), "w") as outfile:
        rel = standardBinPack.solve(jsonData, jsonData["factory_rod_size"], True)
        outfile.write(str(rel))

    # if std != rel:
    #     print(bcolors.OKBLUE +"            opt: " + str(opt))
    #     print(bcolors.OKBLUE +"             std: " + str(std))
    #     print(bcolors.OKBLUE +"             rel: " + str(rel))

