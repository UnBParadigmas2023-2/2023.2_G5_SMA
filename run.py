from cell_model import ModeloSistemaImunologico

# Parâmetros do modelo
num_celulas_imunes = 110
num_virus = 100
largura = 10
altura = 10
num_passos = 10
escolha_virus = 1

# Exibir o menu
print("Escolha o tipo de vírus:")
print("0 - Vírus Normal")
print("1 - Corote-23 (potente)")

# Obter a escolha do usuário
escolha_virus = int(input("Digite o número correspondente ao vírus desejado: "))

# Verificar se a escolha é válida
if escolha_virus not in [0, 1]:
    print("Escolha inválida. Por favor, digite 0 ou 1.")
    exit()

# Instância do modelo
modelo_sistema_imunologico = ModeloSistemaImunologico(num_celulas_imunes, num_virus, largura, altura, escolha_virus)
for _ in range(num_passos):
    modelo_sistema_imunologico.step()

# Resultados finais
contagens_finais = modelo_sistema_imunologico.datacollector.get_agent_vars_dataframe().groupby('Step').agg({'virus': 'sum', 'CelulasImunes': 'sum'})
if contagens_finais['virus'].iloc[-1] > contagens_finais['CelulasImunes'].iloc[-1]:
    print("O vírus venceu :(")
    print(contagens_finais)
elif contagens_finais['virus'].iloc[-1] < contagens_finais['CelulasImunes'].iloc[-1]:
    print("As células de defesa venceram :D")
    print(contagens_finais)
else:
    print("Empate!")
