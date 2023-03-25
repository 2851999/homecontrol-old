from dataclasses import dataclass
from typing import Dict


@dataclass
class HueColour:
    """
    Stores a colour in the Hue format
    """

    # pylint:disable=invalid-name
    x: float
    y: float

    @staticmethod
    def from_dict(data: Dict):
        """
        Returns a colour from its dictionary value
        """
        return HueColour(data["x"], data["y"])

    @staticmethod
    # pylint:disable=invalid-name
    def from_rgb(r: float, g: float, b: float):
        """
        Converts an RGB colour into and xy one in the
        CIE color space as Hue expects
        """
        X = 0.412453 * r + 0.357580 * g + 0.180423 * b
        Y = 0.212671 * r + 0.715160 * g + 0.072169 * b
        Z = 0.019334 * r + 0.119193 * g + 0.950227 * b
        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)
        return HueColour(x=x, y=y)
