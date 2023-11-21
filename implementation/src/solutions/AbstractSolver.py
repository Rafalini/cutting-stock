from abc import ABC, abstractmethod

class AbstractSolver(ABC):
    @abstractmethod
    def solve(self, inputRods, factoryRodSize = 12, relaxation=False):
        pass