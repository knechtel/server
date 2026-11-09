import webserver
import maiosfs
import ujson

ARQUIVO = "usuarios.json"


def carregar_usuarios():
    try:
        conteudo = maiosfs.read(ARQUIVO)
        return ujson.loads(conteudo)
    except:
        return []


def salvar_usuarios(usuarios):
    conteudo = ujson.dumps(usuarios)
    maiosfs.write(ARQUIVO, conteudo)


def page(method, path):

    # Página inicial
    if method == "GET" and path == "/":
        return """
        <h1>maiOs API</h1>
        <p>Servidor funcionando!</p>
        """

    # Consultar usuários
    if method == "GET" and path == "/api/usuarios":
        usuarios = carregar_usuarios()
        return ujson.dumps(usuarios)

    # Inserir usuário
    if method == "POST" and path == "/api/usuarios":

        # Precisamos obter o corpo HTTP aqui.
        # Exemplo: {"nome":"Maiquel"}

        return "Endpoint POST preparado"

    return "404 - Not Found"


webserver.serve(page)
