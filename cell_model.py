import mesa
import random
import uuid


class AgenteCelulaImune(mesa.Agent):

    def __init__(self, identificador_unico, modelo):
        super().__init__(identificador_unico, modelo)
        self.estado = "saudavel"  # Estado inicial da célula imunológica
        
        # tentativa de transformação de celula em vírus
        # self.virus_escolhido = inimigo
        # self.grid = mesa.space.MultiGrid(10, 10, True)
        # self.schedule = mesa.time.RandomActivation(self)

    def remove_agent(self, agent):
        """Remove um agente do modelo."""
        if agent in self.model.schedule.agents:
            self.model.grid.remove_agent(agent)
            self.model.schedule.remove(agent)

    def step(self):
        # O comportamento da célula imunológica
        # A célula imunológica pode estar "saudável" ou "infectada".
        if self.estado == "saudavel":
            # A célula imunológica pode encontrar um Vírus e tentar combatê-lo
            vizinhos = self.model.grid.get_neighbors(self.pos, moore=True, radius=1)
            for vizinho in vizinhos:
                if isinstance(vizinho, Agentevirus):
                    # Se o Vírus estiver presente, tenta combatê-lo
                    if random.random() < 0.4:  # 40% de chance de combater com sucesso o Vírus
                        print(f"Célula imunológica {self.unique_id} combateu um Vírus!")
                        self.remove_agent(vizinho)  # Remove o Vírus do modelo
                    else:
                        print(f"Célula imunológica {self.unique_id} falhou ao combater o Vírus.")
                        self.estado = "infectada"
                if isinstance(vizinho, Corote_23):
                    # Se o Vírus estiver presente, tenta combatê-lo
                    if random.random() < 0.1:  # 10% de chance de combater com sucesso o Vírus
                        print(f"Célula imunológica {self.unique_id} combateu um Vírus!")
                        self.remove_agent(vizinho)  # Remove o Vírus do modelo
                    else:
                        print(f"Célula imunológica {self.unique_id} falhou ao combater o Vírus.")
                        self.estado = "infectada"

        elif self.estado == "infectada":
            # A célula imunológica tenta combater a infecção
            if random.random() < 0.5:  # 50% de chance de combater com sucesso a infecção
                self.estado = "saudavel"
                print(f"Célula imunológica {self.unique_id} combateu com sucesso a infecção!")
            else:
                print(f"Célula imunológica {self.unique_id} falhou ao combater a infecção.")
                self.remove_agent(self)  # Remove a célula imunológica do modelo se falhar em combater a infecção
               
                # tentativa de transformação de celula em vírus
                # if self.virus_escolhido == 0:
                #     virus = Agentevirus(str(uuid.uuid4()), self)
                #     x = self.random.randrange(self.grid.width)
                #     y = self.random.randrange(self.grid.height)
                #     self.grid.place_agent(virus, (x, y))
                #     self.schedule.add(virus)
                # if self.virus_escolhido == 1:
                #     virus = Corote_23(str(uuid.uuid4()), self)
                #     x = self.random.randrange(self.grid.width)
                #     y = self.random.randrange(self.grid.height)
                #     self.grid.place_agent(virus, (x, y))
                #     self.schedule.add(virus)

class Agentevirus(mesa.Agent):

    def __init__(self, identificador_unico, modelo):
        super().__init__(identificador_unico, modelo)

    def step(self):
        # O comportamento do Vírus é multiplicar
        novo_virus = Agentevirus(str(uuid.uuid4()), self.model)
        x = self.random.randrange(self.model.grid.width)
        y = self.random.randrange(self.model.grid.height)
        self.model.grid.place_agent(novo_virus, (x, y))
        print(f"Vírus {self.unique_id} se multiplicou!")

class Corote_23(mesa.Agent):
    def __init__(self, identificador_unico, modelo):
        super().__init__(identificador_unico, modelo)

    def step(self):
        # Adicione aqui a lógica do comportamento do NovoAgente no passo de simulação
        novo_virus = Corote_23(str(uuid.uuid4()), self.model)
        x = self.random.randrange(self.model.grid.width)
        y = self.random.randrange(self.model.grid.height)
        self.model.grid.place_agent(novo_virus, (x, y))
        print(f"Vírus corotão se multiplicou!")

class ModeloSistemaImunologico(mesa.Model):

    def __init__(self, num_celulas_imunes, num_virus, largura, altura, escolha_virus):
        self.num_celulas_imunes = num_celulas_imunes
        self.num_virus = num_virus
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(largura, altura, True)
        self.virus_escolhido = escolha_virus
        global_altura = altura
        global_largura = largura
        # Criar células imunes
        for i in range(self.num_celulas_imunes):
            celula_imune = AgenteCelulaImune(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(celula_imune, (x, y))
            self.schedule.add(celula_imune)

        # Criar Vírus
        for _ in range(self.num_virus): 
            if self.virus_escolhido == 0:
                virus = Agentevirus(str(uuid.uuid4()), self)
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(virus, (x, y))
                self.schedule.add(virus)
            if self.virus_escolhido == 1:
                virus = Corote_23(str(uuid.uuid4()), self)
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(virus, (x, y))
                self.schedule.add(virus)
        # Rastreando o número de agentes ao longo do tempo
        if self.virus_escolhido == 0:
            self.datacollector = mesa.datacollection.DataCollector(
                agent_reporters={"virus": lambda a: isinstance(a, Agentevirus),
                               "CelulasImunes": lambda a: isinstance(a, AgenteCelulaImune)}
            )
        if self.virus_escolhido == 1:   
            self.datacollector = mesa.datacollection.DataCollector(
                agent_reporters={"virus": lambda a: isinstance(a, Corote_23),
                               "CelulasImunes": lambda a: isinstance(a, AgenteCelulaImune)}
            )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
