# Importando módulos necessários do CrewAI
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai import LLM
# Importando ferramentas customizadas
from .tools.wiki_tool import WikiTool
#Importando módulos para lidar com as váriaveis de ambiente
import os
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis de ambiente do arquivo .env(Você precisa criar as suas variáveis de ambiente lá)

API_KEY = os.getenv("GEMINI_API_KEY")  # Aqui você coloca a sua API key do google, obrigatório para uso de modelos Gemini
MODEL = os.getenv("MODEL") #Aqui o modelo de LLM que vai utilizar, nesse projeto foi utilizado gemini-2.5-pro por ser gratuito e rápido.
                           #Outros modelos possíveis : gpt-4, gemini-2.5-flash, basta mudar aqui etc.

#Instanciando a LLM que será utilizada pelos agentes
llm = LLM(
    model=MODEL, # Modelo de linguagem que vai utilizar
    temperature=0.3, #Controlando as respostas do modelo. Quanto maior o valor, mais variada a respostas.
    api_key=MODEL #Aqui você coloca a sua API key do google, obrigatório para 
                                                      #modelos Gemini. Para criar uma API key: https://aistudio.google.com/u/1/api-keys
)

# O decorador @CrewBase indica que essa classe define um crew
@CrewBase
class CriadorArtigoWeb():
    
    """CriadorArtigoWeb crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
 
    # Aqui você adiciona os agentes, tarefas e ferramentas que utilizará, 
    # Seguindo os arquivos de configuração YAML criados na pasta /config
    # A documentação do crewai deixa disponível mais detalhes de configuração nos links abaixo:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    # Tools: https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher_agent(self) -> Agent:
        wiki_tool = WikiTool()
        return Agent(
            config=self.agents_config['researcher_agent'], # type: ignore[index]
            verbose=True,
            llm=llm, #Aqui adiciona a llm que deseja, eu utilizei a gemini-2.5-pro e instanciei 
            tools= [wiki_tool] #Aqui adiciona a tool, seja customizada ou as nativas do crewai
        )
    
    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['writer_agent'], # type: ignore[index]
            verbose=True,
            llm=llm,
        )

    # Aqui estou adicionando as taks que o crew irá executar, também do .YAML da pasta /config
    # A documentação do crewai deixa disponível mais detalhes de configuração, no link abaixo:
    # Task Avançada: https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'], # type: ignore[index]
            output_file='report.md' #Define o nome do arquivo de saída gerado por essa task
        )

    # Aqui o decorador @crew indica que esse método cria o crew com meus respectivos agents e tasks
    @crew
    def crew(self) -> Crew:
        """Creates the CriadorArtigoWeb crew"""

        return Crew(
            agents=self.agents, # Isso é criado automaticamente pelo decorador @agent
            tasks=self.tasks, # Isso é criado automaticamente pelo decorador @task
            process=Process.sequential, # Isso define que as tasks serão executadas de forma sequencial
            verbose=True,
        )
