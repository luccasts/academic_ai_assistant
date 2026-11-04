import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "mockdb.json")


def validateUser(enrollment: str, password: str, users_data: dict):

    user = users_data.get(enrollment)

    if user and user.get("senha") == password:
        return user

    # 3. Se não encontrar ou a senha estiver incorreta, retorna None
    return None


def retrieverDatas(enrollment: str, password: str):
    with open(JSON_PATH, encoding="utf-8") as meu_json:
        dados = json.load(meu_json)  # json.load já devolve um dict Python

    return validateUser(enrollment, password, dados)


# Teste 1: Matrícula e senha corretas
usuario = retrieverDatas("333.333.333", "senhaSegura")
print("Resultado do Teste 1:", usuario)
# Saída: {'nome': 'Lucas', 'senha': 'senhaSegura', 'semestre': '4'}

# Teste 2: Senha errada
usuario_invalido = retrieverDatas("333.333.333", "senhaErrada")
print("Resultado do Teste 2:", usuario_invalido)
# Saída: None