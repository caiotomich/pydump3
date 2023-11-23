# pydump3

O pydump3 é uma ferramenta simples para automatizar o backup de bases de dados MySQL utilizando Python.

## Funcionalidades / Objetivo

- Faça backup de bancos de dados MySQL de forma rápida, eficiente e automatizada;
- Organize seus backups em diretórios estruturados por data e nomes do banco de dados e tabelas;
- Suporte para ignorar bancos de dados padrão do MySQL.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/caiotomich/pydump3.git
   cd pydump3
   ```

2. Crie e ative um ambiente virtual (opcional):
    ```
    python -m venv venv
    source venv/bin/activate   # No Windows: venv\Scripts\activate
    ```

3. Clone o repositório:
    ```
    pip install -r requirements.txt
    ```

## Uso
Execute o script main.py para realizar o backup dos bancos de dados MySQL:
```
python main.py
```

## Configuração
Configure as informações de conexão no script, incluindo host, usuário e senha do MySQL.
Personalize os diretórios de backup conforme necessário no script.

## Problemas e Sugestões
Encontrou um problema ou tem uma sugestão? Abra uma [issues](../../issues).

## Contribuindo
Sua contribuição é muito bem-vinda! Seja você um dev experiente ou não, todos serão bem vindos. Caso sinta em contribuir, peço que leia as [diretrizes de contribuição](CONTRIBUTING.md) e fique à vontade para envias suas ideias, correções ou novas funcionalidades.
