import copy
import os
import random
from typing import Sequence, List

import cv2
import numpy
import scipy.linalg
from matplotlib import pyplot

import problems
from utils import constriction_factor, inertia_weight

cognitiveFactor: float = 2
socialFactor: float = 2
WMin: float = 0.4
WMax: float = 0.9
nParticles: int = 200


# TODO: lbest
class _Particle:
    position: numpy.ndarray
    positionFitness: float
    speed: numpy.ndarray
    bestPosition: numpy.ndarray
    bestPositionFitness: float

    def __init__(self, problem: problems.Problem):
        self.position = numpy.random.uniform(problem.lowLimit,
                                             problem.highLimit,
                                             problem.nVariables)
        self.bestPosition =  numpy.random.uniform(problem.lowLimit,
                                             problem.highLimit,
                                             problem.nVariables)

        if problem.name == "Vaso de Pressão":
            self.position[0] = numpy.ceil(self.position[0]) * 0.0625
            self.position[1] = numpy.ceil(self.position[1]) * 0.0625
            self.bestPosition[0] = numpy.ceil(self.bestPosition[0] * 20) * 0.0625
            self.bestPosition[1] = numpy.ceil(self.bestPosition[1] * 20) * 0.0625

        self.positionFitness = problem.fitness(self.position)
        self.speed = numpy.random.random(problem.nVariables)
        self.bestPositionFitness = problem.fitness(self.bestPosition)

    def info(self):
        print({k: numpy.round(v, 1) for k, v in self.__dict__.items()})

    # POSSIBLE OPTIMIZATION: this could be a matrix. update all with matrix
    # operations
    def update(self, groupBestPosition: numpy.ndarray,
               iteration: int, problem: problems.Problem) -> numpy.ndarray:
        inertia = self.speed
        cognitive = self.bestPosition - self.position
        social = numpy.subtract(groupBestPosition, self.position)
        randomFactor1 = random.random()
        randomFactor2 = random.random()

        self.speed = constriction_factor(cognitiveFactor, socialFactor) * \
                     (inertia_weight(WMin, WMax, problem.maxIterations,
                                     iteration) * inertia +
                      randomFactor1 * cognitiveFactor * cognitive +
                      randomFactor2 * socialFactor * social)

        while scipy.linalg.norm(self.speed) > problem.maxSpeed:
            self.speed /= 2

        if problem.name == "Vaso de Pressão":  # Gambiarra, talvez fazer um metodo
            # update no problem
            self.position[0] += numpy.ceil(
                self.speed[0] * random.randint(1, 10)) * 0.0625
            self.position[1] += numpy.ceil(
                self.speed[1] * random.randint(1, 10)) * 0.0625
            self.position[2:] += self.speed[2:]
        else:
            self.position += self.speed

        self.positionFitness = problem.fitness(self.position)

        if self.positionFitness < self.bestPositionFitness:
            self.bestPosition = self.position
            self.bestPositionFitness = self.positionFitness

        return self.bestPosition


class PSO:
    particles: Sequence[_Particle]
    problem: problems.Problem
    iteration: int
    groupBestPosition: numpy.ndarray
    groupBestPositionFitness: float
    fitnessEvolution: List[float]

    def _update_best_group_position(self):
        for particle in self.particles:
            if particle.bestPositionFitness < self.groupBestPositionFitness:
                self.groupBestPositionFitness = particle.bestPositionFitness
                self.groupBestPosition = particle.bestPosition
        self.fitnessEvolution.append(self.problem.objective(self.groupBestPosition))

    def __init__(self, problem: problems.Problem):
        self.iteration = 0
        self.fitnessEvolution = []
        self.problem = problem
        self.particles = [_Particle(self.problem) for _ in range(nParticles)]

        self.groupBestPositionFitness = self.particles[0].bestPositionFitness
        self.groupBestPosition = self.particles[0].bestPosition
        self._update_best_group_position()

    def solve(self):
        for _ in range(self.problem.maxIterations):
            self.iterate()

    def iterate(self):
        a = copy.deepcopy(self.groupBestPosition)
        for particle in self.particles:
            particle.update(self.groupBestPosition, self.iteration,
                            self.problem)
        self.groupBestPosition = a
        self._update_best_group_position()
        self.iteration += 1

    def info(self):
        print(self.__dict__)
        self.problem.info()
        for i, particle in enumerate(self.particles):
            print("Particula", i)
            particle.info()
            print("\n")

    def plot(self):
        fig, ax = pyplot.subplots()
        X = [particle.position[0] for particle in self.particles]
        Y = [particle.position[1] for particle in self.particles]

        XVec = [particle.speed[0] for particle in self.particles]
        YVec = [particle.speed[1] for particle in self.particles]

        # Plot group best position XY
        ax.plot(self.groupBestPosition[0], self.groupBestPosition[1], 'go')
        # PLot arrow
        ax.quiver(X, Y, XVec, YVec)
        # Plot birds
        ax.scatter(X, Y)

        ax.text(0.05, 0.95, f"Iteration {str(self.iteration)} \n"
                            f"Best"
                            f"Pos "
                            f"{str(numpy.round(self.groupBestPosition, 2))} \n"
                            f"BestFitness "
                            f"{str(round(self.groupBestPositionFitness))}\n"
                            f"BestObj "
                            f"BestRestriction"
                            f"{[str(round(x)) for x in  self.problem.restrictions(self.groupBestPosition)]}",

                transform=ax.transAxes, bbox=dict(boxstyle='round',
                                                  facecolor='wheat', alpha=0.5))
        # Plot bird label
        for i, (x, y) in enumerate(zip(X, Y)):
            ax.annotate(str(i), (x + (0.05 * x), y), )

        ax.set_xlim(0,5)
        ax.set_ylim(0, 5)

        return fig

    def movie(self, frames: int, step: int):
        for frame in range(frames):
            self.plot().savefig(f"{str(frame)}.png")
            self.iterate()

        images = sorted([img for img in os.listdir() if img.endswith(".png")],
                        key=lambda x: int(x.split('.')[0]))
        frame = cv2.imread(images[0])
        # noinspection Mypy
        height, width, layers = frame.shape

        video = cv2.VideoWriter('video.avi', 0, step, (width, height))

        for image in images:
            video.write(cv2.imread(image))

        cv2.destroyAllWindows()
        video.release()
