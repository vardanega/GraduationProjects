import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

# a)


def calcular_soma_pagamentos():
    conn = mysql.connector.connect(
        host='localhost',
        user='luuiz',
        password='Password123',
        database='gestao_imobiliaria_db'
    )

    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            i.id_imovel,
            SUM(p.valor_do_pagamento) AS soma_pagamentos
        FROM
            Pagamento p
        JOIN
            Imovel i ON p.codigo_imovel = i.id_imovel
        GROUP BY
            i.id_imovel
    ''')

    resultados = cursor.fetchall()

    conn.close()

    # Formatando os resultados em um dicionário
    resultado_dict = {str(id_imovel): float(soma_pagamentos) for id_imovel, soma_pagamentos in resultados}

    return jsonify(resultado_dict)


# Rota para a função de soma de pagamentos por imóvel
@app.route('/soma_pagamentos_por_imovel', methods=['GET'])
def rota_soma_pagamentos_por_imovel():
    return calcular_soma_pagamentos()


# b)
def calcular_total_vendas_por_mes_ano():
    conn = mysql.connector.connect(
        hhost='localhost',
        user='luuiz',
        password='Password123',
        database='gestao_imobiliaria_db'
    )

    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            DATE_FORMAT(p.data_do_pagamento, '%m/%Y') AS mes_ano,
            SUM(p.valor_do_pagamento) AS total_vendas
        FROM
            Pagamento p
        GROUP BY
            mes_ano
    ''')

    resultados = cursor.fetchall()

    conn.close()

    # Formatando os resultados em um dicionário
    resultado_dict = {mes_ano: float(total_vendas) for mes_ano, total_vendas in resultados}

    return jsonify(resultado_dict)


# Rota para a função de total de vendas por mês/ano
@app.route('/total_vendas_por_mes_ano', methods=['GET'])
def rota_total_vendas_por_mes_ano():
    return calcular_total_vendas_por_mes_ano()


# c)

def calcular_percentual_vendas_por_tipo():
    conn = mysql.connector.connect(
        host='localhost',
        user='luuiz',
        password='Password123',
        database='gestao_imobiliaria_db'
    )

    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            ti.tipo AS tipo_imovel,
            (SUM(p.valor_do_pagamento) / (SELECT SUM(valor_do_pagamento) FROM Pagamento)) * 100 AS percentual_vendas
        FROM
            Pagamento p
        JOIN
            Imovel i ON p.codigo_imovel = i.id_imovel
        JOIN
            TipoImovel ti ON i.tipo_imovel_id = ti.id_tipo_imovel
        GROUP BY
            ti.tipo
    ''')

    resultados = cursor.fetchall()

    conn.close()

    resultado_dict = {tipo_imovel: f'{percentual_vendas:.2f}%' for tipo_imovel, percentual_vendas in resultados}

    return jsonify(resultado_dict)


# Rota para a função de percentual de vendas por tipo de imóvel
@app.route('/percentual_vendas_por_tipo', methods=['GET'])
def rota_percentual_vendas_por_tipo():
    return calcular_percentual_vendas_por_tipo()


# rotas
# http://127.0.0.1:3306/soma_pagamentos_por_imovel
# http://127.0.0.1:3306/total_vendas_por_mes_ano
# http://127.0.0.1:3306/percentual_vendas_por_tipo
