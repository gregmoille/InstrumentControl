#!/Users/greg/miniforge3/bin/python

import os
import sys
from pprint import pprint
from plotly import graph_objects as go
from yokogawa import Yokogawa

par = dict(centwlgth= 1.21e-06,
            span= 9.8e-07,
            # pts= 50001.0,
            pts_auto= 1,
            resolution= 0.02e-9,
            sensitivity= 3,
        #    resolution= 1e-9, 
        #    sensitivity= 1,
           calib_zero=0
        )


dict(centwlgth= 1.21e-06,
    span= 9.8e-07,
    pts_auto= 1,
    resolution= 1e-9,
    sensitivity= 1,
    calib_zero=0
        )

with Yokogawa(ip ="10.0.0.21") as instr: 
    print('connected to Yokogawa OSA')

    print("**Original Settings:**")
    settings = instr.settings
    pprint(settings)
    
    instr.settings = par
    
    print("**New Settings:**")
    settings = instr.settings
    pprint(settings)
    
    instr.scan = "repeat"
    for ii in range(3):
        trace = instr.trace
        pprint("Trace")
        pprint(trace)
    instr.scan = "stop"


    


