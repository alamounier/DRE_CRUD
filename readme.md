
# 📘 Dataset Generator – Documentation

This project implements a **Python** class for generating synthetic datasets that simulate a multi-store retail scenario.  
The datasets can be used for financial analysis, cash flow simulations, and dashboards in **Power BI**.

---

## 📂 Project Structure

The main class is `DatasetGenerator`, responsible for generating different dimensional and fact tables:

- `dim_stores.csv` → Stores  
- `dim_customers.csv` → Customers  
- `dim_sales.csv` → Sales  
- `fact_receivables.csv` → Receivables  
- `fact_expenses.csv` → Expenses  
- `fact_loans.csv` → Loans  

The output is saved as **CSV files** in the directory defined by the `output_path` parameter.

---

## ⚙️ Class Initialization

```python
generator = DatasetGenerator(output_path="files/en")
```

- `output_path`: Path where generated files will be saved (default = `files/en`).

---

## 📑 Available Methods

### 1. `create_dataset_store(n_stores=23)`

Generates the **stores** dimension.  

- Each store contains:
  - Code and name
  - Address, city, state, phone, manager
  - Sales area in m²
  - Number of employees
  - Fixed employee costs
  - Geographic coordinates (latitude/longitude)

📄 **Output**: `dim_stores.csv`

---

### 2. `create_dataset_sales(n_customers=5000)`

Generates customers, sales, and receivables.  

- **Customers** (`dim_customers`):
  - ID, name, SSN, email, phone, birth date, city, state  

- **Sales** (`dim_sales`):
  - Sale ID, value, date, taxes (15%), installments, payment method, customer, store, and category (In-store / Online).  

- **Receivables** (`fact_receivables`):
  - Transaction ID, sale ID, receipt date, receipt value.  
  - Rules:
    - Credit → Installments (1 to 10x)  
    - Debit → Receipt within 2 days  
    - Pix / Cash → Immediate receipt  

📄 **Outputs**: `dim_customers.csv`, `dim_sales.csv`, `fact_receivables.csv`

---

### 3. `create_dataset_expenses()`

Generates store expenses (fixed and variable).  

- **Fixed expenses** (monthly):  
  - Rent, Electricity, Water, Internet, Salaries.  

- **Variable expenses**:  
  - Merchandise → 40% of sales value, paid in **3 monthly installments**.  

📄 **Output**: `fact_expenses.csv`

---

### 4. `create_dataset_loans(annual_interest_rate=0.12, term_months=24)`

Simulates loans taken by stores.  

- Value = `sales_area_m2 * 50`  
- Contract = 3 months before store opening  
- Amortization = `term_months` (default: 24 months)  
- Annual interest = `annual_interest_rate` (default: 12%)  
- Installment calculation: **PMT formula**  

Generated events:  
- **Capital Injection** (initial full amount)  
- **Loan Installments** (monthly negative payments)  

📄 **Output**: `fact_loans.csv`

---

## 🏗️ Data Model

The model follows a **Star Schema**, with dimensions and fact tables:

- **Dimensions**
  - `dim_stores`
  - `dim_customers`
  - `dim_sales`

- **Facts**
  - `fact_receivables`
  - `fact_expenses`
  - `fact_loans`

---

## 🚀 Example Usage

```python
generator = DatasetGenerator()

# 1. Create stores
df_stores = generator.create_dataset_store(n_stores=20)

# 2. Create sales and receivables
df_customers, df_sales, df_receivables = generator.create_dataset_sales(n_customers=3000)

# 3. Create expenses
df_expenses = generator.create_dataset_expenses()

# 4. Create loans
df_loans = generator.create_dataset_loans()
```

---

## ✅ Expected Outputs

After execution, the following files will be available in the configured directory (`output_path`):

- `dim_stores.csv`  
- `dim_customers.csv`  
- `dim_sales.csv`  
- `fact_receivables.csv`  
- `fact_expenses.csv`  
- `fact_loans.csv`  

---

# 📘 Dataset Generator – Documentação

Este projeto implementa uma classe em **Python** para geração de datasets fictícios que simulam um cenário de varejo multiloja.  
Os datasets produzidos podem ser utilizados em análises financeiras, simulações de fluxo de caixa e dashboards no **Power BI**.

---

## 📂 Estrutura do Projeto

A classe principal é `DatasetGenerator`, responsável por gerar diferentes tabelas dimensionais e factuais:

- `dim_stores.csv` → Lojas  
- `dim_customers.csv` → Clientes  
- `dim_sales.csv` → Vendas  
- `fact_receivables.csv` → Contas a receber  
- `fact_expenses.csv` → Despesas  
- `fact_loans.csv` → Empréstimos  

O output é salvo em **arquivos CSV**, no diretório configurado no parâmetro `output_path`.

---

## ⚙️ Inicialização da Classe

```python
generator = DatasetGenerator(output_path="files/en")
```

- `output_path`: Caminho para salvar os arquivos gerados (default = `files/en`).

---

## 📑 Métodos Disponíveis

### 1. `create_dataset_store(n_stores=23)`

Gera a dimensão de **lojas**.  

- Cada loja possui:
  - Código e nome
  - Endereço, cidade, estado, telefone, gerente
  - Área de vendas em m²
  - Número de funcionários
  - Custos fixos de funcionários
  - Coordenadas geográficas (latitude/longitude)

📄 **Output**: `dim_stores.csv`

---

### 2. `create_dataset_sales(n_customers=5000)`

Gera clientes, vendas e contas a receber.  

- **Clientes** (`dim_customers`):
  - ID, nome, SSN, email, telefone, data de nascimento, cidade, estado  

- **Vendas** (`dim_sales`):
  - ID da venda, valor, data, impostos (15%), número de parcelas, método de pagamento, cliente, loja e categoria (In-store / Online).  

- **Recebíveis** (`fact_receivables`):
  - ID da transação, ID da venda, data do recebimento, valor recebido.  
  - Regras:
    - Crédito → Parcelas (1 a 10x)  
    - Débito → Recebimento em até 2 dias  
    - Pix / Dinheiro → Recebimento imediato  

📄 **Outputs**: `dim_customers.csv`, `dim_sales.csv`, `fact_receivables.csv`

---

### 3. `create_dataset_expenses()`

Gera despesas fixas e variáveis das lojas.  

- **Despesas fixas** (mensais):
  - Aluguel, Energia, Água, Internet, Salários.  

- **Despesas variáveis**:
  - Mercadorias → 40% do valor da venda, pagas em **3 parcelas mensais**.  

📄 **Output**: `fact_expenses.csv`

---

### 4. `create_dataset_loans(annual_interest_rate=0.12, term_months=24)`

Simula empréstimos tomados pelas lojas.  

- Valor = `sales_area_m2 * 50`  
- Contratação = 3 meses antes da abertura da loja  
- Amortização = `term_months` (default: 24 meses)  
- Juros anuais = `annual_interest_rate` (default: 12%)  
- Cálculo das parcelas: fórmula do **PMT**  

Eventos gerados:
- **Capital Injection** (entrada do valor total)  
- **Loan Installments** (parcelas mensais negativas)  

📄 **Output**: `fact_loans.csv`

---

## 🏗️ Modelo de Dados

O modelo segue um **Star Schema**, com dimensões e fatos:

- **Dimensões**
  - `dim_stores`
  - `dim_customers`
  - `dim_sales`

- **Fatos**
  - `fact_receivables`
  - `fact_expenses`
  - `fact_loans`

---

## 🚀 Exemplo de Uso

```python
generator = DatasetGenerator()

# 1. Criar lojas
df_stores = generator.create_dataset_store(n_stores=20)

# 2. Criar vendas e recebíveis
df_customers, df_sales, df_receivables = generator.create_dataset_sales(n_customers=3000)

# 3. Criar despesas
df_expenses = generator.create_dataset_expenses()

# 4. Criar empréstimos
df_loans = generator.create_dataset_loans()
```

---

## ✅ Saídas Esperadas

Após execução, os seguintes arquivos estarão no diretório configurado (`output_path`):

- `dim_stores.csv`  
- `dim_customers.csv`  
- `dim_sales.csv`  
- `fact_receivables.csv`  
- `fact_expenses.csv`  
- `fact_loans.csv`  