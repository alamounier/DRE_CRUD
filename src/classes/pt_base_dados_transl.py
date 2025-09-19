import pandas as pd
import random
from faker import Faker
from datetime import timedelta, date


class GeradorDataset:
    def __init__(self, caminho_saida="files"):
        self.fake = Faker("pt_BR")
        self.caminho_saida = caminho_saida
        self.df_lojas = None
        self.df_clientes = None
        self.df_compras = None
        self.df_recebiveis = None
        self.df_despesas = None
        self.df_emprestimos = None

    # ---------- GERAR LOJAS ----------
    def criar_dataset_lojas(self, n_lojas=23):
        codigos_lojas = [f"LOJA_{i:03d}" for i in range(1, n_lojas + 1)]
        ddds_validos = [
            "11","12","13","14","15","16","17","18","19",
            "21","22","24","27","28","31","32","33","34","35","37","38",
            "41","42","43","44","45","46","47","48","49",
            "51","53","54","55","61","62","64","63","65","66","67","68","69",
            "71","73","74","75","77","79","81","82","83","84","85","86","87","88","89"
        ]

        cidades_brasil = [
            {"cidade": "São Paulo", "estado": "SP", "latitude": -23.5505, "longitude": -46.6333},
            {"cidade": "Rio de Janeiro", "estado": "RJ", "latitude": -22.9068, "longitude": -43.1729},
            {"cidade": "Belo Horizonte", "estado": "MG", "latitude": -19.9167, "longitude": -43.9345},
            {"cidade": "Curitiba", "estado": "PR", "latitude": -25.4284, "longitude": -49.2733},
            {"cidade": "Fortaleza", "estado": "CE", "latitude": -3.7319, "longitude": -38.5267},
            {"cidade": "Salvador", "estado": "BA", "latitude": -12.9777, "longitude": -38.5016},
            {"cidade": "Recife", "estado": "PE", "latitude": -8.0476, "longitude": -34.8770},
            {"cidade": "Porto Alegre", "estado": "RS", "latitude": -30.0346, "longitude": -51.2177},
            {"cidade": "Manaus", "estado": "AM", "latitude": -3.1190, "longitude": -60.0217},
            {"cidade": "Goiânia", "estado": "GO", "latitude": -16.6869, "longitude": -49.2648},
            {"cidade": "Campinas", "estado": "SP", "latitude": -22.9056, "longitude": -47.0608},
            {"cidade": "São Luís", "estado": "MA", "latitude": -2.5307, "longitude": -44.3068}
        ]

        custo_por_funcionario = 3000
        dados_lojas = []

        for codigo in codigos_lojas:
            area_venda_m2 = random.randint(200, 2000)
            num_funcionarios = max(2, area_venda_m2 // 400)
            custo_funcionarios = num_funcionarios * custo_por_funcionario
            peso_loja = round(random.uniform(1, 2.0), 2)

            cidade_escolhida = random.choice(cidades_brasil)

            dados_lojas.append({
                "cd_loja": codigo,
                "nome_loja": self.fake.company(),
                "rua": self.fake.street_name(),
                "numero": random.randint(10, 9999),
                "complemento": random.choice(["", "Loja A", "Loja B", "Bloco 1", "Andar 2"]),
                "bairro": self.fake.bairro(),
                "cidade": cidade_escolhida["cidade"],
                "estado": cidade_escolhida["estado"],
                "pais": "Brasil",
                "cep": self.fake.postcode().replace("-", "").zfill(8),
                "codigo_pais": 55,
                "ddd": random.choice(ddds_validos),
                "telefone": f"{random.randint(90000, 99999)}-{random.randint(0, 9999):04d}",
                "gerente": self.fake.name(),
                "area_venda_m2": area_venda_m2,
                "num_funcionarios": num_funcionarios,
                "custo_mensal_funcionarios": custo_funcionarios,
                "peso_loja": peso_loja,
                "latitude": cidade_escolhida["latitude"],
                "longitude": cidade_escolhida["longitude"],
                "data_criacao": self.fake.date_between(start_date="-2y", end_date="-1y"),
                "data_atualizacao": None
            })

        self.df_lojas = pd.DataFrame(dados_lojas)
        self.df_lojas["data_criacao"] = pd.to_datetime(self.df_lojas["data_criacao"])
        self.df_lojas.to_csv(f"{self.caminho_saida}/dim_lojas.csv", index=False, encoding="utf-8-sig")
        print("✅ Arquivo 'dim_lojas.csv' gerado.")
        return self.df_lojas

    # ---------- GERAR VENDAS ----------
    def criar_dataset_vendas(self, n_clientes=5000):
        if self.df_lojas is None:
            raise ValueError("Você precisa gerar lojas primeiro.")

        # Formas de pagamento
        # 1 = Crédito (único que pode parcelar)
        # 2 = Débito
        # 3 = Pix
        # 4 = Dinheiro
        formas_pagamento = [1, 2, 3, 4]
        pesos_pagamento = [0.55, 0.25, 0.15, 0.05]

        # Categorias de vendas (1=Presencial, 2=Online)
        categorias_vendas = [1, 2]
        pesos_categorias = [0.7, 0.3]

        # Sazonalidade (peso mensal)
        sazonalidade = {
            1: 0.6, 2: 0.7, 3: 0.9, 4: 1.0,
            5: 1.0, 6: 1.1, 7: 1.0, 8: 0.9,
            9: 1.0, 10: 1.2, 11: 1.5, 12: 1.8
        }

        # Criar clientes
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
        self.df_clientes = pd.DataFrame(clientes)

        # Saídas
        dim_compras, fato_recebiveis = [], []

        # Intervalo de datas
        datas = pd.date_range(
            start=self.df_lojas["data_criacao"].min(),
            end=date.today(),
            freq="MS"
        )

        for mes in datas:
            mes = pd.Timestamp(mes)
            mes_num = mes.month

            lojas_ativas = self.df_lojas[self.df_lojas["data_criacao"] <= mes].copy()

            for _, loja in lojas_ativas.iterrows():
                vendas_esperadas = int(random.gauss(50 * loja["peso_loja"] * sazonalidade[mes_num], 10))
                vendas_esperadas = max(vendas_esperadas, 1)

                for _ in range(vendas_esperadas):
                    id_compra = self.fake.uuid4()
                    cliente = random.choice(self.df_clientes["id_cliente"])
                    data_emissao = mes + timedelta(days=random.randint(0, 27))

                    forma_pagamento = random.choices(formas_pagamento, weights=pesos_pagamento, k=1)[0]
                    categoria_venda = random.choices(categorias_vendas, weights=pesos_categorias, k=1)[0]

                    valor_compra = round(random.uniform(100, 600) * loja["peso_loja"], 2)

                    # Parcelamento: apenas crédito
                    if forma_pagamento == 1:
                        parcelas = random.choice(range(1, 11))
                    else:
                        parcelas = 1

                    # Impostos (15%)
                    valor_impostos = round(valor_compra * 0.15, 2)

                    # Registrar compra
                    dim_compras.append({
                        "id_compra": id_compra,
                        "parcelas": parcelas,
                        "data_emissao": data_emissao,
                        "valor_compra": valor_compra,
                        "valor_impostos": valor_impostos,
                        "cd_forma_pagamento": forma_pagamento,
                        "id_cliente": cliente,
                        "cd_categoria_venda": categoria_venda,
                        "cd_loja": loja["cd_loja"]
                    })

                    # --- Recebíveis ---
                    if forma_pagamento == 1:  # Crédito
                        valor_base = round(valor_compra / parcelas, 2)
                        valores_parcelas = [valor_base] * parcelas
                        diferenca = round(valor_compra - sum(valores_parcelas), 2)
                        valores_parcelas[-1] += diferenca

                        for i, valor in enumerate(valores_parcelas, 1):
                            fato_recebiveis.append({
                                "id_transacao": self.fake.uuid4(),
                                "id_compra": id_compra,
                                "data_recebimento": data_emissao + timedelta(days=30 * i),
                                "valor_recebimento": valor
                            })

                    elif forma_pagamento == 2:  # Débito
                        delay = random.randint(1, 2)
                        fato_recebiveis.append({
                            "id_transacao": self.fake.uuid4(),
                            "id_compra": id_compra,
                            "data_recebimento": data_emissao + timedelta(days=delay),
                            "valor_recebimento": valor_compra
                        })

                    else:  # Pix e Dinheiro
                        fato_recebiveis.append({
                            "id_transacao": self.fake.uuid4(),
                            "id_compra": id_compra,
                            "data_recebimento": data_emissao,
                            "valor_recebimento": valor_compra
                        })

        self.df_compras = pd.DataFrame(dim_compras)
        self.df_recebiveis = pd.DataFrame(fato_recebiveis)

        self.df_clientes.to_csv(f"{self.caminho_saida}/dim_clientes.csv", index=False, encoding="utf-8-sig")
        self.df_compras.to_csv(f"{self.caminho_saida}/dim_compras.csv", index=False, encoding="utf-8-sig")
        self.df_recebiveis.to_csv(f"{self.caminho_saida}/fato_recebiveis.csv", index=False, encoding="utf-8-sig")

        print("✅ Arquivos de clientes, compras e recebíveis gerados.")
        return self.df_clientes, self.df_compras, self.df_recebiveis

def criar_dataset_emprestimos(self, taxa_juros_anual=0.12, prazo_meses=24):
    if self.df_lojas is None:
        raise ValueError("Você precisa gerar as lojas primeiro.")

    emprestimos = []
    taxa_juros_mensal = (1 + taxa_juros_anual) ** (1 / 12) - 1

    for _, loja in self.df_lojas.iterrows():
        valor_emprestimo = loja["area_venda_m2"] * 50
        data_contratacao = loja["created_at"] - pd.DateOffset(months=3)

        # Entrada de capital (empréstimo recebido)
        emprestimos.append({
            "cd_codigo_loja": loja["cd_codigo_loja"],
            "data_evento": data_contratacao,
            "tipo_evento": "Entrada de Capital",
            "valor": valor_emprestimo
        })

        # Cálculo da parcela fixa (sistema Price)
        pmt = valor_emprestimo * (taxa_juros_mensal * (1 + taxa_juros_mensal) ** prazo_meses) / (
            (1 + taxa_juros_mensal) ** prazo_meses - 1
        )

        # Geração das parcelas do financiamento
        for i in range(1, prazo_meses + 1):
            data_parcela = data_contratacao + pd.DateOffset(months=i)
            emprestimos.append({
                "cd_codigo_loja": loja["cd_codigo_loja"],
                "data_evento": data_parcela,
                "tipo_evento": "Parcela de Financiamento",
                "valor": (-1) * round(pmt, 2)
            })

    self.df_emprestimos = pd.DataFrame(emprestimos)
    self.df_emprestimos.to_csv(f"{self.output_path}/fato_emprestimos.csv", index=False, encoding="utf-8-sig")
    print("✅ Arquivo 'fato_emprestimos.csv' gerado.")
    return self.df_emprestimos