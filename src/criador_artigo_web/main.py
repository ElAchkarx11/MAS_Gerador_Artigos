#!/usr/bin/env python
# Importando módulos necessários
import sys
import warnings
#Referenciando a data e hora atual para utilizar como variável de input no crew
from datetime import datetime
#Referenciando o crew criado
from criador_artigo_web.crew import CriadorArtigoWeb

# Criando uma variável para referenciar o topico de interesse, altere como desejar
TOPIC = "Segunda Guerra Mundial"

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

    # A pasta main é uma maneira de rodar a crew localmente. 
    # Por recomendação da documentação da própria crewAI, não use lógica desnecessária aqui.
    # Substitua as varíaveis de input que deseje testar, isso vai mudar inferir diretamente nas tasks e agetes.

# Função para rodar o crew
def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': TOPIC, # O tópico que deseja pesquisar e criar o artigo. Será utilizado como "topic" na WikiTool.
        'current_year': str(datetime.now().year) # A variável do ano atual, para referenciar no artigo.
        #Caso seja necessário, adicione mais varíaveis de input aqui como desejar, desde que estejam presentes nas tasks e agentes.
    }
    #Caso tudo dê certo, inicia a execução, se não retorna uma exceção.
    try:
        CriadorArtigoWeb().crew().kickoff(inputs=inputs) #Inicia a execução do crew com os inputs fornecidos
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

# Função para treinar o crew, em quantas interações necessárias ou desejadas
def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": TOPIC,
        'current_year': str(datetime.now().year)
    }
    try:
        CriadorArtigoWeb().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

# Função para replay da execução do crew a partir de uma task específica
def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CriadorArtigoWeb().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

# Função para testar a execução do crew por um número específico de iterações
def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": TOPIC,
        "current_year": str(datetime.now().year)
    }

    try:
        CriadorArtigoWeb().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

# Função para rodar o crew com um payload de trigger específico
def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = CriadorArtigoWeb().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
