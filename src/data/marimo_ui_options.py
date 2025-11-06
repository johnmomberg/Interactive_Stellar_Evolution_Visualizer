# Define all available options in all dropdown/radio selectors 

import marimo as mo 
from dataclasses import dataclass
from typing import Callable

import src.plot 
import src.data.base_option





# Comparison mode: No select, select mass first and compare stages, or select stage first and compare masses 
@dataclass 
class CompareModeOption(src.data.base_option.OptionBase): 
    pass 

COMPAREMODE_NOSELECTION = CompareModeOption(display="") 
COMPAREMODE_MASSFIRST = CompareModeOption(display=" ") 
COMPAREMODE_STAGEFIRST = CompareModeOption(display="  ") 
COMPAREMODE_FREE = CompareModeOption(display="   ") 

COMPAREMODE_OPTIONS = [COMPAREMODE_NOSELECTION, COMPAREMODE_MASSFIRST, COMPAREMODE_STAGEFIRST, COMPAREMODE_FREE]





# Plot mode: HR diagram, history vs time at fixed location in star, or profile vs interior at fixed point in time 
@dataclass 
class PlotModeOption(src.data.base_option.OptionBase): 
    pass 

# Empty because the strings include dropdowns and are displayed separately  
PLOTMODE_HRDIAGRAM = PlotModeOption(display="")
PLOTMODE_HISTORY = PlotModeOption(display=" ")
PLOTMODE_PROFILE = PlotModeOption(display="  ")

PLOTMODE_OPTIONS = [PLOTMODE_HRDIAGRAM, PLOTMODE_HISTORY, PLOTMODE_PROFILE]





# History plots: Composition, radius, or fusion vs time 
@dataclass 
class HistoryPlotOption(src.data.base_option.OptionBase): 
    plot_func: Callable  

HISTORYPLOT_COMPOSITION = HistoryPlotOption(
    display="Center composition", 
    plot_func=src.plot.history.HistoryPlot.composition) 

HISTORYPLOT_RADIUS = HistoryPlotOption(
    display="Radius", 
    plot_func=src.plot.history.HistoryPlot.radius) 

HISTORYPLOT_MASS = HistoryPlotOption( 
    display="Mass", 
    plot_func=src.plot.history.HistoryPlot.mass)

HISTORYPLOT_FUSION = HistoryPlotOption(
    display="Fusion rate", 
    plot_func=src.plot.history.HistoryPlot.fusion)

HISTORYPLOT_OPTIONS = [HISTORYPLOT_COMPOSITION, HISTORYPLOT_RADIUS, HISTORYPLOT_MASS, HISTORYPLOT_FUSION]





# Profile plots: composition, convection, etc vs interior coordinate at a fixed point in time 
@dataclass
class ProfilePlotOption(src.data.base_option.OptionBase):
    plot_func: Callable
    title_str: str

PROFILEPLOT_COMPOSITION = ProfilePlotOption(
    display="Composition (linear)", 
    plot_func=src.plot.profile.profile.ProfilePlot.composition, 
    title_str="Compostion in interior of a") 

PROFILEPLOT_COMPOSITION_LOG = ProfilePlotOption( 
    display="Composition (log)", 
    plot_func=src.plot.profile.profile.ProfilePlot.composition_log, 
    title_str="Composition in interior of a") 

PROFILEPLOT_MU = ProfilePlotOption( 
    display="Mass/particle", 
    plot_func=src.plot.profile.profile.ProfilePlot.mu, 
    title_str=f"Mass/particle ($\mu$) in interior of a")

PROFILEPLOT_CONVECTION = ProfilePlotOption(
    display="Convection", 
    plot_func=src.plot.profile.profile.ProfilePlot.convection, 
    title_str="Convective regions in interior of a")

PROFILEPLOT_TEMP = ProfilePlotOption(
    display="Temperature", 
    plot_func=src.plot.profile.profile.ProfilePlot.temp, 
    title_str="Temperature in interior of a")

PROFILEPLOT_TEMPGRAD = ProfilePlotOption(
    display="Temp grad", 
    plot_func=src.plot.profile.profile.ProfilePlot.tempgrad, 
    title_str="Temperature gradient in interior of a")

PROFILEPLOT_FUSION = ProfilePlotOption(
    display="Fusion rate", 
    plot_func=src.plot.profile.profile.ProfilePlot.fusion, 
    title_str="Fusion in interior of a") 

PROFILEPLOT_DEGENERACY = ProfilePlotOption( 
    display="Degeneracy", 
    plot_func=src.plot.profile.profile.ProfilePlot.degeneracy, 
    title_str="Degeneracy of electrons and baryons inside a") 

PROFILEPLOT_OPTIONS = [PROFILEPLOT_COMPOSITION, PROFILEPLOT_COMPOSITION_LOG, PROFILEPLOT_MU, PROFILEPLOT_CONVECTION, PROFILEPLOT_TEMP, PROFILEPLOT_TEMPGRAD, PROFILEPLOT_FUSION, PROFILEPLOT_DEGENERACY]





# Available model numbers dropdown, used when loading your own MESA file 
@dataclass 
class AvailableModelnumsOption(src.data.base_option.OptionBase): 
    modelnum: int 
    age: float 





# Using a list of options defined above, create a Marimo dropdown or radio selector 
def create_dropdown(options_list, default_index=0, label=""):
    options_dict = {opt.display: opt for opt in options_list} 
    dropdown = mo.ui.dropdown(options=options_dict, value=list(options_dict.keys())[default_index], label=label) 
    return dropdown 

def create_radio(options_list, default_index=0):
    options_dict = {opt.display: opt for opt in options_list}
    radio = mo.ui.radio(options=options_dict, value=list(options_dict.keys())[default_index]) 
    return radio 

    



