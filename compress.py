import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np
from legend import *
import pdb

a = [0,-1,0,-1,0,-2,2,1,2,2,1,2,0,-1,-1,2,2,-3,-4,2,1,-4,1,-1,-1,0,0,0,-2,3,4,-1,-1,2,2,3,0,3,-2,0,1,-2,0,-2,4,1,0,2,4,1,1,0,0,-2,0,4,1,0,-3,4,0,-1,0,2,2,0,1,2,1,2,0,-2,2,1,0,-1,1,2,1,-1,1,3,0,1,1,-1,1,2,4,0,2,1,-1,0,0,-3,0,-2,2,-2,-1,-2,0,0,-2,1,-3,-3,-1,-2,0,2,4,1,-3,2,1,31,-1,-1,0,-3,-1,0,2,-1,0,2,-2,-1,2,0,-5,0,-1,-1,5,0,-1,-2,2,1,3,0,1,2,0,3,1,5,-1,1,-2,1,1,1,0,0,-1,3,0,2,2,0,-2,3,3,0,0,2,1,1,2,0,1,0,3,5,2,3,2,1,3,3,6,3,8,6,8,8,5,14,14,12,14,19,18,23,23,24,24,26,33,30,36,36,40,45,40,25,-81,-36,-51,-86,-93,-78,-41,-29,-26,-27,-20,-7,24,41,46,46,62,72,81,88,92,70,15,15,17,23,33,38,17,52,57,35,7,-32,-54,-78,-89,-86,-84,-80,-71,-63,-59,-48,-46,-39,-35,-32,-29,-26,-23,-18,-17,-16,-13,-10,-8,-12,-8,-11,-10,-6,-9,-6,-9,-11,-7,-5,-6,-8,-5,-6,-4,-4,-5,-5,-3,-1,-5,-6,1,-3,-4,-4,-1,-2,-3,-3,-6,-5,-3,-2,-3,-3,-1,-3,-2,1,-4,-4,-4,0,-3,-4,-2,2,-2,-3,2,-5,-2,-1,0,0,-2,1,-2,1,-1,1,-2,-3,3,-2,-1,1,0,-2,-2,-1,0,-2,2,2,0,-3,2,-3,1,-3,0,-3,-2,0,-2,-2,-1,-2,0,-1,1,1,-3,-1,-1,2,1,4,-1,0,-2,3,-1,0,2,-1,-2,-1,0,3,2,-2,0,-1,-2,-2,2,-1,0,-2,-1,3,0,1,0,3,-2,1,-2]

fig = plt.figure()
plot_axes = fig.gca()

x = list(np.arange(0, len(a)))
plt.plot(x, a, color='g', linewidth=1, label='Original')

sensitivities = np.arange(.1, 1.5, .1)
plasma = cm = plt.get_cmap('plasma') 
cNorm  = colors.Normalize(vmin=sensitivities[0], vmax=sensitivities[-1])
scalar_map = cmx.ScalarMappable(norm=cNorm, cmap=plasma)

for j, sensitivity in enumerate(sensitivities):
    tmp = []
    start = a[0]
    total = a[0]
    number = 1

    #pdb.set_trace()
    for i, v in enumerate(a):
        if i == 0:
            continue
        avg = total/number
        if abs(v-avg) > abs(start*sensitivity):
            tmp.extend([avg]*number)
            number = 1
            total = v
            start = v
        else:
            total += v
            number += 1
    tmp.extend([total/number]*number)
    color_value = scalar_map.to_rgba(sensitivities[j])
    plt.plot(x, tmp, color=color_value, lw=.6, label='Sensitivity: %.1f' % sensitivity)
plt.title('Plot of compression\n(Showing sensitivities between .1 - 1.5)')
legend = Legend(fig, plot_axes, Location.EastOutside)
print('Saving Figure...')
plt.savefig('visual.png', bbox_inches='tight', dpi=250)
print('Showing Figure...')
plt.show()
