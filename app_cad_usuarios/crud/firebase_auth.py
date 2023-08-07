import firebase_admin

from firebase_admin import credentials, firestore

class AuthUsuarios:
    def __init__(self) -> None:
        self.__dir_credencial = 'app_cad_usuarios\crud\credencial.json'
        self.__firebase = self.configura_credenciais()
        self.criar_colecao('admin')
        self.criar_colecao('geral')

    def configura_credenciais(self):
        """cria a conexao de autenticação"""
        try:
            cred = credentials.Certificate(self.__dir_credencial)
            firebase_admin.initialize_app(credential=cred)
            return firestore.client()
        
        except Exception as e:
            print("Erro ao configurar a autenticação", str(e))

    def criar_colecao(self, tipo: str):
        colecao = self.__firebase.collection('usuarios')
        documento_admin = colecao.document(tipo)
        documento_admin.set({})
        documento_admin.collection('id')

    def select_dados(self, email_usuario: str = None, tipo_acesso: str = None):
        """Retorna os dados dentro da coleção"""
        try:
            colecao = self.__firebase.collection('usuarios')

            if tipo_acesso:
                colecao = colecao.document(tipo_acesso).collection('id')

            docs = colecao.get()

            if email_usuario is not None and tipo_acesso is None:
                for doc in docs:
                    for user_doc in doc.reference.collection('id').get():
                        data = user_doc.to_dict()
                        if data.get('email') == email_usuario:
                            return {'id': user_doc.id, 'tipo_acesso': doc.reference.path.split('/')[1], **data}
                return {}
            elif email_usuario is None and tipo_acesso is not None:
                all_users_data = {}
                for doc in docs:
                    data = doc.to_dict()
                    all_users_data[doc.id] = {'tipo_acesso': tipo_acesso, **data}
                return all_users_data
            elif (email_usuario is not None) and (tipo_acesso is not None):
                for doc in docs:
                    data = doc.to_dict()
                    if data.get('email') == email_usuario:
                        return {'id': user_doc.id, 'tipo_acesso': tipo_acesso, **data}
                return all_users_data
            else:
                all_users_data = {}
                for doc in docs:
                    for user_doc in doc.reference.collection('id').get():
                        data = user_doc.to_dict()
                        all_users_data[user_doc.id] = {'tipo_acesso': doc.reference.path.split('/')[1], **data}
                return all_users_data

        except Exception as error:
            raise ValueError(error)


    def inserir_novo_usuario(self, dados: dict, tipo_usuario: str = 'geral'):
        """inseri um novo usuário na base de dados do Firebase"""
        try:
            colecao = self.__firebase.collection('usuarios')\
                                     .document(tipo_usuario)\
                                     .collection('id')
            
            id_do_usuario = colecao.add({**dados})
        except Exception as erro:
            raise ValueError(erro)
    
    def editar_usuario(self, tipo_usuario: str, id_do_usuario: str, novos_dados: dict):
        """Edita os dados de um usuário na base de dados do Firebase"""
        try:
            colecao = self.__firebase.collection('usuarios')\
                                    .document(tipo_usuario)\
                                    .collection('id')\
                                    .document(id_do_usuario)
            
            colecao.update(novos_dados)
        except Exception as erro:
            raise ValueError(erro)
    
    def deletar_usuario(self, tipo_usuario: str, id_do_usuario: str):
        """Deleta um usuário na base de dados do Firebase"""
        try:
            colecao = self.__firebase.collection('usuarios')\
                                    .document(tipo_usuario)\
                                    .collection('id')\
                                    .document(id_do_usuario)
            
            colecao.delete()
        except Exception as erro:
            raise ValueError(erro)

# if __name__ == '__main__':
    # auth = AuthUsuarios()
#     # auth.select_dados()

#     # inserir novo usuario
#     # novo_usuario = {
#     #     'nome': 'Geovanne',
#     #     'senha': '123',
#     #     'avatar_url': 'http//teste',
#     #     'email': 'Geovanne@gmail.com'
#     # }
#     # auth.inserir_novo_usuario(dados=novo_usuario, tipo_usuario='admin')

#     # #Testar auth
#     # # usr = auth.select_dados(nome_usuario='luiz.eduardo', tipo_acesso='geral')
    # usr = auth.select_dados()#nome_usuario="luiz.eduardo", 
    # print(usr)