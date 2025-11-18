import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Optional, Callable, Any 
from matplotlib import cm
import matplotlib.colors as mcolors 









def make_smooth_cmap(base_color, name='smooth_colormap', N=256, dark_factor=0.4, mid_pos=0.6):

    base_rgb = np.array(mcolors.to_rgb(base_color))
    dark_rgb = base_rgb * dark_factor  # darker version of base color

    # Define (position, color) pairs
    colors = [
        (0.0, (1, 1, 1)),     # start (white)
        (mid_pos, base_rgb),  # where base color appears
        (1.0, dark_rgb)       # end (dark)
    ]
    
    return mcolors.LinearSegmentedColormap.from_list(name, colors, N=N)








@dataclass 
class PlotItem: 
    profile_key: Optional[str] = None     
    profile_compute: Optional[Callable] = None    
    history_key: Optional[str] = None
    label: str = ""
    color: Optional[Any] = None   
    cmap: Optional[Any] = None 
    show_initial_abundance: bool = False 


    def evaluate_profile(self, profile):
        if self.profile_compute is not None:
            return self.profile_compute(profile)
        return getattr(profile, self.profile_key) 
    
    def evaluate_colormap(self): 
        if self.cmap is not None: 
            return self.cmap 
        else: 
            return make_smooth_cmap(self.color)









isotope_colors = cm.get_cmap("tab20", 20)
ISOTOPES = [ 
    PlotItem(profile_key="h1",   history_key="center_h1",   label="Hydrogen",     color=isotope_colors(0), show_initial_abundance=True), 
    PlotItem(profile_key="he3",  history_key="center_he3",  label="Helium 3",     color=isotope_colors(2)), 
    PlotItem(profile_key="he4",  history_key="center_he4",  label="Helium 4",     color=isotope_colors(4), show_initial_abundance=True), 
    PlotItem(profile_key="c12",  history_key="center_c12",  label="Carbon 12",    color=isotope_colors(6)), 
    PlotItem(profile_key="n14",  history_key="center_n14",  label="Nitrogen 14",  color=isotope_colors(8)), 
    PlotItem(profile_key="o16",  history_key="center_o16",  label="Oxygen 16",    color=isotope_colors(10)), 
    PlotItem(profile_key="ne20", history_key="center_ne20", label="Neon 20",      color=isotope_colors(12)), 
    PlotItem(profile_key="mg24", history_key="center_mg24", label="Magnesium 24", color=isotope_colors(14)), 
    PlotItem(profile_key="si28", history_key="center_si28", label="Silicon 28",   color=isotope_colors(16)), 
    PlotItem(profile_key="s32",  history_key="center_s32",  label="Sulfur 32",    color=isotope_colors(18)), 
    PlotItem(profile_key="ar36", history_key="center_ar36", label="Argon 36",     color=isotope_colors(1)), 
    PlotItem(profile_key="ca40", history_key="center_ca40", label="Calcium 40",   color=isotope_colors(3)), 
    PlotItem(profile_key="ti44", history_key="center_ti44", label="Titanium 44",  color=isotope_colors(5)), 
    PlotItem(profile_key="cr48", history_key="center_cr48", label="Chromium 48",  color=isotope_colors(7)), 
    PlotItem(profile_key="fe52", history_key="center_fe52", label="Iron 52",      color=isotope_colors(9)), 
    PlotItem(profile_key="fe54", history_key="center_fe54", label="Iron 54",      color=isotope_colors(11)), 
    PlotItem(profile_key="fe56", history_key="center_fe56", label="Iron 56",      color=isotope_colors(13)), 
    PlotItem(profile_key="ni56", history_key="center_ni56", label="Nickel 56",    color=isotope_colors(17)), 
]  




FUSION_RATES = [ 
    PlotItem(profile_key="eps_nuc",                             label="Total fusion",   color="black",      cmap="plasma"), 
    PlotItem(profile_key="pp",          history_key="pp",       label="PP chain",       color="#00759C"), 
    PlotItem(profile_key="cno",         history_key="cno",      label="CNO cycle",      color="#71D2FF"), 
    PlotItem(profile_key="tri_alfa",    history_key="tri_alfa", label="Triple alpha",   color="tab:green"), 
    PlotItem(
        profile_compute=lambda p: p.eps_nuc - p.pp - p.cno - p.tri_alfa,
        label="Heavier elements",
        color="tab:red"
    )
] 




CONVECTIONS = [ 
    PlotItem(
        profile_key = "log_D_conv", 
        profile_compute = lambda p: 10**p.log_D_conv, 
        label = "Convection", 
        color = "tab:blue"
    ), 
    PlotItem(
        profile_key = "log_D_semi", 
        profile_compute = lambda p: 10**p.log_D_semi, 
        label = "Semiconvection", 
        color = "tab:orange"
    ), 
    PlotItem(
        profile_key = "log_D_ovr", 
        profile_compute = lambda p: 10**p.log_D_ovr, 
        label = "Overshoot", 
        color = "tab:green"
    ), 
    PlotItem(
        profile_key = "log_D_thrm", 
        profile_compute = lambda p: 10**p.log_D_thrm, 
        label = "Thermohaline", 
        color = "tab:red"
    ) 
]


