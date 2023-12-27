import pandas as pd
from solutions import BinPack
from solutions import StockCutter
from solutions import AmplSolver
import DataLoader
import os
import time
import argparse

fileNames="summary_1"

def save(tru, opt, std, rel, time_opt, time_std, time_rel):
    data = {
      "true": tru,
      "optimal": opt,
      "backpack": std,
      "backpack_relaxed" : rel
    }

    timedata = {
      "true": tru,
      "optimal": time_opt,
      "backpack": time_std,
      "backpack_relaxed" : time_rel
    }

    #load data into a DataFrame object:
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(args.output_dir, "effi_"+fileNames+".csv"))
    df = pd.DataFrame(timedata)
    df.to_csv(os.path.join(args.output_dir, "time_"+fileNames+".csv"))

parser=argparse.ArgumentParser()
parser.add_argument("--input-dir", help="Input directory", default="input")
parser.add_argument("--output-dir", help="Output directory", default="output")
args=parser.parse_args()

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

beginning = 0

if os.path.exists(os.path.join(args.output_dir, "effi_"+fileNames+".csv")):
  effiPd = pd.read_csv(os.path.join(args.output_dir, "effi_"+fileNames+".csv"))
  timePd = pd.read_csv(os.path.join(args.output_dir, "time_"+fileNames+".csv"))

  tru = effiPd['true'].values.tolist()
  opt = effiPd['optimal'].values.tolist()
  std = effiPd['backpack'].values.tolist()
  rel = effiPd['backpack_relaxed'].values.tolist()

  time_opt = timePd['optimal'].values.tolist()
  time_std = timePd['backpack'].values.tolist()
  time_rel = timePd['backpack_relaxed'].values.tolist()

  beginning = effiPd['Unnamed: 0'].values[-1]

files = os.listdir(args.input_dir)
files.sort()

for idx, input in enumerate(files):
    
    if idx < beginning:
       continue

    print(bcolors.WARNING + "Progress: " + str(round(100 * (idx+1)/len(os.listdir(args.input_dir)),2))+"%   " + input)

    jsonArr = DataLoader.loadData(os.path.join(args.input_dir, input))
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

    ampl = AmplSolver.AmplSolver()
    fileList = ampl.prepareDataFiles(os.path.join(args.input_dir, input))
    tmpOpt = []

    start = time.time()
    for entry in fileList:
        ampl = AmplSolver.AmplSolver()
        tmpOpt.append(ampl.solve(entry))

    opt.append(sum(tmpOpt)/len(tmpOpt))
    time_opt.append("{:.4f}".format((time.time() - start)/len(tmpOpt),5))

    tru.append(jsonArr[0]["optimal_solution"])

    if idx % 3 == 0:
      save(tru, opt, std, rel, time_opt, time_std, time_rel)

save(tru, opt, std, rel, time_opt, time_std, time_rel)

