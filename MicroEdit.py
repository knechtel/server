def microedit(nome="notas.txt"):
    try:
        with open(nome, "r") as arquivo:
            texto = arquivo.read()
    except OSError:
        texto = ""

    print("MicroEdit — editando", nome)
    print("Conteúdo atual:")
    print(texto)
    print("\nDigite o texto novo. Digite . em uma linha para salvar e sair.")

    linhas = []

    while True:
        linha = input()
        if linha == ".":
            break
        linhas.append(linha)

    with open(nome, "w") as arquivo:
        arquivo.write("\n".join(linhas) + "\n")

    print("Salvo. Saindo do MicroEdit.")

microedit()
