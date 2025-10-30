# Criador de Artigos Web

## Objetivo do Projeto
O projeto **Criador de Artigos Web** tem como objetivo automatizar a criação de artigos para websites.
Para tanto, foi desenvolvido um **sistema multiagente(MAS)** baseado na técnica *[Chain Of Thought(ToT)](https://www.promptingguide.ai/pt/techniques/cot)*, utilizando o framework ***CrewAI***.
O sistema realiza pesquisas na API da ***Wikipedia***, formata os resultados e retorna um artigo completo em **JSON**, com no mínimo 300 palavras sobre o tema solicitado.

## Stack e Framework
O projeto utiliza ***Python 3.14*** (versão mais atual em outubro de 2025) e implementa um sistema multiagente (MAS) com o framework ***CrewAI***, permitindo a criação e orquestração de agents, tasks, tools e crews.
As principais dependências são:

  - ***crewai*** - Framework para orquestração de agentes de IA.
  - ***crewai[google-genai]*** - Ferramenta para orquestração de agentes de IA, em específico para o Modelo Gemini(Utilize qual modelo for pertinente).
  - ***crewai-tool*** - Ferramentas pré-construídas para os Agentes de IA.
  - ***pydantic*** - Ferramenta para validação de dados de entrada e saída de em anotações dos agentes e tasks.
  - ***fastapi*** - Criador de endpoints HTTP rápidos e com documentação automática(e o que mais se adequa ao pydantic).
  - ***uvicorn*** - Servidor ASGI, que roda em paralelo com o fastAPI.
  - ***pytest*** - Framework para testes unitários.
  - ***requests*** - Ferramenta para requisições baseadas em URL, que é o caso da API da Wikipedia.
  - ***python-dotenv*** - Ferramenta que trata de varíaveis de ambiente em um arquivo .env.

### Agentes

Foram criados 2 agentes principais:

#### ***Researcher_Agent***
Atua como pesquisador de artigos da ***Wikipedia***, buscando informações relevantes e atualizadas (ano 2025).
Utiliza a API ***MediaWiki*** e retorna dados estruturados para o próximo agente.

#### ***Writer_Agent***
Atua como **redator técnico**, responsável por gerar o relatório detalhado em formato **JSON**, contendo:
  - Título
  - Introdução
  - Corpo do texto
  - Conclusão
  - Fonte
  - Time Stamp
    
Foi desenvolvido com Engenharia de Prompt, aplicando a técnica ***[Chain Of Thought(ToT)](https://www.promptingguide.ai/pt/techniques/cot)***.

Os agentes, caso seja necessário, devem ser modificiadas na pasta **"/config"**(Responsável pela criação dos agentes em arquivos **YAMLs**), e então no arquivo **crew.py**(onde os agentes estarão marcadas com o decorador **@Agents**).  Para mais informações, acessar a documentação ***[CrewAI - Agents](https://docs.crewai.com/en/concepts/agents)***.

### Quais as Tasks criadas?

O sistema contém duas tasks, associadas aos agentes:

#### ***Research_task***:
Executada pelo ***Researcher_Agent***, realiza a pesquisa sobre o tópico e retorna:
  - Título
  - Resumo em Texto simples
  - URL da pesquisa
  - Timestamp
  - Fonte

#### ***Writing_Task***
Executada pelo ***Writer_Agent***, gera o artigo detalhado e formatado em **JSON**, baseado no modelo ***ReportOutputModel***.
  - Titulo
  - Introdução
  - Corpo
  - Conclusão
  - Fonte
  - Time Stamp

As tasks, caso seja necessário, devem ser modificiadas na pasta **"/config"**(Responsável pela criação das tasks em arquivos **YAMLs**), e então no arquivo **crew.py**(onde as tasks estarão marcadas com o decorador **@Task**). Para mais informações, acessar a documentação ***[CrewAI - Tasks](https://docs.crewai.com/en/concepts/tasks)***.

### Quais as minhas tools criadas?
Apenas uma ferramenta foi desenvolvida:
#### ***WikiTool***
Localizada em **"/tools/wiki_tool.py"** essa tool personalizada faz buscas na API da ***Wikipedia***. 
Recebe apenas um *input* de *topic* e produz um output formatado. 
Demais informações sobre tools personalizadas e nativas estão presentes na documentação ***[CrewAI - Tools](https://docs.crewai.com/en/concepts/tools).***
Informações sobre a API da Wikipedia está em  ***[MediaWiki](https://www.mediawiki.org/wiki/API:Tutorial)***.

### Quais os modelos criados?
#### ***ReportOutputModel***
Foi criado apenas um único modelo, presente na pasta **"/models"** que utiliza ***Pydantic*** para modelar o output da task do agente ***Writer_Agent***, que formata a saída em **JSON**:
  - Título
  - Introdução
  - Corpo
  - Conclusão
  - Source
  - TimeStamp

### Quais as APIs utilizadas?
#### ***API da Wikipedia***
Foi utilizada a API da ***Wikipedia***, que através de uma URL com a *query* de pesquisa, é possível buscar conteúdo ou uma lista de conteúdos sobre um determinado topico. O Consumo dessa API é feita através do módulo ***requests***, e está presente na ferramenta personalizada ***WikiTool***, utilizada pelo agente ***Research_Agent***.

#### ***API de Execução***
Através do ***FastAPI***, foi criada uma API personalizada com o objetivo de executar o sistema, esta foi criada com dois métodos:
  - ***GET("/")*** - Utilizada no *root* para redirecionar o usuário para a documentação automática.
  - ***POST("/gerar_artigo")*** - Utilizada para definir a rota que gera o artigo, requere os *inputs*, define o output da crew e retorna o **JSON**.

Para rodar o ***FastAPI*** e acessar o ***Swagger***, utilizar o comando:
   ```
    uvicorn criador_artigo_web.api:app --reload
   ```
Isso abrirá a tela para que seja possível passar o tópico de pesquisa e aguardar o resultado dos agentes. 

#### ***API da Gemini***
Foi utilizado o modelo LLM ***Gemini-2.5-pro***, do ***Google***, para o conhecimento dos agentes e execução da crew. Para isso, foi necessário importar a chave de API desse modelo nas variáveis de ambiente, outros modelos podem ser utilizados como: *Groq*, *OpenRouter*, etc. Caso o modelo Gemini seja utilizado, a chave de API deve ser criada no ***[GoogleAI Studio](https://aistudio.google.com)***.
    
## Acesso e execução do código fonte
Nessa seção será demonstrado como acessar e executar o código do projeto.

1. Clone o repositório
   ```
   # Clone o repositório via Bash
   git clone https://github.com/ElAchkarx11/MAS_Gerador_Artigos.git

   # Acesse o arquivo principal do projeto
   cd criador_artigo_web 
   ```
2. Instale as dependências:
   ```
   pip install -r requeriremets.txt
   ```
3. Crie um arquivo ***.env*** e configure as *variáveis de ambiente*, exemplo:
    ```
    MODEL="Modelo de LLM de escolha"
    GEMINI_API_KEY="Chave da API do modelo que utilizará"
    USER_AGENT= "Criar um user-agent é essencial para que a API da Wiki funcione corretamente. (Ex.: CriadorArtigoWeb/1.0 (+https://github.com/seuusuário))"
    ```
4. Caso queira executar a aplicação localmente:
    ```
    crewai run
    ```
   Lembrando que para a aplicação local, é necessário altera a variável *"TOPIC"*, presente no arquivo *main.py**.
5. Caso queira executar via API, execute a API do ***FastAPI***:
    ```
    uvicorn criador_artigo_web.api:app --reload
    ```
6. Acesse a documentação iterativa:
    ```
     http://127.0.0.1:8000/docs
    ```
7. Caso o *input* seja semelhante ao exemplo abaixo:
    ```
    POST/ gerar_artigo
    {
      "topic": "batata" # Ou qualquer outro input de topic que deseje pesquisar
    }
    ```
   Logo, o resultado será:
   ```
    "status": "success",
    "article": {
      "title": "Batata: Um Pilar da Alimentação Global",
      "introduction": "A batata, cientificamente conhecida como *Solanum tuberosum*, é muito mais do que um simples tubérculo; é um pilar fundamental da alimentação global. Originária das terras altas da Cordilheira dos Andes, na América do Sul, esta planta perene da família das solanáceas transformou-se, ao longo dos séculos, de um alimento regional para o quarto alimento mais consumido em todo o mundo. Sua jornada desde as margens do Lago Titicaca até as mesas de bilhões de pessoas é uma história de adaptação, resiliência e valor nutricional inegável, solidificando seu papel crucial na segurança alimentar e na economia global. Sua versatilidade e capacidade de adaptação a diferentes climas e solos contribuíram para sua disseminação e aceitação universal.",
      "body": "A história da batata começa há milhares de anos, ...",
      "source": "Wikipedia",
      "timestamp": "2025-10-30T01:47:01.774496"
      }
    }
   ```
   
## Testes e Validações

### Quais os testes criados ?
#### ***Test_Wiki_Tool***
Apenas um único teste foi criado, presente na pasta *"/tests"*. Este utiliza o ***pytest*** e é responsável por realizar verificar se os resultados da API da ***Wikipedia*** estão congruentes com as informações do tópico pesquisado no próprio teste, assim, caso a API mude de alguma forma, o teste sempre mostrará alteração.

Para rodar o teste, foi criado um arquivo ***.ini***, logo basta apenas rodar o código:
```
pytest
```

## Fluxo
O fluxograma simples para as projeto é representado abaixo:
```
Entrada[POST] -> FastAPI recebe a requisição -> CrewAI executa Researcher_Agent -> Researcher_Agent busca na API da Wikipedia -> Writer_Agent estrutura o artigo -> Saída Formatada[JSON]
```

## Objetivos futuros
Para objetivos futuros, são propostos os seguintes tópicos:
- Adição de agentes especializados em sumarização e otimização das buscas.
- Criar interface web para visualização do artigo final, atráves do ***React***.
- Integração de banco de dados(***MongoDB*** ou ***PostgreSQL***) para histórico de pesquisas e armazenamento de artigos.
- Implementação de cache para reduzir o tempo de busca.