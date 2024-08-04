# Importação de Módulos
import hashlib
import random
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QLineEdit,
    QPushButton,
    QMessageBox,
)


class GeradorDeSenha(QWidget):
    """Classe para gerar senhas."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Cria a interface da aplicação."""
        self.setWindowIcon(QIcon('/assets/Password.ico'))

        # Layout vertical
        layout = QVBoxLayout()

        # Campos de entrada
        self.nome_input = QLineEdit(self)
        self.nome_input.setPlaceholderText("Digite seu nome completo")
        layout.addWidget(self.nome_input)

        self.cpf_input = QLineEdit(self)
        self.cpf_input.setPlaceholderText("Digite seu CPF")
        layout.addWidget(self.cpf_input)

        # Spinner para seleção do número de caracteres
        self.tamanho_senha = QSpinBox(self)
        self.tamanho_senha.setMinimum(6)
        self.tamanho_senha.setMaximum(256)
        self.tamanho_senha.setValue(6)
        layout.addWidget(self.tamanho_senha)

        # Botão para gerar senha
        self.botao_gerar = QPushButton("Gerar Senha", self)
        self.botao_gerar.clicked.connect(self.gerar_senha)
        layout.addWidget(self.botao_gerar)

        # Label para mostrar a senha gerada
        self.senha_gerada = QLabel("Sua senha aparecerá aqui", self)
        self.senha_gerada.setWordWrap(True)
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
        """Gera uma senha baseada no nome e o CPF do usuário."""
        nome = self.nome_input.text()
        cpf = self.cpf_input.text()
        tamanho = self.tamanho_senha.value()
        senha = self.criar_senha(nome, cpf, tamanho)
        senha_formatada = self.formatar_senha(senha)
        self.senha_gerada.setText(f"Sua senha é:\n{senha_formatada}")

    def criar_senha(self, nome, cpf, tamanho):
        """Gera uma senha baseada no nome e o CPF do usuário."""
        entrada = nome + cpf
        hash_obj = hashlib.sha256(entrada.encode())
        hash_hex = hash_obj.hexdigest()
        senha = "".join(random.choices(hash_hex, k=tamanho))
        return senha

    def formatar_senha(self, senha):
        """Formata a senha para quebras de linha a cada 32 caracteres."""
        return "\n".join(senha[i:i+32] for i in range(0, len(senha), 32))

    def copiar_senha(self):
        """Copia a senha gerada para o clipboard."""
        senha = self.senha_gerada.text().replace(
            "Sua senha é:\n", "").replace("\n", "")
        QGuiApplication.clipboard().setText(senha)
        QMessageBox.information(self, "Senha Copiada",
                                "Senha copiada com sucesso.")


# Executa a aplicação
if __name__ == "__main__":
    app = QApplication([])
    ex = GeradorDeSenha()
    ex.show()
    app.exec()
