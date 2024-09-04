# Dash Gerenciais
Sistema volta ao controle gerenciais

## Pré requisitos:
* Python 3
* Django
* ExecutionPolicy allSigned

## Habilitar execuções de Scripts no Shell (venv)
* Abrir Windowns power Shell
* Verificar se a execução de Scripts autorizada no Shell
* get-ExecutionPolicy
* Caso estiver Restricted
* Executar o comando "set-ExecutionPolicy AllSigned" em seguinda aperte a opção [S]

## Para iniciar o projeto:

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.


```
git clone https://github.com/irkodesenv/Dash.git
cd dash_financeiro
python -m venv .venv  ou  py -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
python manage.py runserver
```

## Links

[djangoproject.com](https://www.djangoproject.com/start/)
