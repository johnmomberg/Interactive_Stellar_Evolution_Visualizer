import matplotlib.ticker as mticker 
import numpy as np 
from fractions import Fraction 





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

