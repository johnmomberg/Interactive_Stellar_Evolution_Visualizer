from dataclasses import dataclass 
from . import base_class 
from ... import misc 



################################################################################


@dataclass 
class ParentStage(base_class.BaseEntity):
    flowchart_x: int 
    short_name: str 
    full_name: str 

    # Automatically generate ID when object is created
    def __post_init__(self):
        self.id = f"ParentStage({self.short_name}, x={self.flowchart_x})"


################################################################################


PARENT_HAYASHI = ParentStage( 
    flowchart_x=0, 
    short_name="Hayashi", 
    full_name="Hayashi track")

PARENT_HENYEY = ParentStage( 
    flowchart_x=1, 
    short_name="Henyey", 
    full_name="Henyey track")

PARENT_MS = ParentStage( 
    flowchart_x=2, 
    short_name="MS", 
    full_name="Main Sequence")

PARENT_POSTMS = ParentStage( 
    flowchart_x=3, 
    short_name="Post-MS", 
    full_name="Post-Main Sequence")

PARENT_RG = ParentStage( 
    flowchart_x=4, 
    short_name="RG", 
    full_name="Red giant")

PARENT_HEIGN = ParentStage( 
    flowchart_x=5, 
    short_name="He ign.", 
    full_name="Helium ignition")

PARENT_HEMS = ParentStage( 
    flowchart_x=6, 
    short_name="He MS", 
    full_name="Helium Main Sequence")

PARENT_AGB = ParentStage( 
    flowchart_x=7, 
    short_name="AGB", 
    full_name="Asymptotic Giant Branch")

PARENT_WD = ParentStage(
    flowchart_x=8, 
    short_name="WD", 
    full_name="White Dwarf")


################################################################################


ALL_PARENTSTAGES_LIST = misc.CustomList([ 
    PARENT_HAYASHI, 
    PARENT_HENYEY, 
    PARENT_MS, 
    PARENT_POSTMS, 
    PARENT_RG, 
    PARENT_HEIGN, 
    PARENT_HEMS, 
    PARENT_AGB, 
    PARENT_WD 
]) 


################################################################################

