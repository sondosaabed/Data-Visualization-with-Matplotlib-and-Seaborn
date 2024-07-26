import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


def print_docstring(func):
    def wrapper(*args, **kwargs):
        return func(func, *args, **kwargs)
    return wrapper


def load_data(file='Data/diamonds.csv'):
   df = pd.read_csv(file)
   
   return df
   
 
@print_docstring
def bar_chart_solution_1(me):
    """
    Here we explicitly order the cut by passing a list to the order parameter. Additionally, we pick
    Tableau Blue.

    """
    print(me.__doc__)
    df = load_data()
    order = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal']
    sns.countplot(data=df, x='cut', color='tab:blue', order=order)
    
    return

 
@print_docstring
def bar_chart_solution_2(me):
    """
    Here we use the pandas normalize argument of the Series value_counts() method. Then we convert the
    Series to a data frame, and use a seaborn barplot.

    """
    print(me.__doc__)
    
    df = load_data()
    colors = df['color'].value_counts(normalize=True)*100.
    colors = colors.sort_index(ascending=True)
    colors = colors.reset_index(drop=False)  # converts to data frame
    colors = colors.rename(columns={'index': 'color_grade', 'color': 'proportion'})

    sns.barplot(data=colors, x='proportion', y='color_grade', color='tab:blue')
    
    return

 
@print_docstring
def histogram_solution_1(me):
    """
    We get a distribution that looks bimodal, with a large peak around 4, a dip, and a secondary peak
    around 6.5mm. It also has a rightward skew.

    """
    print(me.__doc__)
    df = load_data()
    plt.figure(figsize = [4, 3]) 
    bins = np.arange(0, 11, 0.25)
    plt.hist(data=df, x='x', bins=bins)
    
    return
    
 
@print_docstring    
def histogram_solution_2_long_format(me):
    """
    These two solutions should be identical (with small differences in color hue). We see that the x and
    y dimensions are roughly the same, while z is notable smaller.

    """
    print(me.__doc__)
    
    df = load_data()
    df_tidy = pd.melt(df, value_vars=['x', 'y', 'z'])
    bins = np.arange(0, 11, 0.25)
    sns.histplot(data=df_tidy, x='value', hue='variable', bins=bins)
    
    return
    
 
@print_docstring    
def histogram_solution_2_wide_format(me):
    """
    These two solutions should be identical (with small differences in color hue). We see that the x and
    y dimensions are roughly the same, while z is notable smaller.

    """
    print(me.__doc__)
    
    df = load_data()
    bins = np.arange(0, 11, 0.25)
    sns.histplot(data=df, x='x', bins=bins, label='x')
    sns.histplot(data=df, x='y', bins=bins, label='y')
    sns.histplot(data=df, x='z', bins=bins, label='z')
    
    return
    
 
@print_docstring    
def histogram_solution_3(me):
    """
    Price is right-skewed, with a mode around $4500. The bars around $2500 appear to compris about 4-5\%
    of the diamonds in this data set.

    """
    print(me.__doc__)
    df = load_data()
    sns.histplot(data=df, x='price', bins=51, stat='percent')
    
    return
    
 
@print_docstring    
def subplots_solution_1(me):
    """
    There are many ways to switch subplots, so choose one and stick with it! Here we see that the x and y
    distributions are quite similar. The z dimension (height) is much smaller.

    """
    print(me.__doc__)
    
    df = load_data()
    
    plt.figure(figsize = [12, 5]) 
    bins = np.arange(0, 11, 0.25)

    # histogram on left, example of too-large bin size
    # 1 row, 3 cols, subplot 1
    plt.subplot(1, 3, 1) # 1 row, 3 cols, subplot 1
    plt.hist(data=df, x='x', bins=bins);
    plt.xlabel('x (mm)')
    
    plt.subplot(1, 3, 2) # 1 row, 3 cols, subplot 2
    plt.hist(data=df, x='y', bins=bins);
    plt.xlabel('y (mm)')
    
    plt.subplot(1, 3, 3) # 1 row, 3 cols, subplot 3
    plt.hist(data=df, x='z', bins=bins);
    plt.xlabel('z (mm)')
    
    return
    
 
@print_docstring
def subplots_solution_2(me):
    """
    For this exercise, no instructions regarding category order were given. It would be a good practice
    to order them by quality.

    """
    print(me.__doc__)
    
    df = load_data()
    
    plt.figure(figsize = [12, 5]) 
    bins = np.arange(0, 11, 0.25)

    # histogram on left, example of too-large bin size
    # 1 row, 3 cols, subplot 1
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    sns.countplot(data=df, x='cut', color='tab:blue', ax=ax1)
    ax1.set_xlabel('Diamond cut')
    
    sns.countplot(data=df, x='clarity', color='tab:blue', ax=ax2)
    ax2.set_xlabel('Diamond clarity grade')
    
    return

 
@print_docstring
def scaling_solution_1(me):
    """
    Here we use the ax.set_xim() function to set he x-axis limits. We see the bins around $1500 are
    empty. This might be due to psychology, where customer's think they are getting a deal by being less
    than that threshold.

    """
    print(me.__doc__)
    
    df = load_data()
    
    ax = sns.histplot(data=df, x='price', bins=1000)
    ax.set_xlim(0, 2000)
    
    return
    
 
@print_docstring    
def scaling_solution_2(me):
    """
    Once again we use the ax.set_xscale('log') option to set the scale. However, one should also adjust
    the xticks. Refer to the lesson on how to do that.

    """
    print(me.__doc__)
    
    df = load_data()
    
    ax = sns.histplot(data=df, x='price', bins=1000)
    ax.set_xscale('log')
    
    return
