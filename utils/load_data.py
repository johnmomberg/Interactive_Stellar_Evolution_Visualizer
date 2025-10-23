import mesa_reader as mr 
import numpy as np 
from functools import lru_cache 
import matplotlib.ticker as mticker 






# lru_cache allows you to cache function calls. maxsize is the number of distinct calls it can hold in memory at once. 
# If you run load_history() on the same input a 2nd time, it doesn't actually run the function again; 
# it just loads the pre-saved data. This makes load_history much faster. 
@lru_cache(maxsize=32) 
def load_history(MESA_folder_path): 

    try: 
        history = mr.MesaData(str(MESA_folder_path/"history.data"))  
        folder_mesa = mr.MesaLogDir(MESA_folder_path, history_file="history.data") 

    except FileNotFoundError: 
        history = mr.MesaData(str(MESA_folder_path/"trimmed_history.data"))  
        folder_mesa = mr.MesaLogDir(MESA_folder_path, history_file="trimmed_history.data") 

    # Add list of available model numbers to History object 
    history.model_numbers_available = folder_mesa.model_numbers 

    # Calculate the number of sig figs required to display each age so that it's distinct from its neighbors 
    ages = history.star_age
    deltas_left = np.diff(ages, prepend=ages[0])
    deltas_right = np.diff(ages, append=ages[-1])
    min_diffs = np.minimum(deltas_left, deltas_right)
    n_sig = np.clip(np.ceil(-np.log10(min_diffs / np.abs(ages))), 2, 8).astype(int) + 1 
    age_strings = [mticker.EngFormatter()(float(f'{ages[i]:.{n_sig[i]}g}')) for i in range(len(ages))] 
    history.age_strings = age_strings 
    history.initial_mass_string = round(history.star_mass[0], 10)

    return history 





@lru_cache(maxsize=128)
def load_profile(MESA_folder_path, modelnum, history=None): 

    try: 
        folder_mesa = mr.MesaLogDir(str(MESA_folder_path), history_file="history.data") 

    except mr.BadPathError: 
        folder_mesa = mr.MesaLogDir(str(MESA_folder_path), history_file="trimmed_history.data") 

    # Load profile; add some additional important info to profile variable 
    profile = folder_mesa.profile_data(modelnum) 
    profile.modelnum = modelnum 
    profile.index = modelnum-1 
    if history is not None: 
        profile.age = history.star_age[profile.index] 
        profile.age_string = history.age_strings[profile.index] 
        profile.initial_mass = history.star_mass[0] 
        profile.initial_mass_string = history.initial_mass_string 
    return profile 





