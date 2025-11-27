from dataclasses import dataclass 
from matplotlib import cm 
from . import base_class 
from . import parent_stages 
from ... import misc 




################################################################################


@dataclass
class SubStage(base_class.BaseEntity):

    parent_stage: parent_stages.ParentStage 

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
colors = [
    '#468400', 
    "#850000", 
    '#0d1f95', 
    '#9e03bd', 
    "#a77730", 
    '#00b362', 
    '#6600ff', 
    "#8E8C09", 
    "#ce8414", 
    '#0299e4', 
    '#04877e', 
    '#8a420d', 
    "#ca0000", 
    '#005fbe', 
]
colors_iter = iter(colors)


################################################################################


SUB_NONE = SubStage( 

    parent_stage=None, 
    
    flowchart_text = None, 
    flowchart_color="gray", 
    
    mode1_abbrev="____", 
    mode1_desc="(no selection)", 
    mode1_interior_plot_title = "____", 
    
    mode2_abbrev="____", 
    mode2_desc="(no selection)", 
    mode2_interior_plot_title = "____", 

    mass_min=0.1, 
    mass_max=6.0,)


################################################################################


SUB_HAYASHI = SubStage( 

    parent_stage=parent_stages.PARENT_HAYASHI, 
    
    flowchart_text = "Hayashi", 
    flowchart_color=next(colors_iter), 
    
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

    parent_stage=parent_stages.PARENT_HENYEY, 

    flowchart_text = "Henyey", 
    flowchart_color=next(colors_iter), 

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
    
    parent_stage=parent_stages.PARENT_MS, 

    flowchart_text = "Main sequence \n(fully convective)", 
    flowchart_color=next(colors_iter), 
    
    mode1_abbrev="MS", 
    mode1_desc="Main sequence (fully convective)", 
    mode1_interior_plot_title="low-mass MS", 
    
    mode2_abbrev="Fully convective", 
    mode2_desc="Fully convective", 
    mode2_interior_plot_title="fully convective MS", 
    
    mass_min=0.1, 
    mass_max=0.3, )


SUB_MS_MEDMASS = SubStage( 

    parent_stage=parent_stages.PARENT_MS, 
    
    flowchart_text = "Main sequence \n(rad. core \n+ conv. env.)",     
    flowchart_color=next(colors_iter), 
    
    mode1_abbrev="MS", 
    mode1_desc="Main sequence (radiative core + convective envelope)", 
    mode1_interior_plot_title="intermediate-mass MS", 
    
    mode2_abbrev="Rad. core + conv. env.", 
    mode2_desc="Radiative core + convective envelope", 
    mode2_interior_plot_title="rad. core + conv. env MS", 
    
    mass_min=0.3, 
    mass_max=1.5, )


SUB_MS_HIMASS = SubStage( 

    parent_stage=parent_stages.PARENT_MS, 
    
    flowchart_text = "Main sequence \n(conv. core \n+ rad. env.)", 
    flowchart_color=next(colors_iter), 
    
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

    parent_stage=parent_stages.PARENT_POSTMS, 
    
    flowchart_text="Subgiant", 
    flowchart_color=next(colors_iter), 
    
    mode1_abbrev="Subgiant", 
    mode1_desc="Subgiant", 
    mode1_interior_plot_title="Subgiant", 
    
    mode2_abbrev="Subgiant", 
    mode2_desc="Subgiant", 
    mode2_interior_plot_title="Subgiant", 
    
    mass_min=0.3, 
    mass_max=1.5, )


SUB_POSTMS_HGAP = SubStage( 

    parent_stage=parent_stages.PARENT_POSTMS, 
    
    flowchart_text="Hertzsprung gap", 	
    flowchart_color=next(colors_iter), 
    
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

    parent_stage=parent_stages.PARENT_RG, 
    
    flowchart_text="Red giant", 	
    flowchart_color=next(colors_iter), 
    
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

    parent_stage=parent_stages.PARENT_HEIGN, 
    
    flowchart_text="Helium flash", 	
    flowchart_color=next(colors_iter), 
    
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
    
    parent_stage=parent_stages.PARENT_HEIGN, 
    
    flowchart_text="Helium ignites \nstably", 	
    flowchart_color=next(colors_iter), 
    
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

    parent_stage=parent_stages.PARENT_HEMS, 
    
    flowchart_text="Helium main \nsequence", 	
    flowchart_color=next(colors_iter), 
    
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

    parent_stage=parent_stages.PARENT_AGB, 
    
    flowchart_text="Asymptotic \ngiant", 	
    flowchart_color=next(colors_iter), 
    
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

    parent_stage=parent_stages.PARENT_WD, 
    
    flowchart_text="Helium \nwhite dwarf", 	
    flowchart_color=next(colors_iter), 
    
    mode1_abbrev="He WD", 
    mode1_desc="Helium white dwarf", 
    mode1_interior_plot_title="He WD", 
    
    mode2_abbrev="He WD", 
    mode2_desc="Helium white dwarf", 
    mode2_interior_plot_title="He WD", 
    
    mass_min = 0.1, 
    mass_max = 0.5, )


SUB_WD_CO = SubStage( 
    
    parent_stage=parent_stages.PARENT_WD, 
    
    flowchart_text="Carbon + \noxygen \nwhite dwarf", 	
    flowchart_color=next(colors_iter), 
    
    mode1_abbrev="C+O WD", 
    mode1_desc="Carbon + oxygen white dwarf", 
    mode1_interior_plot_title="C+O WD", 
    
    mode2_abbrev="C+O WD", 
    mode2_desc="Carbon + oxygen white dwarf",   
    mode2_interior_plot_title="C+O WD", 
    
    mass_min = 0.5, 
    mass_max = 6.0, )


################################################################################


ALL_SUBSTAGES_LIST = misc.CustomList([ 
    SUB_NONE, 
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
