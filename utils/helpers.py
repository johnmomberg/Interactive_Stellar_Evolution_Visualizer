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
    return round(x, num_sigfigs - int(math.floor(math.log10(abs(x)))) - 1)





# Convert a float to a string and zero-pad it until it has 20 digits before the decimal and then another 20 digits afer the decimal. 
def format_number(num): 
    if num < 1e-4: 
        s = f"{num:.20f}"
    else: 
        s = str(num)
    if '.' not in s:
        s += '.'
    left, right = s.split('.')
    left = left.rjust(20, '0')  # pad to 20 digits on the left
    right = right.ljust(20, '0')  # pad to 20 digits on the right
    return f"{left}.{right[:20]}"  # limit to 20 digits after decimal





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