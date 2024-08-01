import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


def print_docstring(func):
    def wrapper(*args, **kwargs):
        return func(func, *args, **kwargs)
    return wrapper


def load_data(file='../Data/diamonds.csv'):
   df = pd.read_csv(file)
   
   return df
   
 
@print_docstring
def explanatory_solution(me):
    """
    To clean up this plot, I started by re-labeling the x and y axes, and adding clear units. I also changed
    the colors for `Ideal` to `royalblue` (to hint at a beautiful blue diamond) and `darkorange` for `Fair`
    diamonds (I tried yellow, but it was too light to be seen).

    There were too many xticks and labels to cleanly read, so I then only used every other bin label. For the
    y-axis, I switched to log scale and relabeled the y-axis accordingly. I also specified a different legend
    location so that the top left corner wasn't overly crowded.

    """
    print(me.__doc__)
    df = load_data()
    
    df_subset = df[df['cut'].isin(['Ideal', 'Fair'])].reset_index(drop=True)
    
    # define xbins
    step = 0.25
    xbins = np.arange(0, df['carat'].max()+step, step)

    # the bin label is the middle value of the bin
    labels = [lower+step/2 for lower in xbins[:-1]]

    # bin data using pd.cut
    df_subset['carat_avg'] = pd.cut(df_subset['carat'],
                                       bins=xbins,
                                       include_lowest=True,
                                       labels=labels)

    # pd.cut() returns categorical data, so let's make sure they are floats
    df_subset['carat_avg'] = df_subset['carat_avg'].astype(float)

    # let's do a group by bin and diamond cut
    dgroup = df_subset.groupby(by=['carat_avg', 'cut'], as_index=False).agg(
        price_avg=('price', np.mean)
    )

    # now start prettying plots!
    yticks = [100, 300, 1000, 3000, 10000, 30000]
    ylabels = [f'{t}' for t in yticks]

    ax = sns.scatterplot(data=dgroup, x='carat_avg', y='price_avg', hue='cut',
                        palette=['darkorange', 'royalblue'])
    ax.set_xlabel('Diamond size (carat)')
    ax.set_ylabel('Price ($)')
    ax.set_xlim(0, 5.25)
    ax.set_ylim(100, 30000)
    plt.yscale('log')
    plt.xticks(xbins[0::2])  # every other bin labeled
    plt.yticks(yticks, ylabels)
    ax.legend(loc='lower right')
    
    return
