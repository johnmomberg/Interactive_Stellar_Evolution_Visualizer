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





