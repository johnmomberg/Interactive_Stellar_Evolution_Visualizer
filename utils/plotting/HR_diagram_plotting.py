import numpy as np 
from fractions import Fraction 
import functools 

import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 

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
    f_max = 0.5  
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








class SpectralTypeBorderLocator(mticker.Locator):
    def __init__(self, attribute="temp"):
        self.attribute = attribute  

    def __call__(self): 
        if self.attribute == "temp": 
            tick_positions = [st.temp_range[0] for st in plot_options.SPECTRAL_TYPES]
        if self.attribute == "mass": 
            tick_positions = [st.MS_mass_range[0] for st in plot_options.SPECTRAL_TYPES]
        return tick_positions 





class SpectralTypeLabelLocator(mticker.Locator):
    def __init__(self, attribute="temp"):
        self.attribute=attribute 

    def __call__(self):
        
        window_left, window_right = self.axis.get_view_interval() 
        label_positions = [] 

        # HR Diagram: Reverse axis 
        if window_left > window_right: 

            for spectral_type in plot_options.SPECTRAL_TYPES: 

                if self.attribute == "temp": 
                    st_mid = spectral_type.temp_midpoint 
                    st_right, st_left = spectral_type.temp_range 
                if self.attribute == "mass": 
                    st_mid = spectral_type.mass_midpoint  
                    st_right, st_left = spectral_type.MS_mass_range 

                if window_left > st_left and st_right > window_right: 
                    label_positions.append(st_mid)
                elif window_left > st_left and st_left > window_right > st_right: 
                    label_positions.append(np.sqrt(st_left*window_right))
                elif st_right > window_right and st_left > window_left > st_right: 
                    label_positions.append(np.sqrt(window_left*st_right))
                elif st_left > window_left and window_right > st_right: 
                    label_positions.append(np.sqrt(window_left*window_right))
                else: 
                    label_positions.append(2*window_left) 

        # Normal axis 
        if window_left < window_right:

            for spectral_type in plot_options.SPECTRAL_TYPES: 

                if self.attribute == "temp": 
                    st_mid = spectral_type.temp_midpoint 
                    st_left, st_right = spectral_type.temp_range 
                if self.attribute == "mass": 
                    st_mid = spectral_type.mass_midpoint  
                    st_left, st_right = spectral_type.MS_mass_range 

                if window_left < st_left and st_right < window_right: 
                    label_positions.append(st_mid)
                elif window_left < st_left and st_left < window_right < st_right: 
                    label_positions.append(np.sqrt(st_left*window_right))
                elif st_right < window_right and st_left < window_left < st_right: 
                    label_positions.append(np.sqrt(window_left*st_right))
                elif st_left < window_left and window_right < st_right: 
                    label_positions.append(np.sqrt(window_left*window_right))
                else: 
                    label_positions.append(0.5*window_left) 
            
        return label_positions 






class SpectralTypeLabelFormatter(mticker.Formatter):
    def __init__(self):
        pass 

    def __call__(self, x, pos):
        return plot_options.SPECTRAL_TYPES[pos].letter 










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





    @staticmethod 
    def label_spectraltypes(ax, location="top", attribute="temp", label_boundaries=False): 

        if location in ("top", "bottom"):
            ax_labels = ax.secondary_xaxis(location=location)
            axis = ax_labels.xaxis
            span_func = ax.axvspan 
            label_func = ax_labels.set_xlabel

        elif location in ("left", "right"):
            ax_labels = ax.secondary_yaxis(location=location)
            axis = ax_labels.yaxis
            span_func = ax.axhspan 
            label_func = ax_labels.set_ylabel

        # Major ticks = borders (long lines, no labels)
        axis.set_major_locator(SpectralTypeBorderLocator(attribute=attribute)) 
        if label_boundaries == False: 
            axis.set_major_formatter(mticker.NullFormatter()) 
        if label_boundaries == True: 
            axis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{x}"))
        ax_labels.tick_params(length=15, which="major")

        # Minor ticks = labels (no lines, but show text)
        axis.set_minor_locator(SpectralTypeLabelLocator(attribute=attribute))
        axis.set_minor_formatter(SpectralTypeLabelFormatter())
        ax_labels.tick_params(length=0, which="minor", labelsize=14)  

        if attribute=="temp": 
            for spectral_type in plot_options.SPECTRAL_TYPES: 
                span_func(spectral_type.temp_range[1], spectral_type.temp_range[0], color=spectral_type.color, alpha=0.05)

        if attribute=="mass": 
            for spectral_type in plot_options.SPECTRAL_TYPES: 
                span_func(spectral_type.MS_mass_range[1], spectral_type.MS_mass_range[0], color=spectral_type.color, alpha=0.05)

        label_func("Spectral type", fontsize=14)





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




