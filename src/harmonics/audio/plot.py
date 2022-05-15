import matplotlib.pyplot as plt


def audio_plot(x, y,
               xlabel='',
               ylabel='',
               title='',
               show='all',
               figsize=(10, 4),
               scatter=False):
    if show != 'all':
        x = x[:show]
        y = y[:show]
    plt.figure(figsize=figsize)
    plt.plot(x, y)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    if scatter:
        plt.scatter(*scatter, c='r')
    plt.title(title)
    plt.grid()
    plt.show()
