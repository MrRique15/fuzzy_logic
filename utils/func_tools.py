import csv

def stringfy_result(result):
    if result <= 30:
        return 'desempenho baixo'
    elif result <= 70:
        return 'desempenho medio'
    else:
        return 'desempenho alto'
    
def verify_max(combo):
    low_amount = combo.count('baixo')
    medium_amount = combo.count('medio')
    high_amount = combo.count('alto')
    
    if low_amount > medium_amount and low_amount > high_amount:
        return 'baixo'
    elif medium_amount > low_amount and medium_amount > high_amount:
        return 'medio'
    elif high_amount > low_amount and high_amount > medium_amount:
        return 'alto'
    else:
        return 'medio'
    
def get_manual_inputs():
    satisfacao = int(input('Digite o valor da satisfação: '))
    num_projetos = int(input('Digite o valor do número de projetos: '))
    cumprimento_metas = int(input('Digite o valor do cumprimento de metas: '))
    participacao_treinamentos = int(input('Digite o valor da participação em treinamentos: '))
    
    return satisfacao, num_projetos, cumprimento_metas, participacao_treinamentos

def get_csv_inputs(file_name):
    satisfacao = []
    num_projetos = []
    cumprimento_metas = []
    participacao_treinamentos = []
    
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            satisfacao.append(int(row[0]))
            num_projetos.append(int(row[1]))
            cumprimento_metas.append(int(row[2]))
            participacao_treinamentos.append(int(row[3]))
            
    return satisfacao, num_projetos, cumprimento_metas, participacao_treinamentos