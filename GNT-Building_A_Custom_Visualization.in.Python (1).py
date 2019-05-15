
# coding: utf-8

# 
# ### Building a custom visualization

# For this assignment I had to implement a visualization of sample data as described in Ferreria et al (2014). I had implemented the bar coloring as described in the paper, where the color of the bar is actually based on the amount of data covered (a gradient ranging from dark blue for the distribution being certainly below this y-axis, to white if the value is certainly contained, to dark red if the value is certainly not contained as the distribution is above the axis).
# 
# I chose the Even Harder option in which I had to make the plot interactive, allowing the user to click on the y axis to set the value of interest. The bar colors change with respect to what value the user has selected.

# In[1]:

# Initialize data:
import pandas as pd
import numpy as np

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(33500,150000,3650), 
                   np.random.normal(41000,90000,3650), 
                   np.random.normal(41000,120000,3650), 
                   np.random.normal(48000,55000,3650)], 
                  index=[1992,1993,1994,1995])
df


# In[2]:

# Import useful libraries 
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap
get_ipython().magic('matplotlib notebook')

# Compute mean of each sample
df_mean = df.mean(axis=1) 

# Compute standard deviation of the mean (standard error)
df_std = df.std(axis=1)/np.sqrt(df.shape[1])

# Initialize a value for the horizontal axis
y = 37000

# Creating colors for each column sample
norm = Normalize(vmin=-1.96, vmax=1.96)
cmap = get_cmap('seismic')
df_colors = pd.DataFrame([])
df_colors['intensity'] = norm((df_mean-y)/df_std)
df_colors['color'] = [cmap(x) for x in df_colors['intensity']]

# Plot figure
plt.figure(figsize=(10,6))
bar_plot = plt.bar(df.index, df_mean, yerr=df_std*1.96, color=df_colors['color']);
hoz_line = plt.axhline(y=y, color='k', linewidth=2, linestyle='--');
y_text = plt.text(1995.9, y, 'y = %d' %y, bbox=dict(fc='white',ec='k'));

# Add xticks
plt.xticks(df.index+0.4, ('1992', '1993', '1994', '1995'));


# In[4]:


# Add interactivity
def onclick(event):
    for i in range(4):
        shade = cmap(norm((df_mean.values[i]-event.ydata)/df_std.values[i]))
        bar_plot[i].set_color(shade) 
    hoz_line.set_ydata(event.ydata)
    y_text.set_text('y = %d' %event.ydata);
    y_text.set_position((1995.9, event.ydata));
    
plt.gcf().canvas.mpl_connect('button_release_event', onclick);


# In[ ]:



