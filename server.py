
import webserver
import sqlite3
import json


BANCO = "usuarios.db"


def conectar():
    conn = sqlite3.connect(BANCO)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    conn.commit()
    return conn, cursor


def resposta(data):
    return json.dumps(data, ensure_ascii=False)


def listar_usuarios():
    conn, cursor = conectar()

    cursor.execute("SELECT id, nome, email FROM usuarios")
    usuarios = []

    for usuario in cursor.fetchall():
        usuarios.append({
            "id": usuario[0],
            "nome": usuario[1],
            "email": usuario[2]
        })

    conn.close()
    return usuarios




def adicionar_usuario(body):

    print("BODY RECEBIDO:", repr(body))
    print("TIPO DO BODY:", type(body))

    try:
        # Verifica se o body está vazio
        if not body:
            return resposta({
                "erro": "Body vazio"
            })

        # Se vier em bytes
        if isinstance(body, bytes):
            body = body.decode("utf-8")

        # Se já vier como dicionário
        if isinstance(body, dict):
            dados = body
        else:
            dados = json.loads(body)

        nome = dados.get("nome")
        email = dados.get("email")

        if not nome or not email:
            return resposta({
                "erro": "Nome e email são obrigatórios",
                "dados_recebidos": dados
            })

        conn, cursor = conectar()

        cursor.execute("""
            INSERT INTO usuarios (nome, email)
            VALUES (?, ?)
        """, (nome, email))

        novo_id = cursor.lastrowid

        conn.commit()

        conn.close()

        print("USUARIO INSERIDO:", novo_id)

        return resposta({
            "mensagem": "Usuario cadastrado com sucesso",
            "id": novo_id,
            "nome": nome,
            "email": email
        })

    except Exception as erro:

        print("ERRO NO INSERT:", str(erro))

        return resposta({
            "erro": str(erro)
        })



def adicionar_usuario1(body):
    try:
        if isinstance(body, bytes):
            body = body.decode("utf-8")

        dados = json.loads(body)

        nome = dados.get("nome")
        email = dados.get("email")

        if not nome or not email:
            return resposta({
                "erro": "Nome e email sao obrigatorios"
            })

        conn, cursor = conectar()

        cursor.execute(
            "INSERT INTO usuarios (nome, email) VALUES (?, ?)",
            (nome, email)
        )

        novo_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return resposta({
            "mensagem": "Usuario cadastrado",
            "id": novo_id,
            "nome": nome,
            "email": email
        })

    except Exception as erro:
        return resposta({"erro": str(erro)})


def deletar_usuario(path):
    try:
        # Extrair parametros da URL
        parametros = path.split("?", 1)

        if len(parametros) < 2:
            return resposta({
                "erro": "Informe o parametro id"
            })

        query = parametros[1]
        usuario_id = None

        for parametro in query.split("&"):
            campos = parametro.split("=", 1)

            if len(campos) == 2 and campos[0] == "id":
                usuario_id = int(campos[1])
                break

        if usuario_id is None:
            return resposta({
                "erro": "ID nao informado"
            })

        conn, cursor = conectar()

        cursor.execute(
            "DELETE FROM usuarios WHERE id = ?",
            (usuario_id,)
        )

        removidos = cursor.rowcount

        conn.commit()
        conn.close()

        if removidos == 0:
            return resposta({
                "erro": "Usuario nao encontrado"
            })

        return resposta({
            "mensagem": "Usuario removido",
            "id": usuario_id
        })

    except Exception as erro:
        return resposta({"erro": str(erro)})




  

def page2(method, path, body):


    # POST - Adicionar usuario
    if method == "POST" and path == "/api/usuarios":
        return adicionar_usuario(body)


  # GET - Pagina inicial
    if method == "GET" and path == "/":
        conectar()[0].close()

        return """
        <h1>maiOs Server</h1>
        <p>Servidor funcionando!</p>
        """

    # GET - Listar usuarios
    if method == "GET" and path == "/api/usuarios":
        return resposta(listar_usuarios())

    # DELETE - Remover usuario
    if method == "DELETE" and path.startswith("/api/usuarios"):
        return deletar_usuario(path)

    return resposta({
        "erro": "404 - Not Found"
    })




webserver.serve(page2)

