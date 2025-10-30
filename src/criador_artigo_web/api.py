#Importando os módulos necessários para rodar a API
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
#Importando o BaseModel do Pydantic para definir o modelo de dados
from pydantic import BaseModel
from datetime import datetime
#Importanto a crew que criamos para gerar artigos
from .crew import CriadorArtigoWeb
#Importando datetime
from datetime import datetime

"""
    Para rodar essa api, é necessário ter instalado o FastAPI e o Uvicorn.
    E para rodar o servidor, utilize o comando:
        uvicorn src.criador_artigo_web.api:app --reload
"""

app = FastAPI(title="Criador de Artigos Web API") #Título de nossa aplicação FastAPI

#Definindo o modelo de dados para a requisição e entrada de dados
class ArticleRequest(BaseModel):
    topic: str
#Definindo a rota raiz que redireciona para a documentação automática
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

#Definindo a rota para gerar o artigo
@app.post("/gerar_artigo")
async def generate_article(request: ArticleRequest):
    inputs = {
        "topic": request.topic, # Usando o topic fornecido na requisição
        "current_year": str(datetime.now().year) # Obtendo o ano atual
    }
    
    crew = CriadorArtigoWeb().crew()  # Instanciando a crew

    try:
        result = crew.kickoff(inputs=inputs)  # Executa a crew pela com os inputs fornecidos
        final_article = result.json_dict # Retirando o JSON do resultado
        final_article["timestamp"] = datetime.now() #Tranformando o timestamp(antes uma string) em um datetime
        return {"status": "success", "article": final_article} # Retorna o artigo gerado em caso de sucesso
    except Exception as e:
        return {"status": "error", "message": str(e)} # Retorna o erro da exceção, caso tenha

