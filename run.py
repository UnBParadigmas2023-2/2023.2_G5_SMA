from cell_model import ModeloSistemaImunologico

# Parâmetros do modelo
num_celulas_imunes = 110
num_virus = 100
largura = 10
altura = 10
num_passos = 10

# Instância do modelo
modelo_sistema_imunologico = ModeloSistemaImunologico(num_celulas_imunes, num_virus, largura, altura)
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
