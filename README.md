# 📦 B3 Spreadsheet Reader

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

## 🌐 Descrição

O propósito principal desse projeto e calcular o preço médio de ativos, tendo como fonte de dados uma planilha (excell/xlsx) disponibilizada através do site da B3 [Área do investidor](https://www.investidor.b3.com.br/login)

Breve descrição do projeto, seu propósito e problema que resolve. Forneça um contexto claro sobre a motivação por trás do desenvolvimento.

## ✨ Principais Funcionalidades

- Agrupar movimentações: Agrupa por ativos as movimentações registradas categorizando-as
- Calcular preço médio: Depois de agrupado, calcular o preço medio do ativo
- Exibe informações: Imprime no console as informações calculadas
- Registros de Desdobrabendo: Em desenvolvimento
- Salvar com csv: Não implementado

## 🛠️ Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📦 Pré-requisitos

- Python (versão 3.12)

## 🚀 Instalação

1. Clone o repositório
```bash
git clone https://github.com/henriquemanduca/b3_spreadsheet_reader
```

2. Crie um ambinte virtual do python
```bash
python -m venv .venv
```

3. Instale as dependencias
```bash
pip install -r requirements.txt
```

4. Rode os testes (Opcional)
```bash
pytest -v
```

5. Inicie o projeto com parâmetros
```bash
python b3_shpeadsheet_reader.py --input sample.xlsx --tab Movimentação --output report.txt
```

## 🔧 Configuração

Sem mais configurações

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 📧 Contato

Henrique manduca - [Seu LinkedIn](https://linkedin.com/in/seunome)
Link do Projeto: [https://github.com/seu-usuario/nome-do-projeto](https://github.com/seu-usuario/nome-do-projeto)
