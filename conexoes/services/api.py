from typing import Optional
import requests


class Api:

    
    def __init__(self, url: Optional[str] = None, token: Optional[str] = None):
        self.url = url
        self.token = token
        

    def get(self):
        """
            Processa uma chamada à API utilizando a URL e token fornecidos.

            Args: 
                Url -> Obrigatório
                Token -> Livre

            Raises:
                ValueError: Se a URL da API não estiver definida.

            Exemplos de uso:
                api = Api(url = "XXXXXXX")
                api.get()

            Returns:
                obj: Um dicionário contendo os dados retornados pela API.
        """

        if not self.url:
            raise ValueError("URL da API não está definida.")
        
        # Realiza uma requisição GET para a API
        response = requests.get(self.url)

        if isinstance(response, requests.Response) and response.status_code == 200:
            data = response.json()
            return {'success': True, 'code': response.status_code, 'data': data}
        else:
            return {'error': True, 'code': response.status_code, 'data': 'Erro ao chamar API'}