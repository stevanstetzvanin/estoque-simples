import mysql.connector    #Importa a biblioteca para conexao com o mysql

# MADE BY Stevan Stetz Vanin - UFSCar AUTOMAÇÃO INDUSTRIAL 2020
# DB_NAME = estoque ; TABLE = itens ; COLUMNS_NAME = ID, NOME, PRECO, QTD

def inserir(cursor, db_connection):
    nome = input(" Insira o nome do item a ser cadastrado: ")
    preco = input(" Insira o preço do item: ")
    qtd = input(" Insira a quantidade em estoque: ")
    sql = f"INSERT INTO itens (ID, NOME, PRECO, QTD) VALUES (null, '{nome}', {preco}, {qtd});"
    cursor.execute(sql)
    db_connection.commit()
    print(f" Item {nome} adicionado com sucesso.")

def atualizar(cursor, db_connection):
    consultar(cursor)
    id = input(" Digite o ID do item que deseja atualizar o estoque: ")
    qtd = input(" Digite a quantidade a ser adicionada [+] ou removida [-] : ")
    cursor.execute(f"SELECT QTD FROM itens WHERE ID={id}")
    estoque_atual = cursor.fetchall()
    sql = f"UPDATE itens SET QTD={estoque_atual[0][0]+int(qtd)} WHERE ID={id}"
    cursor.execute(sql)
    print(" Estoque atualizado com sucesso.")
    db_connection.commit()

def consultar(cursor):
    cursor.execute("SELECT * FROM itens")
    resultado = cursor.fetchall()
    print("\n   ITENS EM ESTOQUE")
    for linha in resultado:
        print(f"   ID: {linha[0]} Nome: {linha[1]} - Preço: R$ {linha[2]},00 - Quantidade: {linha[3]}")

def atualizarpreco(cursor, db_connection):
    consultar(cursor)
    id = input(" Digite o ID do item que deseja atualizar o preço: ")
    preco = input(" Digite o preço novo: ")
    sql = f"UPDATE itens SET PRECO={preco} WHERE ID={id}"
    cursor.execute(sql)
    print(" Preço atualizado com sucesso.")
    db_connection.commit()

def drop(cursor, db_connection):
    confirmar = input("\n Tem certeza que deseja apagar todos os dados? não será possível recuperá-los. Sim/Não : ")
    if confirmar.lower().strip() == "sim":
        cursor.execute("DELETE FROM itens")
        db_connection.commit()
        print(" Dados apagados com sucesso.")

def main(MY_HOST, MY_USER, MY_PASSWORD, MY_DATABASE):

    db_connection = mysql.connector.connect(host=MY_HOST, user=MY_USER, password=MY_PASSWORD, database=MY_DATABASE)
    cursor = db_connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS itens (ID INTEGER PRIMARY KEY AUTO_INCREMENT, NOME VARCHAR(20) NOT NULL, PRECO INTEGER NOT NULL, QTD INTEGER NOT NULL)")

    while True:
        opt = input("\n1 - Inserir item no banco de dados\n2 - Atualizar a quantidade de estoque de um item\n3 - Consultar todos os itens no banco de dados\n4 - Atualizar o preço de um item\n5 - Sair\n6 - Apagar TODOS os itens do estoque\n Selecione a opção que deseja: ")
        if opt == '1':
            inserir(cursor, db_connection)
        elif opt == '2':
            atualizar(cursor, db_connection)
        elif opt == '3':
            consultar(cursor)
        elif opt == '4':
            atualizarpreco(cursor, db_connection)
        elif opt == '5':
            break
        elif opt == '6':
            # drop(cursor, db_connection)
            print(" Opção desabilitada.")
        else:
            print("\n Opção inválida.")

    cursor.close()
    db_connection.close()

if __name__ == '__main__':
    main('localhost', 'root', None ,'estoque')
