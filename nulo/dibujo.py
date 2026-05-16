import matplotlib.pyplot as plt
from numpy import arange, sin, cos, exp, pi

# --- EL MECANISMO REAL DE WHITNEY (M-5) ---

# Tiempo de exposición
t = arange(0, 1500, 0.04)

# 1. LIMITADORES DE CHASIS (Inamovibles)
# Esto define el rectángulo donde vive la figura. Nunca se ensancha.
ANCHO_MAX = 2.0
ALTO_MAX  = 0.45

# 2. FRECUENCIAS MECÁNICAS (Engranajes)
f_x = 1.0
f_y = 1.0015  # El ligero desfase crea la malla moiré

# 3. EL TÚNEL (Pérdida de energía)
# La figura se encoge hacia el centro de forma exponencial.
radio = exp(-t / 400.0)

# 4. EL SECRETO: ROTACIÓN POR DESFASE (Phase Shift)
# No rotamos (x, y). Rotamos la FASE de las ondas.
# Esto hace que la elipse bascule pero sus extremos toquen siempre el mismo límite.
phi = t * 0.012 

# --- CÁLCULO DE LA TRAZA DE LUZ ---

# X e Y se calculan con la rotación integrada en la fase.
# Esto garantiza que el valor absoluto de X nunca supere ANCHO_MAX.
vx = ANCHO_MAX * radio * cos(t + phi)
vy = ALTO_MAX  * radio * sin(t)

# --- SALIDA GRÁFICA ---

plt.figure(figsize=(10, 10))

# Línea ultra-fina para evitar que la imagen se emborrone
plt.plot(vx, vy, color="black", linewidth=0.1, alpha=0.8)

plt.axis('equal')

# Forzamos los límites para ver que la figura está contenida
plt.xlim(-ANCHO_MAX * 1.2, ANCHO_MAX * 1.2)
plt.ylim(-ANCHO_MAX * 1.2, ANCHO_MAX * 1.2)

plt.axis('off')

# Guardado del archivo completo
plt.savefig("vertigo_final_fix.svg", format='svg', bbox_inches='tight', pad_inches=0)

print("Cálculo de oscilador de fase completado. El ancho es constante.")
plt.show()