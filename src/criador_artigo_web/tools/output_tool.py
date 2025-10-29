# Criado para formatar o output do agente de relatório em arquivo JSON
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime

class ReportInputModel(BaseModel):
    title: str = Field(..., description="Título do artigo")
    introduction: str = Field(..., description="Introdução do artigo")
    body: str = Field(..., description="Corpo do artigo")
    conclusion: str = Field(..., description="Conclusão do artigo")
    source: str = Field(..., description="Fonte das informações utilizadas no artigo")
    timestamp: datetime = Field(description="Timestamp da geração do artigo")

# Criando o modelo de output para a ferramenta de relatório
class ReportOutputModel(BaseModel):
    title: str = Field(..., description="Título do artigo gerado")
    introduction: str = Field(..., description="Introdução do artigo gerado")
    body: str = Field(..., description="Corpo do artigo gerado")
    conclusion: str = Field(..., description="Conclusão do artigo gerado")
    source: str = Field(..., description="Fonte das informações utilizadas no artigo")

# Criando a ferramenta de output que formata o relatório em JSON
class ReportOutputTool(BaseTool):
    name: str = "ReportOutputTool" # Nome da ferramenta (será utilizada pelo agente)
    description: str = "Ferramenta que formata o output do artigo em um arquivo JSON baseado no modelo definido." # Descrição da ferramenta
    args_schema: type[BaseModel] = ReportInputModel # Definido como none pois não há argumentos de Input

    def _run(self, **kwargs) -> ReportOutputModel:
        """Método que implementa a formatação de output do artigo."""
        return ReportOutputModel(
            title=kwargs.get("title"),
            introduction=kwargs.get("introduction"),
            body=kwargs.get("body"),
            conclusion=kwargs.get("conclusion"),
            source=kwargs.get("source"),
            timestamp=datetime.now()
        )