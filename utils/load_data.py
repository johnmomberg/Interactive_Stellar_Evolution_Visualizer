import mesa_reader as mr 
import numpy as np 
from functools import lru_cache 
import matplotlib.ticker as mticker 
import utils.helpers as helpers 






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

    # Add initial mass string (used for plot titles)
    history.initial_mass_string = round(history.star_mass[0], 10)

    # Add list of age strings (used for titles) 
    # Calculates just enough decimal places for each string to be distinct from its neighbors and puts it in engineering notation 
    history.age_strings = [str(age) for age in history.star_age] # Initialize array 
    for ind in range(len(history.model_numbers_available)):

        # current model 
        modelnum_current = history.model_numbers_available[ind]
        age_current = history.star_age[modelnum_current-1]

        # previous model
        if ind == 0:
            modelnum_previous = np.nan
            age_previous = 0.0
        else:
            modelnum_previous = history.model_numbers_available[ind - 1]
            age_previous = history.star_age[modelnum_previous-1]

        # next model
        if ind == len(history.model_numbers_available) - 1:
            modelnum_next = np.nan
            age_next = age_current*2
        else:
            modelnum_next = history.model_numbers_available[ind + 1]
            age_next = history.star_age[modelnum_next-1]


        num_sigfigs = np.max([len(str(age).replace(".", "")) for age in [age_previous, age_current, age_next]]) 
        

        # Initialize 
        rounded_previous = helpers.round_sigfigs(age_previous, num_sigfigs) 
        rounded_current = helpers.round_sigfigs(age_current, num_sigfigs) 
        rounded_next = helpers.round_sigfigs(age_next, num_sigfigs) 

        # Keep looping until rounding has gone too far, then take the previous iteratin 
        while str(rounded_current) != str(rounded_previous) and str(rounded_current) != str(rounded_next): 

            age_previous = rounded_previous 
            age_current = rounded_current 
            age_next = rounded_next 

            rounded_previous = helpers.round_sigfigs(age_previous, num_sigfigs) 
            rounded_current = helpers.round_sigfigs(age_current, num_sigfigs) 
            rounded_next = helpers.round_sigfigs(age_next, num_sigfigs) 

            num_sigfigs-=1 

            # Minimum of 4 sig figs 
            if num_sigfigs <= 2: 
                break         


        power = np.floor(np.log10(age_current)) 
        if power == 12 or power == 13 or power == 14: 
            n = 12 
            suffix = " T years"
        elif power == 9 or power == 10 or power == 11: 
            n = 9 
            suffix = " G years" 
        elif power == 6 or power == 7 or power == 8: 
            n = 6 
            suffix = " M years" 
        elif power == 3 or power == 4 or power == 5: 
            n = 3 
            suffix = " k years"
        else: 
            n = 0 
            suffix = " years" 
        
        
        mantissa = helpers.round_sigfigs(age_current / 10**n, num_sigfigs+2) 
        age_string_final = str(mantissa) + suffix
        history.age_strings[modelnum_current-1] = age_string_final 

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





