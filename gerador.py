"""Módulos de importação"""

import hashlib
import random
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtGui import QGuiApplication


class GeradorDeSenha(QWidget):
    """Classe para gerar senhas."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Cria a interface da aplicação."""
        # Layout vertical
        layout = QVBoxLayout()

        # Campos de entrada
        self.nome_input = QLineEdit(self)
        self.nome_input.setPlaceholderText("Digite seu nome completo")
        layout.addWidget(self.nome_input)

        self.cpf_input = QLineEdit(self)
        self.cpf_input.setPlaceholderText("Digite seu CPF")
        layout.addWidget(self.cpf_input)

        # Botão para gerar senha
        self.botao_gerar = QPushButton("Gerar Senha", self)
        self.botao_gerar.clicked.connect(self.gerar_senha)
        layout.addWidget(self.botao_gerar)

        # Label para mostrar a senha gerada
        self.senha_gerada = QLabel("Sua senha aparecerá aqui", self)
        layout.addWidget(self.senha_gerada)

        # Botão para copiar a senha
        self.botao_copiar = QPushButton("Copiar Senha", self)
        self.botao_copiar.clicked.connect(self.copiar_senha)
        layout.addWidget(self.botao_copiar)

        # Configurações da janela
        self.setLayout(layout)
        self.setWindowTitle("Gerador de Senhas")
        self.setGeometry(300, 300, 300, 200)

    def gerar_senha(self):
        """Gera uma senha baseada no nome e o CPF do usuário."""
        nome = self.nome_input.text()
        cpf = self.cpf_input.text()
        senha = self.criar_senha(nome, cpf)
        self.senha_gerada.setText(f"Sua senha é: {senha}")

    def criar_senha(self, nome, cpf):
        """Gera uma senha baseada no nome e o CPF do usuário."""
        entrada = nome + cpf
        hash_obj = hashlib.sha256(entrada.encode())
        hash_hex = hash_obj.hexdigest()
        senha = "".join(random.choices(hash_hex, k=6))
        return senha

    def copiar_senha(self):
        """Copia a senha gerada para a ação de copiar para o clipboard."""
        senha = self.senha_gerada.text().replace("Sua senha é: ", "")
        QGuiApplication.clipboard().setText(senha)
        QMessageBox.information(self, "Senha Copiada", "Senha copiada com sucesso.")


# Executa a aplicação
if __name__ == "__main__":
    app = QApplication([])
    ex = GeradorDeSenha()
    ex.show()
    app.exec()
