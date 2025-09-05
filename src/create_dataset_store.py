from faker import Faker
import pandas as pd
import random
from datetime import datetime

fake = Faker("pt_BR")

# Lista de códigos de lojas fornecida
codigos_lojas = [
    "LOJA_046","LOJA_048","LOJA_006","LOJA_015","LOJA_052","LOJA_018","LOJA_042","LOJA_001",
    "LOJA_032","LOJA_034","LOJA_047","LOJA_030","LOJA_051","LOJA_031","LOJA_037","LOJA_004",
    "LOJA_036","LOJA_013","LOJA_035","LOJA_008","LOJA_027","LOJA_019","LOJA_003","LOJA_045",
    "LOJA_002","LOJA_017","LOJA_012","LOJA_041","LOJA_050","LOJA_014","LOJA_029","LOJA_026",
    "LOJA_005","LOJA_010","LOJA_049","LOJA_007","LOJA_011","LOJA_020","LOJA_028","LOJA_043",
    "LOJA_024","LOJA_023","LOJA_025","LOJA_040","LOJA_039","LOJA_033","LOJA_044","LOJA_022",
    "LOJA_038","LOJA_021","LOJA_009","LOJA_016"
]

ddds_validos = [
    "11","12","13","14","15","16","17","18","19",  # SP
    "21","22","24",  # RJ
    "27","28",  # ES
    "31","32","33","34","35","37","38",  # MG
    "41","42","43","44","45","46",  # PR
    "47","48","49",  # SC
    "51","53","54","55",  # RS
    "61","62","64","63","65","66","67","68","69",  # Centro-Oeste/Norte
    "71","73","74","75","77","79",  # BA/SE
    "81","82","83","84","85","86","87","88","89"  # NE
]


# Gerar dados
dados_lojas = []
for codigo in codigos_lojas:
    endereco = fake.address().split("\n")
    rua = fake.street_name()
    cidade = fake.city()
    estado = fake.estado_sigla()
    cep = fake.postcode().replace("-", "").zfill(8)
    
    dados_lojas.append({
        "cd_codigo_loja": codigo,
        "nome_loja": f"{fake.company()}",
        "rua": rua,
        "numero": random.randint(10, 9999),
        "complemento": random.choice(["", "Loja A", "Loja B", "Bloco 1", "Andar 2"]),
        "bairro": fake.bairro(),
        "cidade": cidade,
        "estado": estado,
        "pais": "Brazil",
        "cep": cep,
        "codigo_pais": 55,
        "ddd": random.choice(ddds_validos),
        "telefone": f"{random.randint(90000, 99999)}-{random.randint(0, 9999):04d}",
        "gerente_responsavel": fake.name(),
        "area_venda_m2": random.randint(200, 2000),  # tamanho da loja
        "created_at": fake.date_between(start_date="-2y", end_date="-1y"),
        "updated_at": None
    })

# Criar DataFrame
df_lojas = pd.DataFrame(dados_lojas)

# Exportar
df_lojas.to_csv("dim_lojas.csv", index=False, encoding="utf-8-sig")

print("Arquivo 'dim_lojas.csv' gerado com sucesso!")
