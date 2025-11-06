import numpy as np 
from dataclasses import dataclass, field
from typing import List, Tuple 





@dataclass
class SpectralSubtype:
    label: str
    temp: float       
    MS_mass: float 





@dataclass
class SpectralType:
    letter: str
    temp_range: Tuple[float, float]       # (min, max) in Kelvin
    MS_mass_range: Tuple[float, float]
    subtypes: List[SpectralSubtype] = field(default_factory=list)

    @property
    def temp_midpoint(self) -> float:
        a, b = self.temp_range
        return np.sqrt(a * b)

    @property
    def mass_midpoint(self) -> float:
        a, b = self.MS_mass_range
        return np.sqrt(a * b)
    




# From Pecaut & Mamajek (2013) mean dwarf MS data (Teff, Msun) https://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt 

_O = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["O3V", "O4V", "O5V", "O5.5V", "O6V", "O6.5V", "O7V", "O7.5V", "O8V", "O8.5V", "O9V", "O9.5V"],
        [ 44900, 42900, 41400, 40500,   39500, 38300,   37100, 36100,   35100, 34300,   33300, 31900],
        [ 59.0,  48.0,  43.0,  38.0,    35.0,  31.0,    28.0,  26.0,    23.6,  21.9,    20.2,  18.7],
    )
]

_B = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["B0V", "B0.5V", "B1V", "B1.5V", "B2V", "B2.5V", "B3V", "B4V", "B5V", "B6V", "B7V", "B8V", "B9V", "B9.5V"],
        [ 31400, 29000,   26000, 24500,   20600, 18500,   17000, 16400, 15700, 14500, 14000, 12300, 10700, 10400],
        [ 17.7,  14.8,    11.8,  9.9,     7.3,   6.1,     5.4,   5.1,   4.7,   4.3,   3.92,  3.38,  2.75,  2.68],
    )
]

_A = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["A0V", "A1V", "A2V", "A3V", "A4V", "A5V", "A6V", "A7V", "A8V", "A9V"],
        [ 9700,  9300,  8800,  8600,  8250,  8100,  7910,  7760,  7590,  7400],
        [ 2.18,  2.05,  1.98,  1.93,  1.88,  1.86,  1.83,  1.81,  1.77,  1.75],
    )
]

_F = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["F0V", "F1V", "F2V", "F3V", "F4V", "F5V", "F6V", "F7V", "F8V", "F9V", "F9.5V"],
        [ 7220,  7020,  6820,  6750,  6670,  6550,  6350,  6280,  6180,  6050,  5990],
        [ 1.61,  1.50,  1.46,  1.44,  1.38,  1.33,  1.25,  1.21,  1.18,  1.13,  1.08],
    )
]

_G = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["G0V", "G1V", "G2V", "G3V", "G4V", "G5V", "G6V", "G7V", "G8V", "G9V"],
        [ 5930,  5860,  5770,  5720,  5680,  5660,  5600,  5550,  5480,  5380],
        [ 1.06,  1.03,  1.00,  0.99,  0.985, 0.98,  0.97,  0.95,  0.94,  0.90],
    )
]

_K = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["K0V", "K1V", "K2V", "K3V", "K4V"," K5V", "K6V", "K7V", "K8V", "K9V"],
        [ 5270,  5170,  5100,  4830,  4600,  4440,  4300,  4100,  3990,  3930],
        [ 0.88,  0.86,  0.82,  0.78,  0.73,  0.70,  0.69,  0.64,  0.62,  0.59],
    )
]

_M = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["M0V", "M0.5V", "M1V", "M1.5V", "M2V", "M2.5V", "M3V", "M3.5V", "M4V", "M4.5V", "M5V", "M5.5V", "M6V", "M6.5V", "M7V", "M7.5V", "M8V", "M8.5V", "M9V", "M9.5V"],
        [ 3850,  3770,    3660,  3620,    3560,  3470,    3430,  3270,    3210,  3110,    3060,  2930,    2810,  2740,    2680,  2630,    2570,  2420,    2380,  2350],
        [ 0.57,  0.544,   0.50,  0.482,   0.44,  0.421,   0.37,  0.300,   0.23,  0.217,   0.162, 0.156,   0.137, 0.126,   0.120, 0.116,   0.114, 0.104,   0.102, 0.101],
    )
] 

_L = [
    SpectralSubtype(label=label, temp=t, MS_mass=None)
    for label, t in zip(
        ["L0V", "L1V", "L2V", "L3V", "L4V", "L5V", "L6V", "L7V", "L8V", "L9V"],
        [ 2270,  2160,  2060,  1920,  1870,  1710,  1550,  1530,  1420,  1370],
    )
]

_T = [
    SpectralSubtype(label=label, temp=t, MS_mass=None)
    for label, t in zip(
        ["T0V", "T1V", "T2V", "T3V", "T4V", "T4.5V", "T5V", "T5.5V", "T6V", "T7V", "T7.5V", "T8V", "T9V"],
        [ 1255,  1240,  1220,  1200,  1180,  1170,    1160,  1040,    950,   825,   750,     680,   560],
    )
]

_Y = [
    SpectralSubtype(label=label, temp=t, MS_mass=None)
    for label, t in zip(
        ["Y0V", "Y0.5V", "Y1V", "Y1.5V", "Y2V", "Y4V"],
        [ 450,   400,     360,    325,    320,   250],
    )
]





SPECTRAL_TYPES: List[SpectralType] = [
    SpectralType(letter="O", temp_range=(31_650, 999_999_999_999), MS_mass_range=(18.2, 300),  subtypes=_O),
    SpectralType(letter="B", temp_range=(10_000, 31_650),          MS_mass_range=(2.33, 18.2), subtypes=_B),
    SpectralType(letter="A", temp_range=(7_300, 10_000),           MS_mass_range=(1.68, 2.33), subtypes=_A),
    SpectralType(letter="F", temp_range=(5_960, 7_300),            MS_mass_range=(1.07, 1.68), subtypes=_F),
    SpectralType(letter="G", temp_range=(5_330, 5_960),            MS_mass_range=(0.89, 1.07), subtypes=_G),
    SpectralType(letter="K", temp_range=(3_890, 5_330),            MS_mass_range=(0.58, 0.89), subtypes=_K),
    SpectralType(letter="M", temp_range=(2_310, 3_890),            MS_mass_range=(0.1, 0.58),  subtypes=_M),
]
