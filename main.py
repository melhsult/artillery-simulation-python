import math
import matplotlib.pyplot as plt

# -- 1. Definitioner for 152-mm haubits --
m = 43.56
v0 = 864.0
kaliber = 0.152
A = math.pi * (kaliber / 2)**2
g = 9.82
rho = 1.204
Cd = 0.295
k = 0.5 * rho * Cd * A

def beregn_kast(vinkel_grader, dt=0.01):
    vinkel_rad = math.radians(vinkel_grader)
    x, y = 0.0, 0.0
    vx = v0 * math.cos(vinkel_rad)
    vy = v0 * math.sin(vinkel_rad)
    x_data, y_data = [x], [y]
    
    while y >= 0:
        v = math.sqrt(vx**2 + vy**2)
        ax = -(k / m) * v * vx
        ay = -g - (k / m) * v * vy
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt
        if y >= 0:
            x_data.append(x)
            y_data.append(y)
    return x_data, y_data, x

# -- 2. Selve simulationen --
vinkler = [44.5, 45.0, 45.5]
farver = ['red', 'black', 'blue']
resultater = []

for v in vinkler:
    x_d, y_d, slut_x = beregn_kast(v)
    resultater.append((x_d, y_d, slut_x))

# -- 3. Plotting ogs med labels rykket til højre --
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# Graf 1: Overblik
for i in range(len(vinkler)):
    ax1.plot(resultater[i][0], resultater[i][1], color=farver[i], label=f'Vinkel {vinkler[i]}°')
ax1.set_title('Figur 8: Samlet banekurve for 152mm granat', fontsize=12)
ax1.set_xlabel('Afstand (m)')
ax1.set_ylabel('Højde (m)')
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.7)

# Graf 2: Zoom på nedslaget med labels igen rykket til højre
tekst_hoejder = [30, 70, 110]  # Lidt lavere højder for bedre overblik

for i in range(len(vinkler)):
    slut_x = resultater[i][2]
    ax2.plot(resultater[i][0], resultater[i][1], color=farver[i], lw=2)
    ax2.plot(slut_x, 0, marker='o', color=farver[i], markersize=6)
    
    # xytext=(40, ...) rykker teksten lidt mere til højre for punktet
    # ha='left' gør at teksten starter ved pilens slutning
    ax2.annotate(f"Vinkel {vinkler[i]}\n{slut_x:.1f} meter",
        xy=(slut_x, 0),
        xytext=(40, tekst_hoejder[i]),
        textcoords="offset points",
        ha='left',
        va='center',
        fontsize=10,
        color=farver[i],
        fontweight='bold',
        arrowprops=dict(arrowstyle='->',
                        connectionstyle="angle,angleA=0,angleB=90,rad=10",
                        color=farver[i]))

# her indstilles zoom-vinduet (udvidet x-akse til højre for at gøre plads til tekst)
max_x = max([res[2] for res in resultater])
min_x = min([res[2] for res in resultater])
ax2.set_xlim(min_x - 100, max_x + 600)
ax2.set_ylim(-10, 160)
ax2.set_title('Figur 9: Zoom på ballistisk spredning', fontsize=12)
ax2.set_xlabel('Afstand (m)')
ax2.set_ylabel('Højde (m)')
ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

print(f"Total spredning ved 0,5 graders forskel: {max_x - min_x:.2f} meter")
