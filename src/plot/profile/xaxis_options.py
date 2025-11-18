from dataclasses import dataclass
from typing import Callable

from ...data import base_option





# Profile plot x-axis: either use mass coordinate or radius coordinate to represent the location within the interior 
@dataclass
class ProfileXAxisOption(base_option.BaseOption):
    get_values: Callable  # function that takes profile and returns the array 
    xlabel_units: str 
    xlabel: str 
    core_strings: list 

PROFILEXAXIS_MASS = ProfileXAxisOption(
    display="mass coordinate", 
    get_values=lambda profile: profile.mass, 
    xlabel_units="(mass coordinate ($M_{{sun}}$))", 
    xlabel = "$M_{{sun}}$", 
    core_strings = ['he_core_mass', 'c_core_mass', 'o_core_mass', 'si_core_mass', 'fe_core_mass'] ) 

PROFILEXAXIS_RADIUS = ProfileXAxisOption(
    display="radius coordinate", 
    get_values=lambda profile: profile.radius, 
    xlabel_units="(radius coordinate ($R_{{sun}}$))", 
    xlabel = "$R_{{sun}}$", 
    core_strings = ['he_core_radius', 'c_core_radius', 'o_core_radius', 'si_core_radius', 'fe_core_radius'] ) 

PROFILEXAXIS_OPTIONS = [PROFILEXAXIS_MASS, PROFILEXAXIS_RADIUS]



