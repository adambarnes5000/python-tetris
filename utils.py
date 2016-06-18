import time

DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)


def add_tuples(a,b):
    return (a[0]+b[0],a[1]+b[1])


def timestamp():
    return int(round(time.time() * 1000))