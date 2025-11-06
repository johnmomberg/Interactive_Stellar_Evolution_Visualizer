import numpy as np 
from fractions import Fraction 
import functools 
from dataclasses import dataclass, field
import itertools
from typing import List, Tuple, Dict
from itertools import cycle

import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 
from matplotlib.axes import Axes

import utils.config.plot_options as plot_options 






class MajorLogLocator(mticker.Locator):
    def __init__(self):
        pass 

    def __call__(self):
        left, right = self.axis.get_view_interval() 
        return calc_log_ticks(left, right)



class MinorLogLocator(mticker.Locator):
    def __init__(self):
        pass 

    def __call__(self):
        left, right = self.axis.get_view_interval() 
        return calc_log_ticks(left, right, remove_overlaps=False)





# Do not ask me how this works. Too lazy to add comments right now 
def calc_log_ticks(left, right, remove_overlaps=True):
    xmin = np.min([left, right])
    xmax = np.max([left, right])



    def calc_next_depth(depth): 
        if depth == 0: 
            return 1 
        exp = int(np.floor(np.log10(depth)))
        mant = depth / (10**exp)  
        if mant == 1: 
            return int(depth*2) 
        if mant == 2: 
            return int(depth*2.5)
        if mant == 5: 
            return int(depth*2) 
        


    def calc_gaps(input_array, minmax_func=np.min): 

        # Get sorting indices
        sort_idx = np.argsort(input_array)
        sorted_array = input_array[sort_idx]

        # Calculate gaps 
        gaps = [] 
        for i in range(len(sorted_array)): 
            if i==0: 
                gap = np.log10(sorted_array[1]/sorted_array[0])
            elif i==len(sorted_array)-1: 
                gap = np.log10(sorted_array[i]/sorted_array[i-1])
            else: 
                next_gap = np.log10(sorted_array[i+1] / sorted_array[i])
                prev_gap = np.log10(sorted_array[i] / sorted_array[i-1])
                gap = minmax_func([next_gap, prev_gap])
            gaps.append(gap)
        gaps = np.array(gaps)

        # Invert the sorting to get back to original order
        inverse_idx = np.argsort(sort_idx)
        unsorted_gaps = gaps[inverse_idx]

        return unsorted_gaps 



    start_exp = int(np.floor(np.log10(xmin)))
    stop_exp = int(np.floor(np.log10(xmax)))
    depth = 0 
    f_max = 0.33 # original: 0.5 max, 0.1 min  
    f_min = 0.1
    length = np.log10(xmax / xmin) 
    array = np.array([]) 
    gaps = np.array([length]) 



    # Keep subdividing until the largest gap between ticks is smaller than f_max 
    # This will mean the smallest gaps are way too small, but we will remove those points in the next step 
    while len(array) < 4 or (np.max(gaps)>f_max*length):

        depth = calc_next_depth(depth) 

        arrs = []
        for k in range(start_exp, stop_exp+1):
            base = 10**k
            step = base / depth   # e.g. depth=2 → 500, depth=5 → 200
            arr = np.arange(base, 10*base + step, step)
            arrs.append(arr)

        array = np.unique(np.concatenate(arrs))
        array = array[(array >= xmin) & (array <= xmax)]
        array = np.append(array, xmin)
        array = np.append(array, xmax) 
        array = np.unique(array) 
        array = np.sort(array) 

        gaps = calc_gaps(array, minmax_func=np.max) 



    # First, check if we even want to remove overlapping points. 
    # If this is for minor tick LINES, leave overlapping points in so the gridline spacing 
    # matches what you would expect for a log plot, but for major tick LABELS, we don't want any text to overlap. 
    # When removing overlapping points, prioritize keeping "nicer" numbers. 
    # Example: If 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60 etc were the initial labels: 
    # First get rid of 0.1 numbers (what's left: 6, 8, 10, 20, 40, etc)
    # Then get rid of 0.2 numbers (what's left: 5, 10, 15, 20, 25)
    # Then get rid of 0.5 numbers (what's left: 10, 100, 1000) 
    # Prioritize keeping 0.0
    # Keep removing points until no remaining labels are overlapping/too close 
    while remove_overlaps==True:

        gaps = calc_gaps(array) 

        if len(gaps) < 1 or np.min(gaps) >= f_min*length:
            break 

        array_too_close = array[np.where(gaps<f_min*length)]

        exp = np.floor(np.log10(array_too_close)) 
        mant = array_too_close / (10**exp) 
        dec = np.array([round(x%1, 10) for x in mant])
        denoms = np.array([Fraction(x).limit_denominator(100).denominator for x in dec])

        array_least_significant = array_too_close[np.where(denoms==np.max(denoms))] 
        ind_removal_candidates = np.array([np.where(array==x)[0][0] for x in array_least_significant]) 
        ind_remove = np.where(array == array[ind_removal_candidates][np.argmin(np.array(gaps)[ind_removal_candidates])])[0][0]

        array = np.delete(array, ind_remove)

    return array 








class HRDiagram: 

    def __init__(self): 

        # Setup 
        self.fig, self.ax = plt.subplots(figsize=(12.8, 7))
        self.fig.subplots_adjust(top=0.82, bottom=0.13, left=0.10, right=0.81)


        # X axis: Temperature 
        self.ax.set_xlabel("Surface temperature (K)", fontsize=18, labelpad=14)
        self.ax.set_xscale("log")
        self.ax.set_xlim((80000, 1000)) 
        
        # self.ax.xaxis.set_major_locator(MajorLogLocator()) 
        # self.ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}")) 

        # self.ax.xaxis.set_minor_locator(MinorLogLocator()) 
        # self.ax.xaxis.set_minor_formatter(mticker.NullFormatter())         


        # Y axis: Luminosity 
        self.ax.set_ylabel("Luminosity ($L_{{sun}}$)", fontsize=18, labelpad=14)
        self.ax.set_yscale("log")
        self.ax.set_ylim((1e-6, 1e8))



        # Grid, ticks, title 
        self.ax.tick_params(labelsize=14, length=10, which="major") 
        # self.ax.grid(alpha=0.5, which="both")
        self.ax.set_title("Evolutionary Path Across HR Diagram", fontsize=20, pad=15) 



    def add_path(self, history, color=None, label=None, lw=2, alpha=1, modelnum_start=None, modelnum_end=None): 
        if modelnum_start == None:  
            ind_start = 0 
        else: 
            ind_start = modelnum_start-1 
        if modelnum_end == None: 
            ind_end = -1 
        else: 
            ind_end = modelnum_end-1 
        self.ax.plot(
            10**history.log_Teff[ind_start:ind_end], 
            10**history.log_L[ind_start:ind_end], 
            color=color, 
            label=label, 
            lw=lw, 
            alpha=alpha)



    # def legend(self): 
    #     self.ax.legend(fontsize=14) 





    # Add model labels to points on an HR diagram, skipping some models to avoid overlapping labels 
    def add_modelnum_labels(self, history, modelnum_now=None):
        ax = self.ax


        # Check if too points are too close (the labels will overlap)
        def calc_is_too_close(point1, point2, current_bounds): 

            min_x_fractional_sep = 0.08  
            min_y_fractional_sep = 0.08  

            xlim, ylim = current_bounds 

            x_sep = np.abs(point1[0]-point2[0]) 
            y_sep = np.abs(point1[1]-point2[1]) 
            
            log_xlim = np.log10(xlim) 
            log_ylim = np.log(ylim)

            log_xrange = max(log_xlim) - min(log_xlim) 
            log_yrange = max(log_ylim) - min(log_ylim) 

            # Check whether the two points are too close 
            if x_sep < min_x_fractional_sep*log_xrange and y_sep < min_y_fractional_sep*log_yrange:
                return True
            else: 
                return False  



        # Function that runs every time axis limits are changed 
        def update_secondary_axis(ax): 

            # 1) Remove previous points, so only current ones are shown on plot 

            if hasattr(ax, "_model_points"):
                ax._model_points.remove() 
            if hasattr(ax, "_model_label_points"):
                ax._model_label_points.remove() 
            if hasattr(ax, "_model_labels"):
                for label in ax._model_labels: 
                    label.remove()  
            if hasattr(ax, "_modelnum_now_point"): 
                ax._modelnum_now_point.remove() 
            if hasattr(ax, "_modelnum_now_label"): 
                ax._modelnum_now_label.remove() 
            


            # 2) Calculate positions where models are available 

            # Get current axes bounds 
            xlim = ax.get_xlim() 
            ylim = ax.get_ylim() 

            # Return x,y coords of points within axes bounds 
            ind_models_available = history.model_numbers_available-1 
            log_Teff = history.log_Teff[ind_models_available]
            log_L = history.log_L[ind_models_available]
            ind_in_view = functools.reduce(
                np.intersect1d, 
                [
                    np.where(10**log_Teff>min(xlim)), 
                    np.where(10**log_Teff<max(xlim)), 
                    np.where(10**log_L>min(ylim)), 
                    np.where(10**log_L<max(ylim)) ] )
            log_Teff_in_view = log_Teff[ind_in_view]
            log_L_in_view = log_L[ind_in_view]

            if len(log_Teff_in_view) == 0:
                ax._model_points = ax.scatter([], []) 
                ax._model_label_points = ax.scatter([], []) 
                ax._model_labels = [] 
                ax._modelnum_now_point = ax.scatter([], []) 
                ax._modelnum_now_label = ax.text([], [], "") 
                ax.figure.canvas.draw_idle()
                return


            # 3) Calculate positions to place labels (subset of points with model numbers, so that labels don't overlap)

            log_Teff_labeled = [log_Teff_in_view[0]]
            log_L_labeled = [log_L_in_view[0]]

            # try to use modelnum_now if it’s valid and in range
            if modelnum_now is not None:
                x = history.log_Teff[modelnum_now - 1]
                y = history.log_L[modelnum_now - 1] 

                in_x_range = np.log10(min(xlim)) < x < np.log10(max(xlim))
                in_y_range = np.log10(min(ylim)) < y < np.log10(max(ylim))

                if in_x_range and in_y_range:
                    log_Teff_labeled = [x]
                    log_L_labeled = [y] 

            # Loop over all available points 
            for i in np.arange(1, len(log_Teff_in_view)): 

                x = log_Teff_in_view[i] 
                y = log_L_in_view[i] 

                # Check if the current point should be labeled or not 
                # Only label if this point isn't too close to any of the other labels 
                is_too_close = False 
                for j in range(len(log_Teff_labeled)): 
                    x0 = log_Teff_labeled[j]
                    y0 = log_L_labeled[j] 
                    if calc_is_too_close((x,y), ((x0,y0)), (xlim,ylim)): 
                        is_too_close = True 
                        break 
                if is_too_close: 
                    continue 
            
                # If we haven't skipped to the next point, the current point is not too close to any of the current labels, so add it to the list 
                log_Teff_labeled.append(x)
                log_L_labeled.append(y) 

            # Convert lists back to numpy array 
            log_Teff_labeled = np.array(log_Teff_labeled) 
            log_L_labeled = np.array(log_L_labeled) 

            # Remove current model number from labels list and apply a separate label to it 
            if modelnum_now is not None: 
                log_Teff_labeled = log_Teff_labeled[log_Teff_labeled != history.log_Teff[modelnum_now-1]] 
                log_L_labeled = log_L_labeled[log_L_labeled != history.log_L[modelnum_now-1]] 
            


            # 4) Add labels and points calculated in previous sections to the plot 
            
            # Add points to all positions with models 
            ax._model_points = ax.scatter(
                10**log_Teff_in_view, 10**log_L_in_view, 
                zorder=10, color="white", ec="black", s=5) 

            # Add points to the subset of positions with labels 
            ax._model_label_points = ax.scatter(
                10**log_Teff_labeled, 10**log_L_labeled, 
                zorder=30, color="white", edgecolor="black", s=20) 

            # The labels themselves 
            ax._model_labels = [] 
            for i in range(len(log_Teff_labeled)): 
                ax._model_labels.append( ax.text(
                    10**log_Teff_labeled[i], 
                    10**log_L_labeled[i], 
                    np.where(history.log_Teff == log_Teff_labeled[i])[0][0]+1,  
                    fontsize=10, ha='left', va='bottom', zorder=20, clip_on=True, 
                    bbox=dict(facecolor='white', edgecolor='black', alpha=1.0, boxstyle='round,pad=0.2')) )

            if modelnum_now is not None: 
                
                # Point for the currently selected model 
                ax._modelnum_now_point = ax.scatter(
                    10**history.log_Teff[modelnum_now-1], 10**history.log_L[modelnum_now-1], 
                    zorder=30, color="gold", edgecolor="black", s=20) 
            
                # Label the currently selected model 
                ax._modelnum_now_label = ax.text(
                    10**history.log_Teff[modelnum_now-1], 10**history.log_L[modelnum_now-1], 
                    modelnum_now,  
                    fontsize=12, ha='left', va='bottom', zorder=20, clip_on=True, 
                    bbox=dict(facecolor='gold', edgecolor='black', alpha=1.0, boxstyle='round,pad=0.2')) 



        # 5) Connect function to axis so it automatically updates on limit changes 

            # Idk what this does 
            ax.figure.canvas.draw_idle()
            
        # Re-run this function every time the x or y axes limits change 
        ax.callbacks.connect('xlim_changed', update_secondary_axis)
        ax.callbacks.connect('ylim_changed', update_secondary_axis)
        update_secondary_axis(ax)









# ---------------------------
# Data classes
# ---------------------------
@dataclass
class SpectralSubtype:
    label: str
    temp: float       
    MS_mass: float 

@dataclass
class SpectralType:
    letter: str
    temp_range: Tuple[float, float]       # (min, max) in Kelvin
    MS_mass_range: Tuple[float, float]
    subtypes: List[SpectralSubtype] = field(default_factory=list)

    @property
    def temp_midpoint(self) -> float:
        a, b = self.temp_range
        return np.sqrt(a * b)

    @property
    def mass_midpoint(self) -> float:
        a, b = self.MS_mass_range
        return np.sqrt(a * b)
    






# From Pecaut & Mamajek (2013) mean dwarf MS data (Teff, Msun) https://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt 

_O = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["O3V", "O4V", "O5V", "O5.5V", "O6V", "O6.5V", "O7V", "O7.5V", "O8V", "O8.5V", "O9V", "O9.5V"],
        [ 44900, 42900, 41400, 40500,   39500, 38300,   37100, 36100,   35100, 34300,   33300, 31900],
        [ 59.0,  48.0,  43.0,  38.0,    35.0,  31.0,    28.0,  26.0,    23.6,  21.9,    20.2,  18.7],
    )
]

_B = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["B0V", "B0.5V", "B1V", "B1.5V", "B2V", "B2.5V", "B3V", "B4V", "B5V", "B6V", "B7V", "B8V", "B9V", "B9.5V"],
        [ 31400, 29000,   26000, 24500,   20600, 18500,   17000, 16400, 15700, 14500, 14000, 12300, 10700, 10400],
        [ 17.7,  14.8,    11.8,  9.9,     7.3,   6.1,     5.4,   5.1,   4.7,   4.3,   3.92,  3.38,  2.75,  2.68],
    )
]

_A = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["A0V", "A1V", "A2V", "A3V", "A4V", "A5V", "A6V", "A7V", "A8V", "A9V"],
        [ 9700,  9300,  8800,  8600,  8250,  8100,  7910,  7760,  7590,  7400],
        [ 2.18,  2.05,  1.98,  1.93,  1.88,  1.86,  1.83,  1.81,  1.77,  1.75],
    )
]

_F = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["F0V", "F1V", "F2V", "F3V", "F4V", "F5V", "F6V", "F7V", "F8V", "F9V", "F9.5V"],
        [ 7220,  7020,  6820,  6750,  6670,  6550,  6350,  6280,  6180,  6050,  5990],
        [ 1.61,  1.50,  1.46,  1.44,  1.38,  1.33,  1.25,  1.21,  1.18,  1.13,  1.08],
    )
]

_G = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["G0V", "G1V", "G2V", "G3V", "G4V", "G5V", "G6V", "G7V", "G8V", "G9V"],
        [ 5930,  5860,  5770,  5720,  5680,  5660,  5600,  5550,  5480,  5380],
        [ 1.06,  1.03,  1.00,  0.99,  0.985, 0.98,  0.97,  0.95,  0.94,  0.90],
    )
]

_K = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["K0V", "K1V", "K2V", "K3V", "K4V"," K5V", "K6V", "K7V", "K8V", "K9V"],
        [ 5270,  5170,  5100,  4830,  4600,  4440,  4300,  4100,  3990,  3930],
        [ 0.88,  0.86,  0.82,  0.78,  0.73,  0.70,  0.69,  0.64,  0.62,  0.59],
    )
]

_M = [
    SpectralSubtype(label=label, temp=t, MS_mass=m)
    for label, t, m in zip(
        ["M0V", "M0.5V", "M1V", "M1.5V", "M2V", "M2.5V", "M3V", "M3.5V", "M4V", "M4.5V", "M5V", "M5.5V", "M6V", "M6.5V", "M7V", "M7.5V", "M8V", "M8.5V", "M9V", "M9.5V"],
        [ 3850,  3770,    3660,  3620,    3560,  3470,    3430,  3270,    3210,  3110,    3060,  2930,    2810,  2740,    2680,  2630,    2570,  2420,    2380,  2350],
        [ 0.57,  0.544,   0.50,  0.482,   0.44,  0.421,   0.37,  0.300,   0.23,  0.217,   0.162, 0.156,   0.137, 0.126,   0.120, 0.116,   0.114, 0.104,   0.102, 0.101],
    )
] 

_L = [
    SpectralSubtype(label=label, temp=t, MS_mass=None)
    for label, t in zip(
        ["L0V", "L1V", "L2V", "L3V", "L4V", "L5V", "L6V", "L7V", "L8V", "L9V"],
        [ 2270,  2160,  2060,  1920,  1870,  1710,  1550,  1530,  1420,  1370],
    )
]

_T = [
    SpectralSubtype(label=label, temp=t, MS_mass=None)
    for label, t in zip(
        ["T0V", "T1V", "T2V", "T3V", "T4V", "T4.5V", "T5V", "T5.5V", "T6V", "T7V", "T7.5V", "T8V", "T9V"],
        [ 1255,  1240,  1220,  1200,  1180,  1170,    1160,  1040,    950,   825,   750,     680,   560],
    )
]

_Y = [
    SpectralSubtype(label=label, temp=t, MS_mass=None)
    for label, t in zip(
        ["Y0V", "Y0.5V", "Y1V", "Y1.5V", "Y2V", "Y4V"],
        [ 450,   400,     360,    325,    320,   250],
    )
]




SPECTRAL_TYPES: List[SpectralType] = [
    SpectralType(letter="O", temp_range=(31_650, 999_999_999_999), MS_mass_range=(18.2, 300),  subtypes=_O),
    SpectralType(letter="B", temp_range=(10_000, 31_650),          MS_mass_range=(2.33, 18.2), subtypes=_B),
    SpectralType(letter="A", temp_range=(7_300, 10_000),           MS_mass_range=(1.68, 2.33), subtypes=_A),
    SpectralType(letter="F", temp_range=(5_960, 7_300),            MS_mass_range=(1.07, 1.68), subtypes=_F),
    SpectralType(letter="G", temp_range=(5_330, 5_960),            MS_mass_range=(0.89, 1.07), subtypes=_G),
    SpectralType(letter="K", temp_range=(3_890, 5_330),            MS_mass_range=(0.58, 0.89), subtypes=_K),
    SpectralType(letter="M", temp_range=(2_310, 3_890),            MS_mass_range=(0.1, 0.58),  subtypes=_M),
]

# # build combo caches once
# for st in SPECTRAL_TYPES:
#     st.build_combo_cache()

# ---------------------------
# Helper
# ---------------------------
def log_fraction_overlap(range_a: Tuple[float,float], range_b: Tuple[float,float]) -> float:
    amin, amax = np.log10(range_a[0]), np.log10(range_a[1])
    bmin, bmax = np.log10(range_b[0]), np.log10(range_b[1])
    inter_min = max(amin, bmin)
    inter_max = min(amax, bmax)
    if inter_max <= inter_min:
        return 0.0
    overlap = inter_max - inter_min
    view_len = bmax - bmin
    if view_len <= 0:
        return 0.0
    return overlap / view_len

# ---------------------------
# Locators / Formatter
# ---------------------------
class SpectralTypeBorderLocator(mticker.Locator):
    def __init__(self, attribute="temp"):
        self.attribute = attribute
    def __call__(self):
        if self.attribute == "temp":
            return [st.temp_range[0] for st in SPECTRAL_TYPES]
        else:
            return [st.MS_mass_range[0] for st in SPECTRAL_TYPES]

class SmartSpectralLabelLocator(mticker.Locator):
    """
    Locator that uses a fast "center-out" greedy algorithm to place labels.
    """
    def __init__(
        self,
        attribute: str = "temp",
        subtype_fraction_threshold: float = 0.6,
        min_subtype_label_px: int = 70,
        draw_subtype_lines: bool = True,
        fallback_fraction: float = 0.0,
        verbose: bool = False,
    ):
        self.attribute = attribute
        self.subtype_fraction_threshold = subtype_fraction_threshold
        self.min_subtype_label_px = float(min_subtype_label_px)
        self.draw_subtype_lines = draw_subtype_lines
        self.fallback_fraction = float(fallback_fraction)
        self.verbose = verbose
        self._label_map: Dict[float, str] = {}

    def __call__(self):
        # Reset mapping
        self._label_map = {}
        axis = self.axis  # this is an Axis instance set by matplotlib
        vmin, vmax = axis.get_view_interval()
        left, right = (min(vmin, vmax), max(vmin, vmax))
        view_log_min, view_log_max = np.log10(left), np.log10(right)
        view_log_len = view_log_max - view_log_min
        if view_log_len <= 0:
            return []

        tick_positions: List[float] = []

        # Ensure renderer exists (so transforms produce sensible output)
        def ensure_renderer():
            fig = axis.figure
            if getattr(fig.canvas, "renderer", None) is None:
                try:
                    fig.canvas.draw()
                except Exception:
                    pass

        axis_name = getattr(axis, "axis_name", None)

        # replace existing xdata_to_px with this:
        def data_to_px(val: float) -> float:
            """Transform a data coordinate (val) on the axis this locator is attached to
            into pixels along that axis (horizontal pixels for x-axis, vertical pixels for y-axis)."""
            # axis.axis_name is 'x' for xaxis and 'y' for yaxis in Matplotlib
            if axis_name == "x":
                # transform (x, y) -> display coords; return horizontal pixel
                disp = axis.axes.transData.transform((val, 0.0))
                return float(disp[0])
            else:
                # y-axis: transform (x, y) and return vertical pixel coordinate
                disp = axis.axes.transData.transform((0.0, val))
                return float(disp[1])

        ensure_renderer()
        # attempt to get pixel width info
        try:
            display_bbox = axis.axes.get_window_extent()
            view_px_width = display_bbox.width
        except Exception:
            view_px_width = None

        # For each spectral type
        for st in SPECTRAL_TYPES:
            if self.attribute == "temp":
                st_min, st_max = st.temp_range
                st_mid = st.temp_midpoint
            elif self.attribute == "mass":
                st_min, st_max = st.MS_mass_range
                st_mid = st.mass_midpoint 
            else: 
                raise ValueError("'attribute' must be either 'temp' or 'mass' ")

            # fraction of axis view this type occupies (in log-space)
            frac = log_fraction_overlap((st_min, st_max), (left, right))

            # Major letter label: keep edge behavior
            in_view_min = max(st_min, left)
            in_view_max = min(st_max, right)
            if in_view_max > in_view_min:
                if (st_min >= left) and (st_max <= right):
                    label_pos = st_mid
                else:
                    label_pos = np.sqrt(in_view_min * in_view_max)
                if not st.subtypes or frac < self.subtype_fraction_threshold:
                    tick_positions.append(label_pos)
                    self._label_map[label_pos] = st.letter

            # Subtype selection
            if st.subtypes and frac >= self.subtype_fraction_threshold:
                if self.attribute == "temp": 
                    attr = "temp" 
                if self.attribute == "mass": 
                    attr = "MS_mass" 
                # candidates strictly within the currently visible portion
                candidate_indices = [i for i, sub in enumerate(st.subtypes) if (getattr(sub, attr) > left) and (getattr(sub, attr) < right)]
                if not candidate_indices:
                    continue 

                # if pixel info not available, choose up to 3 evenly spaced subtypes
                if view_px_width is None:
                    k = min(3, len(candidate_indices))
                    indices = np.linspace(0, len(candidate_indices) - 1, k, dtype=int)
                    selected = [st.subtypes[candidate_indices[i]] for i in indices]
                    if self.verbose:
                        print(f"[locator] no px info -> pick {len(selected)} evenly spaced for {st.letter}")
                
                # --- START: NEW FAST "CENTER-OUT" ALGORITHM ---
                else:
                    # Get pixel positions for candidate subtypes
                    cand_values = np.array([getattr(st.subtypes[i], attr) for i in candidate_indices], dtype=float)
                    cand_px = np.array([data_to_px(t) for t in cand_values], dtype=float)

                    # Get pixel coords for visible edges of the spectral-type region
                    left_px = data_to_px(in_view_min)
                    right_px = data_to_px(in_view_max)
                    if right_px < left_px:
                        left_px, right_px = right_px, left_px
                    
                    view_center_px = (left_px + right_px) / 2.0

                    n_cand = len(candidate_indices)
                    if n_cand == 0:
                        continue
                    
                    # Sort candidates by pixel position
                    order = np.argsort(cand_px)
                    cand_px_sorted = cand_px[order]
                    # Map from sorted local index back to the original *global* index in st.subtypes
                    cand_global_indices_sorted = [candidate_indices[i] for i in order] 
                    
                    # Find index (in the *sorted* list) of the candidate closest to the center
                    i_center = np.argmin(np.abs(cand_px_sorted - view_center_px))
                    
                    selected_global_indices = [] # This will hold the *global* indices from st.subtypes
                    
                    # Add the center-most label
                    selected_global_indices.append(cand_global_indices_sorted[i_center])
                    
                    # Keep track of the last label placed on the left and right
                    last_px_left = cand_px_sorted[i_center]
                    last_px_right = cand_px_sorted[i_center]
                    
                    # "Walk" outwards
                    i_left = i_center - 1
                    i_right = i_center + 1

                    while i_left >= 0 or i_right < n_cand:
                        
                        # Check the label to the left
                        if i_left >= 0:
                            px_left_current = cand_px_sorted[i_left]
                            # If it's far enough from the last label we added on the left...
                            if abs(px_left_current - last_px_left) >= self.min_subtype_label_px:
                                selected_global_indices.append(cand_global_indices_sorted[i_left])
                                last_px_left = px_left_current # Update the "last" position
                            i_left -= 1 # Move one more to the left
                            
                        # Check the label to the right
                        if i_right < n_cand:
                            px_right_current = cand_px_sorted[i_right]
                            # If it's far enough from the last label we added on the right...
                            if abs(px_right_current - last_px_right) >= self.min_subtype_label_px:
                                selected_global_indices.append(cand_global_indices_sorted[i_right])
                                last_px_right = px_right_current # Update the "last" position
                            i_right += 1 # Move one more to the right

                    selected = [st.subtypes[i] for i in selected_global_indices]
                    
                    if self.verbose:
                        print(f"[locator] {st.letter}: center-out selected k={len(selected)}")
                # --- END: NEW FAST "CENTER-OUT" ALGORITHM ---

                # append selected ticks/labels/optional lines
                for sub in selected:
                    tick_positions.append(getattr(sub, attr))
                    self._label_map[getattr(sub, attr)] = f"{sub.label} \n({getattr(sub, attr):,})" 

        # order ticks consistent with axis direction
        if axis.get_view_interval()[0] > axis.get_view_interval()[1]:
            tick_positions = sorted(tick_positions, reverse=True)
        else:
            tick_positions = sorted(tick_positions)
        return tick_positions





class SmartSpectralLabelFormatter(mticker.Formatter):
    def __init__(self, locator: SmartSpectralLabelLocator, default_fontsize: int = 14):
        self.locator = locator
        self.default_fontsize = default_fontsize
    def __call__(self, x, pos=None):
        if not hasattr(self.locator, "_label_map"):
            return ""
        mapping: Dict[float,str] = self.locator._label_map
        if not mapping:
            return ""
        keys = np.array(list(mapping.keys()))
        # find nearest key in log-space
        idx = np.argmin(np.abs(np.log10(keys) - np.log10(x)))
        key = keys[idx]
        if abs(np.log10(key) - np.log10(x)) < 0.02:
            return mapping[key]
        return ""

# ---------------------------
# Integration function
# ---------------------------
def label_spectraltypes(
    ax: plt.Axes,
    location: str = "top",
    attribute: str = "temp",
    label_boundaries: bool = False,
    subtype_fraction_threshold: float = 0.3,
    min_subtype_label_px: int = 70,
    draw_subtype_lines: bool = True,
    fallback_fraction: float = 0.0,
    verbose: bool = False, 
    axis_label: str = "Spectral type", 
):
    """
    Attach spectral-type labels (major letters + dynamic subtypes) to 'ax' via a secondary axis.
    """ 

    # Thousands formatter 
    def thousands_formatter(x, pos=None):
        val = x / 1000.0
        if val.is_integer():
            return f"{int(val)}k"
        return f"{val:.1f}k"

    # Is spectral type axis on the top/bottom (x axis) or left/right (y axis)? 
    if location in ("top", "bottom"):
        sec = ax.secondary_xaxis(location=location)
        axis = sec.xaxis
        span_func = ax.axvspan 
        line_func = ax.axvline 
        set_label = sec.set_xlabel
    else:
        sec = ax.secondary_yaxis(location=location)
        axis = sec.yaxis
        span_func = ax.axhspan 
        line_func = ax.axhline 
        set_label = sec.set_ylabel 

    # Are we plotting the temperature or MS mass? 
    if attribute=="temp": 
        attribute_range = "temp_range" 
        formatter = mticker.FuncFormatter(thousands_formatter)
    else: 
        attribute_range = "MS_mass_range" 
        formatter = mticker.ScalarFormatter() 

    axis.set_major_locator(SpectralTypeBorderLocator(attribute=attribute))
    if label_boundaries: 
        axis.set_major_formatter(formatter) 
    else:
        axis.set_major_formatter(mticker.NullFormatter())
    axis.set_tick_params(which="major", length=20)

    locator = SmartSpectralLabelLocator(
        attribute=attribute,
        subtype_fraction_threshold=subtype_fraction_threshold,
        min_subtype_label_px=min_subtype_label_px,
        draw_subtype_lines=draw_subtype_lines,
        fallback_fraction=fallback_fraction,
        verbose=verbose,
    )
    axis.set_minor_locator(locator)
    axis.set_minor_formatter(SmartSpectralLabelFormatter(locator))
    axis.set_tick_params(which="minor", length=4, labelsize=10)



    st_boundary_colorbands = True   
    st_boundary_lines = False 

    # paint background bands 
    if st_boundary_colorbands == True: 
        colors = cycle(["black", "white"])
        for st in SPECTRAL_TYPES:
            span_func(getattr(st, attribute_range)[1], getattr(st, attribute_range)[0], color=next(colors), alpha=0.03)

    # Add lines separating out each spectral type 
    if st_boundary_lines == True: 
        for st in SPECTRAL_TYPES: 
            line_func(getattr(st, attribute_range)[0], color="black", lw=0.5, ls=(0,(3,12)))

    # Add label ("Spectral type" by default)
    set_label(axis_label, fontsize=14, labelpad=10)






