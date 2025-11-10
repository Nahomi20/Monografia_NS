# Sistema de Simulación de Cafetería
## Examen de Suficiencia - Simulación de Sistemas 2025

### Descripción del Proyecto
Sistema completo de simulación de una cafetería universitaria que modela el flujo de clientes, tiempos de servicio, gestión de inventario y análisis estadístico con integración de inteligencia artificial para predicción de demanda.

### Características Principales
- ✅ Simulación de eventos discretos estocástica
- ✅ Modelo de colas M/M/c con múltiples servidores
- ✅ Análisis estadístico completo (media, varianza, distribuciones)
- ✅ Predicción de demanda con IA (Machine Learning)
- ✅ Visualización interactiva en tiempo real
- ✅ Generación de reportes y métricas
- ✅ Diagramas de flujo y estructura del modelo

### Tecnologías Utilizadas
- **Backend**: Python 3 (Flask, NumPy, SciPy, Pandas, Scikit-learn)
- **Frontend**: HTML5, CSS3, JavaScript (Chart.js)
- **Simulación**: SimPy (Discrete Event Simulation)
- **IA**: Regresión lineal y predicción de series temporales

### Estructura del Proyecto
```
/vercel/sandbox/
├── app.py                 # Servidor Flask principal
├── simulation/
│   ├── cafeteria_model.py # Motor de simulación
│   ├── ai_predictor.py    # Módulo de IA para predicción
│   └── statistics.py      # Análisis estadístico
├── static/
│   ├── css/
│   │   └── style.css      # Estilos de la aplicación
│   └── js/
│       └── main.js        # Lógica del frontend
├── templates/
│   └── index.html         # Interfaz principal
├── docs/
│   ├── diagrams/          # Diagramas de flujo
│   └── report.md          # Informe técnico
└── requirements.txt       # Dependencias Python
```

### Instalación y Ejecución

#### 1. Instalar dependencias
```bash
pip3 install -r requirements.txt
```

#### 2. Ejecutar la aplicación
```bash
python3 app.py
```

#### 3. Abrir en el navegador
```
http://localhost:5000
```

### Modelo de Simulación

#### Variables Exógenas (Entrada)
- Tasa de llegada de clientes (λ)
- Número de servidores (cajeros/cocineros)
- Tiempo de simulación
- Capacidad del sistema

#### Variables Endógenas (Salida)
- Tiempo promedio de espera
- Longitud de cola
- Utilización de servidores
- Clientes atendidos
- Clientes rechazados

#### Componentes del Sistema
1. **Generador de Clientes**: Llegadas según distribución de Poisson
2. **Cola de Espera**: FIFO (First In, First Out)
3. **Servidores**: Múltiples estaciones de servicio
4. **Procesamiento**: Tiempo de servicio exponencial
5. **Salida**: Registro de métricas y estadísticas

### Análisis Estadístico
- Distribución de tiempos de llegada (Poisson)
- Distribución de tiempos de servicio (Exponencial)
- Cálculo de esperanza matemática E[X]
- Cálculo de varianza Var(X)
- Intervalos de confianza
- Validación del modelo

### Integración de IA
- **Predicción de demanda**: Modelo de regresión para predecir llegadas futuras
- **Optimización**: Sugerencias de número óptimo de servidores
- **Análisis de patrones**: Identificación de horas pico

### Autor
**Nahomi Salazar Loredo**
Fecha: 19/10/2025
Docente: MSc. Irene Martínez Mejía
Curso: Simulación de Sistemas
