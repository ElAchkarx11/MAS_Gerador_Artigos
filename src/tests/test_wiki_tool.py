#Aqui foi criado um teste simples para a ferramenta de WikiTool, utilizando o Pytest (Será referencia na documentação de como rodar esse teste)
from criador_artigo_web.tools.wiki_tool import WikiTool #Importando a minha ferramenta


#Criando o teste para a ferramenta WikiTool
def test_wikipedia_tool_run():
    tool = WikiTool() #Referenciando a ferramenta
    topico = "Python (linguagem de programação)" # Definindo um termo de busca conhecido na Wikipedia
    result = tool._run(topic=topico) #Executando a ferramenta com o termo definido
    
    assert "Python" in result.article_title #Verificando se meu termo tem o título retornado
    assert "Python" in result.summary #Verificando se o sumário contém esse termo
    assert result.url.startswith("https://pt.wikipedia.org/")#Verificando se a url é válida da Wikipedia em português
