from enum import Enum

# -----------------------------
# Constraint: Tube / Mandrel Diameters
# -----------------------------
class TubeDiameter(Enum):
    D4pt5IN = 0.1143  # 4.5 inch OD, meters
    D5pt5IN = 0.1397  # 5.5 inch OD, meters
    D6pt0IN = 0.1524  # 6.0 inch OD, meters

    @property
    def radius(self) -> float:
        return self.value / 2
    
    @property
    def area(self) -> float:
        """Frontal reference area (m^2)."""
        import math
        return math.pi * (self.value/2)**2


# -----------------------------
# Constraint: Materials (structural options)
# -----------------------------
class Material(Enum):
    ALUMINUM = ("Aluminum 6061-T6", 2700)   # kg/m³
    CARBON_FIBER = ("Carbon Fiber/Epoxy", 1600)
    FIBERGLASS = ("Fiberglass/Epoxy", 1850)
    #TODO: add 3d printed pla for nosecone?
    # 3D printed inconel 

    def __init__(self, fullname, density):
        self.fullname = fullname
        self.density = density

    @property
    def rho(self) -> float:
        """Density in kg/m^3."""
        return self.density

# -----------------------------
# Nosecone shapes (RocketPy supported)
# -----------------------------
class NoseconeType(Enum):
    VON_KARMAN = "vonKarman"
    CONICAL = "conical"
    OGIVE = "ogive"
    LV_HAACK = "lvHaack"
    POWER_SERIES = "powerSeries"


# -----------------------------
# Fin profiles (RocketPy supported)
# -----------------------------
class FinType(Enum):
    TRAPEZOIDAL = "trapezoidal"


# -----------------------------
# Fin airfoils (RocketPy supported)
# -----------------------------
class FinAirfoil(Enum):
    DIAMOND = "diamond"
    FLATPLATE = "flatplate"


# -----------------------------
# Tailcone / Boattail options
# -----------------------------
class TailType(Enum):
    NONE = "none"
    CONICAL = "conical"

csys = "nose_to_tail"
pro98_len = 1 #[m] TODO: fill in w real val

