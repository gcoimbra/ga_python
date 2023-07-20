import math
from abc import ABC, abstractmethod
from typing import Iterable, List

import numpy
import sklearn.preprocessing
from matplotlib import pyplot as plt


class Problem(ABC):
    nVariables: int
    name: str
    maxSpeed: int
    lowLimit: List[int]
    highLimit: List[int]
    maxIterations: int

    def fitness(self, solution: numpy.ndarray) -> float:
        obj = self.objective(solution)

        return sum(self.restrictions(solution)) ** 2 + obj

    def plot(self, step: int):
        assert self.nVariables == 2
        I = numpy.linspace(self.lowLimit[0], self.highLimit[0], step)
        J = numpy.linspace(self.lowLimit[1], self.highLimit[1], step)
        mat = numpy.zeros((len(I), len(J)))

        for i, ival in enumerate(I):
            for j, jval in enumerate(J):
                solution = numpy.array((ival, jval,))
                restr = sum(self.restrictions(solution))
                if restr > 0:
                    obj = 0
                else:
                    obj = self.objective(solution)
                mat[i][j] = obj

        z = sklearn.preprocessing.MinMaxScaler() \
            .fit_transform(numpy.array(mat.flatten()).reshape(-1, 1))
        z = list(map(lambda x: (x, x, 0), z.flatten()))
        z = numpy.array(z).reshape(step, step, 3)
        fig, ax = plt.subplots()
        ax.imshow(z)
        # ax.set_xticks(range(10))
        ax.set_xticklabels(numpy.round(I,3)[::10])
        ax.set_yticklabels(numpy.round(J,3)[::10])

        plt.show()

    @abstractmethod
    def restrictions(self, solution: numpy.ndarray) -> Iterable[float]:
        pass

    @abstractmethod
    def objective(self, solution: numpy.ndarray):
        pass

    def info(self) -> None:
        print(self.__dict__)


class Trelica(Problem):
    _SIGMA: float = 2
    _L: float = 100
    _P: float = 2
    maxSpeed = 1
    name = "Treliça"
    nVariables = 2
    maxIterations = 40
    lowLimit = [0, 0]
    highLimit = [1, 1]

    def restrictionValues(self, solution):
        twoRoot = math.sqrt(2)

        rest1 = (twoRoot * solution[0] + solution[1]) * self._P / \
                (twoRoot * solution[0] ** 2 + 2
                 * solution[0] * solution[
                     1]) - self._SIGMA
        rest2 = (solution[1]) * self._P / (
            twoRoot * solution[0] ** 2 + 2
            * solution[0] * solution[
                1]) - self._SIGMA
        rest3 = self._P / (twoRoot * solution[1] +
                           solution[0]) - self._SIGMA
        return rest1, rest2, rest3

    def restrictions(self, solution: numpy.ndarray) -> Iterable[float]:
        twoRoot = math.sqrt(2)

        rest1 = (twoRoot * solution[0] + solution[1]) * self._P / \
                (twoRoot * solution[0] ** 2 + 2
                 * solution[0] * solution[
                     1]) - self._SIGMA
        rest2 = (solution[1]) * self._P / (
            twoRoot * solution[0] ** 2 + 2
            * solution[0] * solution[
                1]) - self._SIGMA
        rest3 = self._P / (twoRoot * solution[1] +
                           solution[0]) - self._SIGMA
        return (
            0 if rest1 < 0 else 100 * rest1 + 100,
            0 if rest1 < 0 else 100 * rest2 + 100,
            0 if rest1 < 0 else 100 * rest3 + 100,
            # Restrição 0 <= x1 <= 1
            0 if (0 <= solution[0] <= 1) else 100 + abs(solution[0]) * 100,
            # Restrição 0 <= x2 <= 1
            0 if (0 <= solution[1] <= 1) else 100 + abs(solution[1]) * 100,
        )

    def objective(self, solution: numpy.ndarray) -> float:
        return (2 * math.sqrt(2) * solution[0] + solution[1]) * self._L


class EggHolder(Problem):
    nVariables = 2
    name = "Vaso"
    maxSpeed = 50
    maxIterations = 500
    lowLimit = [-512, -512]
    highLimit = [512, 512]

    def restrictionValues(self, solution):
        return [0]

    def restrictions(self, solution: numpy.ndarray) -> Iterable[float]:
        return (0 if (-512 <= solution[0] <= 512) else 100 * abs(solution[0]) + 100,
                0 if (-512 <= solution[1] <= 512) else 100 * abs(solution[1]) + 100)

    def objective(self, solution: numpy.ndarray):
        x = solution[0]
        y = solution[1]
        return -((y + 47) * math.sin(math.sqrt(abs((x / 2) + (y + 47))))) - \
               (x * math.sin(math.sqrt(abs(x - (y + 47)))))


class Paredao(Problem):
    nVariables = 2
    name = "Vaso"
    maxSpeed = 5
    maxIterations = 500
    lowLimit = [-10, -10]
    highLimit = [10, 10]

    def restrictionValues(self, solution):
        return [0]

    def restrictions(self, solution: numpy.ndarray) -> Iterable[float]:
        return (0 if (-10 <= solution[0] <= 10) else 100 * abs(solution[0]) + 100,
                0 if (-10 <= solution[1] <= 10) else 100 * abs(solution[1]) + 100)

    def objective(self, solution: numpy.ndarray):
        x = solution[0]
        y = solution[1]
        return -0.0001 * (abs(math.sin(x) * math.sin(y) * math.exp(
            abs(100 - math.sqrt(x ** 2 + y ** 2) / math.pi))) + 1) ** 0.1


class Vaso(Problem):
    nVariables = 4
    name = "Vaso de Pressão"
    maxSpeed = 10
    maxIterations = 100
    lowLimit = [0, 0, 10, 10]
    highLimit = [100, 100, 200, 200]

    def restrictionValues(self, solution: numpy.ndarray):
        rest1 = -solution[0] + 0.0193 * solution[2]
        rest2 = - solution[1] + 0.00954 * solution[2]
        rest3 = - math.pi * solution[2] ** 2 * solution[3] - 4 / 3 * math.pi * solution[
            2] ** 3 + 1296000
        rest4 = solution[3] - 240
        return rest1, rest2, rest3, rest4

    def restrictions(self, solution: numpy.ndarray) -> Iterable[float]:

        # Restrição 10 <= xi <= 200, i =3,4
        if solution[3] < 10:
            restrictionX3 = 10 - solution[3]
        elif solution[3] > 200:
            restrictionX3 = solution[3] - 200
        else:
            restrictionX3 = 0

        if solution[2] < 10:
            restrictionX4 = (10 - solution[2])
        elif solution[2] > 200:
            restrictionX4 = solution[2] - 200
        else:
            restrictionX4 = 0

        rest1 = -solution[0] + 0.0193 * solution[2]
        rest2 = - solution[1] + 0.00954 * solution[2]
        rest3 = - math.pi * solution[2] ** 2 * solution[3] - 4 / 3 * math.pi * solution[
            2] ** 3 + 1296000
        rest4 = solution[3] - 240
        return (
            0 if rest1 < 0 else 100 * rest1 + 100,
            0 if rest2 < 0 else 100 * rest2 + 100,
            0 if rest3 < 0 else 100 * rest3 + 100,
            0 if rest4 < 0 else 100 * rest4 + 100,

            # Restrição 0 <= xi <= 100, i =1,2
            0 if (0 <= solution[0] <= 100) else 100 * abs(solution[0]) + 100,
            0 if (0 <= solution[1] <= 100) else 100 * abs(solution[1]) + 100,
            restrictionX3,
            restrictionX4
        )


    def objective(self, solution: numpy.ndarray) -> float:
        return 0.6224 * solution[0] * solution[2] * solution[3] \
               + 1.7781 * solution[1] * (solution[2] ** 2) \
               + 3.1661 * (solution[0] ** 2) * solution[3] \
               + 19.84 * (solution[0] ** 2) * solution[2]
