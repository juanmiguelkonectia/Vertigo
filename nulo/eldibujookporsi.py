import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox

# --- EL MOTOR MATEMÁTICO DE LA M-5 ---

def calcular_trayectoria(Ax, Ay, fx, fy, omega, k, delta, duracion=1000):
    t = np.linspace(0, duracion, 20000)
    
    # 1. El Efecto Túnel (Reducción Mecánica)
    R = np.exp(-k * t)
    
    # 2. Osciladores de Brazo Rígido (Límites fijos por Ax y Ay)
    x_arm = Ax * np.cos(fx * t + delta) * R
    y_arm = Ay * np.sin(fy * t) * R
    
    # 3. Plataforma de Rotación Constante (Matriz de rotación física)
    vx = x_arm * np.cos(omega * t) - y_arm * np.sin(omega * t)
    vy = x_arm * np.sin(omega * t) + y_arm * np.cos(omega * t)
    
    return vx, vy

# --- INTERFAZ DE USUARIO Y MÁQUINA ---

fig, ax = plt.subplots(figsize=(11, 8.5))
plt.subplots_adjust(bottom=0.45)  # Espacio ampliado para acomodar los controles
ax.set_facecolor('white')

# Valores iniciales (Configuración Bass clásica)
params = {'Ax': 2.0, 'Ay': 0.6, 'fx': 1.0, 'fy': 1.002, 'omega': 0.015, 'k': 0.002, 'delta': 0.0}

line, = ax.plot([], [], color='black', lw=0.5, alpha=0.8)
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)
ax.axis('off')

# Diccionarios globales para almacenar los objetos de los widgets y evitar que se destruyan
sliders = {}
text_boxes = {}

def actualizar(val=None, origen=None):
    try:
        # Si el cambio viene de un slider, actualizamos su caja de texto correspondiente
        if origen == 'slider':
            for k in params.keys():
                text_boxes[k].set_val(f"{sliders[k].val:.5f}")
        # Si el cambio viene de una caja de texto, actualizamos su slider correspondiente
        elif origen == 'text':
            for k in params.keys():
                try:
                    val_num = float(text_boxes[k].text)
                    # Forzar el valor dentro de los límites del slider para evitar desbordamientos
                    val_num = max(sliders[k].valmin, min(sliders[k].valmax, val_num))
                    sliders[k].set_val(val_num)
                except ValueError:
                    pass

        # Leer los valores finales directamente de los controles
        for k in params.keys():
            params[k] = sliders[k].val

        vx, vy = calcular_trayectoria(params['Ax'], params['Ay'], params['fx'], 
                                     params['fy'], params['omega'], params['k'], params['delta'])
        line.set_data(vx, vy)
        
        # El límite visual se ajusta al tope de acero para asegurar que no se corte
        lim = max(params['Ax'], params['Ay']) * 1.1
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        fig.canvas.draw_idle()
    except Exception as e:
        print(f"Error en la actualización: {e}")

# --- DISEÑO DE LOS MANDOS COMBINADOS (MANEJADOR + INPUT + FRASE) ---

# Coordenadas verticales para cada fila de control
y_positions = [0.38, 0.33, 0.28, 0.23, 0.18, 0.13, 0.08]
keys = ['Ax', 'Ay', 'fx', 'fy', 'omega', 'k', 'delta']
labels = [
    'Tope Físico X:\nDefine el ancho máximo del chasis de acero.',
    'Tope Físico Y:\nDefine el alto máximo del chasis de acero.',
    'Engranaje Brazo X:\nControla la velocidad del vaivén horizontal.',
    'Engranaje Brazo Y:\nControla la velocidad del vaivén vertical.',
    'Motor del Plato:\nDetermina el giro constante de la plataforma.',
    'Tornillo sin fin:\nFuerza la caída progresiva hacia el centro.',
    'Calibración de Fase:\nModifica la apertura angular del "ojo" inicial.'
]
ranges = [(0.1, 4.0), (0.1, 4.0), (0.5, 2.0), (0.5, 2.0), (-0.05, 0.05), (0.0, 0.01), (-3.14, 3.14)]
formats = ['%1.2f', '%1.2f', '%1.4f', '%1.4f', '%1.4f', '%1.5f', '%1.2f']

# Construcción iterativa de los pares Slider-TextBox para no tocar la estructura del gráfico
for y, k, label, r, fmt in zip(y_positions, keys, labels, ranges, formats):
    ax_slider = plt.axes([0.35, y, 0.45, 0.03])
    ax_text = plt.axes([0.83, y, 0.10, 0.03])
    
    sliders[k] = Slider(ax_slider, label, r[0], r[1], valinit=params[k], valfmt=fmt)
    text_boxes[k] = TextBox(ax_text, '', initial=f"{params[k]:.5f}")
    
    # Conexiones de eventos independientes para evitar bucles infinitos de actualización
    sliders[k].on_changed(lambda val, orig='slider': actualizar(val, orig))
    text_boxes[k].on_submit(lambda text, orig='text': actualizar(text, orig))

# Referencias directas para mantener la compatibilidad con el ámbito global de matplotlib
s_Ax, s_Ay, s_fx, s_fy, s_omega, s_k, s_delta = [sliders[k] for k in keys]

# --- EXPORTACIÓN DE RESULTADOS ---

def exportar(event):
    nombre_base = "resultado_M5"
    # Guardar Gráfico SVG (Vectorial para máxima calidad)
    plt.savefig(f"{nombre_base}.svg", format='svg', bbox_inches='tight', pad_inches=0)
    
    # Guardar Informe de Variables
    with open(f"{nombre_base}_informe.txt", "w") as f:
        f.write("--- INFORME DE CONFIGURACIÓN MÁQUINA M-5 ---\n")
        for k, v in params.items():
            f.write(f"{k}: {v}\n")
        f.write("\nConfiguración válida para replicar el dibujo exacto.")
    
    print(f"Archivos '{nombre_base}.svg' e informe guardados correctamente.")

ax_export = plt.axes([0.4, 0.02, 0.2, 0.04])
btn_export = Button(ax_export, 'EXPORTAR RESULTADOS', color='lightgray', hovercolor='skyblue')
btn_export.on_clicked(exportar)

# Dibujo inicial al arrancar el programa
actualizar()
plt.show()