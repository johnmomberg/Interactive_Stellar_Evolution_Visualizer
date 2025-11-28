import numpy as np 
import math 
import matplotlib.colors as mcolors 





def to_engineering(x): 

    exponent = int(np.floor(np.log10(x)))
    coeff = x / 10**exponent 

    while exponent % 3 != 0: 
        exponent = exponent = exponent-1
        coeff = x / 10**exponent  

    return f"{coeff} x 10^{exponent}" 





def round_sigfigs(x, num_sigfigs): 
    if x == 0:
        return 0.0 
    rounded_num = round(x, num_sigfigs - int(math.floor(math.log10(abs(x)))) - 1) 
    if rounded_num - math.floor(rounded_num) == 0.0: 
        rounded_num = int(rounded_num) 
    return rounded_num 





# Input: mass (solar masses) 
# Output: luminosity (solar luminosities) 
def mass_luminosity_relation(M): 
    if M<0.43: 
        L_predicted = 0.23 * M**2.3
    if 0.43<=M<2: 
        L_predicted = M**4 
    if 2<=M<55: 
        L_predicted = 1.4 * M**3.5 
    if M>=55: 
        L_predicted = 32000 * M 
    return L_predicted 





# Convert from matlotlib color name (i.e., "dodgerblue") to the string used in CSS to set text color
def set_textcolor_css(text, mpl_color): 
    css_color = mcolors.to_hex(mpl_color) 
    colored_text = f"<span style='color:{css_color}'>{text}</span>" 
    return colored_text 





# Custom version of List that acts exactly the same, except when you print it, each item is displayed on its own line 
class CustomList(list):
    def __str__(self):
        # Add header, body (each item on its own line), and footer
        inner = "\n".join("  " + str(item) for item in self)
        return f"CustomList([\n{inner}\n])"

    def __repr__(self):
        return self.__str__()





# Blend a color with white to get what that color would be if it had an alpha of 1 
def blend_with_white(input_color, alpha=None):
    
    # Input must be either 3 length array, tuple, or string 
    if type(input_color) is str: 
        color_rgb_3array = np.array(mcolors.to_rgb(input_color)) 
    elif type(input_color) is tuple and len(input_color) == 3: 
        color_rgb_3array = np.array(input_color) 
    elif type(input_color) is np.ndarray and len(input_color) == 3: 
        color_rgb_3array = input_color 
    elif type(input_color) is tuple and len(input_color) == 4: 
        color_rgb_3array = np.array(input_color)[0:3] 
        alpha = np.array(input_color)[3] 
    elif type(input_color) is np.ndarray and len(input_color) == 4: 
        color_rgb_3array = input_color[0:3] 
        alpha = input_color[3] 
    else: 
        raise ValueError("Input error")

    color_rgba_4array = np.append(color_rgb_3array, alpha) 
    output_color = color_rgba_4array[0:3]*color_rgba_4array[3] + np.array([1.0, 1.0, 1.0]) * (1 - color_rgba_4array[3]) 
    return output_color 