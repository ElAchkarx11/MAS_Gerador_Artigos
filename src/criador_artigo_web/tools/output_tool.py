# Criado para formatar o output do agente de relatório em arquivo JSON
from pydantic import BaseModel, Field
from datetime import datetime

class ReportInputModel(BaseModel):
    title: str = Field(..., description="Título do artigo")
    introduction: str = Field(..., description="Introdução do artigo")
    body: str = Field(..., description="Corpo do artigo")
    conclusion: str = Field(..., description="Conclusão do artigo")
    source: str = Field(..., description="Fonte das informações utilizadas no artigo")
    timestamp: str = Field(description="Timestamp da geração do artigo")

# Criando o modelo de output para a ferramenta de relatório
class ReportOutputModel(BaseModel):
    title: str = Field(..., description="Título do artigo gerado")
    introduction: str = Field(..., description="Introdução do artigo gerado")
    body: str = Field(..., description="Corpo do artigo gerado")
    conclusion: str = Field(..., description="Conclusão do artigo gerado")
    source: str = Field(..., description="Fonte das informações utilizadas no artigo")
    timestamp: str = Field(description="Timestamp da geração do artigo")