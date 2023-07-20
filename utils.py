import math


def constriction_factor(cognitiveFactor: float, socialFactor: float) -> float:
    tau = cognitiveFactor + socialFactor

    return 2 / abs(2 - tau - math.sqrt(tau ** 2 - 4 * tau))


def inertia_weight(WMin: float, WMax: float,
                   maxIterations: int, iteration: int) -> float:
    return WMax - (WMax - WMin) * iteration / maxIterations


