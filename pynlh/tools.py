from time import time


def timer(func):
    """Wrapper function to time the elapesd time of a certain function.
     Can be used as a decorator.
    """
    def timed(*args, **kwargs):
        ts = time()
        result = func(*args, **kwargs)
        te = time()

        t = (te-ts)
        t_print = t
        if t > 3600:
            unit = 'h'
            t_print /= 3600
        elif t > 60:
            unit = 'm'
            t_print /= 60
        elif t > 1:
            unit = 's'
        else:
            unit = 'ms'
            t_print *= 1000
        print(f"{func.__name__} took {t_print:2.3f}{unit}")
        return result

    return timed
