import os
import threading
import time
# import ipdb
import numpy as np
from functools import wraps


class Catch(object):
    '''
    ------------------------------------------------------
    G. Moille - NIST - 2018
    ------------------------------------------------------
    '''
    def error(fun):
        def wrap(*args, **kwargs):
            instr = args[0]
            out = fun(*args, **kwargs)
            # s('catch error')
            if hasattr(instr, 'has_error'):
                if instr.has_error:
                    instr._err_msg += '\n' + instr.error
            return out
        return wrap


class InOut(object):
    '''
    ------------------------------------------------------
    G. Moille - NIST - 2018
    ------------------------------------------------------
    '''
    def output(*types):
        def convert(fun):
            @wraps(fun)
            def wrap(*args, **kwargs):
                instr = args[0]
                while True:

                    # first get the result
                    out = fun(*args, **kwargs)
                    if hasattr(instr, 'has_error'):
                        if instr.has_error:
                            # print('accept')
                            err = instr.error
                            instr._err_msg +=  '\n' + err
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
                            if t == bool:
                                out2[cnt] = t(int(o))
                            else:
                                out2[cnt] = t(o)
                            cnt+=1
                        break

                    # if it didnt' work, try to redo
                    # it again
                    except Exception as e:

                        # print('Exception:')
                        # print(e)
                        # print(o)
                        # ipdb.set_trace()
                        # print('-----communication error... retrying...')
                        # time.sleep(0.1)
                        if hasattr(instr, 'has_error'):
                            err =  instr.error + 'Comminication issue  ..retrying..'
                            # print(err)

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
                    if t == float and type(a) == int:
                        pass
                    elif not isinstance(a,t):
                        failed = True
                if not failed:
                    out = fun(*args, **kwargs)
                    if hasattr(instr, 'has_error'):
                        if instr.has_error:
                            print('accept')
                            err = instr.error
                            instr._err_msg +=  '\n' + err
                    else:
                        out = None
                else:
                    out = None

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
                    print('Changing State Loop')
                    if laser._open:
                        err_stat = len(laser._err_msg.split('\n'))<2
                        print(err_stat)
                        err_dum = ''.join(laser._err_msg.split('\n'))
                        print('--' + err_dum + '--')
                        if not np.abs(target_lbd-laser.lbd)<0.01 and err_stat:
                            laser._is_changing_lbd = True
                        else:
                            laser._is_changing_lbd = False
                            break
                    else:
                        laser._is_changing_lbd = False
                        break


            thread = threading.Thread(target=CheckWavelength, args=())
            thread.daemon = True
            out = fun(*args, **kwargs)
            if hasattr(laser, 'has_error'):
                if laser.has_error:
                    # print('accept')
                    err = laser.error
                    laser._err_msg +=  '\n' + err
            thread.start()
            return out

        return wrapper

    def scan(start_word, stop_word):
        def decorator(fun):
            @wraps(fun)
            def wrapper(*args,**kwargs):
                # def the function to be thread which check the wavelength
                def ReturnWavelength():
                    while not target_lbd-laser.lbd<0.02 and laser._is_scaning :
                        laser._is_scaning = True
                        # laser._lbdscan = laser.lbd

                    laser._is_scaning = False
                    laser.Query(stop_word)
                    # laser._err_msg += '\n' + str(laser.error)  + 'END OF SCAN--'
                    print(laser.error  + 'END OF SCAN--')

                # retrieve params
                laser = args[0]
                lim = laser.scan_limit
                target_lbd = lim[1]

                # setup the thread in case
                laser.threadscan = threading.Thread(target=ReturnWavelength, args=())
                laser.threadscan.daemon = True

                # exec the fun
                out = fun(*args,**kwargs)
                if hasattr(laser, 'has_error'):
                    if laser.has_error:
                        # print('accept')
                        err = laser.error
                        laser._err_msg +=  '\n' + err
                if laser._scan:
                    laser._is_scaning = True
                    # laser._lbdscan = laser.lbd
                    laser.threadscan.start()
                else:
                    laser._is_scaning = False
                return out
            return wrapper
        return decorator

if __name__ == "__main__":
    pass
