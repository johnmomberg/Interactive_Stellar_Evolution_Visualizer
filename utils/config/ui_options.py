# Define all available options in all dropdown/radio selectors 

import marimo as mo 
from dataclasses import dataclass
from typing import Callable

import utils.plotting.history_plotting as history_plotting 
import utils.plotting.profile_plotting as profile_plotting 
from utils.config.option_base import OptionBase 





# Comparison mode: No select, select mass first and compare stages, or select stage first and compare masses 
@dataclass 
class CompareModeOption(OptionBase): 
    pass 

COMPAREMODE_NOSELECTION = CompareModeOption(display="") 
COMPAREMODE_MASSFIRST = CompareModeOption(display=" ") 
COMPAREMODE_STAGEFIRST = CompareModeOption(display="  ") 
COMPAREMODE_FREE = CompareModeOption(display="   ") 

COMPAREMODE_OPTIONS = [COMPAREMODE_NOSELECTION, COMPAREMODE_MASSFIRST, COMPAREMODE_STAGEFIRST, COMPAREMODE_FREE]





# Plot mode: HR diagram, history vs time at fixed location in star, or profile vs interior at fixed point in time 
@dataclass 
class PlotModeOption(OptionBase): 
    pass 

# Empty because the strings include dropdowns and are displayed separately  
PLOTMODE_HRDIAGRAM = PlotModeOption(display="")
PLOTMODE_HISTORY = PlotModeOption(display=" ")
PLOTMODE_PROFILE = PlotModeOption(display="  ")

PLOTMODE_OPTIONS = [PLOTMODE_HRDIAGRAM, PLOTMODE_HISTORY, PLOTMODE_PROFILE]





# History plots: Composition, radius, or fusion vs time 
@dataclass 
class HistoryPlotOption(OptionBase): 
    plot_func: Callable  

HISTORYPLOT_COMPOSITION = HistoryPlotOption(
    display="Center composition", 
    plot_func=history_plotting.HistoryPlot.composition) 

HISTORYPLOT_RADIUS = HistoryPlotOption(
    display="Radius", 
    plot_func=history_plotting.HistoryPlot.radius) 

HISTORYPLOT_FUSION = HistoryPlotOption(
    display="Fusion rate", 
    plot_func=history_plotting.HistoryPlot.fusion)

HISTORYPLOT_OPTIONS = [HISTORYPLOT_COMPOSITION, HISTORYPLOT_RADIUS, HISTORYPLOT_FUSION]





# Profile plots: composition, convection, etc vs interior coordinate at a fixed point in time 
@dataclass
class ProfilePlotOption(OptionBase):
    plot_func: Callable
    title_str: str

PROFILEPLOT_COMPOSITION = ProfilePlotOption(
    display="Composition (linear)", 
    plot_func=profile_plotting.ProfilePlot.composition, 
    title_str="Compostion in interior of a") 

PROFILEPLOT_COMPOSITION_LOG = ProfilePlotOption( 
    display="Composition (log)", 
    plot_func=profile_plotting.ProfilePlot.composition_log, 
    title_str="Composition in interior of a")

PROFILEPLOT_CONVECTION = ProfilePlotOption(
    display="Convection", 
    plot_func=profile_plotting.ProfilePlot.convection, 
    title_str="Convective regions in interior of a")

PROFILEPLOT_TEMP = ProfilePlotOption(
    display="Temperature (degeneracy)", 
    plot_func=profile_plotting.ProfilePlot.temp, 
    title_str="Temperature in interior of a")

PROFILEPLOT_TEMPGRAD = ProfilePlotOption(
    display="Temperature gradient (heat transport)", 
    plot_func=profile_plotting.ProfilePlot.tempgrad, 
    title_str="Temperature gradient in interior of a")

PROFILEPLOT_FUSION = ProfilePlotOption(
    display="Fusion rate", 
    plot_func=profile_plotting.ProfilePlot.fusion, 
    title_str="Fusion in interior of a")

PROFILEPLOT_OPTIONS = [PROFILEPLOT_COMPOSITION, PROFILEPLOT_COMPOSITION_LOG, PROFILEPLOT_CONVECTION, PROFILEPLOT_TEMP, PROFILEPLOT_TEMPGRAD, PROFILEPLOT_FUSION]





# Using a list of options defined above, create a Marimo dropdown or radio selector 
def create_dropdown(options_list, default_index=0):
    options_dict = {opt.display: opt for opt in options_list} 
    dropdown = mo.ui.dropdown(options=options_dict, value=list(options_dict.keys())[default_index]) 
    return dropdown 

def create_radio(options_list, default_index=0):
    options_dict = {opt.display: opt for opt in options_list}
    radio = mo.ui.radio(options=options_dict, value=list(options_dict.keys())[default_index]) 
    return radio 

    



