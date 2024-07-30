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
def scatterplot_solution(me):
    """
    1. The relationship is appears fairly linear until util about 30mpg. But some ultra-efficient cars
    tend to be much more efficient in cities. This might be worth investigating.
    
    2. There are some points that seem in-between the two trends discussed above.
    
    3. We could also plot two lines, and try to capture both trends.
    """
    print(me.__doc__)
    
    # data setup
    df = load_data()

    plt.scatter(data=df, x='city', y='highway', alpha = 1/8)
    plt.plot([10,60], [10,60], color='tab:red', ls='--') # diagonal line from (10,10) to (60,60)
    plt.xlabel('City Fuel Eff. (mpg)')
    plt.ylabel('Highway Fuel Eff. (mpg)')
    
    return

 
@print_docstring
def heatmap_solution(me):
    """
    The expelled co2 clearly depends engine size, but in a non-linear fashion. There are notably fewer
    entries in the extreme bins, however, compared to smaller engines.

    """
    print(me.__doc__)
    
    # data setup
    df = load_data()

    bins_x = np.arange(0.6, df['displ'].max()+0.4, 0.4)
    bins_y = np.arange(0, df['co2'].max()+50, 50)
    plt.hist2d(data=df, x='displ', y='co2', bins=[bins_x, bins_y], 
               cmap='viridis_r', cmin = 0.5)
    plt.colorbar()
    plt.xlabel('Displacement (l)')
    plt.ylabel('CO2 (g/mi)')
    
    return

 
@print_docstring
def boxplot_solution(me):
    """
    Note here we have a larger variation Premium and Regular gasoline vehicles. It's likely these are
    the most prominent classes. There are very few for the other grades, so we can't draw any
    conclusions for them.

    """
    print(me.__doc__)
    
    # data setup
    df = load_data()

    fueltypes = ['Premium Gasoline', 'Midgrade Gasoline',
                     'Regular Gasoline', 'Diesel', 'Natural Gas']
    fclasses = pd.CategoricalDtype(ordered=True, categories=fueltypes)
    df['VClass'] = df['VClass'].astype(fclasses);
    
    # plotting
    sns.boxplot(data=df, x='fuelType', y='displ', color='tab:blue', order=fueltypes)
    plt.xticks(rotation = 15)
    
    return

 
@print_docstring
def violin_solution(me):
    """
    We should probably drop the Automatic (A1) class, as there is only one entry. Otherwise, we see
    All-Wheel, Front-Wheel, and Rear Wheel drive appear fairly unimodel. 4-Wheel Drive and Part-time
    4-Wheel appear more bimodal, and much less efficient.

    On average, front-wheel drive appears the most efficient.
    """
    print(me.__doc__)
    
    # data setup
    df = load_data()
    
    # plotting
    sns.violinplot(data=df, x='drive', y='highway', color='tab:red')
    plt.xticks(rotation=15)
    
    return
    
 
@print_docstring
def categorical_solution_1(me):
    """
    There are definitely differences in recommended fuel type depending on the vehicle class.
    Minicompact and subcompact cars overwhelming use premium gasoline, while midsize cars use regular
    gas to premium by about 20%. Compact and large cars prefer premium by a smaller margin.
    """
    print(me.__doc__)
    
    # data setup
    df = load_data()
    
    sedan_classes = ['Minicompact Cars', 'Subcompact Cars', 'Compact Cars', 'Midsize Cars', 'Large Cars']
    vclasses = pd.CategoricalDtype(ordered=True, categories=sedan_classes)
    df['VClass'] = df['VClass'].astype(vclasses);
    
    fuel_econ_sub = df.loc[df['fuelType'].isin(['Premium Gasoline', 'Regular Gasoline'])]

    # plotting
    ax = sns.countplot(data=fuel_econ_sub, x='VClass', hue='fuelType')
    ax.legend(loc='upper left')
    plt.xticks(rotation = 15)
    
    return

 
@print_docstring
def facet_plot_solution(me):
    """
    Due to the large number of manufacturers to plot, I've gone with a faceted plot of histograms rather
    than a single figure like a box plot. As part of setting up the FacetGrid object, I have sorted the
    manufacturers by average mileage, and wrapped the faceting into a six-column by three-row grid. One
    interesting thing to note is that there are a very large number of BMW cars in the data, almost twice
    as many as the second-most prominent maker, Mercedes-Benz. One possible refinement could be to change
    the axes to be in terms of relative frequency or density to normalize the axes, making the
    less-frequent manufacturers easier to read.
    
    NOTE: You may get a warning message depending on how you average various classes. In my code, I
    had to specify average numeric columns only, with numeric_only=True. This is because future
    versions of python will require this flag.
    
    """
    print(me.__doc__)
    
    # data setup
    df = load_data()
    
    THRESHOLD = 80
    make_frequency = df['make'].value_counts()
    idx = np.sum(make_frequency > THRESHOLD)

    most_makes = make_frequency.index[:idx]
    fuel_econ_sub = df.loc[df['make'].isin(most_makes)]

    make_means = fuel_econ_sub.groupby('make').mean(numeric_only=True)
    comb_order = make_means.sort_values('comb', ascending = False).index

    # plotting
    g = sns.FacetGrid(data=fuel_econ_sub,
                      col='make', col_wrap=6, col_order=comb_order)
    # try sb.distplot instead of plt.hist to see the plot in terms of density!
    g.map(plt.hist, 'comb', bins=np.arange(12, fuel_econ_sub['comb'].max()+2, 2))
    g.set_titles('{col_name}')
    
    return

 
@print_docstring
def additional_plot(me):
    """
    Seaborn's barplot function makes short work of this exercise. Since there are a lot of 'make' levels,
    I've made it a horizontal bar chart. In addition, I've set the error bars to represent the standard
    deviation of the car mileages.

    """
    print(me.__doc__)
    
    # data setup
    df = load_data()
    
    THRESHOLD = 80
    make_frequency = df['make'].value_counts()
    idx = np.sum(make_frequency > THRESHOLD)

    most_makes = make_frequency.index[:idx]
    fuel_econ_sub = df.loc[df['make'].isin(most_makes)]

    make_means = fuel_econ_sub.groupby('make').mean()
    comb_order = make_means.sort_values('comb', ascending = False).index

    # plotting
    sns.barplot(data = fuel_econ_sub, x='comb', y='make',
                color='tab:blue', order=comb_order, errorbar='sd')
    plt.xlabel('Average Combined Fuel Eff. (mpg)')
