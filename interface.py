import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from cell_model import ModeloSistemaImunologico

def executar_simulacao(escolha_virus):
    num_celulas_imunes = 110
    num_virus = 100
    largura = 10
    altura = 10
    num_passos = 10
    num_vacinas = 5

    modelo = ModeloSistemaImunologico(num_celulas_imunes, num_virus, largura, altura,num_vacinas, escolha_virus)
    for _ in range(num_passos):
        modelo.step()

    dados = modelo.datacollector.get_agent_vars_dataframe()
    atualizar_grafico(dados)
    determinar_vencedor(dados)

def atualizar_grafico(dados):
    contagens = dados.groupby('Step').agg({'virus': 'sum', 'CelulasImunes': 'sum'})

    ax.clear()
    ax.plot(contagens.index, contagens['virus'], label='Vírus')
    ax.plot(contagens.index, contagens['CelulasImunes'], label='Células Imunes')
    ax.legend()
    ax.grid(True, linestyle='--')

    canvas.draw()

def determinar_vencedor(dados):
    contagens_finais = dados.groupby('Step').agg({'virus': 'sum', 'CelulasImunes': 'sum'}).iloc[-1]
    if contagens_finais['virus'] > contagens_finais['CelulasImunes']:
        resultado_var.set("Resultado: O vírus venceu!")
    elif contagens_finais['virus'] < contagens_finais['CelulasImunes']:
        resultado_var.set("Resultado: As células imunes venceram!")
    else:
        resultado_var.set("Resultado: Empate!")

root = tk.Tk()
root.title("Simulação do Sistema Imunológico")

escolha_virus = tk.IntVar()
radio_virus_normal = tk.Radiobutton(root, text="Vírus Normal", variable=escolha_virus, value=0)
radio_virus_normal.pack()
radio_corote_23 = tk.Radiobutton(root, text="Corote-23 (potente)", variable=escolha_virus, value=1)
radio_corote_23.pack()

fig = Figure(figsize=(6, 4))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

resultado_var = tk.StringVar()
resultado_label = tk.Label(root, textvariable=resultado_var)
resultado_label.pack()

btn_iniciar = tk.Button(root, text="Iniciar Simulação", command=lambda: executar_simulacao(escolha_virus.get()))
btn_iniciar.pack(side=tk.BOTTOM)

def sair():
    root.destroy()

btn_sair = tk.Button(root, text="Sair", command=sair)
btn_sair.pack(side=tk.BOTTOM)

root.mainloop()
