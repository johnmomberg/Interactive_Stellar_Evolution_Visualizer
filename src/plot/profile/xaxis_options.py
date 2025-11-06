from dataclasses import dataclass
from typing import Callable

import src.data.base_option





# Profile plot x-axis: either use mass coordinate or radius coordinate to represent the location within the interior 
@dataclass
class ProfileXAxisOption(src.data.base_option.BaseOption):
    get_values: Callable  # function that takes profile and returns the array 
    xlabel_units: str 

PROFILEXAXIS_MASS = ProfileXAxisOption(
    display="mass coordinate", 
    get_values=lambda profile: profile.mass, 
    xlabel_units="(mass coordinate ($M_{{sun}}$))" ) 

PROFILEXAXIS_RADIUS = ProfileXAxisOption(
    display="radius coordinate", 
    get_values=lambda profile: profile.radius, 
    xlabel_units="(radius coordinate ($R_{{sun}}$))" )

PROFILEXAXIS_OPTIONS = [PROFILEXAXIS_MASS, PROFILEXAXIS_RADIUS]



