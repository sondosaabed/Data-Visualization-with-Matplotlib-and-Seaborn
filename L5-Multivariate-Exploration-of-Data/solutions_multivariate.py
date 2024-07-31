import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns



def print_docstring(func):
    def wrapper(*args, **kwargs):
        return func(func, *args, **kwargs)
    return wrapper  


def load_data(file='../Data/fuel-econ.csv'):
   df = pd.read_csv(file)
   
   return df
   
 
@print_docstring      
def encodings_solution_1(me):
    """
    1. The engine displacement is the independent variable. This is essentially engine size, and
    determines efficiency and emissions.
    
    2. One could choose either efficiency or CO2 emissions for the color axis, but here I choose
    efficiency because mpg is easier for me to think about.
    
    3. These two variables are correlated, since more efficient engines emit fewer emissions. We see that
    here. We also see a non-linear relationship with engine size. This is important, as it means even a
    slightly smaller engine will likely be much more efficient.

    """
    print(me.__doc__)
    
    # data setup
    df = load_data()

    plt.scatter(data=df, x='displ', y='highway', c='co2', cmap='viridis')
    plt.colorbar()
    plt.ylabel('highway (mpg)')
    plt.xlabel('engine displacement (liters)')
    
    return

 
@print_docstring   
def encodings_solution_2(me):
    """
    Chevrolet has a much high ghgScore for Regular Gas, and a much tighter distribution. It also has a
    slightly higher rating for Premium gas, but it's difficult to say because both have such prominent
    left skews. More specific commentary would require looking at histograms, or perhaps violin plots.

    """
    print(me.__doc__)
    
    # data setup
    df = load_data()

    df_subset = df[(df['fuelType'] == 'Premium Gasoline') | (df['fuelType'] == 'Regular Gasoline')]
    df_subset = df_subset[(df_subset['make'] == 'Chevrolet') | (df_subset['make'] == 'Ford')]

    sns.boxplot(data=df_subset, y='ghgScore', x='fuelType', hue='make',)
    plt.xticks(rotation = 15)
    
    return

 
@print_docstring   
def encodings_solution_3(me):
    """
    I went with a clustered box plot on this task since there were too many levels to make a clustered
    violin plot accessible. The plot shows that in each vehicle class, engine sizes were larger for
    premium-fuel cars than regular-fuel cars. Engine size generally increased with vehicle class within
    each fuel type, but the trend was noisy for the smallest vehicle classes.

    """
    print(me.__doc__)
    
    # data setup
    df = load_data()
    
    sedan_classes = ['Minicompact Cars', 'Subcompact Cars', 'Compact Cars', 'Midsize Cars', 'Large Cars']
    vclasses = pd.CategoricalDtype(ordered=True, categories=sedan_classes)
    df['VClass'] = df['VClass'].astype(vclasses);
    
    fuel_econ_sub = df.loc[df['fuelType'].isin(['Premium Gasoline', 'Regular Gasoline'])]
    
    # plotting
    sns.boxplot(data=fuel_econ_sub, x='VClass', y='displ', hue='fuelType')
    plt.legend(loc=6, bbox_to_anchor=(1.0, 0.5)) # legend to right of figure
    plt.xticks(rotation = 15)

    
    return

 
@print_docstring   
def facetgrid_solution_1(me):
    """
    Due to overplotting, I've taken a faceting approach to this task There don't seem to be any obvious
    differences in the main cluster across vehicle classes, except that the minicompact and large sedans'
    arcs are thinner than the other classes due to lower counts. The faceted plots clearly show that most
    of the high-efficiency cars are in the mid-size and compact car classes.

    """
    print(me.__doc__)
    
    # data setup
    df = load_data()
    
    sedan_classes = ['Minicompact Cars', 'Subcompact Cars', 'Compact Cars', 'Midsize Cars', 'Large Cars']
    vclasses = pd.CategoricalDtype(ordered=True, categories=sedan_classes)
    df['VClass'] = df['VClass'].astype(vclasses);
    
    g = sns.FacetGrid(data=df, col='VClass', height=3, col_wrap=3)
    g.map(plt.scatter, 'city', 'highway', alpha=1/5)

    
    return
    
 
@print_docstring   
def pairplot_solution_1(me):
    """
    I set up my PairGrid to plot scatterplots off the diagonal and histograms on the diagonal. The
    intersections where 'co2' meets the fuel mileage measures are fairly interesting in how tight the
    curves are. You'll explore this more in the next task.

    """
    print(me.__doc__)
    
    # data setup
    df = load_data()
    
    g = sns.PairGrid(data=df, vars=['displ', 'co2', 'city', 'highway', 'comb'])
    g.map_diag(sns.kdeplot)
    g.map_offdiag(plt.scatter)
    
    return

 
@print_docstring   
def additionalplot_solution_1(me):
    """
    Due to the high number of data points and their high amount of overlap, I've chosen to plot the data
    in a faceted plot. You can see that engine sizes are smaller for cars that use regular gasoline
    against those that use premium gas. Most cars fall in an emissions band a bit below 9 kg CO2 per
    gallon; diesel cars are consistently higher, a little above 10 kg CO2 per gallon. This makes sense,
    since a gallon of gas gets burned no matter how efficient the process. More strikingly, there's a
    smattering of points with much smaller emissions. If you inspect these points more closely you'll see
    that they represent hybrid cars that use battery energy in addition to conventional fuel! To pull
    these mechanically out of the dataset requires more data than that which was trimmed to create it -
    and additional research to understand why these points don't fit the normal CO2 bands.

    """
    print(me.__doc__)
    
    # data setup
    df = load_data()
    
    df['co2_gal'] = df['comb'] * df['co2']
    
    df_sub = df.loc[df['fuelType'].isin(['Premium Gasoline', 'Regular Gasoline', 'Diesel'])]
    # plotting
    g = sns.FacetGrid(data=df_sub, col='fuelType', height=4, col_wrap=3)
    g.map(sns.regplot, 'co2_gal', 'displ', y_jitter=0.04, fit_reg=False, scatter_kws={'alpha': 1/5})
    g.set_ylabels('Engine displacement (l)')
    g.set_xlabels('CO2 (g/gal)')
    g.set_titles('{col_name}') 
    
    return
