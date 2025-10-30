from dataclasses import dataclass 
from pathlib import Path 
from matplotlib import cm 



data_folder = Path("C:/Users/johnm/Local Desktop/Gayley/MESA output files/")





# Custom version of List that acts exactly the same, except when you print it, each item is displayed on its own line 
class CustomList(list):
    def __str__(self):
        # Add header, body (each item on its own line), and footer
        inner = "\n".join("  " + str(item) for item in self)
        return f"CustomList([\n{inner}\n])"

    def __repr__(self):
        return self.__str__()





# Base class that gives ParentStage, SubStage, and Model classes a __str__ and __repr__ function (so they print their ID's)
@dataclass
class BaseEntity:
    def __str__(self):
        return getattr(self, 'id', f"{self.__class__.__name__}()")

    def __repr__(self):
        return self.__str__()








################################################################################


@dataclass 
class ParentStage(BaseEntity):
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


ALL_PARENTSTAGES_LIST = CustomList([ 
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




















################################################################################


@dataclass
class SubStage(BaseEntity):

    parent_stage: ParentStage 

    flowchart_text: str      # Text for the flowchart box (e.g., "Conv. core\n+ rad. env.") 
    flowchart_color: str 
    
    mode1_abbrev: str   # Mode1: Choose mass and compare evolutionary phases. Abbreviation goes inside the tab
    mode1_desc: str     # Full description of phase is displayed below the tabs element when this tab is selected 
    mode1_interior_plot_title: str 
    
    mode2_abbrev: str   # Mode2: Choose an evolutionary phase and compare masses. Abbreviation goes inside the tab
    mode2_desc: str     # Full description of phase is displayed below the tabs element when this tab is selected 
    mode2_interior_plot_title: str 

    mass_min: float # Minimum mass that exhibits this substage 
    mass_max: float # Maximum mass that exhibits this substage 

    # Automatically generate ID when object is created
    def __post_init__(self):
        self.id = f"SubStage({self.mode2_abbrev}, massrange={self.mass_min}-{self.mass_max})"

    @property
    def mode2_abbrev_with_massrange(self) -> str:
        return f"{self.mass_min:.1f}-{self.mass_max:.1f}: {self.mode2_abbrev}"

    @property
    def mode2_desc_with_massrange(self) -> str:
        return f"{self.mass_min:.1f}-{self.mass_max:.1f}: {self.mode2_desc}"



# Choose the colormap 
cmap = cm.get_cmap("Spectral", 14)

################################################################################


SUB_HAYASHI = SubStage( 

    parent_stage=PARENT_HAYASHI, 
    
    flowchart_text = "Hayashi", 
    flowchart_color=cmap(11), 
    
    mode1_abbrev="Hayashi", 
    mode1_desc="Hayashi track", 
    mode1_interior_plot_title = "Hayashi track", 
    
    mode2_abbrev="Hayashi", 
    mode2_desc="Hayashi track", 
    mode2_interior_plot_title = "Hayashi track", 

    mass_min=0.1, 
    mass_max=6.0,)


################################################################################


SUB_HENYEY = SubStage(

    parent_stage=PARENT_HENYEY, 

    flowchart_text = "Henyey", 
    flowchart_color=cmap(5), 

    mode1_abbrev="Henyey", 
    mode1_desc="Henyey track", 
    mode1_interior_plot_title="Henyey track", 

    mode2_abbrev="Henyey", 
    mode2_desc="Henyey track", 
    mode2_interior_plot_title="Henyey track", 
    
    mass_min=0.5, 
    mass_max=6.0, )


################################################################################


SUB_MS_LOWMASS = SubStage(
    
    parent_stage=PARENT_MS, 

    flowchart_text = "Main sequence \n(fully convective)", 
    flowchart_color=cmap(1), 
    
    mode1_abbrev="MS", 
    mode1_desc="Main sequence (fully convective)", 
    mode1_interior_plot_title="low-mass MS", 
    
    mode2_abbrev="Fully convective", 
    mode2_desc="Fully convective", 
    mode2_interior_plot_title="fully convective MS", 
    
    mass_min=0.1, 
    mass_max=0.3, )


SUB_MS_MEDMASS = SubStage( 

    parent_stage=PARENT_MS, 
    
    flowchart_text = "Main sequence \n(rad. core \n+ conv. env.)",     
    flowchart_color=cmap(10), 
    
    mode1_abbrev="MS", 
    mode1_desc="Main sequence (radiative core + convective envelope)", 
    mode1_interior_plot_title="intermediate-mass MS", 
    
    mode2_abbrev="Rad. core + conv. env.", 
    mode2_desc="Radiative core + convective envelope", 
    mode2_interior_plot_title="rad. core + conv. env MS", 
    
    mass_min=0.3, 
    mass_max=1.5, )


SUB_MS_HIMASS = SubStage( 

    parent_stage=PARENT_MS, 
    
    flowchart_text = "Main sequence \n(conv. core \n+ rad. env.)", 
    flowchart_color=cmap(13), 
    
    mode1_abbrev="MS", 
    mode1_desc="Main sequence (convective core + radiative envelope)", 
    mode1_interior_plot_title="high-mass MS", 
    
    mode2_abbrev="Conv. core + rad. env.", 
    mode2_desc="Convective core + radiative envelope", 
    mode2_interior_plot_title="conv. core + rad. env. MS", 
    
    mass_min=1.5, 
    mass_max=6.0, )


################################################################################


SUB_POSTMS_SUBGIANT = SubStage( 

    parent_stage=PARENT_POSTMS, 
    
    flowchart_text="Subgiant", 
    flowchart_color=cmap(4), 
    
    mode1_abbrev="Subgiant", 
    mode1_desc="Subgiant", 
    mode1_interior_plot_title="Subgiant", 
    
    mode2_abbrev="Subgiant", 
    mode2_desc="Subgiant", 
    mode2_interior_plot_title="Subgiant", 
    
    mass_min=0.3, 
    mass_max=1.5, )


SUB_POSTMS_HGAP = SubStage( 

    parent_stage=PARENT_POSTMS, 
    
    flowchart_text="Hertzsprung gap", 	
    flowchart_color=cmap(8), 
    
    mode1_abbrev="Hertzsprung gap", 
    mode1_desc="Hertzsprung gap", 
    mode1_interior_plot_title="Hertzsprung gap", 
    
    mode2_abbrev="Hertzsprung gap", 
    mode2_desc="Hertzsprung gap", 
    mode2_interior_plot_title="Hertzsprung gap", 
    
    mass_min=1.5, 
    mass_max=6.0, ) 


################################################################################


SUB_RG = SubStage( 

    parent_stage=PARENT_RG, 
    
    flowchart_text="Red giant", 	
    flowchart_color=cmap(0), 
    
    mode1_abbrev="RG", 
    mode1_desc="Red giant", 
    mode1_interior_plot_title="Red giant", 
    
    mode2_abbrev="RG", 
    mode2_desc="Red giant", 
    mode2_interior_plot_title="Red giant", 
    
    mass_min=0.3, 
    mass_max=6.0, )


################################################################################


SUB_HEIGN_HEFLASH = SubStage( 

    parent_stage=PARENT_HEIGN, 
    
    flowchart_text="Helium flash", 	
    flowchart_color=cmap(12), 
    
    mode1_abbrev="He flash", 
    mode1_desc="Helium ignition (unstable; helium flash)", 
    mode1_interior_plot_title="He flash", 
    
    mode2_abbrev="Unstable", 
    mode2_desc="Unstable helium ignition (helium flash)", 
    mode2_interior_plot_title="He flash", 
    
    mass_min=0.5, 
    mass_max=2.0, )


################################################################################


SUB_HEIGN_STABLE = SubStage(
    
    parent_stage=PARENT_HEIGN, 
    
    flowchart_text="Helium ignites \nstably", 	
    flowchart_color=cmap(3), 
    
    mode1_abbrev="He ign.", 
    mode1_desc="Helium ignition (stable)", 
    mode1_interior_plot_title="He ign. (stable)", 
    
    mode2_abbrev="Stable", 
    mode2_desc="Stable helium ignition", 
    mode2_interior_plot_title="He ign. (stable)", 
    
    mass_min=2.0, 
    mass_max=6.0, )


################################################################################


SUB_HEMS = SubStage( 

    parent_stage=PARENT_HEMS, 
    
    flowchart_text="Helium main \nsequence", 	
    flowchart_color=cmap(6), 
    
    mode1_abbrev="He MS", 
    mode1_desc="Helium main sequence", 
    mode1_interior_plot_title="He MS", 
    
    mode2_abbrev="He MS", 
    mode2_desc="Helium main sequence", 
    mode2_interior_plot_title="He MS", 
    
    mass_min=0.5, 
    mass_max=6.0, )


################################################################################


SUB_AGB = SubStage( 

    parent_stage=PARENT_AGB, 
    
    flowchart_text="Asymptotic \ngiant", 	
    flowchart_color=cmap(9), 
    
    mode1_abbrev="AGB", 
    mode1_desc="Asymptotic giant", 
    mode1_interior_plot_title="AGB", 
    
    mode2_abbrev="AGB", 
    mode2_desc="Asymptotic giant", 
    mode2_interior_plot_title="AGB", 
    
    mass_min=0.5, 
    mass_max=6.0, )


################################################################################


SUB_WD_HE = SubStage( 

    parent_stage=PARENT_WD, 
    
    flowchart_text="Helium \nwhite dwarf", 	
    flowchart_color=cmap(2), 
    
    mode1_abbrev="He WD", 
    mode1_desc="Helium white dwarf", 
    mode1_interior_plot_title="He WD", 
    
    mode2_abbrev="He WD", 
    mode2_desc="Helium white dwarf", 
    mode2_interior_plot_title="He WD", 
    
    mass_min = 0.1, 
    mass_max = 0.5, )


SUB_WD_CO = SubStage( 
    
    parent_stage=PARENT_WD, 
    
    flowchart_text="Carbon + \noxygen \nwhite dwarf", 	
    flowchart_color=cmap(7), 
    
    mode1_abbrev="C+O WD", 
    mode1_desc="Carbon + oxygen white dwarf", 
    mode1_interior_plot_title="C+O WD", 
    
    mode2_abbrev="C+O WD", 
    mode2_desc="Carbon + oxygen white dwarf",   
    mode2_interior_plot_title="C+O WD", 
    
    mass_min = 0.5, 
    mass_max = 6.0, )


################################################################################


ALL_SUBSTAGES_LIST = CustomList([ 
    SUB_HAYASHI, 
    SUB_HENYEY, 
    SUB_MS_LOWMASS, 
    SUB_MS_MEDMASS, 
    SUB_MS_HIMASS, 
    SUB_POSTMS_SUBGIANT, 
    SUB_POSTMS_HGAP, 
    SUB_RG, 
    SUB_HEIGN_HEFLASH, 
    SUB_HEIGN_STABLE, 
    SUB_HEMS, 
    SUB_AGB, 
    SUB_WD_HE, 
    SUB_WD_CO
]) 


################################################################################




















################################################################################


@dataclass 
class Model(BaseEntity): 
    mass: float 
    substage: SubStage 
    model_start: int 
    model_example: int 
    model_end: int 
    MESA_folder_path: str 

    # Automatically generate ID when object is created
    def __post_init__(self):
        self.id = f"Model(mass={self.mass}, model_example={self.model_example}, substage={self.substage})"


################################################################################


MODEL_0_2_HAYASHI = Model( 
    mass=0.2, 
    substage=SUB_HAYASHI, 
    model_start=None, 
    model_example=150, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=0.2") 

MODEL_0_2_MS = Model( 
    mass=0.2, 
    substage=SUB_MS_LOWMASS, 
    model_start=None, 
    model_example=273, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=0.2") 

MODEL_0_2_HEWD = Model( 
    mass=0.2, 
    substage=SUB_WD_HE, 
    model_start=None, 
    model_example=1200, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=0.2") 


################################################################################


MODEL_0_4_HAYASHI = Model( 
    mass=0.4, 
    substage=SUB_HAYASHI, 
    model_start=None, 
    model_example=200, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=0.4") 

MODEL_0_4_MS = Model( 
    mass=0.4, 
    substage=SUB_MS_MEDMASS, 
    model_start=None, 
    model_example=309, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=0.4") 

MODEL_0_4_SUBGIANT = Model( 
    mass=0.4, 
    substage=SUB_POSTMS_SUBGIANT, 
    model_start=None, 
    model_example=450, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=0.4") 

MODEL_0_4_RG = Model( 
    mass=0.4, 
    substage=SUB_RG, 
    model_start=None, 
    model_example=3000, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=0.4") 

MODEL_0_4_HEWD = Model( 
    mass=0.4, 
    substage=SUB_WD_HE, 
    model_start=None, 
    model_example=5159, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=0.4") 


################################################################################


MODEL_1_0_HAYASHI = Model( 
    mass=1.0, 
    substage=SUB_HAYASHI, 
    model_start=1,
    model_example=150, 
    model_end=202,
    MESA_folder_path=data_folder/"M=1.0") 

MODEL_1_0_HENYEY = Model( 
    mass=1.0, 
    substage=SUB_HENYEY, 
    model_start=202,
    model_example=220, 
    model_end=240,
    MESA_folder_path=data_folder/"M=1.0") 

MODEL_1_0_MS = Model( 
    mass=1.0, 
    substage=SUB_MS_MEDMASS, 
    model_start=240, 
    model_example=296, 
    model_end=330,
    MESA_folder_path=data_folder/"M=1.0") 

MODEL_1_0_SUBGIANT = Model( 
    mass=1.0, 
    substage=SUB_POSTMS_SUBGIANT, 
    model_start=330, 
    model_example=389, 
    model_end=415, 
    MESA_folder_path=data_folder/"M=1.0") 

MODEL_1_0_RG = Model( 
    mass=1.0, 
    substage=SUB_RG, 
    model_start=415, 
    model_example=5000, 
    model_end=9500, 
    MESA_folder_path=data_folder/"M=1.0") 

MODEL_1_0_HEFLASH = Model( 
    mass=1.0, 
    substage=SUB_HEIGN_HEFLASH, 
    model_start=9500, 
    model_example=9700, 
    model_end=10500, 
    MESA_folder_path=data_folder/"M=1.0") 

MODEL_1_0_HEMS = Model( 
    mass=1.0, 
    substage=SUB_HEMS, 
    model_start=10500, 
    model_example=10650, 
    model_end=10950, 
    MESA_folder_path=data_folder/"M=1.0") 

MODEL_1_0_AGB = Model(
    mass=1.0, 
    substage=SUB_AGB, 
    model_start=10950, 
    model_example=12300, 
    model_end=13600, 
    MESA_folder_path=data_folder/"M=1.0") 

MODEL_1_0_COWD = Model( 
    mass=1.0, 
    substage=SUB_WD_CO, 
    model_start=13600, 
    model_example=14300, 
    model_end=14300, 
    MESA_folder_path=data_folder/"M=1.0") 


################################################################################


MODEL_1_75_HAYASHI = Model(
    mass=1.75, 
    substage=SUB_HAYASHI, 
    model_start=1, 
    model_example=140, 
    model_end=200, 
    MESA_folder_path=data_folder/"Mass=1.75_models=every5")

MODEL_1_75_HENYEY = Model(
    mass=1.75, 
    substage=SUB_HENYEY, 
    model_start=200, 
    model_example=235, 
    model_end=250, 
    MESA_folder_path=data_folder/"Mass=1.75_models=every5")

MODEL_1_75_MS = Model(
    mass=1.75, 
    substage=SUB_MS_HIMASS, 
    model_start=250, 
    model_example=285, 
    model_end=340, 
    MESA_folder_path=data_folder/"Mass=1.75_models=every5")

MODEL_1_75_HGAP = Model(
    mass=1.75, 
    substage=SUB_POSTMS_HGAP, 
    model_start=340, 
    model_example=389, 
    model_end=420, 
    MESA_folder_path=data_folder/"Mass=1.75_models=every5")

MODEL_1_75_RG = Model(
    mass=1.75, 
    substage=SUB_RG, 
    model_start=420, 
    model_example=1000, 
    model_end=8763, 
    MESA_folder_path=data_folder/"Mass=1.75_models=every5")

MODEL_1_75_HEFLASH = Model(
    mass=1.75, 
    substage=SUB_HEIGN_HEFLASH, 
    model_start=8763, 
    model_example=8802, 
    model_end=9000, 
    MESA_folder_path=data_folder/"Mass=1.75_models=every5")

MODEL_1_75_HEMS = Model(
    mass=1.75, 
    substage=SUB_HEMS, 
    model_start=9000, 
    model_example=9800, 
    model_end=10000, 
    MESA_folder_path=data_folder/"Mass=1.75_models=every5")

MODEL_1_75_AGB = Model(
    mass=1.75, 
    substage=SUB_AGB, 
    model_start=10000, 
    model_example=11425, 
    model_end=13635, 
    MESA_folder_path=data_folder/"Mass=1.75_models=every5")

MODEL_1_75_COWD = Model(
    mass=1.75, 
    substage=SUB_HENYEY, 
    model_start=None, 
    model_example=None, 
    model_end=None, 
    MESA_folder_path=data_folder/"Mass=1.75_models=every5")


################################################################################


MODEL_3_0_HAYASHI = Model( 
    mass=3.0, 
    substage=SUB_HAYASHI, 
    model_start=None, 
    model_example=150, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=3.0") 

MODEL_3_0_HENYEY = Model( 
    mass=3.0, 
    substage=SUB_HENYEY, 
    model_start=None, 
    model_example=225, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=3.0") 

MODEL_3_0_MS = Model( 
    mass=3.0, 
    substage=SUB_MS_HIMASS, 
    model_start=None, 
    model_example=300, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=3.0") 

MODEL_3_0_HGAP = Model( 
    mass=3.0, 
    substage=SUB_POSTMS_HGAP, 
    model_start=None, 
    model_example=363, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=3.0") 

MODEL_3_0_RG = Model( 
    mass=3.0, 
    substage=SUB_RG, 
    model_start=None, 
    model_example=400, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=3.0") 

MODEL_3_0_HESTABLE = Model( 
    mass=3.0, 
    substage=SUB_HEIGN_STABLE, 
    model_start=None, 
    model_example=None, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=3.0") 

MODEL_3_0_HEMS = Model( 
    mass=3.0, 
    substage=SUB_HEMS, 
    model_start=None, 
    model_example=650, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=3.0") 

MODEL_3_0_AGB = Model( 
    mass=3.0, 
    substage=SUB_AGB, 
    model_start=None, 
    model_example=1700, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=3.0") 

MODEL_3_0_COWD = Model( 
    mass=3.0, 
    substage=SUB_WD_CO, 
    model_start=None, 
    model_example=None, 
    model_end=None, 
    MESA_folder_path=data_folder/"M=3.0") 


################################################################################

ALL_MODELS_LIST = CustomList([ 
    MODEL_0_2_HAYASHI,
    MODEL_0_2_MS, 
    MODEL_0_2_HEWD, 

    MODEL_0_4_HAYASHI, 
    MODEL_0_4_MS, 
    MODEL_0_4_SUBGIANT, 
    MODEL_0_4_RG,
    MODEL_0_4_HEWD, 

    MODEL_1_0_HAYASHI,
    MODEL_1_0_HENYEY, 
    MODEL_1_0_MS, 
    MODEL_1_0_SUBGIANT, 
    MODEL_1_0_RG, 
    MODEL_1_0_HEFLASH,
    MODEL_1_0_HEMS,
    MODEL_1_0_AGB, 
    MODEL_1_0_COWD, 

    MODEL_1_75_HAYASHI,
    MODEL_1_75_HENYEY, 
    MODEL_1_75_MS, 
    MODEL_1_75_HGAP, 
    MODEL_1_75_RG, 
    MODEL_1_75_HEFLASH,
    MODEL_1_75_HEMS,
    MODEL_1_75_AGB, 
    MODEL_1_75_COWD, 

    MODEL_3_0_HAYASHI,
    MODEL_3_0_HENYEY, 
    MODEL_3_0_MS, 
    MODEL_3_0_HGAP, 
    MODEL_3_0_RG, 
    MODEL_3_0_HESTABLE,
    MODEL_3_0_HEMS,
    MODEL_3_0_AGB, 
    MODEL_3_0_COWD 
]) 


################################################################################


