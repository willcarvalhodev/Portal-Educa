def Verificar_Perfil(email):

    email_minusculo = email.lower()

    if email_minusculo.endswith("@coordenador.educa"):
        return "Perfil: Coordenador"
    elif email_minusculo.endswith("@professor.educa"):
        return "Perfil: Professor"
    elif email_minusculo.endswith("@aluno.educa"):
        return "Perfil: Aluno"
    else:
        return "E-mail informado está errado."


login_input = input("Digite o E-mail fornecido pela instituição: ")

print(Verificar_Perfil(login_input))
