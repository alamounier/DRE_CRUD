from faker import Faker
import pandas as pd
import random
from datetime import timedelta

fake = Faker('pt_BR')
n_compras = 500000  # número de compras únicas
codigos_lojas_conglomerado = [f"LOJA_{i:03d}" for i in range(1, 53)]
formas_pagamento = [1, 2, 3, 4, 5]
categorias_vendas = [1, 2, 3]

dados_receber = []

for _ in range(n_compras):
    id_compra = fake.uuid4()
    cliente = fake.name()
    data_emissao = fake.date_between(start_date='-24M', end_date='today')
    forma_pagamento = random.choice(formas_pagamento)
    valor_compra = round(random.uniform(50, 2000), 2)
    
    # Número de parcelas
    if forma_pagamento in [1, 2, 4]:  # Pix, débito, dinheiro → à vista
        parcelas = 1
    else:  # crédito ou boleto
        parcelas = random.choice([2, 3, 4, 5, 6])
    
    # Entrada inicial (50% apenas para crédito/boleto)
    valor_entrada = round(valor_compra * 0.5, 2) if (forma_pagamento in [3, 5] and random.choice([True, False])) else 0
    
    # Valor restante para parcelar
    valor_restante = valor_compra - valor_entrada
    valor_parcela = round(valor_restante / parcelas, 2) if parcelas > 0 else 0

    # Criar transações para cada parcela
    for i in range(1, parcelas + 1):
        # Simula se parcela foi paga ou ficou inadimplente
        recebido = random.choices([True, False], weights=[0.85, 0.15])[0]
        atraso = random.randint(-5, 15) if recebido else 0
        data_recebimento = data_emissao + timedelta(days=30*i) + timedelta(days=atraso) if recebido else None
        
        valor_pago = valor_parcela if recebido else round(valor_parcela * random.uniform(0, 0.8), 2)  # simula inadimplência parcial

        dados_receber.append({
            "id_transacao": fake.uuid4(),
            "id_compra": id_compra,
            "parcela": i,
            "data_emissao": data_emissao,
            "data_recebimento": data_recebimento,
            "valor_compra": valor_compra,
            "valor_parcela": valor_parcela,
            "valor_pago": valor_pago,
            "valor_entrada": valor_entrada if i==1 else 0,
            "cd_forma_pagamento": forma_pagamento,
            "cliente": cliente,
            "cd_categoria_venda": random.choice(categorias_vendas),
            "cd_codigo_loja": random.choice(codigos_lojas_conglomerado),
            "status": "Recebido" if recebido else "Em aberto"
        })

df_receber = pd.DataFrame(dados_receber)
df_receber.to_csv("sales.csv", index=False, encoding="utf-8-sig")
print("Arquivo 'sales.csv' gerado com sucesso!")