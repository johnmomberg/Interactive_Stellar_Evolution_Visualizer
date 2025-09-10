from dataclasses import dataclass 







# Base class: each class will need a "display" keyword so no need to copy it many times 
# Each instance of this class or a child class corresponds to one option in a particular dropdown or radio selector 
# Using a class allows me to hold all info relevant to that option, such as the plotting function that it uses 
@dataclass
class OptionBase:
    display: str # The string that is displayed next to this option in the dropdown 

