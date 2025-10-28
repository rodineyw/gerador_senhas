# Gerador de Senhas

![Criação de Senha com Python](https://github.com/rodineyw/gerador_senhas/blob/main/assets/gerador_senha.png)

## Descrição

Aplicação de geração de senhas com PyQt6 focada em segurança e simplicidade.

- Geração aleatória segura usando fonte criptográfica (`secrets`).
- Opções de caracteres: A–Z, a–z, 0–9 e símbolos; filtro para evitar caracteres ambíguos (Il1O0, etc.).
- Medidor de força com cálculo de entropia em bits.
- Exibir/ocultar senha e copiar para a área de transferência.

## Instalação

Para rodar este projeto, siga estes passos:

1. Clone este repositório:

   ```
   git clone https://github.com/rodineyw/gerador_senhas.git
   ```

2. Instale as dependências:

   ```
   pip install PyQt6
   ```

3. Execute o programa:

   ```
   python gerador.py
   ```

## Uso

- Escolha o tamanho da senha (recomendado: 12+). O mínimo agora é 8.
- Selecione os conjuntos de caracteres (A–Z, a–z, 0–9, símbolos) conforme sua necessidade.
- Ative “Evitar caracteres ambíguos” para remover caracteres como Il1O0.
- Clique em “Gerar Senha” e use “Mostrar/Ocultar” para visualizar a senha.
- Clique em “Copiar Senha” para enviar a senha gerada ao clipboard.

### Segurança

- Use comprimento maior e múltiplos conjuntos de caracteres para aumentar a entropia.

## Contribuições

Contribuições são sempre bem-vindas! Por favor, crie um fork do repositório e faça uma pull request com suas sugestões.

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](https://github.com/rodineyw/gerador_senhas/blob/main/LICENSE) para mais informações.
