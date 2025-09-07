from faker import Faker
import pandas as pd
import random
from datetime import timedelta, date

fake = Faker("pt_BR")

# Lojas
codigos_lojas = [f"LOJA_{i:03d}" for i in range(1, 24)]

# Tipos de despesas
tipos_despesas = [
    "Aluguel", "Luz", "Água", "Internet", 
    "Salário Funcionários", "Impostos", 
    "Financiamento"
]

# Datas de análise (últimos 24 meses + 10 meses no futuro)
data_inicio = date.today().replace(day=1) - timedelta(days=730)  # 24 meses atrás
data_fim = date.today().replace(day=1) + pd.DateOffset(months=10)
datas = pd.date_range(start=data_inicio, end=data_fim, freq="MS")  # início de cada mês

# Pesos de lojas para despesas
pesos_lojas = {loja: random.uniform(0.8, 2.0) for loja in codigos_lojas}

# Pesos sazonais (somente aplicados a algumas despesas)
sazonalidade = {
    1: 0.6, 2: 0.7, 3: 0.9, 4: 1.0, 5: 1.0, 6: 1.1,
    7: 1.0, 8: 0.9, 9: 1.0, 10: 1.2, 11: 1.5, 12: 1.8
}

# Gerar despesas
despesas = []

for loja in codigos_lojas:
    for mes in datas:
        for despesa in tipos_despesas:
            mes_num = mes.month
            # Valor base da despesa
            if despesa == "Aluguel":
                valor = round(random.uniform(5000, 15000) * pesos_lojas[loja], 2)
            elif despesa == "Internet":
                valor = round(random.uniform(300, 1500) * pesos_lojas[loja], 2)
            elif despesa == "Financiamento":
                valor = round(random.uniform(20000, 30000) * pesos_lojas[loja], 2)
            else:
                # Despesas com sazonalidade
                if despesa == "Luz":
                    valor_base = random.uniform(300, 1500)
                elif despesa == "Água":
                    valor_base = random.uniform(300, 1500)
                elif despesa == "Salário Funcionários":
                    valor_base = random.uniform(15000, 50000) #salário e comissões
                elif despesa == "Impostos":
                    valor_base = random.uniform(2500, 5000) #alvará e publicidade -- parcelado em 10x/ano
                valor = round(valor_base * pesos_lojas[loja] * sazonalidade[mes_num], 2)

            despesas.append({
                "cd_codigo_loja": loja,
                "data_mes": mes,
                "tipo_despesa": despesa,
                "valor_despesa": valor
            })

df_despesas = pd.DataFrame(despesas)

# Exportar
df_despesas.to_csv("files/fato_despesas.csv", index=False, encoding="utf-8-sig")

print("Arquivo 'fato_despesas.csv' gerado com sucesso!")
