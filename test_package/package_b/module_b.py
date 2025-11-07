import numpy as np 
import test_package.package_a.module_a


def func_b(x): 
    return np.sin(test_package.package_a.module_a.func_a(x)) 