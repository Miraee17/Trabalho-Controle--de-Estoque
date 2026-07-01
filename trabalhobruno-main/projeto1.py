import database as db
from projeto2 import menu_fornecedores

def exibir_menu_principal():
    print("\n" + "="*30)
    print("      SISTEMA DE GESTÃO")
    print("="*30)
    print("1. Gerenciar Fornecedores")
    print("2. Gerenciar Compras")
    print("3. Relatórios e Pesquisas")
    print("0. Sair")
    print("="*30)


exibir_menu_principal() 
funcao1 = input("Escolha uma opção: ")
if funcao1 == '1':
    print("Acessando o menu de fornecedores...")
    menu_fornecedores()
elif funcao1 == '2':    
    print("Funcionalidade de Compras em desenvolvimento...")
elif funcao1 == '3':
    print("Funcionalidade de Relatórios em desenvolvimento...") 


def menu_fornecedores():
    while True:
        print("\n--- GERENCIAR FORNECEDORES ---")
        print("1. Cadastrar Fornecedor")
        print("2. Listar Fornecedores")
        print("3. Atualizar Fornecedor")
        print("4. Excluir Fornecedor")
        print("5. Buscar por CPF/CNPJ")
        print("0. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            nome = input("Nome: ")
            documento = input("CPF/CNPJ: ")
            contato = input("Telefone: ")
            db.Database.inserir_fornecedor(nome, documento, contato)
            print("\n[OK] Fornecedor cadastrado com sucesso!")
        elif opcao == '2':
            fornecedores = db.listar_fornecedores()
            if fornecedores:
                print("\n--- LISTA DE FORNECEDORES ---")
                for f in fornecedores:
                    print(f"ID: {f[0]} | Nome: {f[1]} | Documento: {f[2]} | Contato: {f[3]}")
            else:
                print("\n[INFO] Nenhum fornecedor encontrado.")
        
        elif opcao == "3":
            id_forn = input("Digite o Nome do fornecedor que deseja atualizar: ")
            novo_nome = input("Novo Nome: ")
            novo_doc = input("Novo CPF/CNPJ: ")
            novo_contato = input("Novo Contato: ")
            db.Database.atualizar_fornecedor(id_forn, novo_nome, novo_doc, novo_contato)
            print("Fornecedor atualizado!")
                
        elif opcao == '4':
            excluir = input("digite o Nome do fornecedor que deseja excluir: ")
            db.database.excluir_fornecedor(nome)
            print("Fornecedor excluido com sucesso!")
             

 
        elif opcao == '0':
            voltar= input(" digite a opçao:  ")

            print("Voltando ao menu principal...")
            break
        

       

        
 
      