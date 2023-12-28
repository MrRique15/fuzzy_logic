import itertools
import numpy as np
import skfuzzy as fuzz
import utils.func_tools as functools

from skfuzzy import control as ctrl
from matplotlib import pyplot as plt



class fuzzy_core:
    def __init__(self, defuzzify_method='centroid', log_file=None):
        
        self.RULES_FILE = 'used_rules.txt'
        self.LOG_FILE =  log_file if log_file is not None else 'log.txt'
        self.GRAPH_FILE_NAME = 'graph'
        
        # Criação das variáveis de entrada
        satisfacao = ctrl.Antecedent(np.arange(0, 11, 1), 'satisfacao')
        num_projetos = ctrl.Antecedent(np.arange(0, 11, 1), 'num_projetos')
        cumprimento_metas = ctrl.Antecedent(np.arange(0, 11, 1), 'cumprimento_metas')
        participacao_treinamentos = ctrl.Antecedent(np.arange(0, 11, 1), 'participacao_treinamentos')

        # Criação da variável de saída
        desempenho = ctrl.Consequent(np.arange(0, 101, 1), 'desempenho', defuzzify_method=defuzzify_method)

        # Fuzificação das variáveis de entrada
        # Definição das funções de pertinência para cada variável
        satisfacao['baixo'] = fuzz.trapmf(satisfacao.universe, [0, 0, 2, 4])
        satisfacao['medio'] = fuzz.trapmf(satisfacao.universe, [2, 4, 6, 8])
        satisfacao['alto']  = fuzz.trapmf(satisfacao.universe, [6, 8, 10, 10])
        
        num_projetos['baixo'] = fuzz.trapmf(num_projetos.universe, [0, 0, 2, 4])
        num_projetos['medio'] = fuzz.trapmf(num_projetos.universe, [2, 4, 6, 8])
        num_projetos['alto']  = fuzz.trapmf(num_projetos.universe, [6, 8, 10, 10])

        cumprimento_metas['baixo'] = fuzz.trapmf(cumprimento_metas.universe, [0, 0, 2, 4])
        cumprimento_metas['medio'] = fuzz.trapmf(cumprimento_metas.universe, [2, 4, 6, 8])
        cumprimento_metas['alto']  = fuzz.trapmf(cumprimento_metas.universe, [6, 8, 10, 10])

        participacao_treinamentos['baixo'] = fuzz.trapmf(participacao_treinamentos.universe, [0, 0, 2, 4])
        participacao_treinamentos['medio'] = fuzz.trapmf(participacao_treinamentos.universe, [2, 4, 6, 8])
        participacao_treinamentos['alto']  = fuzz.trapmf(participacao_treinamentos.universe, [6, 8, 10, 10])

        # Definição das funções de pertinência para a variável de saída
        desempenho['baixo'] = fuzz.trapmf(desempenho.universe, [0, 0, 20, 40])
        desempenho['medio'] = fuzz.trapmf(desempenho.universe, [20, 40, 60, 80])
        desempenho['alto']  = fuzz.trapmf(desempenho.universe, [60, 80, 100, 100])

        # Listas de variáveis e seus conjuntos
        variaveis = [num_projetos, satisfacao, cumprimento_metas, participacao_treinamentos]
        conjuntos = ['baixo', 'medio', 'alto']

        # Lista de todas as combinações possíveis
        combinacoes = list(itertools.product(conjuntos, repeat=len(variaveis)))

        rules_file = open(self.RULES_FILE, 'w')
        # Criar regras dinamicamente
        rules = []
        for combo in combinacoes:
            antecedentes = []
            for var, conj in zip(variaveis, combo):
                antecedentes.append(var[conj])
            consequente = functools.verify_max(combo)
            antecedente = antecedentes[0] & antecedentes[1] & antecedentes[2] & antecedentes[3]
            rule = ctrl.Rule(antecedente, desempenho[consequente])
            rules.append(rule)
            rules_file.write(str(rule) + '\n')
            
        rules_file.close()
        
        # Criação do sistema de controle
        self.desempenho_ctrl = ctrl.ControlSystem(rules)
        self.plot_graph(desempenho, satisfacao)
        
    def get_simulator(self):
        desempenho_simulador = ctrl.ControlSystemSimulation(self.desempenho_ctrl)
        return desempenho_simulador
    
    def get_log_file(self):
        return self.LOG_FILE
    
    def get_rules_file(self):
        return self.RULES_FILE
    
    def get_graph_file(self):
        return self.GRAPH_FILE_NAME + '.png'
    
    def plot_graph(self, desempenho, satisfacao):
        # Plot
        desempenho.view(sim=self.get_simulator())
        plt.savefig(self.GRAPH_FILE_NAME + '_desempenho' + '.png')
        
        satisfacao.view(sim=self.get_simulator())
        plt.savefig(self.GRAPH_FILE_NAME + '_inputs' + '.png')
        
        