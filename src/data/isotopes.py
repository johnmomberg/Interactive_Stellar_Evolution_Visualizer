import numpy as np
from dataclasses import dataclass
from matplotlib import cm





# Define all isotopes (hydrogen, helium, etc) for use with composition plots (both profile data and history data)

@dataclass
class Isotope:
    """Represents an isotope with its plotting properties."""
    profile_key: str                        # The attribute name in the MESA profile (e.g., "profile.h1") 
    history_key: str                        # The attribute name in the MESA history (e.g., "history.center_h1")
    label: str                              # The label for the plot legend (e.g., 'Hydrogen')
    color: str                              # The color for the plot line 
    show_initial_abundance: bool = False    # Include a horizontal dashed line in profile plots to indicate the initial abundance of this element? 

    def evaluate_profile(self, profile): 
        return getattr(profile, self.profile_key)
    
# Choose the colormap 
cmap = cm.get_cmap("tab20", 20)

ISOTOPES = [ 
    Isotope(profile_key="h1",   history_key="center_h1",   label="Hydrogen",     color=cmap(0), show_initial_abundance=True), 
    Isotope(profile_key="he3",  history_key="center_he3",  label="Helium 3",     color=cmap(2)), 
    Isotope(profile_key="he4",  history_key="center_he4",  label="Helium 4",     color=cmap(4), show_initial_abundance=True), 
    Isotope(profile_key="c12",  history_key="center_c12",  label="Carbon 12",    color=cmap(6)), 
    Isotope(profile_key="n14",  history_key="center_n14",  label="Nitrogen 14",  color=cmap(8)), 
    Isotope(profile_key="o16",  history_key="center_o16",  label="Oxygen 16",    color=cmap(10)), 
    Isotope(profile_key="ne20", history_key="center_ne20", label="Neon 20",      color=cmap(12)), 
    Isotope(profile_key="mg24", history_key="center_mg24", label="Magnesium 24", color=cmap(14)), 
    Isotope(profile_key="si28", history_key="center_si28", label="Silicon 28",   color=cmap(16)), 
    Isotope(profile_key="s32",  history_key="center_s32",  label="Sulfur 32",    color=cmap(18)), 
    Isotope(profile_key="ar36", history_key="center_ar36", label="Argon 36",     color=cmap(1)), 
    Isotope(profile_key="ca40", history_key="center_ca40", label="Calcium 40",   color=cmap(3)), 
    Isotope(profile_key="ti44", history_key="center_ti44", label="Titanium 44",  color=cmap(5)), 
    Isotope(profile_key="cr48", history_key="center_cr48", label="Chromium 48",  color=cmap(7)), 
    Isotope(profile_key="fe52", history_key="center_fe52", label="Iron 52",      color=cmap(9)), 
    Isotope(profile_key="fe54", history_key="center_fe54", label="Iron 54",      color=cmap(11)), 
    Isotope(profile_key="fe56", history_key="center_fe56", label="Iron 56",      color=cmap(13)), 
    Isotope(profile_key="ni56", history_key="center_ni56", label="Nickel 56",    color=cmap(17)), 
]  




