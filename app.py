"""
Sistema de Simulación de Cafetería
Aplicación Flask principal
Autor: Nahomi Salazar Loredo
Fecha: 19/10/2025
"""

from flask import Flask, render_template, request, jsonify
import json
from simulation.cafeteria_model import CafeteriaSimulation
from simulation.ai_predictor import DemandPredictor
from simulation.statistics import StatisticalAnalysis

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal de la aplicación"""
    return render_template('index.html')

@app.route('/api/simulate', methods=['POST'])
def simulate():
    """
    Endpoint para ejecutar la simulación
    Recibe parámetros y retorna resultados
    """
    try:
        data = request.get_json()
        
        # Parámetros de entrada
        arrival_rate = float(data.get('arrival_rate', 2.0))  # clientes/minuto
        service_rate = float(data.get('service_rate', 3.0))  # clientes/minuto por servidor
        num_servers = int(data.get('num_servers', 2))
        sim_time = int(data.get('sim_time', 480))  # minutos (8 horas)
        queue_capacity = int(data.get('queue_capacity', 50))
        
        # Ejecutar simulación
        sim = CafeteriaSimulation(
            arrival_rate=arrival_rate,
            service_rate=service_rate,
            num_servers=num_servers,
            sim_time=sim_time,
            queue_capacity=queue_capacity
        )
        
        results = sim.run()
        
        # Análisis estadístico
        stats = StatisticalAnalysis(results)
        statistical_analysis = stats.analyze()
        
        # Predicción con IA
        predictor = DemandPredictor()
        predictions = predictor.predict_demand(results['arrival_times'])
        
        # Combinar resultados
        response = {
            'success': True,
            'simulation_results': results,
            'statistical_analysis': statistical_analysis,
            'ai_predictions': predictions,
            'recommendations': generate_recommendations(results, num_servers)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/optimize', methods=['POST'])
def optimize():
    """
    Endpoint para optimización del sistema
    Sugiere el número óptimo de servidores
    """
    try:
        data = request.get_json()
        arrival_rate = float(data.get('arrival_rate', 2.0))
        service_rate = float(data.get('service_rate', 3.0))
        
        # Probar diferentes configuraciones
        results = []
        for num_servers in range(1, 6):
            sim = CafeteriaSimulation(
                arrival_rate=arrival_rate,
                service_rate=service_rate,
                num_servers=num_servers,
                sim_time=480,
                queue_capacity=50
            )
            result = sim.run()
            results.append({
                'servers': num_servers,
                'avg_wait': result['avg_wait_time'],
                'utilization': result['server_utilization'],
                'customers_served': result['customers_served']
            })
        
        # Encontrar configuración óptima
        optimal = min(results, key=lambda x: x['avg_wait'] if x['avg_wait'] > 0 else float('inf'))
        
        return jsonify({
            'success': True,
            'results': results,
            'optimal_config': optimal
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def generate_recommendations(results, num_servers):
    """Genera recomendaciones basadas en los resultados"""
    recommendations = []
    
    # Análisis de utilización
    if results['server_utilization'] > 0.9:
        recommendations.append({
            'type': 'warning',
            'message': f'Alta utilización de servidores ({results["server_utilization"]:.1%}). Considere agregar más personal.'
        })
    elif results['server_utilization'] < 0.5:
        recommendations.append({
            'type': 'info',
            'message': f'Baja utilización de servidores ({results["server_utilization"]:.1%}). Puede reducir personal en horas valle.'
        })
    
    # Análisis de tiempo de espera
    if results['avg_wait_time'] > 10:
        recommendations.append({
            'type': 'warning',
            'message': f'Tiempo de espera alto ({results["avg_wait_time"]:.1f} min). Mejore la velocidad de servicio.'
        })
    
    # Análisis de cola
    if results['max_queue_length'] > 20:
        recommendations.append({
            'type': 'alert',
            'message': f'Cola máxima de {results["max_queue_length"]} clientes. Considere expandir capacidad.'
        })
    
    # Clientes rechazados
    if results['customers_rejected'] > 0:
        recommendations.append({
            'type': 'alert',
            'message': f'{results["customers_rejected"]} clientes rechazados por capacidad. Aumente el espacio de espera.'
        })
    
    return recommendations

if __name__ == '__main__':
    print("=" * 60)
    print("Sistema de Simulación de Cafetería")
    print("Iniciando servidor Flask...")
    print("Acceda a: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
