from solutions.AbstractSolver import AbstractSolver

class BinPacker(AbstractSolver):
    def getOrderLengths(self, jsonFile):
        lengths = []
        lengths = []
        for i in jsonFile["order"]:
            for j in range(i["rods_number"]):
                lengths.append(i["rod_size"])
        return lengths


    def getRelaxedOrderLengths(self, jsonFile):
        lengths = []
        for i in jsonFile["relaxedOrder"]:
            for j in range(i["relaxation_number"]):
                lengths.append(i["rod_size"] - i["relaxation_length"])
            for j in range(i["rods_number"] - i["relaxation_number"]):
                lengths.append(i["rod_size"])
        return lengths


class StandardBinPackSolver(BinPacker):

    def solve(self, inputJsonDict, factoryRodSize=12, relaxation=False):
        res = 0
        if relaxation:
            inputRods = self.getRelaxedOrderLengths(inputJsonDict)
        else:
            inputRods = self.getOrderLengths(inputJsonDict)

        # Create an array to store remaining space in bins
        bin_rem = [0] * len(inputRods)
        for i in range(len(inputRods)):
            # Find the first bin that can accommodate inputRods[i]
            j = 0
            min = factoryRodSize + 1
            bi = 0

            for j in range(res):
                if (bin_rem[j] >= inputRods[i] and bin_rem[j] - inputRods[i] < min):
                    bi = j
                    min = bin_rem[j] - inputRods[i]

            # If no bin could accommodate inputRods[i],
            # create a new bin
            if (min == factoryRodSize + 1):
                bin_rem[res] = factoryRodSize - inputRods[i]
                res += 1
            else:  # Assign the item to best bin
                bin_rem[bi] -= inputRods[i]
        return res