import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

score = 0
token = None


def print_result(test_name, success):
    global score
    if success:
        print(f"[✔] {test_name}")
        score += 3
    else:
        print(f"[✘] {test_name}")


def auth_headers():
    return {"Authorization": f"Bearer {token}"} if token else {}


def setup_auth():
    global token
    stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    email = f"teste_{stamp}@email.com"

    r = requests.post(f"{BASE_URL}/users", json={
        "nome": "Admin Teste",
        "email": email,
        "senha": "123456",
    })
    if r.status_code not in [200, 201]:
        return False

    r = requests.post(f"{BASE_URL}/login", json={
        "email": email,
        "senha": "123456",
    })
    if r.status_code != 200:
        return False

    data = r.json()
    token = data.get("data", {}).get("token")
    return token is not None


def test_create_team():
    response = requests.post(
        f"{BASE_URL}/teams",
        json={"nome": "Equipe Teste"},
        headers=auth_headers(),
    )
    success = response.status_code in [200, 201]
    print_result("Criar equipe", success)

    if success:
        return response.json()["data"]["id"]
    return None


def test_list_teams():
    response = requests.get(f"{BASE_URL}/teams")
    success = response.status_code == 200 and isinstance(response.json()["data"], list)
    print_result("Listar equipes", success)


def test_create_participant(team_id):
    response = requests.post(
        f"{BASE_URL}/participants",
        json={
            "nome": "João",
            "idade": 18,
            "team_id": team_id,
        },
        headers=auth_headers(),
    )
    success = response.status_code in [200, 201]
    print_result("Criar participante válido", success)

    if success:
        return response.json()["data"]["id"]
    return None


def test_invalid_team():
    response = requests.post(
        f"{BASE_URL}/participants",
        json={
            "nome": "Erro",
            "idade": 20,
            "team_id": 9999,
        },
        headers=auth_headers(),
    )
    success = response.status_code == 404
    print_result("Erro ao criar participante com equipe inválida", success)


def test_list_participants():
    response = requests.get(f"{BASE_URL}/participants")
    success = response.status_code == 200 and isinstance(response.json()["data"], list)
    print_result("Listar participantes", success)


def test_participants_by_team(team_id):
    response = requests.get(f"{BASE_URL}/teams/{team_id}/participants")
    success = response.status_code == 200 and isinstance(response.json()["data"], list)
    print_result("Listar participantes por equipe", success)


def test_validation():
    response = requests.post(
        f"{BASE_URL}/teams",
        json={},
        headers=auth_headers(),
    )
    success = response.status_code == 400
    print_result("Validação de dados obrigatórios", success)


def test_login():
    response = requests.post(f"{BASE_URL}/login", json={
        "email": "invalido@email.com",
        "senha": "errada",
    })
    success = response.status_code == 401
    print_result("Login com credenciais inválidas", success)


def test_protected_without_token():
    response = requests.post(f"{BASE_URL}/teams", json={"nome": "Sem Token"})
    success = response.status_code == 401
    print_result("Rota protegida sem token", success)


def test_public_get():
    response = requests.get(f"{BASE_URL}/teams")
    success = response.status_code == 200
    print_result("Rota pública GET", success)


print("\n🚀 Iniciando testes...\n")

if setup_auth():
    print_result("Autenticação JWT", True)
    team_id = test_create_team()
    test_list_teams()

    if team_id:
        test_create_participant(team_id)
        test_participants_by_team(team_id)

    test_invalid_team()
    test_list_participants()
    test_validation()
    test_login()
    test_protected_without_token()
    test_public_get()
else:
    print_result("Autenticação JWT", False)

print(f"\n🎯 Pontuação final: {score}/30\n")
