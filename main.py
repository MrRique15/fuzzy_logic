from utils import \
    func_tools as funcTools, \
    fuzzy_core as fuzzyCoreClass

CSV_INPUT_FILE = 'input.csv'

def main():
    defussify_method = input("Digite o método de defuzzificação ('centroid', 'bisector', 'mom', 'som', 'lom'): ")
    if(defussify_method not in ['centroid', 'bisector', 'mom', 'som', 'lom']):
        print("Método de defuzzificação inválido")
        return
    
    log_file_name = f"log_{defussify_method}_results.out"
    
    fuzzyCore = fuzzyCoreClass.fuzzy_core(defuzzify_method=defussify_method, log_file=log_file_name)
    simulador = fuzzyCore.get_simulator()
    log_file = fuzzyCore.get_log_file()

    logger = open(f"outputs/{log_file}", 'w')
    
    input_type = input("Digite o tipo de entrada ('manual' ou 'csv'): ")
    if input_type == 'manual':
        satisfacao, num_projetos, cumprimento_metas, participacao_treinamentos = funcTools.get_manual_inputs()
        simulador.input['satisfacao'] = satisfacao
        simulador.input['num_projetos'] = num_projetos
        simulador.input['cumprimento_metas'] = cumprimento_metas
        simulador.input['participacao_treinamentos'] = participacao_treinamentos
        
        # Computação do resultado
        simulador.compute()
        
        logger.write(f"INPUT: {satisfacao},{num_projetos},{cumprimento_metas},{participacao_treinamentos}\nRESULTADO: {round(simulador.output['desempenho'], 2)}\n")
        logger.close()
    elif input_type == 'csv':
        satisfacao_arr, num_projetos_arr, cumprimento_metas_arr, participacao_treinamentos_arr = funcTools.get_csv_inputs(CSV_INPUT_FILE)
        
        for satisfacao, num_projetos, cumprimento_metas, participacao_treinamentos in zip(satisfacao_arr, num_projetos_arr, cumprimento_metas_arr, participacao_treinamentos_arr):
            simulador.input['satisfacao'] = satisfacao
            simulador.input['num_projetos'] = num_projetos
            simulador.input['cumprimento_metas'] = cumprimento_metas
            simulador.input['participacao_treinamentos'] = participacao_treinamentos
            
            # Computação do resultado
            simulador.compute()
            
            input_print = f"INPUT: [{format(satisfacao, '2')},{format(num_projetos, '2')},{format(cumprimento_metas, '2')},{format(participacao_treinamentos, '2')}]"
            result_print = f"DESEMPENHO: {format(round(simulador.output['desempenho'], 2), '5')},"
            logger.write(f"{input_print} | {result_print}\n")
        logger.close()
    else:
        print('Entrada inválida')
        return
    
    print(f"Resultado salvo em -> outputs/{log_file}")
    print(f"Regras utilizadas salvas em -> outputs/{fuzzyCore.get_rules_file()}")
    print(f"Gráficos salvos em -> outputs/{fuzzyCore.get_graph_file()}.png")
    print("Fim da execução.")
        
    return

if __name__ == '__main__':
    main()