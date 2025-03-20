import numpy as np
import matplotlib.pyplot as plt

v0 = float(input("Enter the initial velocity of the projectile: "))
theta = np.radians(float(input("Enter the vertical angle at which the projectile was launched: ")))
threeDim = input("Is this a 3D simulation? (y or n): ")

if threeDim == 'y':
    phi = np.radians(float(input("Enter the horizontal launch angle: ")))
else:
    phi = 0

res = input("Do you want to factor in air resistance? (y or n): ")

if res=='y':
    shape_dict = {
        "shape": 0.47, "half-sphere": 0.42,
        "cone": 0.5, "cube": 1.05, "long cylinder": 0.82,
        "short cylinder": 1.15, "streamlined body": 0.04
    }

    invalid = True
    while invalid:
        shape = input("Enter the shape of the projectile(sphere, half-sphere, cone, cube, long cylinder, short cylinder, streamlined body): ")
        if shape in shape_dict:
            invalid = False
            DRAGCOEF = shape_dict[shape]
        else:
            print("ERROR: Invalid shape")

    area = float(input("Enter the cross-sectional area of the object: "))
else:
    DRAGCOEF = 0
    area = 0

G = 9.80665
RHO = 1.225
dt = 0.01

vx0 = v0 * np.cos(theta) * np.cos(phi)
vy0 = v0 * np.sin(theta)
vz0 = v0 * np.cos(theta) * np.sin(phi)

t_max = 2 * v0 * np.sin(theta) / G
if res == 'y':
    t_max *= 5

t = np.arange(0, t_max, dt)

x = np.zeros_like(t)
y = np.zeros_like(t)
z = np.zeros_like(t)
vx = np.zeros_like(t)
vy = np.zeros_like(t)
vz = np.zeros_like(t)

vx[0] = vx0
vy[0] = vy0
vz[0] = vz0

for i in range(1, len(t)):
    v = np.sqrt(vx[i-1]**2 + vy[i-1]**2 + vz[i-1]**2)
    
    dragForce = 0.5 * DRAGCOEF * area * RHO * v**2
    
    if v == 0:
        ax, ay, az = 0, -G, 0
    else:
        ax = -(dragForce * (vx[i-1]/v))
        ay = -(dragForce * (vy[i-1]/v)) - G
        az = -(dragForce * (vz[i-1]/v))

    vx[i] = vx[i-1] + (ax * dt)
    vy[i] = vy[i-1] + (ay * dt)
    vz[i] = vz[i-1] + (az * dt)
    
    x[i] = x[i-1] + (vx[i] * dt)
    y[i] = y[i-1] + (vy[i] * dt)
    z[i] = z[i-1] + (vz[i] * dt)

    if y[i] < 0:
        x = x[:i]
        y = y[:i]
        z = z[:i]
        break

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, z, y)
ax.set_xlabel("Distance (m) for x")
ax.set_ylabel("Distance (m) for z")
ax.set_zlabel("Height (m)")
ax.set_title("Projectile Motion")
plt.show()
