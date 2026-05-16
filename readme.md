![1778946028987](image/readme/1778946028987.png)

# M-5 Vertigo Simulator: Emulación de la Máquina de John Whitney

Este proyecto consiste en un motor de renderizado matemático desarrollado en **Python** que emula el funcionamiento mecánico del  **Director de Tiro M-5** , la computadora analógica de la Segunda Guerra Mundial utilizada por **John Whitney** y **Saul Bass** para crear las icónicas espirales del póster y la secuencia de créditos de la película *Vértigo* (1958).

## 🎯 Objetivo del Proyecto

El objetivo principal es trascender la simple generación de espirales digitales para **emular la lógica física y mecánica** de la máquina M-5 original. A diferencia de un software de dibujo estándar, este simulador replica los tres sistemas independientes de la máquina de Whitney:

1. **Oscilación armónica** mediante brazos mecánicos (Ejes X e Y).
2. **Mecanismo de reducción** por tornillo sin fin para crear el efecto de "túnel".
3. **Rotación de plataforma** constante que genera los patrones de interferencia o curvas de Lissajous.

## ✨ Características Principales

* **Simulación de "Topes de Acero":** Implementación de límites físicos ($A_x, A_y$) que garantizan que el rastro de luz jamás escape del radio definido por el armazón mecánico.
* **Precisión de Engranajes:** Control de frecuencias ($f_x, f_y$) con desajustes sutiles (ej. 1.000 vs 1.002) para recrear las mallas de hilos cruzados características del póster.
* **Modelado de Péndulo Físico:** Incorporación del parámetro de amortiguación ($k$) que emula la fricción natural del péndulo de pintura original.
* **Parámetros Históricos Preconfigurados:** Incluye los valores exactos para recrear el "Óvalo de Saul Bass" con su relación de aspecto de 1.25.

## 📋 Requisitos Previos

Para ejecutar este simulador, necesitarás:

* **Python 3.x**
* **NumPy:** Para el manejo de matrices de rotación y cálculos de funciones trigonométricas.
* **Matplotlib:** Para la generación y visualización de los trazados de larga exposición.

## ⚙️ Instrucciones de Instalación

1. Clona el repositorio:
   ```
   git clone https://github.com/juanmiguelkonectia/Vertigo.git
   ```
2. Accede al directorio del proyecto:
   ```
   cd Vertigo
   ```
3. Instala las dependencias necesarias:
   ```
   pip install numpy matplotlib
   ```

## 🚀 Cómo usarlo (Ejemplos)

El núcleo del simulador se encuentra en `vertigo.py`. Puedes ajustar los parámetros mecánicos para obtener diferentes variaciones de la espiral.

![1778943614925](https://file+.vscode-resource.vscode-cdn.net/c%3A/Users/envyJ/Documents/Accesos%20directos%20habituales/02_Curso%20programacion/Repositorios/Vertigo/image/readme/1778943614925.jpg)

## 📄 Licencia

Este proyecto se distribuye bajo la licencia  **MIT** , permitiendo su uso para fines educativos y creativos en el ámbito del diseño gráfico y la historia del cine.

---

*Este proyecto busca honrar el legado de Saul Bass y John Whitney, transformando la ingeniería militar del Director de Tiro M-5 en una herramienta de expresión artística digital.*
