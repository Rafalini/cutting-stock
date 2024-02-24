import pandas as pd
from solutions import BinPack
from solutions import StockCutter
from solutions import AmplSolver
import DataLoader
import os, glob
import time
import argparse
# import warnings

# warnings.filterwarnings("ignore", category=DeprecationWarning) 
fileNames=""

def save(filename, data, timedata):
    # data = {
    #   "true": tru,
    #   "optimal": opt,
    #   "optimal_relaxed": opt_rel,
    #   "backpack": std,
    #   "backpack_relaxed" : rel
    # }

    # timedata = {
    #   "true": tru,
    #   "optimal": time_opt,
    #   "optimal_relaxed": time_opt_rel,
    #   "backpack": time_std,
    #   "backpack_relaxed" : time_rel
    # }

    #load data into a DataFrame object:
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(args.output_dir, "effi"+fileNames+filename+".csv"))
    df = pd.DataFrame(timedata)
    df.to_csv(os.path.join(args.output_dir, "time"+fileNames+filename+".csv"))

def genDict():
    data = {}
    data["true"] = []
    data["optimal"] = []
    data["optimal_relaxed"] = []
    data["backpack"] = []
    data["backpack_relaxed"] = []
    return data
   
parser=argparse.ArgumentParser()
parser.add_argument("--input-dir", help="Input directory", default="input")
parser.add_argument("--output-dir", help="Output directory", default="input")
args=parser.parse_args()

if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

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

dataNotExtended = genDict()
timeNotExtended = genDict()

dataExtended = genDict()
timeExtended = genDict()

files = os.listdir(args.input_dir)
files = [s for s in files if s.endswith('.json')]
files.sort()
ampl = AmplSolver.AmplSolver()

def goBinPackNoRelax(dataArr, timeArr, jsonArr, orderType):
    start = time.time()
    tmpStd = []
    for jsonData in jsonArr:
      tmpStd.append(standardBinPack.solve(jsonData[orderType], jsonData["factory_rod_size"], False))
    timeArr.append("{:.4f}".format((time.time() - start)/len(tmpStd),5))
    dataArr.append(sum(tmpStd)/len(tmpStd))


def goBinPackRelax(dataArr, timeArr, jsonArr, orderType):
    start = time.time()
    tmpStd = []
    for jsonData in jsonArr:
      tmpStd.append(standardBinPack.solve(jsonData[orderType], jsonData["factory_rod_size"], True))
    timeArr.append("{:.4f}".format((time.time() - start)/len(tmpStd),5))
    dataArr.append(sum(tmpStd)/len(tmpStd))

def goCollumnGenNoRelax(dataArr, timeArr, input, orderType):
    ampl.reset()
    fileList = ampl.prepareDataFiles(os.path.join(args.input_dir, input), orderType, False)
    tmpOpt = []

    start = time.time()
    for entry in fileList:
        ampl.reset()
        tmpOpt.append(ampl.solve(entry))
    timeArr.append("{:.4f}".format((time.time() - start)/len(tmpOpt),5))
    dataArr.append(sum(tmpOpt)/len(tmpOpt))

def goCollumnGenRelax(dataArr, timeArr, fileList, orderType):
    ampl.reset()
    fileList = ampl.prepareDataFiles(os.path.join(args.input_dir, input), orderType, True)
    tmpOpt = []

    start = time.time()
    for entry in fileList:
        ampl.reset()
        tmpOpt.append(ampl.solve(entry))

    timeArr.append("{:.4f}".format((time.time() - start)/len(tmpOpt),5))
    dataArr.append(sum(tmpOpt)/len(tmpOpt))

for idx, input in enumerate(files):
    print(bcolors.WARNING + "Progress: " + str(round(100 * (idx+1)/len(files),2))+"%   " + input)

    jsonArr = DataLoader.loadData(os.path.join(args.input_dir, input))
    dataNotExtended["true"].append(jsonArr[0]["optimal_solution"])
    timeNotExtended["true"].append(jsonArr[0]["optimal_solution"])
    dataExtended["true"].append(jsonArr[0]["optimal_solution"])
    timeExtended["true"].append(jsonArr[0]["optimal_solution"])

    goBinPackNoRelax(dataNotExtended["backpack"], timeNotExtended["backpack"], jsonArr, "order")
    goBinPackRelax(dataNotExtended["backpack_relaxed"], timeNotExtended["backpack_relaxed"], jsonArr, "order")
    goCollumnGenNoRelax(dataNotExtended["optimal"], timeNotExtended["optimal"], input, "order")
    goCollumnGenRelax(dataNotExtended["optimal_relaxed"], timeNotExtended["optimal_relaxed"], input, "order")

    #extendedOrder
    goBinPackNoRelax(dataExtended["backpack"], timeExtended["backpack"], jsonArr, "extendedOrder")
    goBinPackRelax(dataExtended["backpack_relaxed"], timeExtended["backpack_relaxed"], jsonArr, "extendedOrder")
    goCollumnGenNoRelax(dataExtended["optimal"], timeExtended["optimal"], input, "extendedOrder")
    goCollumnGenRelax(dataExtended["optimal_relaxed"], timeExtended["optimal_relaxed"], input, "extendedOrder")

    save("_no_ext", dataNotExtended, timeNotExtended)
    save("_extend", dataExtended, timeExtended)

save("_no_ext", dataNotExtended, timeNotExtended)
save("_extend", dataExtended, timeExtended)
