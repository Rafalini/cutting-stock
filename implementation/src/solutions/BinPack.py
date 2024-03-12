from solutions.AbstractSolver import AbstractSolver

class BinPacker(AbstractSolver):
    def getOrderLengths(self, rodList, relaxation):
        lengths = []
        lengths = []
        for i in rodList:
            if relaxation:
                shorten = i["rod_size"] - i["relaxation_length"]
                lengths = lengths + [shorten for _ in range(i["relaxation_number"])]
                rest = i["rods_number"] - i["relaxation_number"]
                lengths = lengths + [i["rod_size"]  for _ in range(rest)]
            else:
                lengths = lengths + [i["rod_size"] for _ in range(i["rods_number"])]
        return lengths

class StandardBinPackSolver(BinPacker):

    def solve(self, rodList, factoryRodSize, relaxation):
        res = 0
        inputRods = self.getOrderLengths(rodList, relaxation)

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