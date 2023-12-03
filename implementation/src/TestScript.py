import pandas as pd
from solutions import BinPack
from solutions import StockCutter
from solutions import AmplSolver
import DataLoader
import os
import time

IN_DIR = "input2"
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
tru = []
opt = []
std = []
rel = []

time_opt = []
time_std = []
time_rel = []


files = os.listdir(IN_DIR)
files.sort()

for idx, input in enumerate(files):

    print(bcolors.WARNING + "Progress: " + str(round(100 * (idx+1)/len(os.listdir(IN_DIR)),2))+"%   " + input)

    jsonArr = DataLoader.loadData(os.path.join(IN_DIR, input))
#Standard binpack
    start = time.time()
    tmpStd = []
    for jsonData in jsonArr:
      tmpStd.append(standardBinPack.solve(jsonData, jsonData["factory_rod_size"], False))

    time_std.append("{:.4f}".format((time.time() - start)/len(tmpStd),5))
    std.append(sum(tmpStd)/len(tmpStd))
#Relaxed binpack
    start = time.time()
    tmpRel = []
    for jsonData in jsonArr:
      tmpRel.append(standardBinPack.solve(jsonData, jsonData["factory_rod_size"], True))

    time_rel.append("{:.4f}".format((time.time() - start)/len(tmpRel),5))
    rel.append(sum(tmpRel)/len(tmpRel))
#Optimal

    # start = time.time()
    # tmpOpt = []
    # for jsonData in jsonArr:
    #   jsonData["fileDir"] = OUT_DIR
    #   name = "optimal_" + input.split(".")[0]
    #   jsonData["fileName"] = name
    #   jsonData["saveFigure"] = False

    #   if idx < 23: #above this constraint, standard solver becomes very time consuming
    #     tmpOpt.append(optimalCutter.solve(jsonData, jsonData["factory_rod_size"]))
    #   else:  
    #     tmpOpt.append(jsonData["optimal_solution"])

    # opt.append(sum(tmpOpt)/len(tmpOpt))
    # time_opt.append("{:.4f}".format((time.time() - start)/len(tmpOpt),5))

    ampl = AmplSolver.AmplSolver()
    fileList = ampl.prepareDataFiles(os.path.join(IN_DIR, input))
    tmpOpt = []

    start = time.time()
    for entry in fileList:
        ampl = AmplSolver.AmplSolver()
        tmpOpt.append(ampl.solve(entry))

    opt.append(sum(tmpOpt)/len(tmpOpt))
    time_opt.append("{:.4f}".format((time.time() - start)/len(tmpOpt),5))

    tru.append(jsonArr[0]["optimal_solution"])

data = {
  "true": tru,
  "optimal": opt,
  "backpack": std,
  "backpack_relaxed" : rel
}

timedata = {
  "optimal": time_opt,
  "backpack": time_std,
  "backpack_relaxed" : time_rel
}

#load data into a DataFrame object:
df = pd.DataFrame(data)
df.to_csv(os.path.join(OUT_DIR, "effi_summary.csv"))
df = pd.DataFrame(timedata)
df.to_csv(os.path.join(OUT_DIR, "time_summary.csv"))
