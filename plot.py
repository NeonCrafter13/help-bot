import matplotlib.pyplot as plt
import numpy as np
import math as m

def render(expr: str):
    # 100 linearly spaced numbers
    x = np.linspace(-5, 5, 50)

    # the function, which is y = x^2 here
    exec("global y;" + expr)

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.margins(0)

    global y

    # plot the function
    plt.plot(x, y, 'r')
    # print(type(plt))

    plt.savefig('data/plot.png', bbox_inches='tight')
