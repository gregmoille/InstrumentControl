import os
import threading
import time
import ipdb
import numpy as np
from functools import wraps

class InOut(object):
    def output(*types):
        def convert(fun):
            @wraps(fun)
            def wrap(*args, **kwargs):
                instr = args[0]
                while True:
                    
                    # first get the result
                    out = fun(*args, **kwargs)

                    # check if we specified a type
                    # for all the outputs
                    if not type(out) == list:
                        out = [out]
                    assert len(out) == len(types)

                    out2 = [None]*len(out)
                    cnt = 0
                    # ipdb.set_trace()
                    try:
                        ##convert into the right type 
                        for o, t in zip(out, types):
                            out2[cnt] = t(o)
                            cnt+=1
                        break

                    # if it didnt' work, try to redo
                    # it again
                    except:
                        
                        # ipdb.set_trace()
                        print('communication error... retrying...')
                        time.sleep(0.05)
                        if hasattr(instr, 'error'):
                            err = instr.error
                            print(err)

                # avoid to return a list if the 
                # length is only 1
                if len(out2) == 1:
                    return out2[0]
                else:
                    return out2

            return wrap
        return convert
    def accepts(*types):
        def check(fun):
            @wraps(fun)
            def wrap(*args, **kwargs):
                instr = args[0]
                assert len(types) == len(args) - 1
                failed = False
                for a, t in zip(args[1::], types):
                    if not isinstance(a,t):
                        failed = True
                
                if not failed:    
                    while true:
                        out = fun(*args, **kwargs)
                        if hasattr(instr, 'error'):
                            err = instr.error
                            if not err == instr._no_error:
                                break
                        else:
                            break
                    return out
            return wrap
        return check

class ChangeState(object):
    def lbd(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            # get the class
            # ipdb.set_trace()
            laser = args[0]
            target_lbd = args[1]
            laser._old_lbd = laser.lbd
            def CheckWavelength():
                while True:
                    if not np.abs(target_lbd-laser.lbd)<0.01:
                        laser._is_changing_lbd = True
                    else:
                        laser._is_changing_lbd = False
                        break

            thread = threading.Thread(target=CheckWavelength, args=())
            thread.daemon = True
            out = fun(*args, **kwargs)
            thread.start()
            return out

        return wrapper

    def scan(start_word, stop_word):
        def decorator(fun):
            @wraps(fun)
            def wrapper(*args,**kwargs):
                # def the function to be thread which check the wavelength
                def ReturnWavelength():
                    while not np.abs(target_lbd-laser.lbd)<0.01 and laser._is_scaning:
                        laser._is_scaning = True
                        laser._lbdscan = laser.lbd

                    
                    laser.Querry(stop_word)
                    laser._is_scaning = False
                    print(laser.error)
                    


                # retrieve params
                laser = args[0]
                lim = laser.scan_limit
                target_lbd = lim[1]
                
                # setup the thread in case
                laser.threadscan = threading.Thread(target=ReturnWavelength, args=())
                laser.threadscan.daemon = True

                # exec the fun
                out = fun(*args,**kwargs)

                if laser._scan:
                    laser._is_scaning = True
                    laser._lbdscan = laser.lbd
                    laser.threadscan.start()
                else:
                    laser._is_scaning = False
                return out
            return wrapper
        return decorator

if __name__ == "__main__":
    pass
