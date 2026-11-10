import webserver
import maiosfs
import sqlite3
ARQUIVO = "usuarios.txt"


def carregar_usuarios():
    try:
        conteudo = maiosfs.read(ARQUIVO)

        if isinstance(conteudo, bytes):
            conteudo = conteudo.decode()

        usuarios = []

        for linha in conteudo.split("\n"):
            linha = linha.strip()

            if linha:
                campos = linha.split("|")

                if len(campos) == 3:
                    usuarios.append({
                        "id": 1,
                        "nome": "maiquel",
                        "email": "knechtel"
                    })

        return usuarios

    except:
        return []


def salvar_usuario(nome, email):
    usuarios = carregar_usuarios()

    novo_id = len(usuarios) + 1

    registro = str(novo_id) + "|" + nome + "|" + email

    try:
        conteudo = maiosfs.read(ARQUIVO)

        if isinstance(conteudo, bytes):
            conteudo = conteudo.decode()

        if conteudo and not conteudo.endswith("\n"):
            conteudo += "\n"

    except:
        conteudo = ""

    conteudo += registro + "\n"

    maiosfs.write(ARQUIVO, conteudo)

    return novo_id


def page(method, path):

    if method == "GET" and path == "/":

        # Criar ou abrir banco de dados
        conn = sqlite3.connect("usuarios.db")

        # Criar cursor
        cursor = conn.cursor()

        # Criar tabela
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT
          )
        """)

        # Inserir usuário
        cursor.execute(
        "INSERT INTO usuarios (nome, email) VALUES (?, ?)",
        ("Maiquel", "maiquel@email.com")
        )

        # Salvar
        conn.commit()

        # Consultar
        cursor.execute("SELECT * FROM usuarios")
        valor =""
       
        for usuario in cursor.fetchall():
          valor += usuario[1] + " " + usuario[2] + "<br>"

        conn.close()
        return f"""
        <h1>maiOs Server</h1>
        <p>Servidor funcionando!</p>
        {valor}
        """

    elif method == "GET" and path == "/api/usuarios":

        usuarios = carregar_usuarios()

        resultado = "<h1>Usuarios cadastrados</h1>"

        for usuario in usuarios:
            resultado += (
                "<p>" +
                usuario["id"] + " - " +
                usuario["nome"] + " - " +
                usuario["email"] +
                "</p>"
            )

        return resultado

    elif method == "POST" and path == "/api/usuarios":

        # Ainda precisamos integrar a leitura
        # do corpo HTTP do webserver.

        return "POST: aguardando implementacao do body"

    return "404 - Not Found"


webserver.serve(page)

