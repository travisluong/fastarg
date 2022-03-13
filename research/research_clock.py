import time

def clock(func):
    def clocked(*args): #
        t0 = time.perf_counter()
        result = func(*args) #
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    
    return clocked #

@clock
def snooze(seconds):
    time.sleep(seconds)

snooze(5)