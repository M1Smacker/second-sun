"""Fixed circular, edge-on orbit geometry for the preregistered P bench."""
from dataclasses import dataclass
import math

from scipy.optimize import brentq


@dataclass(frozen=True)
class Orbit:
    binary_period: float
    binary_epoch: float
    planet_period: float
    planet_epoch: float

    def crossings(self, start, end):
        """Return primary-star centre and limb-to-limb duration in days."""
        # Kepler scaling in AU and days. Project the secondary-mass fraction.
        a1 = (1.5 * (self.binary_period / 365.25) ** 2) ** (1 / 3) / 3
        ap = (1.5 * (self.planet_period / 365.25) ** 2) ** (1 / 3)
        radius = .00465047  # nominal solar radius in AU

        def separation(t):
            return ap * math.sin(math.tau * (t - self.planet_epoch) / self.planet_period) - a1 * math.sin(
                math.tau * (t - self.binary_epoch) / self.binary_period)

        # At either endpoint the planet lies beyond the projected stellar limb.
        half = math.asin((a1 + radius) / ap) * self.planet_period / math.tau
        first = math.ceil((start - half - self.planet_epoch) / self.planet_period)
        last = math.floor((end + half - self.planet_epoch) / self.planet_period)
        for cycle in range(first, last + 1):
            anchor = self.planet_epoch + cycle * self.planet_period
            low, high = anchor - half - 1e-8, anchor + half + 1e-8
            centre = brentq(separation, low, high)
            left = brentq(lambda t: separation(t) + radius, low, centre)
            right = brentq(lambda t: separation(t) - radius, centre, high)
            if right >= start and left <= end:
                yield centre, right - left
