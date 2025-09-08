from classes.datasets import DatasetGenerator

if __name__ == "__main__":
    generator = DatasetGenerator(output_path="files")

    # Gera datasets
    df_lojas = generator.create_dataset_store()
    df_clientes, df_compras, df_recebiveis = generator.create_dataset_sales()
    df_despesas = generator.create_dataset_expenses()

    print("🚀 Todos os datasets foram gerados com sucesso!")
