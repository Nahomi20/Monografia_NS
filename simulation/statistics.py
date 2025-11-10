"""
Análisis Estadístico de Resultados de Simulación
Autor: Nahomi Salazar Loredo
"""

import numpy as np
from scipy import stats
import math

class StatisticalAnalysis:
    """
    Realiza análisis estadístico completo de los resultados de simulación
    """
    
    def __init__(self, simulation_results):
        """
        Inicializa con los resultados de la simulación
        """
        self.results = simulation_results
        self.wait_times = simulation_results.get('wait_times', [])
        self.service_times = simulation_results.get('service_times', [])
        
    def analyze(self):
        """
        Realiza análisis estadístico completo
        """
        return {
            'descriptive_stats': self.descriptive_statistics(),
            'distributions': self.test_distributions(),
            'confidence_intervals': self.confidence_intervals(),
            'hypothesis_tests': self.hypothesis_tests(),
            'correlation': self.correlation_analysis()
        }
    
    def descriptive_statistics(self):
        """
        Estadísticas descriptivas básicas
        """
        wait_times = np.array(self.wait_times)
        service_times = np.array(self.service_times)
        
        return {
            'wait_times': {
                'mean': round(np.mean(wait_times), 2) if len(wait_times) > 0 else 0,
                'median': round(np.median(wait_times), 2) if len(wait_times) > 0 else 0,
                'std': round(np.std(wait_times), 2) if len(wait_times) > 0 else 0,
                'variance': round(np.var(wait_times), 2) if len(wait_times) > 0 else 0,
                'min': round(np.min(wait_times), 2) if len(wait_times) > 0 else 0,
                'max': round(np.max(wait_times), 2) if len(wait_times) > 0 else 0,
                'q25': round(np.percentile(wait_times, 25), 2) if len(wait_times) > 0 else 0,
                'q75': round(np.percentile(wait_times, 75), 2) if len(wait_times) > 0 else 0,
                'skewness': round(stats.skew(wait_times), 2) if len(wait_times) > 2 else 0,
                'kurtosis': round(stats.kurtosis(wait_times), 2) if len(wait_times) > 2 else 0
            },
            'service_times': {
                'mean': round(np.mean(service_times), 2) if len(service_times) > 0 else 0,
                'median': round(np.median(service_times), 2) if len(service_times) > 0 else 0,
                'std': round(np.std(service_times), 2) if len(service_times) > 0 else 0,
                'variance': round(np.var(service_times), 2) if len(service_times) > 0 else 0,
                'min': round(np.min(service_times), 2) if len(service_times) > 0 else 0,
                'max': round(np.max(service_times), 2) if len(service_times) > 0 else 0
            }
        }
    
    def test_distributions(self):
        """
        Prueba de bondad de ajuste para distribuciones
        """
        wait_times = np.array(self.wait_times)
        service_times = np.array(self.service_times)
        
        results = {}
        
        # Test de normalidad (Shapiro-Wilk)
        if len(wait_times) >= 3:
            stat_wait, p_wait = stats.shapiro(wait_times[:min(len(wait_times), 5000)])
            results['wait_times_normality'] = {
                'test': 'Shapiro-Wilk',
                'statistic': round(stat_wait, 4),
                'p_value': round(p_wait, 4),
                'is_normal': p_wait > 0.05
            }
        
        # Test de exponencialidad (Kolmogorov-Smirnov)
        if len(service_times) >= 3:
            mean_service = np.mean(service_times)
            if mean_service > 0:
                stat_exp, p_exp = stats.kstest(service_times, 'expon', args=(0, mean_service))
                results['service_times_exponential'] = {
                    'test': 'Kolmogorov-Smirnov',
                    'statistic': round(stat_exp, 4),
                    'p_value': round(p_exp, 4),
                    'is_exponential': p_exp > 0.05
                }
        
        return results
    
    def confidence_intervals(self, confidence=0.95):
        """
        Calcula intervalos de confianza
        """
        wait_times = np.array(self.wait_times)
        
        if len(wait_times) < 2:
            return {}
        
        mean = np.mean(wait_times)
        std_error = stats.sem(wait_times)
        margin = std_error * stats.t.ppf((1 + confidence) / 2, len(wait_times) - 1)
        
        return {
            'wait_time_ci': {
                'confidence_level': confidence,
                'mean': round(mean, 2),
                'lower_bound': round(mean - margin, 2),
                'upper_bound': round(mean + margin, 2),
                'margin_of_error': round(margin, 2)
            }
        }
    
    def hypothesis_tests(self):
        """
        Pruebas de hipótesis
        """
        results = {}
        
        # Test t de una muestra (H0: tiempo de espera promedio = 5 minutos)
        wait_times = np.array(self.wait_times)
        if len(wait_times) >= 2:
            hypothesized_mean = 5.0
            t_stat, p_value = stats.ttest_1samp(wait_times, hypothesized_mean)
            results['wait_time_ttest'] = {
                'null_hypothesis': f'Mean wait time = {hypothesized_mean} minutes',
                't_statistic': round(t_stat, 4),
                'p_value': round(p_value, 4),
                'reject_null': p_value < 0.05,
                'actual_mean': round(np.mean(wait_times), 2)
            }
        
        return results
    
    def correlation_analysis(self):
        """
        Análisis de correlación entre variables
        """
        if len(self.wait_times) < 2 or len(self.service_times) < 2:
            return {}
        
        # Asegurar misma longitud
        min_len = min(len(self.wait_times), len(self.service_times))
        wait = np.array(self.wait_times[:min_len])
        service = np.array(self.service_times[:min_len])
        
        if min_len >= 2:
            correlation, p_value = stats.pearsonr(wait, service)
            return {
                'wait_vs_service': {
                    'correlation_coefficient': round(correlation, 4),
                    'p_value': round(p_value, 4),
                    'interpretation': self.interpret_correlation(correlation)
                }
            }
        
        return {}
    
    def interpret_correlation(self, r):
        """
        Interpreta el coeficiente de correlación
        """
        abs_r = abs(r)
        if abs_r < 0.3:
            strength = 'débil'
        elif abs_r < 0.7:
            strength = 'moderada'
        else:
            strength = 'fuerte'
        
        direction = 'positiva' if r > 0 else 'negativa'
        return f'Correlación {strength} {direction}'
