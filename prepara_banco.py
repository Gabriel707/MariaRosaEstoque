import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin123*'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Usuário ou senha incorretos')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `mariarosa`;")
cursor.execute("CREATE DATABASE `mariarosa`;")
cursor.execute("USE `mariarosa`;")

# Criação de tabelas
TABLES = {}
TABLES['Macaquinhos'] = ('''
    CREATE TABLE `macaquinhos` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `nome` varchar(50) NOT NULL,
    `cor` varchar(40) NOT NULL,
    `valor` decimal(10,2) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
    CREATE TABLE `usuarios` (
    `nome` varchar(20) NOT NULL,
    `nickname` varchar(15) NOT NULL,  # Aumentado para 15
    `senha` varchar(100) NOT NULL,
    PRIMARY KEY (`nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

# Inserção de usuários
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuario = [
    ("Gabriel Santana", "gsaraujo", generate_password_hash("admin123*").decode('utf-8')),
    ("Andre Santana", "andaraujo", generate_password_hash("lafayette33#").decode('utf-8')),
    ("Natalie Araujo", "nsaraujo", generate_password_hash("jadeGOD7@").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuario)

cursor.execute('SELECT * FROM usuarios')
print('**************  Usuários  **************')
for user in cursor.fetchall():
    print(user[1])

# Inserção de produtos (Macaquinhos)
macaquinhos_sql = 'INSERT INTO macaquinhos (nome, cor, valor) VALUES (%s, %s, %s)'
macaquinhos = [
    ('Macaquinho Raposa', 'Amarelo', 44.99),
    ('Macaquinho Bambi', "Cinza estampado", 44.99),
    ('Macaquinho Ursinho Polar', 'Azul Estampado', 44.99)
]
cursor.executemany(macaquinhos_sql, macaquinhos)

cursor.execute('SELECT * FROM macaquinhos')
print('----------------- Macaquinhos: -----------------')
for macaquinho in cursor.fetchall():
    print(macaquinho[1])

# Aplicar as alterações ao banco de dados
conn.commit()

cursor.close()
conn.close()
