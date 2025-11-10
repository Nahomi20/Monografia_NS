"""
Módulo de Inteligencia Artificial para Predicción de Demanda
Utiliza Machine Learning para predecir patrones de llegada
Autor: Nahomi Salazar Loredo
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import warnings
warnings.filterwarnings('ignore')

class DemandPredictor:
    """
    Predictor de demanda usando Machine Learning
    Implementa regresión lineal y polinomial para predecir llegadas futuras
    """
    
    def __init__(self):
        self.model = None
        self.poly_features = None
        
    def predict_demand(self, arrival_times, forecast_periods=10):
        """
        Predice la demanda futura basándose en tiempos de llegada históricos
        
        Args:
            arrival_times: Lista de tiempos de llegada observados
            forecast_periods: Número de períodos a predecir
            
        Returns:
            Diccionario con predicciones y métricas
        """
        if len(arrival_times) < 5:
            return {
                'predictions': [],
                'trend': 'insufficient_data',
                'confidence': 0
            }
        
        # Preparar datos
        X, y = self.prepare_time_series(arrival_times)
        
        if len(X) < 3:
            return {
                'predictions': [],
                'trend': 'insufficient_data',
                'confidence': 0
            }
        
        # Entrenar modelo de regresión lineal
        model = LinearRegression()
        model.fit(X, y)
        
        # Hacer predicciones
        last_index = len(arrival_times)
        future_indices = np.array([[i] for i in range(last_index, last_index + forecast_periods)])
        predictions = model.predict(future_indices)
        
        # Calcular tendencia
        slope = model.coef_[0]
        trend = self.interpret_trend(slope)
        
        # Calcular confianza (R²)
        confidence = model.score(X, y)
        
        # Análisis de patrones
        patterns = self.analyze_patterns(arrival_times)
        
        return {
            'predictions': [round(p, 2) for p in predictions.tolist()],
            'trend': trend,
            'slope': round(slope, 4),
            'confidence': round(confidence, 4),
            'r_squared': round(confidence, 4),
            'patterns': patterns,
            'recommendations': self.generate_ai_recommendations(trend, patterns)
        }
    
    def prepare_time_series(self, arrival_times):
        """
        Prepara datos de serie temporal para regresión
        """
        # Agrupar llegadas en intervalos de tiempo
        if len(arrival_times) == 0:
            return np.array([]), np.array([])
        
        max_time = max(arrival_times)
        interval = max(1, max_time / 20)  # Dividir en ~20 intervalos
        
        bins = np.arange(0, max_time + interval, interval)
        counts, _ = np.histogram(arrival_times, bins=bins)
        
        X = np.arange(len(counts)).reshape(-1, 1)
        y = counts
        
        return X, y
    
    def interpret_trend(self, slope):
        """
        Interpreta la tendencia basada en la pendiente
        """
        if slope > 0.1:
            return 'increasing'
        elif slope < -0.1:
            return 'decreasing'
        else:
            return 'stable'
    
    def analyze_patterns(self, arrival_times):
        """
        Analiza patrones en los tiempos de llegada
        """
        if len(arrival_times) < 10:
            return {
                'peak_detected': False,
                'periodicity': 'unknown'
            }
        
        # Calcular intervalos entre llegadas
        intervals = np.diff(sorted(arrival_times))
        
        # Detectar picos (períodos de alta frecuencia)
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        
        # Períodos con intervalos menores a media - std son "picos"
        peak_threshold = mean_interval - std_interval
        peak_periods = np.sum(intervals < peak_threshold)
        peak_percentage = peak_periods / len(intervals) if len(intervals) > 0 else 0
        
        return {
            'peak_detected': peak_percentage > 0.2,
            'peak_percentage': round(peak_percentage, 2),
            'avg_interarrival': round(mean_interval, 2),
            'std_interarrival': round(std_interval, 2),
            'periodicity': 'high_variability' if std_interval > mean_interval else 'regular'
        }
    
    def generate_ai_recommendations(self, trend, patterns):
        """
        Genera recomendaciones basadas en IA
        """
        recommendations = []
        
        if trend == 'increasing':
            recommendations.append({
                'type': 'ai_insight',
                'message': '📈 IA detecta tendencia creciente. Prepare recursos adicionales para demanda futura.',
                'priority': 'high'
            })
        elif trend == 'decreasing':
            recommendations.append({
                'type': 'ai_insight',
                'message': '📉 IA detecta tendencia decreciente. Considere optimizar recursos.',
                'priority': 'medium'
            })
        
        if patterns.get('peak_detected'):
            recommendations.append({
                'type': 'ai_insight',
                'message': f'⚡ IA detecta períodos pico ({patterns["peak_percentage"]:.0%} del tiempo). Implemente estrategia de personal flexible.',
                'priority': 'high'
            })
        
        if patterns.get('periodicity') == 'high_variability':
            recommendations.append({
                'type': 'ai_insight',
                'message': '🔄 IA detecta alta variabilidad en llegadas. Sistema de colas adaptativo recomendado.',
                'priority': 'medium'
            })
        
        return recommendations
    
    def optimize_servers(self, arrival_rate, service_rate, target_wait_time=5):
        """
        Optimiza el número de servidores usando teoría de colas
        Fórmula de Erlang C
        """
        # Calcular intensidad de tráfico
        rho = arrival_rate / service_rate
        
        # Encontrar número mínimo de servidores
        min_servers = int(np.ceil(rho)) + 1
        
        # Estimar tiempo de espera para diferentes configuraciones
        recommendations = []
        for c in range(min_servers, min_servers + 3):
            utilization = rho / c
            if utilization < 1:
                # Aproximación del tiempo de espera (fórmula de Pollaczek-Khinchine)
                expected_wait = (rho / (c * service_rate * (1 - utilization)))
                recommendations.append({
                    'servers': c,
                    'utilization': round(utilization, 2),
                    'expected_wait': round(expected_wait, 2),
                    'meets_target': expected_wait <= target_wait_time
                })
        
        return {
            'optimal_servers': min_servers,
            'recommendations': recommendations
        }
