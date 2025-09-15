import numpy as np 
from fractions import Fraction 
import functools 

import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 

import utils.config.plot_options as plot_options 

from dataclasses import dataclass, field
import itertools
from typing import List, Tuple, Dict




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

        self.fig, self.ax = plt.subplots(figsize=(10.7, 7))
        self.fig.subplots_adjust(top=0.87, bottom=0.15, left=0.12, right=0.96)


        # X axis: Temperature 
        self.ax.set_xlabel("Effective Temperature (K)", fontsize=18, labelpad=14)
        self.ax.set_xscale("log")
        self.ax.set_xlim((80000, 1000)) 
        
        self.ax.xaxis.set_major_locator(MajorLogLocator()) 
        self.ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}")) 

        self.ax.xaxis.set_minor_locator(MinorLogLocator()) 
        self.ax.xaxis.set_minor_formatter(mticker.NullFormatter())         


        # Y axis: Luminosity 
        self.ax.set_ylabel("Luminosity ($L_{{sun}}$)", fontsize=18, labelpad=14)
        self.ax.set_yscale("log")
        self.ax.set_ylim((1e-6, 1e8))

        # Grid, ticks, title 
        self.ax.tick_params(labelsize=14, length=10, which="major") 
        # self.ax.tick_params(length=0, which="minor") 
        self.ax.grid(alpha=0.5, which="both")
        self.ax.set_title("Evolutionary Path on HR Diagram", fontsize=20, pad=15) 



    def add_path(self, history, color=None, label=None, lw=2, alpha=1): 
        self.ax.plot(
            10**history.log_Teff, 
            10**history.log_L, 
            color=color, 
            label=label, 
            lw=lw, 
            alpha=alpha)



    def legend(self): 
        self.ax.legend(fontsize=14) 





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
    temp: float       # Teff in Kelvin
    MS_mass: float = 1.0

@dataclass
class SpectralType:
    letter: str
    temp_range: Tuple[float, float]       # (min, max) in Kelvin
    MS_mass_range: Tuple[float, float]
    color: str
    subtypes: List[SpectralSubtype] = field(default_factory=list)
    combo_cache: Dict[int, List[Dict]] = field(default_factory=dict, init=False)

    @property
    def temp_midpoint(self) -> float:
        a, b = self.temp_range
        return np.sqrt(a * b)

    @property
    def mass_midpoint(self) -> float:
        a, b = self.MS_mass_range
        return np.sqrt(a * b)

    def build_combo_cache(self, min_k: int = 2):
        """
        Precompute combinations for the subtype list. For each k in [min_k..n],
        produce a list of dicts {'indices': (i1,i2,..), 'min_log_spacing': float}
        sorted descending by min_log_spacing (heuristic) so likely-good combos are tried first.
        """
        self.combo_cache = {}
        n = len(self.subtypes)
        if n < min_k:
            return
        # precompute logs
        subtype_logs = np.array([np.log10(s.temp) for s in self.subtypes], dtype=float)
        edge_left_log = np.log10(self.temp_range[0])
        edge_right_log = np.log10(self.temp_range[1])
        for k in range(min_k, n + 1):
            combos = []
            for comb in itertools.combinations(range(n), k):
                seq_logs = np.concatenate(([edge_left_log], subtype_logs[list(comb)], [edge_right_log]))
                spacings = np.diff(seq_logs)
                min_log_spacing = float(np.min(spacings))
                combos.append({'indices': comb, 'min_log_spacing': min_log_spacing})
            combos.sort(key=lambda d: d['min_log_spacing'], reverse=True)
            self.combo_cache[k] = combos

# ---------------------------
# Default spectral data
# ---------------------------
_O = [SpectralSubtype(label=f"O{n}", temp=t) for n, t in zip(range(3,10), [                     44900, 42900, 41400, 39500, 37100, 35100, 33100])]
_B = [SpectralSubtype(label=f"B{n}", temp=t) for n, t in zip(range(0,10), [31400, 26000, 20600, 17000, 16400, 15700, 14500, 14000, 12300, 10700])]
_A = [SpectralSubtype(label=f"A{n}", temp=t) for n, t in zip(range(0,10), [9700,  9300,  8800,  8600,  8250,  8100,  7910,  7760,  7590,  7400])]
_F = [SpectralSubtype(label=f"F{n}", temp=t) for n, t in zip(range(0,10), [7220,  7020,  6820,  6750,  6670,  6550,  6350,  6280,  6180,  6050])]
_G = [SpectralSubtype(label=f"G{n}", temp=t) for n, t in zip(range(0,10), [5930,  5860,  5770,  5720,  5680,  5660,  5600,  5550,  5480,  5380])]
_K = [SpectralSubtype(label=f"K{n}", temp=t) for n, t in zip(range(0,10), [5270,  5170,  5100,  4830,  4600,  4440,  4300,  4100,  3990,  3930])]  
_M = [SpectralSubtype(label=f"M{n}", temp=t) for n, t in zip(range(0,10), [3850,  3660,  3560,  3430,  3210,  3060,  2810,  2680,  2570,  2380])]  

SPECTRAL_TYPES: List[SpectralType] = [
    SpectralType(letter="O", temp_range=(33000.0, 500000.0), MS_mass_range=(16, 300), color="black", subtypes=_O),
    SpectralType(letter="B", temp_range=(10000.0, 33000.0),  MS_mass_range=(2.1, 16),  color="white", subtypes=_B),
    SpectralType(letter="A", temp_range=(7300.0, 10000.0),   MS_mass_range=(1.4, 2.1), color="black", subtypes=_A),
    SpectralType(letter="F", temp_range=(6000.0, 7300.0),    MS_mass_range=(1.04, 1.4), color="white", subtypes=_F),
    SpectralType(letter="G", temp_range=(5300.0, 6000.0),    MS_mass_range=(0.8, 1.04), color="black", subtypes=_G),
    SpectralType(letter="K", temp_range=(3900.0, 5300.0),    MS_mass_range=(0.45, 0.8), color="white", subtypes=_K),
    SpectralType(letter="M", temp_range=(2300.0, 3900.0),    MS_mass_range=(0.08, 0.45), color="black", subtypes=_M),
]

# build combo caches once
for st in SPECTRAL_TYPES:
    st.build_combo_cache()

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
    Locator that uses precomputed combo_cache on SpectralType objects to speed up selection.
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

        def xdata_to_px(xdata: float) -> float:
            disp = axis.axes.transData.transform((xdata, 0.0))
            return float(disp[0])

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
            else:
                st_min, st_max = st.MS_mass_range
                st_mid = st.mass_midpoint

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
                # candidates strictly within the currently visible portion
                candidate_indices = [i for i, sub in enumerate(st.subtypes) if (sub.temp > left) and (sub.temp < right)]
                if not candidate_indices:
                    continue

                # if pixel info not available, choose up to 3 evenly spaced subtypes
                if view_px_width is None:
                    k = min(3, len(candidate_indices))
                    indices = np.linspace(0, len(candidate_indices) - 1, k, dtype=int)
                    selected = [st.subtypes[candidate_indices[i]] for i in indices]
                    if self.verbose:
                        print(f"[locator] no px info -> pick {len(selected)} evenly spaced for {st.letter}")
                else:
                    # pixel positions for candidate temps
                    cand_temps = np.array([st.subtypes[i].temp for i in candidate_indices], dtype=float)
                    cand_px = np.array([xdata_to_px(t) for t in cand_temps], dtype=float)

                    # pixel coords for visible edges of the spectral-type region
                    left_px = xdata_to_px(in_view_min)
                    right_px = xdata_to_px(in_view_max)
                    if right_px < left_px:
                        left_px, right_px = right_px, left_px

                    n_cand = len(candidate_indices)
                    if n_cand == 1:
                        selected = [st.subtypes[candidate_indices[0]]]
                    else:
                        # sort candidates by pixel coordinate left->right
                        order = np.argsort(cand_px)
                        cand_px_sorted = cand_px[order]
                        cand_idx_sorted = [candidate_indices[i] for i in order]
                        cand_list_sorted = [st.subtypes[i] for i in cand_idx_sorted]

                        # lazy build cache if missing
                        if not hasattr(st, "combo_cache") or not st.combo_cache:
                            st.build_combo_cache(min_k=2)

                        # helper: minimal adjacent pixel spacing for a combo of global indices
                        def min_px_spacing_for_combo_global_indices(combo_indices):
                            px_seq = [left_px]
                            for gi in combo_indices:
                                try:
                                    pos = cand_idx_sorted.index(gi)
                                except ValueError:
                                    # combo uses a subtype not currently visible -> invalid for this view
                                    return -1.0
                                px_seq.append(float(cand_px_sorted[pos]))
                            px_seq.append(right_px)
                            spacings = np.diff(np.array(px_seq))
                            return float(np.min(spacings))

                        # find best pair using cache first
                        best2_min = -1.0
                        best2_indices = None
                        cache_k2 = st.combo_cache.get(2, [])
                        for rec in cache_k2:
                            comb = rec['indices']
                            # skip combos not fully in candidate set
                            if not all((gi in cand_idx_sorted) for gi in comb):
                                continue
                            min_px = min_px_spacing_for_combo_global_indices(comb)
                            if min_px > best2_min:
                                best2_min = min_px
                                best2_indices = comb

                        # fallback: explicit check of pairs among candidate set if cache offered none
                        if best2_indices is None:
                            for comb in itertools.combinations(cand_idx_sorted, 2):
                                min_px = min_px_spacing_for_combo_global_indices(comb)
                                if min_px > best2_min:
                                    best2_min = min_px
                                    best2_indices = comb

                        # If best pair doesn't meet threshold, pick single-best
                        if best2_min < self.min_subtype_label_px:
                            best_single_score = -1.0
                            best_single_idx = cand_idx_sorted[0]
                            for gi in cand_idx_sorted:
                                pos = cand_idx_sorted.index(gi)
                                d_left = abs(cand_px_sorted[pos] - left_px)
                                d_right = abs(right_px - cand_px_sorted[pos])
                                score = min(d_left, d_right)
                                if score > best_single_score:
                                    best_single_score = score
                                    best_single_idx = gi
                            selected = [st.subtypes[best_single_idx]]
                            if self.verbose:
                                print(f"[locator] {st.letter}: best pair min_px={best2_min:.1f}px < threshold {self.min_subtype_label_px:.1f}px -> single selected")
                        else:
                            accepted_indices = best2_indices
                            accepted_k = 2
                            # try larger k using cache then explicit combos among candidate set
                            n_total = len(st.subtypes)
                            for k in range(3, n_total + 1):
                                best_min_for_k = -1.0
                                best_inds_for_k = None
                                cachek = st.combo_cache.get(k, [])
                                for rec in cachek:
                                    comb = rec['indices']
                                    if not all((gi in cand_idx_sorted) for gi in comb):
                                        continue
                                    min_px = min_px_spacing_for_combo_global_indices(comb)
                                    if min_px > best_min_for_k:
                                        best_min_for_k = min_px
                                        best_inds_for_k = comb
                                    # small early break heuristic: if min_px already >> threshold we might accept quickly
                                # if none from cache matched, explicitly try combos formed from candidate set
                                if best_inds_for_k is None:
                                    if len(cand_idx_sorted) >= k:
                                        for comb_local in itertools.combinations(cand_idx_sorted, k):
                                            min_px = min_px_spacing_for_combo_global_indices(comb_local)
                                            if min_px > best_min_for_k:
                                                best_min_for_k = min_px
                                                best_inds_for_k = comb_local
                                if best_inds_for_k is not None and best_min_for_k >= self.min_subtype_label_px:
                                    accepted_indices = best_inds_for_k
                                    accepted_k = k
                                    continue
                                else:
                                    # stop and keep previous accepted_k
                                    break
                            selected = [st.subtypes[i] for i in accepted_indices]
                            if self.verbose:
                                print(f"[locator] {st.letter}: accepted_k={accepted_k}")

                # append selected ticks/labels/optional lines
                for sub in selected:
                    tick_positions.append(sub.temp)
                    self._label_map[sub.temp] = sub.label
                    # if self.draw_subtype_lines:
                    #     axis.axes.axvline(sub.temp, ymin=0, ymax=1, linestyle=':', linewidth=0.6, alpha=0.5, zorder=1)

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
    do_axis_label: bool = True, 
):
    """
    Attach spectral-type labels (major letters + dynamic subtypes) to 'ax' via a secondary axis.
    """
    if location in ("top", "bottom"):
        sec = ax.secondary_xaxis(location=location)
        axis = sec.xaxis
        span_func = ax.axvspan
        set_label = sec.set_xlabel
    else:
        sec = ax.secondary_yaxis(location=location)
        axis = sec.yaxis
        span_func = ax.axhspan
        set_label = sec.set_ylabel

    axis.set_major_locator(SpectralTypeBorderLocator(attribute=attribute))
    if label_boundaries: 

        if attribute == "temp": 
            def thousands_formatter(x, pos=None):
                val = x / 1000.0
                if val.is_integer():
                    return f"{int(val)}k"
                return f"{val:.1f}k"
            axis.set_major_formatter(mticker.FuncFormatter(thousands_formatter))
        else: 
            axis.set_major_formatter(mticker.ScalarFormatter()) 
    else:
        axis.set_major_formatter(mticker.NullFormatter())
    axis.set_tick_params(which="major", length=12)

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
    axis.set_tick_params(which="minor", length=6, labelsize=14, pad=6)

    # paint background bands
    if attribute == "temp":
        for st in SPECTRAL_TYPES:
            span_func(st.temp_range[1], st.temp_range[0], color=st.color, alpha=0.05)
    else:
        for st in SPECTRAL_TYPES:
            span_func(st.MS_mass_range[1], st.MS_mass_range[0], color=st.color, alpha=0.05)

    if do_axis_label==True: 
        set_label("Spectral type", fontsize=14)





