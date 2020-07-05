# -*- coding: utf-8 -*-

# Does not work because both the module "u" and the function
# orbital_speed() in the with block become undefined.

import numpy as np
import astropy.units as u
from astropy.constants import G, M_earth, R_earth
from guietta import Gui, ___, HValueSlider

def orbital_speed(h):
    '''h = height over earth surface'''
    return np.sqrt(G * M_earth / (R_earth + h))


hslider = HValueSlider('h', myrange=range(500,40000), unit='km')

gui = Gui(
   ['Orbital height:', hslider, ___ ],
   [ 'results', ___, ___ ],

)

with gui.h:
    info = {}
    info['Orbital height:'] = gui.h * u.km
    info['Orbital speed:'] = orbital_speed(gui.h * u.km)
    info['Orbital length:'] = 2*np.pi*gui.h * u.km
    gui.results = info

gui.run()
