import webserver

def page(method, path):
    return "maiOs diz olá! Você pediu " + path

webserver.serve(page)
