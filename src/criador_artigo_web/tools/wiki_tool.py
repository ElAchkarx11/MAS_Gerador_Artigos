from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import requests

#Criando o modelo de input para a ferramenta
class WikiToolInput(BaseModel):
    # Query String para pesquisa na WIkipedia
    termo: str = Field(..., description="Query string para pesquisa na Wikipedia")

#Criando um modelo de Output da ferramenta
class WikiToolOutput(BaseModel):
    #Query String de saída da ferramenta
    article_title: str = Field(..., description="Título do artigo retornado da Wikipedia")
    summary: str = Field(..., description="Sumário do artigo retornado da Wikipedia")
    url: str = Field(..., description="URL do artigo retornado da Wikipedia")

#Criando a ferramenta que faz a busca na base da Wikipedia
class WikiTool(BaseTool): 
    name: str = "WikiTool" #Define o nome da ferramenta (Será utilizada pelo agente)
    description: str = "Ferramenta que será utilizada para buscar informações na Wikipedia." #Descrição da ferramenta, importante para o agente
    args_schema: type[BaseModel] = WikiToolInput #Define o modelo de input que a ferramenta recebe, nesse caso somente um input "Termo"
    def _run(self, termo: str) -> WikiToolOutput:#Aqui é a implementação da lógica, referenciando o output criado dessa ferramenta
        #Tratando possíveis exceções que podem ocorrer
        try:
            """Método que implementa a lógica da ferramenta."""
            endpoint = "https://pt.wikipedia.org/w/api.php" #A API pública da Wikipedia, é o endpoint padrão para consultas. 
                                                            # O "pt" representa a base em português, existem outras bases, como "en" para inglês.
            headers = { 
                "User-Agent": "CriadorArtigoWeb/1.0 (+https://github.com/ElAchkarx11)" #Por questões políticas de uso da API, a própria recomenda
                                                                                        #a utilização de um User-Agent personalizado para identificar a 
                                                                                        # aplicação que está fazendo as requisições.
            }

            # A ideia princípal para esse bloco de código é:
                # 1. Fazer uma busca inicial para encontrar o título mais relevante;
                # 2. Utilizar esse título para extrair um conteúdo abrangente do artigo da Wiki.
            # Para mais informações sobre a API da Wikipedia, consulte: https://www.mediawiki.org/wiki/API:Main_page/pt
            search_params = {
                "action": "query", # Parâmetro: Obtem dados sobre as páginas da Wikipedia
                "list": "search", # Parâmetro: Realiza uma busca por texto completo
                "srsearch": termo, # Parâmetro: Termo de busca fornecido pelo usuário
                "format": "json" # Parâmetro: Formato da resposta (JSON)
            }

            # Utilizando o módulo requests para fazer uma requisição GET na API da Wikipedia
            search_response = requests.get(endpoint, params=search_params, headers=headers)
            # Convertendo a resposta para JSON - Que já vem por padrão nesse tipo de API
            search_data = search_response.json()

            # Pegando meus resultados de busca ou retornando "Nada encontrado" caso não haja resultados
            search_results = search_data.get("query", {}).get("search", [])
            if not search_results:
                return "Nada encontrado."

            # Pega o primeiro resultado mais relevante
            page_title = search_results[0]["title"]

            #Criando parâmetros para extração das informações encontradas
            extract_params = {
                "action": "query", 
                "prop": "extracts", # Parâmetro: Extraí o conteúdo do artigo
                "titles": page_title, # Parâmetro: Título do artigo a ser extraído, nesse caso o mais relevante
                "format": "json", 
                "explaintext": 1 # Parâmetro: Uma forma de complementar o "Extracts", retornando o texto puro sem formatação HTML
            }

            #Fazend uma nova requisção, uma nova extração de JSON, agora para extrair o conteúdo desse artigo
            extract_response = requests.get(endpoint, params=extract_params, headers=headers)
            extract_data = extract_response.json()
            
            #Extraindo os resultados, se não retornando que nada foi encontrado
            extract_results = extract_data.get("query", {}).get("pages", {})
            if not extract_results:
                return "Nada encontrado."
            
            # A API retorna dados em um dicionário, onde a chave é o ID da página (Dinâmico), 
            # então pego o primeiro valor desse dicionário
            results = next(iter(extract_results.values()))
            result = results.get("extract", {}) # Pegando o conteúdo extraído do artigo
            url_format = f"https://pt.wikipedia.org/wiki/{page_title.replace(' ', '_')}" # Formatando a minha URL de saída, para acesso direto.
                                                                                         # Formatando o título em um padrão de URL com "_", sem espaços.
            # Retornando o output da ferramenta, conforme o modelo criado
            return WikiToolOutput(
                article_title=page_title,
                summary=result,
                url = url_format
            )
        except Exception as e:
            return f"Erro ao buscar na Wikipedia: {str(e)}" #Caso tudo de errado, retorna o erro

