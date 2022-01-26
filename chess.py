import numpy as np

def countSquares(row, column, maximum):
     
    # Count top left squares
    topLeft = min(row, column) - 1
     
    # Count bottom right squares
    bottomRight = maximum - 1 - max(row, column)
     
    # Count top right squares
    topRight = min(row, maximum-column) -1
     
    # Count bottom left squares
    bottomLeft = maximum - 1 - max(row, maximum-column)
 
     
    # Return total count
    return topLeft + topRight + bottomRight + bottomLeft

N = 10

grid = np.meshgrid(range(1,N),range(1,N))

vals = np.vectorize(countSquares)(grid[0],grid[1],N)

import seaborn as sns
import matplotlib.pyplot as plt 
plt.figure(figsize=(20,18))
sns.heatmap(vals,annot=True)
plt.show()