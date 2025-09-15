# import numpy as np 
# from dataclasses import dataclass





# # Define all isotopes (hydrogen, helium, etc) for use with composition plots (both profile data and history data)

# @dataclass
# class Isotope:
#     """Represents an isotope with its plotting properties."""
#     profile_key: str                        # The attribute name in the MESA profile (e.g., "profile.h1") 
#     history_key: str                        # The attribute name in the MESA history (e.g., "history.center_h1")
#     label: str                              # The label for the plot legend (e.g., 'Hydrogen')
#     color: str                              # The color for the plot line 
#     show_initial_abundance: bool = False    # Include a horizontal dashed line to profile plots to indicate the initial abundance of this element? 

# ISOTOPES = [ 
#     Isotope(profile_key="h1",   history_key="center_h1",   label="Hydrogen",     color="tab:blue", show_initial_abundance=True), 
#     Isotope(profile_key="he3",  history_key="center_he3",  label="Helium 3",     color="tab:orange"), 
#     Isotope(profile_key="he4",  history_key="center_he4",  label="Helium 4",     color="tab:green", show_initial_abundance=True), 
#     Isotope(profile_key="c12",  history_key="center_c12",  label="Carbon 12",    color="tab:red"), 
#     Isotope(profile_key="n14",  history_key="center_n14",  label="Nitrogen 14",  color="tab:purple"), 
#     Isotope(profile_key="o16",  history_key="center_o16",  label="Oxygen 16",    color="tab:brown"), 
#     Isotope(profile_key="ne20", history_key="center_ne20", label="Neon 20",      color="tab:pink"), 
#     Isotope(profile_key="mg24", history_key="center_mg24", label="Magnesium 24", color="tab:grey"), 
#     Isotope(profile_key="si28", history_key="center_si28", label="Silicon 28",   color="tab:olive"), 
#     Isotope(profile_key="s32",  history_key="center_s32",  label="Sulfur 32",    color="tab:cyan"), 
#     Isotope(profile_key="ar36", history_key="center_ar36", label="Argon 36",     color="mediumblue"), 
#     Isotope(profile_key="ca40", history_key="center_ca40", label="Calcium 40",   color="orange"), 
#     Isotope(profile_key="ti44", history_key="center_ti44", label="Titanium 44",  color="mediumspringgreen"), 
#     Isotope(profile_key="cr48", history_key="center_cr48", label="Chromium 48",  color="maroon"), 
#     Isotope(profile_key="fe52", history_key="center_fe52", label="Iron 52",      color="mediumslateblue"), 
#     Isotope(profile_key="fe54", history_key="center_fe54", label="Iron 54",      color="saddlebrown"), 
#     Isotope(profile_key="fe56", history_key="center_fe56", label="Iron 56",      color="magenta"), 
#     Isotope(profile_key="ni56", history_key="center_ni56", label="Nickel 56",    color="black"), 
# ]  





# # Define all spectral types for use with HR diagram plots 
# @dataclass
# class SpectralType: 
#     """Represents a Spectral Type (O, B, etc) with its plotting properties.""" 
#     letter: str             # "O", "B", "A" "F", "G", "K", or "M" 
#     temp_range: tuple       # (lower bound, upper bound)    # From: https://en.wikipedia.org/wiki/Stellar_classification#Harvard_spectral_classification 
#     MS_mass_range: tuple    # (lower bound, upper bound)    # From: https://en.wikipedia.org/wiki/Stellar_classification#Harvard_spectral_classification 
#     color: str              # Color used to represent this region on HR diagram 

#     @property
#     def temp_midpoint(self) -> int: 
#         midpoint = np.sqrt(self.temp_range[1]*self.temp_range[0]) 
#         if np.isfinite(midpoint) == False: 
#             midpoint = 1.2*self.temp_range[0] 
#         return midpoint 

#     @property 
#     def mass_midpoint(self) -> float: 
#         midpoint = np.sqrt(self.MS_mass_range[1]*self.MS_mass_range[0])
#         if np.isfinite(midpoint) == False: 
#             midpoint = 1.2*self.MS_mass_range[0] 
#         return midpoint 



# SPECTRAL_TYPES = [ 
#     SpectralType(letter="O", temp_range=(33_000, 99999999), MS_mass_range=(16, 99999999), color="black"), 
#     SpectralType(letter="B", temp_range=(10_000, 33_000),   MS_mass_range=(2.1, 16),      color="white"), 
#     SpectralType(letter="A", temp_range=(7_300, 10_000),    MS_mass_range=(1.4, 2.1),     color="black"), 
#     SpectralType(letter="F", temp_range=(6_000, 7_300),     MS_mass_range=(1.04, 1.4),    color="white"), 
#     SpectralType(letter="G", temp_range=(5_300, 6_000),     MS_mass_range=(0.8, 1.04),    color="black"), 
#     SpectralType(letter="K", temp_range=(3_900, 5_300),     MS_mass_range=(0.45, 0.8),    color="white"), 
#     SpectralType(letter="M", temp_range=(2_300, 3_900),     MS_mass_range=(0.08, 0.45),   color="black"), 
# ]














import numpy as np
from dataclasses import dataclass

# ==============================================================================
# ISOTOPE DATA (No changes needed here)
# ==============================================================================

# Define all isotopes (hydrogen, helium, etc) for use with composition plots (both profile data and history data)

@dataclass
class Isotope:
    """Represents an isotope with its plotting properties."""
    profile_key: str                        # The attribute name in the MESA profile (e.g., "profile.h1") 
    history_key: str                        # The attribute name in the MESA history (e.g., "history.center_h1")
    label: str                              # The label for the plot legend (e.g., 'Hydrogen')
    color: str                              # The color for the plot line 
    show_initial_abundance: bool = False    # Include a horizontal dashed line to profile plots to indicate the initial abundance of this element? 

ISOTOPES = [ 
    Isotope(profile_key="h1",   history_key="center_h1",   label="Hydrogen",     color="tab:blue", show_initial_abundance=True), 
    Isotope(profile_key="he3",  history_key="center_he3",  label="Helium 3",     color="tab:orange"), 
    Isotope(profile_key="he4",  history_key="center_he4",  label="Helium 4",     color="tab:green", show_initial_abundance=True), 
    Isotope(profile_key="c12",  history_key="center_c12",  label="Carbon 12",    color="tab:red"), 
    Isotope(profile_key="n14",  history_key="center_n14",  label="Nitrogen 14",  color="tab:purple"), 
    Isotope(profile_key="o16",  history_key="center_o16",  label="Oxygen 16",    color="tab:brown"), 
    Isotope(profile_key="ne20", history_key="center_ne20", label="Neon 20",      color="tab:pink"), 
    Isotope(profile_key="mg24", history_key="center_mg24", label="Magnesium 24", color="tab:grey"), 
    Isotope(profile_key="si28", history_key="center_si28", label="Silicon 28",   color="tab:olive"), 
    Isotope(profile_key="s32",  history_key="center_s32",  label="Sulfur 32",    color="tab:cyan"), 
    Isotope(profile_key="ar36", history_key="center_ar36", label="Argon 36",     color="mediumblue"), 
    Isotope(profile_key="ca40", history_key="center_ca40", label="Calcium 40",   color="orange"), 
    Isotope(profile_key="ti44", history_key="center_ti44", label="Titanium 44",  color="mediumspringgreen"), 
    Isotope(profile_key="cr48", history_key="center_cr48", label="Chromium 48",  color="maroon"), 
    Isotope(profile_key="fe52", history_key="center_fe52", label="Iron 52",      color="mediumslateblue"), 
    Isotope(profile_key="fe54", history_key="center_fe54", label="Iron 54",      color="saddlebrown"), 
    Isotope(profile_key="fe56", history_key="center_fe56", label="Iron 56",      color="magenta"), 
    Isotope(profile_key="ni56", history_key="center_ni56", label="Nickel 56",    color="black"), 
]  






# ==============================================================================
# SPECTRAL TYPE DATA (Restructured for clarity and subtypes)
# ==============================================================================

# This class defines the broad ranges for background shading and zoomed-out labels
@dataclass
class SpectralType:
    """Represents a broad Spectral Type (O, B, A, etc.) with its plotting properties."""
    letter: str
    temp_range: tuple       # (lower bound, upper bound) in Kelvin
    MS_mass_range: tuple    # (lower bound, upper bound) in Solar Masses
    color: str

    @property
    def temp_midpoint(self) -> float:
        """Calculates geometric mean for logarithmic scale plotting."""
        midpoint = np.sqrt(self.temp_range[1] * self.temp_range[0])
        return midpoint if np.isfinite(midpoint) else 1.2 * self.temp_range[0]

    @property
    def mass_midpoint(self) -> float:
        """Calculates geometric mean for logarithmic scale plotting."""
        midpoint = np.sqrt(self.MS_mass_range[1] * self.MS_mass_range[0])
        return midpoint if np.isfinite(midpoint) else 1.2 * self.MS_mass_range[0]

# This class defines the specific points for zoomed-in subtype labels
@dataclass
class SpectralSubtype:
    """Represents a specific Spectral Subtype (A0, G2, etc.) at a precise point."""
    label: str
    temp: float         # Specific temperature in Kelvin
    MS_mass: float      # Specific Main Sequence mass in Solar Masses 

# Data for the broad spectral types (for background shading)
# Source: Wikipedia - Stellar Classification
SPECTRAL_TYPES = [
    SpectralType(letter="O", temp_range=(33_000, 500_000),  MS_mass_range=(16, 300),     color="black"),
    SpectralType(letter="B", temp_range=(10_000, 33_000),  MS_mass_range=(2.1, 16),      color="white"),
    SpectralType(letter="A", temp_range=(7_300, 10_000),   MS_mass_range=(1.4, 2.1),     color="black"),
    SpectralType(letter="F", temp_range=(6_000, 7_300),    MS_mass_range=(1.04, 1.4),    color="white"),
    SpectralType(letter="G", temp_range=(5_300, 6_000),    MS_mass_range=(0.8, 1.04),    color="black"),
    SpectralType(letter="K", temp_range=(3_900, 5_300),    MS_mass_range=(0.45, 0.8),    color="white"),
    SpectralType(letter="M", temp_range=(2_300, 3_900),    MS_mass_range=(0.08, 0.45),   color="black"),
]

# Data for the specific spectral subtypes (for detailed labels when zoomed in)
SPECTRAL_SUBTYPES = [
    SpectralSubtype(label="O3", temp=44900, MS_mass=1.0), 
    SpectralSubtype(label="O4", temp=42900, MS_mass=1.0), 
    SpectralSubtype(label="O5", temp=41400, MS_mass=1.0), 
    SpectralSubtype(label="O6", temp=39500, MS_mass=1.0), 
    SpectralSubtype(label="O7", temp=37100, MS_mass=1.0), 
    SpectralSubtype(label="O8", temp=35100, MS_mass=1.0), 
    SpectralSubtype(label="O9", temp=33100, MS_mass=1.0), 

    SpectralSubtype(label="B0", temp=31400, MS_mass=1.0), 
    SpectralSubtype(label="B1", temp=26000, MS_mass=1.0), 
    SpectralSubtype(label="B2", temp=20600, MS_mass=1.0), 
    SpectralSubtype(label="B3", temp=17000, MS_mass=1.0), 
    SpectralSubtype(label="B4", temp=16400, MS_mass=1.0), 
    SpectralSubtype(label="B5", temp=15700, MS_mass=1.0), 
    SpectralSubtype(label="B6", temp=14500, MS_mass=1.0), 
    SpectralSubtype(label="B7", temp=14000, MS_mass=1.0), 
    SpectralSubtype(label="B8", temp=12300, MS_mass=1.0), 
    SpectralSubtype(label="B9", temp=10700, MS_mass=1.0), 

    SpectralSubtype(label="A0", temp=9700, MS_mass=1.0), 
    SpectralSubtype(label="A1", temp=9300, MS_mass=1.0), 
    SpectralSubtype(label="A2", temp=8800, MS_mass=1.0), 
    SpectralSubtype(label="A3", temp=8600, MS_mass=1.0), 
    SpectralSubtype(label="A4", temp=8250, MS_mass=1.0), 
    SpectralSubtype(label="A5", temp=8100, MS_mass=1.0), 
    SpectralSubtype(label="A6", temp=7910, MS_mass=1.0), 
    SpectralSubtype(label="A7", temp=7760, MS_mass=1.0), 
    SpectralSubtype(label="A8", temp=7590, MS_mass=1.0), 
    SpectralSubtype(label="A9", temp=7400, MS_mass=1.0), 

    SpectralSubtype(label="F0", temp=7220, MS_mass=1.0), 
    SpectralSubtype(label="F1", temp=7020, MS_mass=1.0), 
    SpectralSubtype(label="F2", temp=6820, MS_mass=1.0), 
    SpectralSubtype(label="F3", temp=6750, MS_mass=1.0), 
    SpectralSubtype(label="F4", temp=6670, MS_mass=1.0), 
    SpectralSubtype(label="F5", temp=6550, MS_mass=1.0), 
    SpectralSubtype(label="F6", temp=6350, MS_mass=1.0), 
    SpectralSubtype(label="F7", temp=6280, MS_mass=1.0), 
    SpectralSubtype(label="F8", temp=6180, MS_mass=1.0), 
    SpectralSubtype(label="F9", temp=6050, MS_mass=1.0), 

    SpectralSubtype(label="G0", temp=5930, MS_mass=1.0), 
    SpectralSubtype(label="G1", temp=5860, MS_mass=1.0), 
    SpectralSubtype(label="G2", temp=5770, MS_mass=1.0), 
    SpectralSubtype(label="G3", temp=5720, MS_mass=1.0), 
    SpectralSubtype(label="G4", temp=5680, MS_mass=1.0), 
    SpectralSubtype(label="G5", temp=5660, MS_mass=1.0), 
    SpectralSubtype(label="G6", temp=5600, MS_mass=1.0), 
    SpectralSubtype(label="G7", temp=5550, MS_mass=1.0), 
    SpectralSubtype(label="G8", temp=5480, MS_mass=1.0), 
    SpectralSubtype(label="G9", temp=5380, MS_mass=1.0), 
]




