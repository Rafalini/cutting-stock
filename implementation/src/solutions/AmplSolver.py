from solutions.AbstractSolver import AbstractSolver
from amplpy import AMPL
import DataLoader, os
from amplpy import amplpython

class OutputHandler(amplpython.OutputHandler): #supress ampl logs
    def output(self, kind, msg):
       pass

class AmplSolver(AbstractSolver):
    
    def __init__(self):
        self.workingDir = "ampl_working_dir"
        if not os.path.exists(self.workingDir):
            os.makedirs(self.workingDir)
        self.solver = AMPL()
        self.solver.set_output_handler(OutputHandler())
        self.solver.option['solver'] = 'cplex'

    def reset(self):
        self.solver.reset()

    def prepareData(self, inputOrder, outputFile):

        with open(outputFile, "w") as outfile:
            outfile.write("""
data;
param rawBarWidth := """)
            outfile.write(str(inputOrder["factory_rod_size"]))
            outfile.write(""";
param: ORDERS: widths  barsNum  maxRelax :=
""")
            i = 1
            for order in inputOrder["relaxedOrder"]:
                if order["relaxation_number"] > 0:
                    outfile.write(str(i)+" "+str(order["rod_size"]) +" "+str(order["relaxation_number"]) +" "+ str(order["relaxation_length"])+"\n")
                    i+=1
                    order["rods_number"]-=order["relaxation_number"]
                if order["rods_number"] > 0:
                    outfile.write(str(i)+" "+str(order["rod_size"]) +" "+ str(order["rods_number"]) +" 0\n")
                    i+=1
            outfile.write(";")
        return 0

    def solve(self, inputFile):
        dataModelString = """
                            model {modelFile};
                            data {dataFile};
        """.format(dataFile=inputFile, modelFile="ampl/cut.mod")
        
        self.solver.eval(dataModelString+r"""
            option solver cplex;
            option solution_round 6;

            problem Cutting_Opt: Cut, Number, Fill;
            option relax_integrality 1;
            option presolve 0;

            problem Pattern_Gen: Use, Relax, ReducedCost, WidthLimit, RelaxLimit;
            option relax_integrality 0;
            option presolve 1;

            #let relaxCost := 100; #uncomment to solve without relax
            let nPAT := 0;
            #setting up one pattern for every width
            for {i in ORDERS} 
            {			
                let nPAT := nPAT + 1;
                let wfep[i,nPAT] := floor (rawBarWidth/widths[i]);
                let {i2 in ORDERS: i2 <> i} wfep[i2,nPAT] := 0;
                let {i2 in ORDERS} rfep[i2,nPAT] := 0;
            };

            repeat
            {
                solve Cutting_Opt;

                #new price is a cost in raw bars associated with incrementing orders by 1 for every width
                let {i in ORDERS} price[i] := Fill[i].dual;

                solve Pattern_Gen;
                    
                if ReducedCost > 0.00001 then 
                {
                    let nPAT := nPAT + 1;
                    let {i in ORDERS} wfep[i,nPAT] := Use[i];
                    let {i in ORDERS} rfep[i,nPAT] := Relax[i];
                }
                else
                    break;
            };

            option Cutting_Opt.relax_integrality 0;
            option Cutting_Opt.presolve 10;
            solve Cutting_Opt;
        """)
        
        return self.solver.get_objective("Number").value()
    

    def prepareDataFiles(self, inputFile):
        data = DataLoader.loadData(inputFile)

        fileList = []
        for idx, entry in enumerate(data):
            fileName = os.path.join(self.workingDir, str(idx) + ".dat")
            fileList.append(fileName)
            self.prepareData(entry, fileName)

        return fileList
