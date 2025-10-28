# Importação de Módulos
from pathlib import Path
import hashlib
import secrets
import string
import math
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QSpinBox,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QCheckBox,
    QProgressBar,
)


class GeradorDeSenha(QWidget):
    """Classe para gerar senhas."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Cria a interface da aplicação."""
        icon_path = Path(__file__).resolve().parent / "assets" / "Password.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # Layouts
        layout = QVBoxLayout()
        form = QFormLayout()

        # Campos de entrada removidos (Nome e CPF) — geração sempre aleatória

        # Spinner para seleção do número de caracteres
        self.tamanho_senha = QSpinBox(self)
        self.tamanho_senha.setMinimum(8)
        self.tamanho_senha.setMaximum(256)
        self.tamanho_senha.setValue(12)
        form.addRow("Tamanho:", self.tamanho_senha)

        # Opções de caracteres
        self.chk_upper = QCheckBox("A–Z")
        self.chk_upper.setChecked(True)
        self.chk_lower = QCheckBox("a–z")
        self.chk_lower.setChecked(True)
        self.chk_digits = QCheckBox("0–9")
        self.chk_digits.setChecked(True)
        self.chk_symbols = QCheckBox("!@#$…")
        self.chk_symbols.setChecked(True)
        opts_row = QHBoxLayout()
        opts_row.addWidget(self.chk_upper)
        opts_row.addWidget(self.chk_lower)
        opts_row.addWidget(self.chk_digits)
        opts_row.addWidget(self.chk_symbols)
        char_opts = QWidget()
        char_opts.setLayout(opts_row)
        form.addRow("Caracteres:", char_opts)

        self.chk_ambiguous = QCheckBox("Evitar caracteres ambíguos (Il1O0 …)")
        self.chk_ambiguous.setChecked(True)
        form.addRow("Filtro:", self.chk_ambiguous)

        # Modo derivado removido por solicitação: sempre aleatório seguro

        layout.addLayout(form)

        # Saída da senha com alternar visibilidade
        out_row = QHBoxLayout()
        self.senha_saida = QLineEdit(self)
        self.senha_saida.setReadOnly(True)
        self.senha_saida.setPlaceholderText("Sua senha aparecerá aqui")
        self.senha_saida.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_toggle = QPushButton("Mostrar")
        self.btn_toggle.setCheckable(True)
        self.btn_toggle.toggled.connect(self._toggle_visibility)
        out_row.addWidget(self.senha_saida)
        out_row.addWidget(self.btn_toggle)
        layout.addLayout(out_row)

        # Medidor de força
        self.strength_label = QLabel("Força: —")
        self.strength_bar = QProgressBar(self)
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        layout.addWidget(self.strength_label)
        layout.addWidget(self.strength_bar)

        # Botões de ação
        actions = QHBoxLayout()
        self.botao_gerar = QPushButton("Gerar Senha", self)
        self.botao_gerar.clicked.connect(self.gerar_senha)
        self.botao_copiar = QPushButton("Copiar Senha", self)
        self.botao_copiar.clicked.connect(self.copiar_senha)
        actions.addWidget(self.botao_gerar)
        actions.addWidget(self.botao_copiar)
        layout.addLayout(actions)

        # Configurações da janela
        self.setLayout(layout)
        self.setWindowTitle("Gerador de Senhas")
        self.setGeometry(300, 300, 520, 260)

        # Estilo básico
        self.setStyleSheet(
            """
            QWidget { font-size: 12px; }
            QLineEdit[readOnly="true"] { background: palette(Base); color: palette(Text); }
            QProgressBar { height: 12px; }
            """
        )

        # Atualiza força ao mudar opções
        self.tamanho_senha.valueChanged.connect(self._update_strength)
        self.chk_upper.toggled.connect(self._update_strength)
        self.chk_lower.toggled.connect(self._update_strength)
        self.chk_digits.toggled.connect(self._update_strength)
        self.chk_symbols.toggled.connect(self._update_strength)
        self.chk_ambiguous.toggled.connect(self._update_strength)
        self._update_strength()

    def gerar_senha(self):
        """Gera uma senha segura aleatória ou derivada (menos seguro)."""
        length = self.tamanho_senha.value()
        alphabet, groups = self._build_alphabet()

        if len(alphabet) == 0:
            QMessageBox.warning(self, "Configuração inválida", "Selecione pelo menos um conjunto de caracteres.")
            return
        if length < max(8, len(groups)):
            QMessageBox.warning(self, "Tamanho insuficiente", f"Aumente o tamanho para pelo menos {max(8, len(groups))}.")
            return

        pwd = self._random_password(length, alphabet, groups)

        self.senha_saida.setText(pwd)
        self._update_strength()

    def _build_alphabet(self):
        """Monta o alfabeto e grupos selecionados com opção de remover ambíguos."""
        groups = []
        if self.chk_upper.isChecked():
            groups.append(list(string.ascii_uppercase))
        if self.chk_lower.isChecked():
            groups.append(list(string.ascii_lowercase))
        if self.chk_digits.isChecked():
            groups.append(list(string.digits))
        if self.chk_symbols.isChecked():
            groups.append([c for c in string.punctuation])

        alphabet = [c for g in groups for c in g]
        if self.chk_ambiguous.isChecked():
            ambiguous = set("Il1O0`'\"|\\/.,:; ")
            alphabet = [c for c in alphabet if c not in ambiguous]
            groups = [[c for c in g if c not in ambiguous] for g in groups]
            groups = [g for g in groups if len(g) > 0]

        return alphabet, groups

    def _random_password(self, length, alphabet, groups):
        """Gera senha aleatória garantindo ao menos um de cada grupo."""
        rng = secrets.SystemRandom()
        pwd_chars = [rng.choice(g) for g in groups]
        pwd_chars += [rng.choice(alphabet) for _ in range(length - len(pwd_chars))]
        rng.shuffle(pwd_chars)
        return "".join(pwd_chars)

    # Modo de derivação removido

    def _toggle_visibility(self, checked: bool):
        self.senha_saida.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password)
        self.btn_toggle.setText("Ocultar" if checked else "Mostrar")

    def _update_strength(self):
        alphabet, _ = self._build_alphabet()
        length = self.tamanho_senha.value()
        base = max(1, len(alphabet))
        bits = length * math.log2(base)
        percent = int(min(100, (bits / 128) * 100))
        self.strength_bar.setValue(percent)
        label = self._strength_label(bits)
        self.strength_label.setText(f"Força: {label} ({bits:.1f} bits)")

    def _strength_label(self, bits: float) -> str:
        if bits < 28:
            return "Fraca"
        if bits < 36:
            return "Aceitável"
        if bits < 60:
            return "Forte"
        return "Muito forte"

    def copiar_senha(self):
        """Copia a senha gerada para o clipboard."""
        senha = self.senha_saida.text().strip()
        if not senha:
            QMessageBox.information(self, "Nada para copiar", "Gere uma senha primeiro.")
            return
        QGuiApplication.clipboard().setText(senha)
        QMessageBox.information(self, "Senha Copiada", "Senha copiada com sucesso.")


# Executa a aplicação
if __name__ == "__main__":
    app = QApplication([])
    ex = GeradorDeSenha()
    ex.show()
    app.exec()
