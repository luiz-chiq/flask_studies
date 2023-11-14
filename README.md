# Projeto Flask - Rede Social/Forum API

![Logo Flask](https://flask.palletsprojects.com/en/2.3.x/_images/flask-horizontal.png)

Este projeto consiste em uma ideia de API backend para uma rede social ou fórum desenvolvida em Flask, um micro-framework web leve e poderoso para Python.

Os comandos abaixo devem ser feitos na pasta backend

## Configuração do Ambiente Virtual

### Windows:

1. Abra o PowerShell no diretório do projeto
2. Crie um ambiente virtual com o comando:

    ```powershell
    python -m venv venv
    ```

3. Ative o ambiente virtual:

    ```powershell
    .\venv\Scripts\Activate
    ```

### Linux:

1. Abra um terminal no diretório do projeto
2. Crie um ambiente virtual com o comando:

    ```bash
    python3 -m venv venv
    ```

3. Ative o ambiente virtual:

    ```bash
    source venv/bin/activate
    ```

## Instalação das Dependências

Com o ambiente virtual ativo execute o comando:

```bash
pip install -r requirements.txt
```

## Inicialização do Projeto
Inicie o projeto usando o seguinte comando:

```bash
flask run
```

O servidor será iniciado e estará disponível em http://127.0.0.1:5000/
