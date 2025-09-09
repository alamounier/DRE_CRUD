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
