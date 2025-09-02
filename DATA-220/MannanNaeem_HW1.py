from sympy import symbols, plot
from sympy.plotting import plot3d

x, y = symbols('x y')

f = 2*x**3 - 9*x + 4
g = 12*x + 3
z = 3*x**2 - 2*y**2

#plot(f, g, (x, 0, 10), title="my first graph")

plot3d(z, (x, -10, 10), (y, -10, 10))