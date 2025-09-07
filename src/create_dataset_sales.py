from faker import Faker
import pandas as pd
import random
from datetime import timedelta

fake = Faker("pt_BR")
n_compras = 200000  

# Lojas
codigos_lojas = [f"LOJA_{i:03d}" for i in range(1, 24)]
formas_pagamento = [1, 2, 3, 4]  # 1=dinheiro, 2=débito, 3=crédito, 4=pix
categorias_vendas = [1, 2]       # 1=presencial, 2=online

# Pesos sazonais
sazonalidade = {
    1: 0.6, 2: 0.7, 3: 0.9, 4: 1.0, 5: 1.0, 6: 1.1,
    7: 1.0, 8: 0.9, 9: 1.0, 10: 1.2, 11: 1.5, 12: 1.8
}

# Pesos de vendas das lojas
pesos_lojas = {loja: random.uniform(0.5, 2.0) for loja in codigos_lojas}

# Datas de abertura
abertura_lojas = {loja: fake.date_between(start_date='-24M', end_date='-1M') for loja in codigos_lojas}

# Criar clientes únicos
n_clientes = 5000
clientes = []
for i in range(n_clientes):
    clientes.append({
        "id_cliente": f"CLI_{i+1:05d}",
        "nome": fake.name(),
        "cpf": fake.cpf(),
        "email": fake.email(),
        "telefone": fake.phone_number(),
        "data_nascimento": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "cidade": fake.city(),
        "estado": fake.estado_sigla()
    })
df_dim_clientes = pd.DataFrame(clientes)

# Tabelas finais
dim_compras = []
fato_recebiveis = []

for _ in range(n_compras):
    id_compra = fake.uuid4()
    cliente = random.choice(df_dim_clientes["id_cliente"])

    # Loja escolhida por peso
    loja = random.choices(codigos_lojas, weights=pesos_lojas.values(), k=1)[0]
    data_inicio_loja = abertura_lojas[loja]

    # Data de emissão ajustada pela sazonalidade
    while True:
        data_emissao = fake.date_between(start_date=data_inicio_loja, end_date="today")
        if random.random() < sazonalidade[data_emissao.month] / 2:
            break

    forma_pagamento = random.choice(formas_pagamento)
    valor_compra = round(random.uniform(50, 2000) * pesos_lojas[loja], 2)

    # Parcelas
    if forma_pagamento in [1, 2, 4]:  # à vista
        parcelas = 1
    else:
        parcelas = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    # Inserir na dimensão
    dim_compras.append({
        "id_compra": id_compra,
        "parcelas": parcelas,
        "data_emissao": data_emissao,
        "valor_compra": valor_compra,
        "cd_forma_pagamento": forma_pagamento,
        "id_cliente": cliente,
        "cd_categoria_venda": random.choice(categorias_vendas),
        "cd_codigo_loja": loja
    })

    # Gerar recebíveis da compra (com ajuste na última parcela)
    valor_base = round(valor_compra / parcelas, 2)
    valores_parcelas = [valor_base] * parcelas
    diferenca = round(valor_compra - sum(valores_parcelas), 2)
    valores_parcelas[-1] += diferenca  # ajusta última parcela

    if parcelas == 1:  # pagamentos à vista
        fato_recebiveis.append({
            "id_transacao": fake.uuid4(),
            "id_compra": id_compra,
            "data_hora_recebimento": data_emissao,
            "valor_recebimento": valores_parcelas[0]
        })
    else:
        for i, valor in enumerate(valores_parcelas, 1):
            data_recebimento = data_emissao + timedelta(days=30 * i)
            fato_recebiveis.append({
                "id_transacao": fake.uuid4(),
                "id_compra": id_compra,
                "data_hora_recebimento": data_recebimento,
                "valor_recebimento": valor
            })

# Criar DataFrames
df_dim_compras = pd.DataFrame(dim_compras)
df_fato_recebiveis = pd.DataFrame(fato_recebiveis)

# Exportar
df_dim_clientes.to_csv("dim_clientes.csv", index=False, encoding="utf-8-sig")
df_dim_compras.to_csv("dim_compras.csv", index=False, encoding="utf-8-sig")
df_fato_recebiveis.to_csv("fato_recebiveis.csv", index=False, encoding="utf-8-sig")

print("Arquivos 'dim_clientes.csv', 'dim_compras.csv' e 'fato_recebiveis.csv' gerados com sucesso!")
