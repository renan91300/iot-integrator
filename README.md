# Como inicializar o projeto:

    1 - Instale o MongoDB 3.4 ou superior. Recomendo a versão 5.0
    2 - Crie um ambiente virtual. Recomendo o venv ou o miniconda.
    3 - Instale as dependências do projeto utilizando o comando "pip install -r requirements.txt"
    4 - Para a criação do banco de dados e a população inicial das tabelas, execute os comandos:
        python -m manage migrate        
        python -m manage loaddata 001_initial_seed
    5 - Agora as tabelas já terão dados iniciais para teste. Um superusuário com as seguintes credenciais foi criado:
        - email: "superuser@cibele.com"
        - password: "#superuser9130"

        Com esse usuário você poderá logar no sistema e criar outros usuários


# Como executar o worker do celery para escutar o tópico de logs:

 - No windows
    ```bash
        python -m celery -A cibele worker --pool=solo -l info
    ```
 - No linux
    ```bash
        python -m celery -A cibele worker -l info
    ```
