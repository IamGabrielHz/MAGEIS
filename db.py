import psycopg2
import random



class investimentos:
    def __init__(self,ativo,quantidade, valor_unit, taxa_corretagem, tipo_transacao, valor_operacao=0.0,  b3=0.0, valor_total=0.0, preco_medio = 0, resultado = None, total_lc = 0):
        self.__codigo  = criar_cod()
        self.__ativo = ativo
        self.__quantidade = quantidade
        self.__valor_unit = valor_unit
        self.__taxa_corretagem = taxa_corretagem
        self.__tipo_transacao = tipo_transacao
        self.__b3 = b3
        self.__valor_operacao = valor_operacao
        self.__valor_total = valor_total
        self.__preco_medio = preco_medio
        self.__resultado = resultado
        self.__total_lc = total_lc



    @property
    def codigo(self):
        return self.__codigo
    @property
    def ativo(self):
        return self.__ativo
    @property
    def quantidade(self):
        return self.__quantidade
    @property
    def valor_unit(self):
        return self.__valor_unit
    @property
    def taxa_corretagem(self):
        return self.__taxa_corretagem
    @property
    def tipo_transacao(self):
        return self.__tipo_transacao
    @property
    def b3(self):
        return self.__b3
    @property
    def valor_operacao(self):
        return self.__valor_operacao
    @property
    def valor_total(self):
        return self.__valor_total
    @property
    def preco_medio(self):
        return self.__preco_medio
    @property
    def total_lc(self):
        return self.__total_lc
    


    def calc(self):
        self.__valor_operacao = self.__valor_unit * self.__quantidade
        self.__b3 = self.__valor_operacao * 0.03 / 100
        self.__valor_total = self.__valor_operacao + self.__taxa_corretagem + self.__b3


    
    
    def salvarDados(self):
        conn = psycopg2.connect(database="yynfswhx", 
                                user="yynfswhx", 
                                password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X", 
                                host="silly.db.elephantsql.com", 
                                port="5432")
        
        cur = conn.cursor()
        cur.execute("INSERT INTO investimentos VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)", (self.__codigo,self.ativo,self.__quantidade, self.__valor_unit, self.__taxa_corretagem, self.__tipo_transacao, self.__valor_operacao,  self.__b3, self.__valor_total, 0.0, self.__resultado, 0.0))
        conn.commit()
        cur.close()
        conn.close()
        


    def atualizarDados(self):     
        conn = psycopg2.connect(database="yynfswhx", 
                                user="yynfswhx", 
                                password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X", 
                                host="silly.db.elephantsql.com", 
                                port="5432")

        cur = conn.cursor()

        cur.execute('UPDATE investimentos SET quantidade = %s, valor_unit = %s, taxa_corretagem = %s, tipo_transacao = %s, valor_operacao = %s, b3 = %s, valor_total = %s, preco_medio = %s, resultado = %s, total_lc = %s WHERE codigo = %s', 
                    (self.__quantidade, self.__valor_unit, self.__taxa_corretagem, self.__tipo_transacao, self.__valor_operacao, self.__b3, self.__valor_total, self.__preco_medio, self.__resultado,self.__total_lc, self.__codigo))
        conn.commit()
        cur.close()
        conn.close()



    def precoMedio(self):
        conn = psycopg2.connect(database="yynfswhx", 
                                user="yynfswhx", 
                                password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X", 
                                host="silly.db.elephantsql.com", 
                                port="5432")

        cur = conn.cursor()
        preco_medio = self.valor_total / self.quantidade
        cur.execute("UPDATE investimentos SET preco_medio = %s WHERE codigo = %s", (preco_medio, self.__codigo))
        conn.commit()
        conn.close()    
        cur.close()



    def lucro_prejuizo(self):
        conn = psycopg2.connect(database="yynfswhx", 
                                user="yynfswhx", 
                                password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X", 
                                host="silly.db.elephantsql.com", 
                                port="5432")
        cur = conn.cursor()
        l_c = (self.__valor_unit - self.__preco_medio) * self.quantidade
        if l_c > 0: 
            rest = 'LUCRO'
        else:
            rest = 'PREJUIZO'
        
        cur.execute('UPDATE investimentos SET resultado = %s, total_lc = %s WHERE codigo = %s', (rest,l_c,self.__codigo))
        conn.commit()
        conn.close()
        cur.close()



def lc_ativo():
    conn = psycopg2.connect(database="yynfswhx", 
                                user="yynfswhx", 
                                password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X", 
                                host="silly.db.elephantsql.com", 
                                port="5432")
    cur = conn.cursor()
    ativo = input('Insira o nome do ativo: ')
    cur.execute('SELECT total_lc FROM investimentos WHERE ativo = %s', (ativo))
    conn.commit()
    res = cur.fetchall()
    for row in res:
        print(row)
    conn.close()
    cur.close()



def lc_carteira():
    conn = psycopg2.connect(database="yynfswhx", 
                                user="yynfswhx", 
                                password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X", 
                                host="silly.db.elephantsql.com", 
                                port="5432")
    cur = conn.cursor()
    cur.execute('SELECT SUM(total_lc) as total_lucro FROM investimentos')
    conn.commit()
    res = cur.fetchall()
    print(res)
    conn.close()
    cur.close()



def criar_cod():
    cod = ''.join(random.choices('0123456789', k=5))
    return cod



def detalhamento():
    conn = psycopg2.connect(database="yynfswhx", 
                            user="yynfswhx", 
                            password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X", 
                            host="silly.db.elephantsql.com", 
                            port="5432")   
    cur = conn.cursor()
    ativo = input('Insira o ativo da transação: ').upper()
    cur.execute("select * from investimentos where ativo = %s", (ativo,))
    res = cur.fetchall()
    for row in res:
        print(row)



def cadastrar_dados():
    ativo = input('Insira o nome do ativo: ').upper()
    quantidade = int(input('Insira a quantidade: '))
    valor_unit = float(input('Insira o valor unitário do ativo: '))
    taxa_corretagem = float(input('Insira a corretagem: '))
    tipo_op = input('Insira o tipo de transação: ').upper()
    inv = investimentos(ativo, quantidade, valor_unit, taxa_corretagem, tipo_op)
    if tipo_op == 'COMPRA':
        inv.calc()
        inv.salvarDados()
    else:
        inv.calc()
        inv.precoMedio
        inv.lucro_prejuizo()
