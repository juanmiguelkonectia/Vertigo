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
# Ajuste nativo de subplots para centrar la figura arriba y dejar espacio libre abajo sin recuadros rígidos
plt.subplots_adjust(left=0.15, right=0.85, bottom=0.45, top=0.95)  
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
text_objects = {}  # Almacena las etiquetas de texto responsive

def actualizar(val=None, origen=None, clave_exacta=None):
    try:
        if origen == 'slider' and clave_exacta:
            text_boxes[clave_exacta].disconnect(text_boxes[clave_exacta]._cid)
            text_boxes[clave_exacta].set_val(f"{sliders[clave_exacta].val:.5f}")
            text_boxes[clave_exacta]._cid = text_boxes[clave_exacta].on_submit(lambda text, k=clave_exacta: actualizar(text, 'text', k))
            
        elif origen == 'text' and clave_exacta:
            try:
                val_num = float(text_boxes[clave_exacta].text)
                val_num = max(sliders[clave_exacta].valmin, min(sliders[clave_exacta].valmax, val_num))
                
                sliders[clave_exacta].disconnect(sliders[clave_exacta]._cid)
                sliders[clave_exacta].set_val(val_num)
                sliders[clave_exacta]._cid = sliders[clave_exacta].on_changed(lambda val, k=clave_exacta: actualizar(val, 'slider', k))
            except ValueError:
                pass

        # Persistencia absoluta de los valores en el diccionario de control
        for k in params.keys():
            params[k] = sliders[k].val

        vx, vy = calcular_trayectoria(params['Ax'], params['Ay'], params['fx'], 
                                     params['fy'], params['omega'], params['k'], params['delta'])
        line.set_data(vx, vy)
        
        # Se aumenta el multiplicador de seguridad a 1.6 para ampliar el hueco visual y evitar cortes laterales
        lim = max(params['Ax'], params['Ay']) * 1.6
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        fig.canvas.draw_idle()
    except Exception as e:
        print(f"Error en la actualización: {e}")

# --- DISEÑO DE LOS MANDOS COMBINADOS Y TEXTOS RESPONSIVE ---

y_positions = [0.38, 0.33, 0.28, 0.23, 0.18, 0.13, 0.08]
keys = ['Ax', 'Ay', 'fx', 'fy', 'omega', 'k', 'delta']
labels_text = [
    'Tope Físico X: Al alterarlo modificas el ancho máximo absoluto\ndel dibujo para evitar que se corte por los lados.',
    'Tope Físico Y: Al alterarlo modificas la altura máxima inicial\ncontrolando qué tan abierto verticalmente empieza el ojo.',
    'Engranaje Brazo X: Al alterarlo cambias los ciclos horizontales;\nvalores próximos a Y generan la malla de hilos cruzados.',
    'Engranaje Brazo Y: Al alterarlo cambias los ciclos verticales;\nrompe o junta la simetría de la trama o efecto moiré.',
    'Motor del Plato: Al alterarlo aceleras o inviertes el giro,\ndispersando o conceptualizando la espiral sobre sí misma.',
    'Tornillo sin fin: Al alterarlo regulas la caída al vacío;\na mayor valor, el túnel se cierra más rápido al centro.',
    'Calibración de Fase: Al alterarlo rotas la orientación geométrica\ny el ángulo de apertura de la primera elipse trazada.'
]
ranges = [(0.1, 4.0), (0.1, 4.0), (0.5, 2.0), (0.5, 2.0), (-0.05, 0.05), (0.0, 0.01), (-3.14, 3.14)]
formats = ['%1.2f', '%1.2f', '%1.4f', '%1.4f', '%1.4f', '%1.5f', '%1.2f']

for y, k, label, r, fmt in zip(y_positions, keys, labels_text, ranges, formats):
    ax_slider = plt.axes([0.48, y, 0.33, 0.025])
    ax_text = plt.axes([0.90, y, 0.07, 0.025])
    
    sliders[k] = Slider(ax_slider, '', r[0], r[1], valinit=params[k], valfmt=fmt)
    text_objects[k] = fig.text(0.02, y - 0.005, label, transform=fig.transFigure, linespacing=1.3)
    
    text_boxes[k] = TextBox(ax_text, '', initial=f"{params[k]:.5f}", color='white', hovercolor='#F0F4F8')
    text_boxes[k].text_disp.set_size(8.5)
    
    def al_confirmar(text, k_key=k):
        text_boxes[k_key].ax.set_facecolor('white')  
        text_boxes[k_key].text_disp.set_color('black')  
        actualizar(text, 'text', k_key)             
        
    sliders[k]._cid = sliders[k].on_changed(lambda val, k_key=k: actualizar(val, 'slider', k_key))
    text_boxes[k]._cid = text_boxes[k].on_submit(lambda text, k_key=k: al_confirmar(text, k_key))

# --- GESTOR GLOBAL DE CLICKS PARA ACTIVAR SELECCIÓN AZUL Y PERSISTENCIA AL SALIR ---

def manejar_clics_foco(event):
    if event.inaxes is None:
        for k, tb in text_boxes.items():
            if tb.ax.get_facecolor() != (1.0, 1.0, 1.0, 1.0): 
                tb.ax.set_facecolor('white')
                tb.text_disp.set_color('black')
                actualizar(tb.text, 'text', k)
        fig.canvas.draw_idle()
        return

    for k, tb in text_boxes.items():
        if event.inaxes == tb.ax:
            tb.ax.set_facecolor('#D0E2FF')      
            tb.text_disp.set_color('#0056B3')   
        else:
            if tb.ax.get_facecolor() != (1.0, 1.0, 1.0, 1.0): 
                tb.ax.set_facecolor('white')
                tb.text_disp.set_color('black')
                actualizar(tb.text, 'text', k)
                
    fig.canvas.mpl_connect('button_press_event', manejar_clics_foco)

fig.canvas.mpl_connect('button_press_event', manejar_clics_foco)

# --- CONTROLADOR RESPONSIVE DE TIPOGRAFÍA ---

def ajustar_textos_responsive(event):
    ancho_ventana = fig.get_window_extent().width
    nuevo_tamano = max(6.5, min(9.0, ancho_ventana / 135.0))
    
    for txt in text_objects.values():
        txt.set_size(nuevo_tamano)
    fig.canvas.draw_idle()

fig.canvas.mpl_connect('resize_event', ajustar_textos_responsive)

# --- PERSONALIZACIÓN DE LA HERRAMIENTA SUBPLOT CONFIGURATION TOOL ---

subplot_explanations = {
    'left': 'Margen Izquierdo:\nDesplaza horizontalmente el chasis de la máquina hacia la izquierda del encuadre.',
    'bottom': 'Margen Inferior:\nModifica la elevación base del soporte físico del papel respecto al suelo del visor.',
    'right': 'Margen Derecho:\nDesplaza horizontalmente el chasis de la máquina hacia la derecha del encuadre.',
    'top': 'Margen Superior:\nModifica el tope físico superior del encuadre para delimitar el cielo de la captura fotográfica.',
    'wspace': 'Espaciado Ancho:\nRegula la separación lateral interna si estuviéramos exponiendo múltiples placas simultáneas.',
    'hspace': 'Espaciado Alto:\nRegula la separación vertical interna si estuviéramos exponiendo múltiples placas simultáneas.'
}

def inyectar_explicaciones_subplot_tool(tool_fig):
    tool_fig.subplots_adjust(left=0.35, right=0.85)
    for ax_widget in tool_fig.axes:
        for child in ax_widget.get_children():
            if hasattr(child, 'get_text'):
                text_content = child.get_text()
                if text_content in subplot_explanations:
                    child.set_text(subplot_explanations[text_content])
                    child.set_size(7.5)

def comprobar_ventanas_emergentes(event):
    for num in plt.get_fignums():
        f = plt.figure(num)
        if "Subplot Configuration Tool" in f.canvas.manager.get_window_title():
            inyectar_explicaciones_subplot_tool(f)
            f.canvas.draw_idle()

fig.canvas.mpl_connect('button_press_event', comprobar_ventanas_emergentes)

# --- INTERCAMBIO DE DATOS (IMPORTAR / EXPORTAR) ---

def exportar(event):
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%dd_%H%M")
    nombre_base = f"resultado_M5_{timestamp}"
    
    plt.savefig(f"{nombre_base}.svg", format='svg', bbox_inches='tight', pad_inches=0)
    
    m_left = fig.subplotpars.left
    m_right = fig.subplotpars.right
    m_bottom = fig.subplotpars.bottom
    m_top = fig.subplotpars.top
    m_wspace = fig.subplotpars.wspace
    m_hspace = fig.subplotpars.hspace

    with open(f"{nombre_base}_informe.txt", "w", encoding="utf-8") as f:
        f.write("--- INFORME DE CONFIGURACIÓN MÁQUINA M-5 ---\n\n")
        f.write("[MÓDULO DE CINEMÁTICA Y OSCILACIÓN]\n")
        f.write(f"Tope Físico X (Ax)         : {params['Ax']:.5f} -> Ancho máximo del chasis de acero.\n")
        f.write(f"Tope Físico Y (Ay)         : {params['Ay']:.5f} -> Altura máxima inicial del ojo.\n")
        f.write(f"Engranaje Brazo X (fx)     : {params['fx']:.5f} -> Frecuencia de vaivén horizontal.\n")
        f.write(f"Engranaje Brazo Y (fy)     : {params['fy']:.5f} -> Frecuencia de vaivén vertical (Efecto Moiré).\n")
        f.write(f"Motor del Plato (omega)    : {params['omega']:.5f} -> Velocidad angular de giro de la plataforma.\n")
        f.write(f"Tornillo sin fin (k)       : {params['k']:.5f} -> Velocidad de caída/absorción hacia el centro.\n")
        f.write(f"Calibración de Fase (delta): {params['delta']:.5f} -> Ángulo de apertura inicial de la figura.\n\n")
        
        f.write("[MÓDULO DE CONFIGURACIÓN DE SUBPLOT (MÁRGENES DE ENCUADRE)]\n")
        f.write(f"Margen Izquierdo (left)    : {m_left:.5f} -> Desplazamiento horizontal izquierdo.\n")
        f.write(f"Margen Derecho (right)     : {m_right:.5f} -> Desplazamiento horizontal derecho.\n")
        f.write(f"Margen Inferior (bottom)   : {m_bottom:.5f} -> Elevación de soporte respecto al suelo visual.\n")
        f.write(f"Margen Superior (top)      : {m_top:.5f} -> Delimitación del cielo de la captura fotográfica.\n")
        f.write(f"Espacio Ancho (wspace)     : {m_wspace:.5f} -> Separación lateral entre placas expuestas.\n")
        f.write(f"Espacio Alto (hspace)      : {m_hspace:.5f} -> Separación vertical entre placas expuestas.\n")
        f.write("\nConfiguración guardada correctamente de forma permanente.")
    
    print(f"Archivos '{nombre_base}.svg' e informe guardados correctamente.")

def importar(event):
    import os
    from tkinter import Tk, filedialog
    
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)  
    
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar informe de máquina M-5 para importar",
        filetypes=[("Archivos de Informe de Texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    root.destroy()  
    
    if not ruta_archivo:
        print("Importación cancelada por el usuario.")
        return
        
    try:
        nuevos_params = {}
        nuevos_márgenes = {}
        
        mapeo_claves = {
            '(Ax)': 'Ax', '(Ay)': 'Ay', '(fx)': 'fx', '(fy)': 'fy', 
            '(omega)': 'omega', '(k)': 'k', '(delta)': 'delta'
        }
        mapeo_margenes = {
            '(left)': 'left', '(right)': 'right', '(bottom)': 'bottom', 
            '(top)': 'top', '(wspace)': 'wspace', '(hspace)': 'hspace'
        }
        
        # Sistema tolerante de lectura para admitir tanto UTF-8 (nuevos) como ANSI/CP1252 (antiguos)
        lineas = []
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                lineas = f.readlines()
        except UnicodeDecodeError:
            with open(ruta_archivo, "r", encoding="cp1252") as f:
                lineas = f.readlines()

        for linea in lineas:
            for subcadena, clave in mapeo_claves.items():
                if subcadena in linea:
                    valor = float(linea.split(":")[1].split("->")[0].strip())
                    nuevos_params[clave] = valor
            for subcadena, margen in mapeo_margenes.items():
                if subcadena in linea:
                    valor = float(linea.split(":")[1].split("->")[0].strip())
                    nuevos_márgenes[margen] = valor

        for clave, valor in nuevos_params.items():
            if clave in sliders:
                sliders[clave].disconnect(sliders[clave]._cid)
                sliders[clave].set_val(valor)
                sliders[clave]._cid = sliders[clave].on_changed(lambda val, k_key=clave: actualizar(val, 'slider', k_key))
                
                text_boxes[clave].disconnect(text_boxes[clave]._cid)
                text_boxes[clave].set_val(f"{valor:.5f}")
                text_boxes[clave]._cid = text_boxes[clave].on_submit(lambda text, k_key=clave: al_confirmar(text, k_key))
        
        if nuevos_márgenes:
            fig.subplots_adjust(
                left=nuevos_márgenes.get('left', fig.subplotpars.left),
                right=nuevos_márgenes.get('right', fig.subplotpars.right),
                bottom=nuevos_márgenes.get('bottom', fig.subplotpars.bottom),
                top=nuevos_márgenes.get('top', fig.subplotpars.top),
                wspace=nuevos_márgenes.get('wspace', fig.subplotpars.wspace),
                hspace=nuevos_márgenes.get('hspace', fig.subplotpars.hspace)
            )

        actualizar()
        print(f"Configuración importada con éxito desde: {os.path.basename(ruta_archivo)}")
    except Exception as e:
        print(f"Error al procesar el archivo de importación: {e}")

# Ubicación y configuración de la botonera inferior balanceada
ax_import = plt.axes([0.43, 0.02, 0.22, 0.035])
btn_import = Button(ax_import, 'IMPORTAR CONFIGURACIÓN', color='lightgray', hovercolor='palegreen')
btn_import.on_clicked(importar)

ax_export = plt.axes([0.67, 0.02, 0.22, 0.035])
btn_export = Button(ax_export, 'EXPORTAR RESULTADOS', color='lightgray', hovercolor='skyblue')
btn_export.on_clicked(exportar)

# Inicialización y renderizado
actualizar()
fig.canvas.draw()
ajustar_textos_responsive(None)
plt.show()