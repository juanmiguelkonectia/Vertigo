import matplotlib.pyplot as plt
from numpy import arange, sin, cos, exp

# Generación de datos
i  = arange(5000)
x1 = 1.0*cos(i/10.0)*exp(-i/2500.0)
y1 = 1.4*sin(i/10.0)*exp(-i/2500.0)
d  = 450.0
vx = cos(i/d)*x1 - sin(i/d)*y1
vy = sin(i/d)*x1 + cos(i/d)*y1

# Configuración del gráfico
plt.figure(figsize=(10, 10))
plt.plot(vx, vy, color="black", linewidth=0.8)

# Ajustes de visualización
plt.axis('equal')
plt.axis('off')

# --- GUARDADO DEL ARCHIVO ---
# Esta línea crea el archivo en la misma carpeta donde esté tu script dibujo.py
plt.savefig("mi_dibujo_vectorial.svg", format='svg', bbox_inches='tight', pad_inches=0)

# Muestra el resultado en pantalla
print("Archivo 'mi_dibujo_vectorial.svg' guardado con éxito.")
plt.show()