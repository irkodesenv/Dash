from conexoes.services.firebird import Conexao
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Usuario():

    def __init__(self, usuario = None, senha = None):
        self.id_usuario = None
        self.usuario = usuario
        self.senha = senha
        self.email = None
        self.conexao = Conexao()


    def authenticate(self):       
        data = self.conexao.select("TABCADUSUARIOS") \
                            .values("CODIGO, NOME")\
                            .where(f"(UPPER(nomeACESSO) = '{self.usuario.upper()}' AND senha = '{self.senha}'")\
                            .execute()
        
        if data:
            User = get_user_model()        
            # Tenta obter ou criar o usuário
            user = User.objects.get_or_create(username=self.usuario)

            try:
                user.save()
            except Exception as e:
                user = user[0]
                user.save()

            return user

        return False