"""
Motor de Simulación de Cafetería
Modelo de colas M/M/c con eventos discretos estocásticos
Autor: Nahomi Salazar Loredo
"""

import simpy
import numpy as np
from collections import defaultdict
import random

class CafeteriaSimulation:
    """
    Simulación de una cafetería usando SimPy
    
    Modelo: M/M/c (Markoviano/Markoviano/c servidores)
    - Llegadas: Proceso de Poisson (distribución exponencial entre llegadas)
    - Servicio: Distribución exponencial
    - Servidores: c servidores en paralelo
    - Disciplina: FIFO (First In, First Out)
    """
    
    def __init__(self, arrival_rate, service_rate, num_servers, sim_time, queue_capacity):
        """
        Inicializa el modelo de simulación
        
        Args:
            arrival_rate: Tasa de llegada (λ) en clientes/minuto
            service_rate: Tasa de servicio (μ) en clientes/minuto por servidor
            num_servers: Número de servidores (c)
            sim_time: Tiempo de simulación en minutos
            queue_capacity: Capacidad máxima de la cola
        """
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.num_servers = num_servers
        self.sim_time = sim_time
        self.queue_capacity = queue_capacity
        
        # Métricas de salida
        self.customers_served = 0
        self.customers_rejected = 0
        self.wait_times = []
        self.service_times = []
        self.system_times = []
        self.queue_lengths = []
        self.arrival_times = []
        self.server_busy_time = 0
        self.max_queue_length = 0
        
    def customer_generator(self, env, servers, queue_capacity):
        """
        Genera clientes según proceso de Poisson
        """
        customer_id = 0
        while True:
            # Tiempo entre llegadas (distribución exponencial)
            interarrival_time = random.expovariate(self.arrival_rate)
            yield env.timeout(interarrival_time)
            
            customer_id += 1
            self.arrival_times.append(env.now)
            
            # Verificar capacidad de la cola
            if len(servers.queue) < queue_capacity:
                env.process(self.customer_process(env, customer_id, servers))
            else:
                self.customers_rejected += 1
                
    def customer_process(self, env, customer_id, servers):
        """
        Proceso de un cliente individual
        """
        arrival_time = env.now
        
        # Registrar longitud de cola
        queue_length = len(servers.queue)
        self.queue_lengths.append(queue_length)
        self.max_queue_length = max(self.max_queue_length, queue_length)
        
        # Solicitar servidor
        with servers.request() as request:
            yield request
            
            # Tiempo de espera en cola
            wait_time = env.now - arrival_time
            self.wait_times.append(wait_time)
            
            # Tiempo de servicio (distribución exponencial)
            service_time = random.expovariate(self.service_rate)
            self.service_times.append(service_time)
            
            # Simular servicio
            service_start = env.now
            yield env.timeout(service_time)
            service_end = env.now
            
            # Tiempo total en el sistema
            system_time = service_end - arrival_time
            self.system_times.append(system_time)
            
            self.customers_served += 1
            self.server_busy_time += service_time
            
    def run(self):
        """
        Ejecuta la simulación y retorna resultados
        """
        # Crear entorno de simulación
        env = simpy.Environment()
        
        # Crear recursos (servidores)
        servers = simpy.Resource(env, capacity=self.num_servers)
        
        # Iniciar generador de clientes
        env.process(self.customer_generator(env, servers, self.queue_capacity))
        
        # Ejecutar simulación
        env.run(until=self.sim_time)
        
        # Calcular métricas
        results = self.calculate_metrics()
        
        return results
    
    def calculate_metrics(self):
        """
        Calcula métricas de desempeño del sistema
        """
        # Métricas básicas
        avg_wait_time = np.mean(self.wait_times) if self.wait_times else 0
        avg_service_time = np.mean(self.service_times) if self.service_times else 0
        avg_system_time = np.mean(self.system_times) if self.system_times else 0
        avg_queue_length = np.mean(self.queue_lengths) if self.queue_lengths else 0
        
        # Utilización de servidores
        total_server_time = self.num_servers * self.sim_time
        server_utilization = self.server_busy_time / total_server_time if total_server_time > 0 else 0
        
        # Varianzas
        var_wait_time = np.var(self.wait_times) if len(self.wait_times) > 1 else 0
        var_service_time = np.var(self.service_times) if len(self.service_times) > 1 else 0
        
        # Tasa efectiva de llegadas
        effective_arrival_rate = len(self.arrival_times) / self.sim_time if self.sim_time > 0 else 0
        
        # Probabilidad de rechazo
        total_arrivals = self.customers_served + self.customers_rejected
        rejection_probability = self.customers_rejected / total_arrivals if total_arrivals > 0 else 0
        
        return {
            # Métricas principales
            'customers_served': self.customers_served,
            'customers_rejected': self.customers_rejected,
            'avg_wait_time': round(avg_wait_time, 2),
            'avg_service_time': round(avg_service_time, 2),
            'avg_system_time': round(avg_system_time, 2),
            'avg_queue_length': round(avg_queue_length, 2),
            'max_queue_length': self.max_queue_length,
            'server_utilization': round(server_utilization, 4),
            
            # Métricas estadísticas
            'var_wait_time': round(var_wait_time, 2),
            'var_service_time': round(var_service_time, 2),
            'std_wait_time': round(np.sqrt(var_wait_time), 2),
            'std_service_time': round(np.sqrt(var_service_time), 2),
            
            # Tasas
            'effective_arrival_rate': round(effective_arrival_rate, 4),
            'rejection_probability': round(rejection_probability, 4),
            
            # Datos para análisis
            'wait_times': [round(t, 2) for t in self.wait_times[:100]],  # Primeros 100
            'service_times': [round(t, 2) for t in self.service_times[:100]],
            'queue_lengths': self.queue_lengths[:100],
            'arrival_times': [round(t, 2) for t in self.arrival_times[:100]],
            
            # Parámetros de entrada
            'input_params': {
                'arrival_rate': self.arrival_rate,
                'service_rate': self.service_rate,
                'num_servers': self.num_servers,
                'sim_time': self.sim_time,
                'queue_capacity': self.queue_capacity
            }
        }
