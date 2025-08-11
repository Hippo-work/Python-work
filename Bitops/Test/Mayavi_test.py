from mayavi import mlab
import numpy as np

x, y, z = np.ogrid[-5:5:100j, -5:5:100j, -5:5:100j]
data = np.sin(x*y*z) / (x*y*z)

mlab.contour3d(data)
mlab.show()