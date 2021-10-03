import math
import random
import string

# Implementação da Cifra de César
def cipher_ceaser(msg):

    encrypted_msg = ''
    # Recebendo valor da chave
    print('Digite o valor da chave : (2-126)')
    k = int(input())
    n = 126
    
    # Encriptando mensagem com a cifra de César
    for letter in msg:
        value = (ord(letter)+k)%(n)
        encrypted_msg += chr(value)
    
    # Saída
    print('\nCIFRA DE CÉSAR\n\
        \nk :', k,'\
        \nMensagem Original :', msg,'\
        \nMensagem Criptografada: \n',
        encrypted_msg,'\n')

# Implementação da Cifra de Transposição Colunar
def cipher_columnar_transpositon(msg):
    
    # Removendo espaços da mensagem
    msg = msg.replace(' ', '')    
    encrypted_msg = '' 

    print('Digite a palavra chave:')
    keyword = input()

    # Separando a mensagem em uma Matriz  
    lenght = len(keyword)
    col = lenght
    row = math.ceil(len(msg)/lenght)
    matrix = [[0] * col for _ in range(row)]
    row = 0
    col = 0
    for letter in msg:

        matrix [row][col] = letter
        col += 1   
        if (col >= lenght) :
            row += 1
            col = 0

    while col < (lenght) :
        matrix [row][col] = random.choice(string.ascii_letters)
        col += 1

    # Descobrindo ordem
    order = []
    keyword_order = sorted(keyword)

    for letter in keyword :
        order.append(keyword_order.index(letter))

    
    # Encriptando mensagem com a Cifra de Transposição Colunar   
    for x in range(lenght):
        
        i = order.index(x)

        for j in range(len(matrix)):
            encrypted_msg += matrix[j][i]
            
    # Saída
    print('\nCIFRA DE TRANSPOSIÇÃO COLUNAR\n')
    print('Palavra-chave: ', keyword)
    print('Mensagem Original: ', msg)
    print('Matriz :')
    
    for i in range(len(matrix)):
        print(matrix[i],',')    

    print('\nMensagem Criptografada :\n',encrypted_msg, '\n')

# Implementação da Cifra de Vigenere
def cipher_vigenere(msg):
    
    encrypted_msg = '' 
    vigenere_degree = [[0] * 26 for _ in range(26)]
    ref = {}
    inv_ref = {}

    # Auxiliadores para criar a tabela
    for x in range(26):
        value = ord('A') + x
        ref[chr(value)] = x
        inv_ref[x] = chr(value)

    # Criando a Tabela de Vigenere    
    for i in range(26):
        for j in range(26):
            index = (j+i) % 26
            vigenere_degree[i][j] = inv_ref[index]
    
    # Recevendo valor da chave
    print('Digite a palavra chave com  até ', len(msg), ' letras: ')
    keyword = input()

    # Deixando mensagem com letras maiusculas
    if not msg.isupper():
	    msg = msg.upper()
    # Removendo espaços da mensagem
    msg = msg.replace(' ', '')
    
    # Deixando chave com letras maiusculas
    if not keyword.isupper():
	    keyword = keyword.upper()
    
    # Removendo espaços da mensagem
    keyword = keyword.replace(' ', '')

    # Duplicando a palavra chave para ter o mesmo tamanho que a mensagem
    lst_letter = 0
    while len(keyword) < len(msg) :
        keyword += keyword[lst_letter]
        lst_letter += 1

    # Encriptando mensagem com a Cifra de Transposição Vigenere   
    for i in range(len(msg)):      
        encrypted_msg += vigenere_degree[ref[msg[i]]][ref[keyword[i]]] 

    # Saída
    print('\nCIFRA DE VINEGENERE\n')
    print('Palavra-chave: ', keyword)
    print('Mensagem Original: ', msg)
    print('\nMensagem Criptografada :\n',encrypted_msg, '\n')

def cipher_playfair(msg):

    print('Digite a palavra chave:')
    keyword = input()

    # Deixando mensagem com letras maiusculas e sem espaços
    if not msg.isupper():
	    msg = msg.upper()
    msg = msg.replace(' ', '')    
    
    # Deixando chave com letras maiusculas e sem repetições
    if not keyword.isupper():
	    keyword = keyword.upper()
    clean = ''
    dict_keyword = {}
    for i in range(len(keyword)):    
        if not keyword[i] in dict_keyword:
            dict_keyword[keyword[i]] = i
            clean += keyword[i]
    keyword = clean

    # Criando matriz com a palavra chave
    matrix = [[''] * 5 for _ in range(5)]
    dict = {}
    index = 0

    # Inserindo palavra chave na matriz
    for i in range(5):
        for j in range(5):
            if index < len(keyword):
                matrix[i][j] = keyword[index]
                dict[keyword[index]] = 1
                dict_keyword[keyword[index]] = (i, j)
                index +=1 
            else :
                break

    # Inserindo outras letras do alfabeto na matriz
    j = index%5
    i = math.floor(index/5)
    letter = 'A'
    while i < 5:
        while j < 5 :
            while letter in dict or letter == 'J':
                letter = chr(ord(letter)+1)
            dict[letter] = 1
            matrix[i][j] = letter
            dict_keyword[letter] = (i, j)
            j += 1
        j = 0
        i += 1


    # Encriptando mensagem com a Cifra de Playfair
    encrypted_msg = ''
    x = 0
    while x < len(msg):
        pair = ''
        pair += msg[x]
        if x == (len(msg)-1) or pair == msg[x+1] :
            pair += 'X'
        else:
            pair += msg[x+1]
            x +=1
        
        encrypted_msg += take_pair(pair, matrix, dict_keyword)
        x += 1
        
    
    # Saída
    print('\nCIFRA DE PLAYFAIR\n')
    print('Palavra-chave: ', keyword)
    print('Mensagem Original: ', msg)
    print('Matriz :')
    for i in range(len(matrix)):
        print(matrix[i],',')    
    print('\nMensagem Criptografada :\n',encrypted_msg, '\n')

# Função auxiliar para a Cifra de Playfair
def take_pair(pair, matrix, dict_matrix):
    
    out = ''
    st_pos = dict_matrix[pair[0]]
    nd_pos = dict_matrix[pair[1]]
    
    # Caso os dois valores estejam na mesma linha
    if st_pos[0] == nd_pos[0]:
        out += matrix[st_pos[0]][(st_pos[1]+1)%5]
        out += matrix[nd_pos[0]][(nd_pos[1]+1)%5]
    
    # Caso os dois valores estejam na mesma coluna
    elif st_pos[1] == nd_pos[1]:
        out += matrix[(st_pos[0]+1)%5][st_pos[1]]
        out += matrix[(nd_pos[0]+1)%5][nd_pos[1]]
    # Caso normal
    else :
        out += matrix[st_pos[0]][nd_pos[1]]
        out += matrix[nd_pos[0]][st_pos[1]]
        
    return out


def print_menu():
    print('\
        Escolha uma das opções:\n\n\
        1- Escrever Mensagem:\n\
        2- Criptografia da Cifra de César:\n\
        3- Criptografia de Tranposição Colunar:\n\
        4- Criptografia da Cifra de Vigernere:\n\
        5- Criptografia da Cifra de Playfair:\n\
        6- Finalizar programa\n')

msg = ''
while(1)  :

    print_menu()
    choice = input()
    
    if choice == '1':             
        print('Digite a mensagem a ser criptografada:')
        msg = input()

    elif choice == '2':
        print(msg)
        cipher_ceaser(msg)
    
    elif choice == '3':
        cipher_columnar_transpositon(msg)
    
    elif choice == '4':
        cipher_vigenere(msg)
    
    elif choice == '5':
        cipher_playfair(msg)

    else :
        break



