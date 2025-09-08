import pandas as pd
import random
from faker import Faker
from datetime import timedelta, date

class DatasetGenerator:
    def __init__(self, output_path="files"):
        self.fake = Faker("pt_BR")
        self.output_path = output_path
        self.df_lojas = None
        self.df_dim_clientes = None
        self.df_dim_compras = None
        self.df_fato_recebiveis = None
        self.df_despesas = None

        # ---------- GERAR LOJAS ----------
    def create_dataset_store(self, n_lojas=23):
        codigos_lojas = [f"LOJA_{i:03d}" for i in range(1, n_lojas+1)]
        ddds_validos = [
            "11","12","13","14","15","16","17","18","19",
            "21","22","24","27","28","31","32","33","34","35","37","38",
            "41","42","43","44","45","46","47","48","49",
            "51","53","54","55","61","62","64","63","65","66","67","68","69",
            "71","73","74","75","77","79","81","82","83","84","85","86","87","88","89"
        ]
        custo_por_funcionario = 3000
        dados_lojas = []

        for codigo in codigos_lojas:
            area_venda_m2 = random.randint(200, 2000)

            # cálculo de funcionários
            num_funcionarios = max(2, area_venda_m2 // 400)
            custo_funcionarios = num_funcionarios * custo_por_funcionario

            # peso da loja
            peso_loja = round(random.uniform(1, 2.0), 2)

            dados_lojas.append({
                "cd_codigo_loja": codigo,
                "nome_loja": self.fake.company(),
                "rua": self.fake.street_name(),
                "numero": random.randint(10, 9999),
                "complemento": random.choice(["", "Loja A", "Loja B", "Bloco 1", "Andar 2"]),
                "bairro": self.fake.bairro(),
                "cidade": self.fake.city(),
                "estado": self.fake.estado_sigla(),
                "pais": "Brazil",
                "cep": self.fake.postcode().replace("-", "").zfill(8),
                "codigo_pais": 55,
                "ddd": random.choice(ddds_validos),
                "telefone": f"{random.randint(90000, 99999)}-{random.randint(0, 9999):04d}",
                "gerente_responsavel": self.fake.name(),
                "area_venda_m2": area_venda_m2,
                "num_funcionarios": num_funcionarios,
                "custo_mensal_funcionarios": custo_funcionarios,
                "peso_loja": peso_loja,
                "created_at": self.fake.date_between(start_date="-2y", end_date="-1y"),
                "updated_at": None
            })

        # criar dataframe
        self.df_lojas = pd.DataFrame(dados_lojas)
        self.df_lojas["created_at"] = pd.to_datetime(self.df_lojas["created_at"])

        # exportar
        self.df_lojas.to_csv(f"{self.output_path}/dim_lojas.csv", index=False, encoding="utf-8-sig")
        print("✅ Arquivo 'dim_lojas.csv' gerado.")
        return self.df_lojas


    # ---------- GERAR VENDAS ----------
    def create_dataset_sales(self, n_clientes=5000):
        if self.df_lojas is None:
            raise ValueError("Você precisa gerar lojas primeiro.")

        formas_pagamento = [1, 2, 3, 4]
        categorias_vendas = [1, 2]
        sazonalidade = {1: 0.6, 2: 0.7, 3: 0.9, 4: 1.0, 5: 1.0, 6: 1.1,
                        7: 1.0, 8: 0.9, 9: 1.0, 10: 1.2, 11: 1.5, 12: 1.8}

        clientes = []
        for i in range(n_clientes):
            clientes.append({
                "id_cliente": f"CLI_{i+1:05d}",
                "nome": self.fake.name(),
                "cpf": self.fake.cpf(),
                "email": self.fake.email(),
                "telefone": self.fake.phone_number(),
                "data_nascimento": self.fake.date_of_birth(minimum_age=18, maximum_age=80),
                "cidade": self.fake.city(),
                "estado": self.fake.estado_sigla()
            })
        self.df_dim_clientes = pd.DataFrame(clientes)

        dim_compras, fato_recebiveis = [], []
        datas = pd.date_range(start=self.df_lojas["created_at"].min(), end=date.today(), freq="MS")

        for mes in datas:
            mes = pd.Timestamp(mes)
            mes_num = mes.month
            lojas_ativas = self.df_lojas[self.df_lojas["created_at"] <= mes].copy()

            for _, loja in lojas_ativas.iterrows():
                vendas_esperadas = int(random.gauss(50 * loja["peso_loja"] * sazonalidade[mes_num], 10))
                vendas_esperadas = max(vendas_esperadas, 1)

                for _ in range(vendas_esperadas):
                    id_compra = self.fake.uuid4()
                    cliente = random.choice(self.df_dim_clientes["id_cliente"])
                    data_emissao = mes + timedelta(days=random.randint(0, 27))
                    forma_pagamento = random.choice(formas_pagamento)
                    valor_compra = round(random.uniform(50, 2000) * loja["peso_loja"], 2)
                    parcelas = 1 if forma_pagamento in [1, 2, 4] else random.choice(range(1, 11))

                    dim_compras.append({
                        "id_compra": id_compra,
                        "parcelas": parcelas,
                        "data_emissao": data_emissao,
                        "valor_compra": valor_compra,
                        "cd_forma_pagamento": forma_pagamento,
                        "id_cliente": cliente,
                        "cd_categoria_venda": random.choice(categorias_vendas),
                        "cd_codigo_loja": loja["cd_codigo_loja"]
                    })

                    valor_base = round(valor_compra / parcelas, 2)
                    valores_parcelas = [valor_base] * parcelas
                    diferenca = round(valor_compra - sum(valores_parcelas), 2)
                    valores_parcelas[-1] += diferenca

                    for i, valor in enumerate(valores_parcelas, 1):
                        fato_recebiveis.append({
                            "id_transacao": self.fake.uuid4(),
                            "id_compra": id_compra,
                            "data_hora_recebimento": data_emissao + timedelta(days=30 * i),
                            "valor_recebimento": valor
                        })

        self.df_dim_compras = pd.DataFrame(dim_compras)
        self.df_fato_recebiveis = pd.DataFrame(fato_recebiveis)

        self.df_dim_clientes.to_csv(f"{self.output_path}/dim_clientes.csv", index=False, encoding="utf-8-sig")
        self.df_dim_compras.to_csv(f"{self.output_path}/dim_compras.csv", index=False, encoding="utf-8-sig")
        self.df_fato_recebiveis.to_csv(f"{self.output_path}/fato_recebiveis.csv", index=False, encoding="utf-8-sig")

        print("✅ Arquivos de clientes, compras e recebíveis gerados.")
        return self.df_dim_clientes, self.df_dim_compras, self.df_fato_recebiveis

    # ---------- GERAR DESPESAS ----------
    
    def create_dataset_expenses(self):
        if self.df_lojas is None:
            raise ValueError("Você precisa gerar lojas primeiro.")
        if self.df_dim_compras is None:
            raise ValueError("Você precisa gerar compras primeiro.")

        tipos_despesas = [
            "Aluguel", "Luz", "Água", "Internet",
            "Salário Funcionários", "Impostos",
            "Financiamento", "Custo Mercadoria"
        ]

        data_inicio = self.df_lojas["created_at"].min()
        data_fim = date.today() + pd.DateOffset(months=10)
        datas = pd.date_range(start=data_inicio, end=data_fim, freq="MS")

        valores_iniciais = {
            "Aluguel": 5000, "Luz": 200, "Água": 100, "Internet": 100,
            "Salário Funcionários": 3000, "Impostos": 250, "Financiamento": 50000 / len(datas)
        }
        valores_finais = {
            "Aluguel": 6000, "Luz": 300, "Água": 150, "Internet": 150,
            "Salário Funcionários": 3000, "Impostos": 500, "Financiamento": 50000
        }

        despesas = []

        # --- Despesas fixas/variáveis por loja ---
        for _, loja in self.df_lojas.iterrows():
            for i, mes in enumerate(datas):
                if mes < loja["created_at"]:
                    continue
                for despesa in tipos_despesas:
                    if despesa == "Custo Mercadoria":
                        # este será gerado depois com base nas compras
                        continue
                    if despesa == "Aluguel":
                        valor = round(12 * loja["area_venda_m2"] * loja["peso_loja"], 2)
                    elif despesa == "Salário Funcionários":
                        valor = round(loja["num_funcionarios"] * valores_iniciais[despesa], 2)
                    elif despesa == "Impostos":
                        valor = round(random.uniform(250, 500) * loja["peso_loja"], 2)
                    elif despesa == "Luz":
                        valor = round(0.5 * loja["area_venda_m2"], 2)
                    elif despesa == "Água":
                        valor = round(0.2 * loja["area_venda_m2"], 2)
                    else:  # Internet, Financiamento
                        incremento = (valores_finais[despesa] - valores_iniciais[despesa]) / (len(datas) - 1)
                        valor = valores_iniciais[despesa] + incremento * i

                    despesas.append({
                        "cd_codigo_loja": loja["cd_codigo_loja"],
                        "data_mes": mes,
                        "tipo_despesa": despesa,
                        "valor_despesa": valor
                    })

        # --- Custos de mercadoria (baseado nas compras) ---
        for _, compra in self.df_dim_compras.iterrows():
            custo_total = round(compra["valor_compra"] * 0.35, 2)
            parcelas = 10
            valor_base = round(custo_total / parcelas, 2)
            valores_parcelas = [valor_base] * parcelas
            diferenca = round(custo_total - sum(valores_parcelas), 2)
            valores_parcelas[-1] += diferenca

            for i, valor in enumerate(valores_parcelas, 1):
                data_parcela = compra["data_emissao"] + pd.DateOffset(months=i)
                despesas.append({
                    "cd_codigo_loja": compra["cd_codigo_loja"],
                    "data_mes": data_parcela,
                    "tipo_despesa": "Custo Mercadoria",
                    "valor_despesa": valor
                })

        # Criar DataFrame final
        self.df_despesas = pd.DataFrame(despesas)
        self.df_despesas.to_csv(f"{self.output_path}/fato_despesas.csv", index=False, encoding="utf-8-sig")
        print("✅ Arquivo 'fato_despesas.csv' gerado.")
        return self.df_despesas
