import sqlite3 # Importação do banco de dados

conn = sqlite3.connect("passwords.db") # Acessando o BD

cursor = conn.cursor() # Salvando a conexão

# Criação da tabela admin (para administrar o sistema)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin(
        login TEXT NOT NULL,
        senha TEXT NOT NULL
    )
''')

# Criação da tabela users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

def menu():                                                 # Função para apresentação do menu
    print("==================================================")
    print("| i : inserir uma nova senha                     |")
    print("| l : listar serviços salvos                     |")
    print("| r : recuperar senha                            |")
    print("| m : modificar sua senha de administrador       |")
    print("| c : cadastrar um novo acesso de administrador  |")
    print("| s : sair                                       |")
    print("==================================================")

def cadSenhaAdm(login, senha):                              # Função para cadastrar admin
    cursor.execute(f'''
        INSERT INTO admin (login, senha)
        VALUES ('{login}', '{senha}')
    ''')
    conn.commit()

def updateSenhaAdm(login, senha):                           # Função para atualizar o admin 
    cursor.execute(f'''
        UPDATE admin SET 
        login = '{login}',
        senha = '{senha}'
    ''')
    conn.commit()

def get_password(service):                                  # Função para pegar a senha
    cursor.execute(f'''
        SELECT username, password 
        FROM users
        WHERE service = '{service}' 
    ''')
    if cursor.rowcount == 0:
        print("Serviço não cadastrado (Use 'l' para consultar os serviços).")
    else:
        for user in cursor.fetchall():
            print(user)

def insert_password(service, username, password):           # Função para salvar um anova senha
    cursor.execute(f'''
        INSERT INTO users (service, username, password)
        VALUES ('{service}', '{username}', '{password}')
    ''')
    conn.commit()

def show_services():                                        # Função para mostrar todos cadastros
    cursor.execute('''
        SELECT service, password FROM users;
    ''')

    for service in cursor.fetchall():
        print(service)

def main():
    print("\nJá tem um cadastro? ")
    a = input("(S/n) >>> ")

    if (a.upper() not in ['S', 'N']):
        print("Opção invalida! Tente novamente.")
        print("Encerrando ...")
        exit()

    if (a.upper() == 'N'):
        try:
            login = input('Digite o login de acesso adm: ')
            senha = input('Digite sua senha de acesso adm: ')
            
            cursor.execute('SELECT * from admin WHERE login="%s" AND senha="%s"' % (login, senha))

            if cursor.fetchone() is not None:
                print ("ADM já cadastrado! \n")
                a = 'S'
            else:
                cadSenhaAdm(login, senha)
                print("Novo ADM cadastrado com sucesso.")
                a = 'S'
        except:
            print("Ops! Algo de errado não está certo.")
            print("Reinicie o programa e tente novamente.")

    if (a.upper() == 'S'):         
        login = input("Login: ")
        senha = input("senha: ")

        cursor.execute('SELECT * from admin WHERE login="%s" AND senha="%s"' % (login, senha))
             
        if cursor.fetchone() is not None:
            print ("\nSeja Bem Vindo " + login)
        else:
            print ("\nAcesso Inválido! Encerrando...")
            exit()
        
        while True: 
            menu()

            op = input("\nO que deseja fazer? ")
            op = op.lower()

            if op not in ['l', 'i', 'r', 'm', 'c', 's']:
                print("Ops!!!")
                print("Opção ivalida. Tente novamente!")
                continue
            
            if op == 's':
                print("Fechando...")
                exit()

            if op == 'm':
                login = input('Digite seu novo login de acesso: ')
                senha = input('Digite sua nova senha de acesso: ')
                cSenha = input('Confirme a senha digitada acima: ')
                if cSenha != senha:
                    print('As duas senhas não conferem, tente novamente.')
                    menu()
                else:
                    updateSenhaAdm(login, senha)
                print("")

            if op == 'c':
                login = input('Digite o login de acesso desse adm: ')
                senha = input('Digite sua nova senha de acesso: ')
                cadSenhaAdm(login, senha)
                print("")

            if op == 'i':
                service = input('Qual o nome do serviço? ')
                username = input('Qual o nome de usuário? ')
                password = input('Qual a senha? ')
                insert_password(service, username, password)
                print("")

            if op == 'l':
                show_services()
                print("")
            
            if op == 'r':
                service = input("Qual o serviço para quer a senha? ")
                get_password(service)
                print("")

main()

conn.close() # Encerrando a conexão com BD