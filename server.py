import webserver
import ujson

from database import Database

db = Database()

def page(method, path):

    if path == "/":
        return """
        <h1>maiOs Web Server</h1>
        <a href="/usuarios">Consultar usuários</a>
        """

    elif path == "/usuarios":

        usuarios = db.select("usuarios")

        html = "<h1>Usuários do maiOs</h1>"

        for usuario in usuarios:
            html += "<p>"
            html += str(usuario["id"]) + " - "
            html += usuario["nome"]
            html += "</p>"

        return html

    elif path == "/api/usuarios":

        usuarios = db.select("usuarios")

        return ujson.dumps(usuarios)

    return "Página não encontrada: " + path


webserver.serve(page)
