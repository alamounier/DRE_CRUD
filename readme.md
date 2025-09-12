# PROJETO FLUXO DE CAIXA
# 📊 Dataset de Vendas Simulado - Conglomerado de Lojas

Este dataset foi gerado artificialmente para simular operações de
**contas a receber** de um conglomerado de lojas, considerando
sazonalidade, inauguração de lojas, diferentes formas de pagamento e
inadimplência.

------------------------------------------------------------------------

## 📁 Arquivo

-   **Nome:** `sales_sazonal.csv`
-   **Formato:** CSV (UTF-8)
-   **Linhas:** \~500.000 compras únicas com múltiplas parcelas
-   **Período coberto:** Últimos 24 meses

------------------------------------------------------------------------

## 🏷️ Dicionário de Dados

  --------------------------------------------------------------------------------
  Coluna                             Tipo               Descrição
  ---------------------------------- ------------------ --------------------------
  `id_transacao`                     UUID               Identificador único da
                                                        transação (uma linha por
                                                        parcela/entrada).

  `id_compra`                        UUID               Identificador único da
                                                        compra (pode ter várias
                                                        transações).

  `parcela`                          Inteiro            Número da parcela da
                                                        compra (1 = entrada ou
                                                        primeira parcela).

  `data_emissao`                     Data               Data da compra/emissão da
                                                        venda.

  `data_recebimento`                 Data               Data efetiva do
                                                        recebimento (ou `NULL` em
                                                        caso de inadimplência).

  `valor_compra`                     Decimal            Valor total da compra.

  `valor_parcela`                    Decimal            Valor esperado de cada
                                                        parcela.

  `valor_pago`                       Decimal            Valor efetivamente pago
                                                        (pode ser menor em caso de
                                                        inadimplência).

  `valor_entrada`                    Decimal            Valor de entrada pago na
                                                        compra (apenas em algumas
                                                        operações de
                                                        crédito/boletos).

  `cd_forma_pagamento`               Inteiro            Código da forma de
                                                        pagamento:`<br>`{=html}1 =
                                                        Pix`<br>`{=html}2 = Cartão
                                                        Débito`<br>`{=html}3 =
                                                        Cartão
                                                        Crédito`<br>`{=html}4 =
                                                        Dinheiro`<br>`{=html}5 =
                                                        Boleto

  `cliente`                          Texto              Nome do cliente.

  `cd_categoria_venda`               Inteiro            Categoria da
                                                        venda:`<br>`{=html}1 =
                                                        Venda loja`<br>`{=html}2 =
                                                        Venda online`<br>`{=html}3
                                                        = Serviço adicional

  `cd_codigo_loja`                   Texto              Código da loja (`LOJA_001`
                                                        até `LOJA_052`).

  `status`                           Texto              Status do pagamento:
                                                        `Recebido` ou `Em aberto`.
  --------------------------------------------------------------------------------

------------------------------------------------------------------------

## ⚙️ Regras de Negócio Simuladas

1.  **Formas de Pagamento**
    -   À vista (Pix, Débito, Dinheiro) → sempre 1 parcela.
    -   Crédito/Boleto → entre 2 e 6 parcelas, podendo ter entrada de
        50% do valor.
2.  **Inadimplência**
    -   \~15% das parcelas podem ficar em aberto ou parcialmente pagas.
3.  **Sazonalidade**
    -   Mais vendas em novembro e dezembro (Black Friday e Natal).
    -   Queda em janeiro/fevereiro.
4.  **Lojas**
    -   Cada loja tem um "peso" de vendas diferente.
    -   Algumas lojas foram inauguradas recentemente (não possuem dados
        em todo o período).
5.  **Variação no Valor das Compras**
    -   Lojas maiores tendem a ter tickets médios maiores.

------------------------------------------------------------------------

## 💡 Possíveis Análises

-   Evolução mensal de vendas e recebimentos.
-   Taxa de inadimplência por loja e forma de pagamento.
-   Comparação de sazonalidade entre lojas e categorias de venda.
-   Ticket médio por cliente/loja.
-   Volume de vendas por região.

------------------------------------------------------------------------

## 🚀 Uso

Este dataset é ideal para: - Simulações de **DRE (Demonstrativo de
Resultados do Exercício)**. - Criação de dashboards financeiros. -
Testes de modelos de previsão de inadimplência e fluxo de caixa. -
Estudos de sazonalidade e comportamento de clientes.

------------------------------------------------------------------------

✍️ **Gerado automaticamente com Python + Faker**\
📅 Data de geração: 05/09/2025


**dataset financiamento**

Criar um novo dataset fato_financiamentos que contenha:

Entrada (captação de capital) → valor do empréstimo 3 meses antes da abertura da loja.

Parcelas de pagamento → começam 1 mês após a contratação, duram 24 meses (2 anos), e incluem juros do mercado.

Base do cálculo: R$ 50 por m² de área de vendas da loja.
	​
![Fórmula Financiamento](images/formula%20financiamento.png)


*** dataset compras ***

Impostos no Brasil sobre faturamento (varejo)

No caso de empresas do varejo, os tributos mais comuns são:

ICMS: em média entre 12% e 18% (depende do estado e produto).

PIS/COFINS (cumulativo ou não cumulativo): entre 3,65% e 9,25%.

Em Simples Nacional, tudo vem consolidado, mas a alíquota efetiva gira em torno de 6% a 12% para comércio.

👉 Para simplificar no dataset, podemos assumir imposto médio de 15% sobre o valor da venda.


*** Insights ***

# 📊 Dashboard de Fluxo de Caixa

## 🎯 Objetivo
Monitorar o fluxo de caixa e a rentabilidade por loja e de forma consolidada, permitindo a análise de entradas, saídas e comportamento de pagamento dos clientes.

---

## 🔗 Fontes de Dados
- **Vendas** (f_compras)
- **Despesas** (f_despesas)
- **Financiamentos** (f_loans)
- **Calendário** (d_calendario)

---

## 📈 Principais KPIs
- **Vendas:** $2.408 → YoY $2.061 (+16,9%)  
- **Saídas (despesas):** ($2.143) → YoY ($1.583) (+35,4%)  
- **Lucro:** $460 → YoY $304 (+51,3%)  
- **Saldo por loja:** $20 → YoY $16 (+25,0%)  
- **Vendas médias por loja:** $105 → YoY $108 (-3,5%)  
- **Despesas médias por loja:** $77 → YoY $67 (+15,6%)  

---

## 💰 Fluxo de Caixa Consolidado
- **Fluxo Operacional:** $8.769 no acumulado.  
- **Recebimento Líquido:** $35.844  
  - Vendas: $42.725  
  - Imposto: -$6.882  
- **Desembolsos:** -$27.075  
  - Mercadoria: -$16.317  
  - Aluguel: -$7.280  
  - Salários: -$3.132  
  - Luz, água, internet: -$347  
- **Atividades de Financiamento:** $120  
  - Captações: $1.256  
  - Amortização e juros: -$1.136  
- **Fluxo de Caixa Líquido:** $8.888  

---

## 🛒 Comportamento de Pagamento
- **Distribuição média:**  
  - À vista no crédito: ~61%  
  - À vista: ~25%  
  - A prazo: ~14%  
- **Tendência:**  
  - Vendas parceladas entre 12% e 15%  
  - Leve queda no % de parcelados (mais vendas à vista/crédito)  
- **Forma de pagamento (snapshot):**  
  - Crédito: 55%  
  - Débito: 25%  
  - Pix: 15%  
  - Dinheiro: 5%  

---

## 👥 Volume & Clientes
- **Volume de vendas por cidade:** distribuído em diferentes regiões.  
- **Quantidade de clientes:** 961 até 2.250 por mês, com sazonalidade forte (ex: pico em fev/25).  

---

## 🔎 Insights Principais
1. Receita cresce **+16,9%**, mas despesas cresceram **+35,4%**, pressionando margens.  
2. **Mercadoria = ~60% dos desembolsos** → principal ponto para revisão.  
3. **Dependência de crédito/à vista (86%)**, apenas 14% a prazo.  
4. **Sazonalidade forte** em clientes e vendas → exige planejamento de estoque e caixa.  
5. **Captação de financiamento manteve caixa positivo**, mas amortizações são altas.  
6. Lucro líquido positivo, mas **margem ainda sensível** a aumento de custos.  

---

## 📑 Recomendações
- Revisar contratos e custos de mercadoria.  
- Monitorar sazonalidade para preparar estoque e fluxo de caixa.  
- Avaliar equilíbrio entre captação e amortização de financiamentos.  

