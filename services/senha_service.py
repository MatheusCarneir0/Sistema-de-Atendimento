import json
import os
from models.senhas import Senha
from dados.fila_data import fila_prioritaria, fila_normal

class SenhaService:
    def __init__(self):
        self.caminho = 'dados/senhas.json'
        self._inicializar_arquivo()

    def _inicializar_arquivo(self):
        if not os.path.exists(self.caminho):
            with open(self.caminho, 'w') as f:
                json.dump({'emitidas': [], 'atendidas': []}, f)

    def _carregar_dados(self):
        with open(self.caminho, 'r') as f:
            return json.load(f)

    def _salvar_dados(self, dados):
        with open(self.caminho, 'w') as f:
            json.dump(dados, f, indent=4)

    def emitir_senha(self, cliente):
        senha = Senha(cliente, cliente.tipo)

        # Salvar no JSON
        dados = self._carregar_dados()
        dados['emitidas'].append(senha.to_dict())
        self._salvar_dados(dados)

        # Adicionar à fila correta
        if senha.tipo == 'P':
            fila_prioritaria.append(senha)
        else:
            fila_normal.append(senha)

        return senha

    def proxima_senha(self):
        if fila_prioritaria:
            return fila_prioritaria.popleft()
        elif fila_normal:
            return fila_normal.popleft()
        return None

    def registrar_atendimento(self, senha):
        dados = self._carregar_dados()

        senha.status = 'finalizado'
        dados['emitidas'] = [s for s in dados['emitidas'] if s['numero'] != senha.numero]
        dados['atendidas'].append(senha.to_dict())

        self._salvar_dados(dados)
