# Helpers

def combinar_dados_nexxcera(sistema_a, sistema_b):
    """
        Combina os dados de dois sistemas, recalcula a porcentagem e retorna a estrutura combinada.

        Args:
        - sistema_a (dict): Dados do Sistema A.
        - sistema_b (dict): Dados do Sistema B.

        Returns:
        - dict: Estrutura combinada com os totalizadores e a porcentagem recalculada.
    """

    # Verificar se os sistemas têm a chave 'data' e 'nexxera'
    if 'data' not in sistema_a or 'data' not in sistema_b:
        raise ValueError("Ambos os sistemas devem conter a chave 'data'.")
    
    if 'nexxera' not in sistema_a['data'] or 'nexxera' not in sistema_b['data']:
        raise ValueError("Ambos os sistemas devem conter a chave 'nexxera' dentro de 'data'.")

    # Extrair dados de cada sistema
    a_data = sistema_a['data']
    b_data = sistema_b['data']
    
    a_nexxera = a_data['nexxera']
    b_nexxera = b_data['nexxera']
    
    # Calcular totais combinados
    total_clientes = a_data['total_clientes'] + b_data['total_clientes']
    total_empresas = a_nexxera['total_empresas'] + b_nexxera['total_empresas']
    empresas_nexxera = a_nexxera['empresas_nexxera'] + b_nexxera['empresas_nexxera']
    empresas_sem_nexxera = a_nexxera['empresas_sem_nexxera'] + b_nexxera['empresas_sem_nexxera']
    
    # Calcular a porcentagem
    if total_empresas > 0:
        porcentagem = (empresas_nexxera / total_empresas) * 100
    else:
        porcentagem = 0
    
    porcentagem_formatada = f"{porcentagem:.2f}"
    
    # Criar o resultado combinado
    resultado = {
        'data': {
            'code': 200,  # Presumivelmente o código de resposta é o mesmo
            'total_clientes': total_clientes,
            'nexxera': {
                'total_empresas': total_empresas,
                'empresas_nexxera': empresas_nexxera,
                'empresas_sem_nexxera': empresas_sem_nexxera,
                'porcentagem': porcentagem_formatada
            }
        },
        'success': True  # Presumivelmente o status de sucesso é o mesmo
    }
    
    return resultado


def combinar_dados_bancos(tabela1, tabela2):
    def calcular_porcentagens_e_ordenar(ranking):
        # Calcula o total de contas
        total_contas = sum(banco['QtdeContas'] for banco in ranking.values())
        
        # Calcula a nova porcentagem para cada banco
        for banco_id, dados in ranking.items():
            dados['Porcentagem'] = round((dados['QtdeContas'] / total_contas) * 100, 2)
        
        # Ordena os bancos pelo número de contas em ordem decrescente
        ranking_ordenado = dict(sorted(ranking.items(), key=lambda item: item[1]['QtdeContas'], reverse=True))
        
        return ranking_ordenado

    # Extraindo as listas de bancos das tabelas
    lista_bancos1 = tabela1.get('lista_bancos', {})
    lista_bancos2 = tabela2.get('lista_bancos', {})

    # Combinando os dados da tabela 1 com informações da tabela 2
    for nome_banco2, dados2 in lista_bancos2.items():
        if nome_banco2 in lista_bancos1:
            dados1 = lista_bancos1[nome_banco2]
            # Atualizando quantidade de contas e clientes
            dados1['qtd_contas'] += dados2['qtd_contas']
            dados1['qtd_clientes'] = str(int(dados1['qtd_clientes']) + dados2['qtd_clientes'])
        else:
            # Adicionando novo banco da tabela 2 à tabela 1
            lista_bancos1[nome_banco2] = dados2

    # Atualizando o ranking de bancos
    ranking1 = tabela1.get('ranking_bancos', {})
    ranking2 = tabela2.get('ranking_bancos', {})

    # Combinando o ranking com novos dados
    for codigo, dados2 in ranking2.items():
        if codigo in ranking1:
            # Atualizando quantidade de contas e porcentagem
            ranking1[codigo]['QtdeContas'] += dados2['QtdeContas']
        else:
            if len(ranking1) < 6:           
                # Adicionando novos bancos ao ranking
                ranking1[codigo] = dados2

    # Calcular as porcentagens e ordenar o ranking
    ranking1 = calcular_porcentagens_e_ordenar(ranking1)

    # Atualizar a tabela1 com os dados combinados
    tabela1['lista_bancos'] = lista_bancos1
    tabela1['ranking_bancos'] = ranking1

    return tabela1