# Atividade Complementar – Cálculo Numérico (UNIVASF, 2026.2)

Questões resolvidas: **01.3** (Gauss), **02.3** (Gauss-Seidel), **03.1** (mínimos quadrados) e
**04.2** (Trapézio e Simpson repetidos). Os métodos estão implementados em Python puro.

## Instalação e execução

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py                   # programa interativo
python -m pytest tests/          # testes automáticos
```

Em cada questão dá para usar os dados do enunciado ou digitar novos dados. Os números aceitam
vírgula decimal (`0,55`) e são separados por espaço ou `;`. Ao final, o programa oferece
**novo cálculo**, **voltar ao menu** ou **sair**. Os gráficos são salvos em `graficos/`.

## Respostas

### 01.3 – Minas (Eliminação de Gauss com pivoteamento parcial)
```
0,55x1 + 0,25x2 + 0,25x3 = 4800   (areia)
0,30x1 + 0,45x2 + 0,20x3 = 5800   (cascalho fino)
0,15x1 + 0,30x2 + 0,55x3 = 5700   (cascalho grosso)
```
**Mina 1 ≈ 2.416,67 m³ · Mina 2 ≈ 9.193,33 m³ · Mina 3 = 4.690,00 m³**

### 02.3 – Circuito (Gauss-Seidel, x⁰ = bᵢ/aᵢᵢ, ε = 0,0001)
Lei das malhas com todas as correntes no sentido horário (ΣR·i = ΣE):
```
 9,5i1 − 2,5i2         − 2i4        =  12
−2,5i1 + 11i2 − 3,5i3         − 5i5 = −16
       − 3,5i2 + 15,5i3       − 4i5 =  14
−2i1                  + 7i4  − 3i5 =  10
       − 5i2  − 4i3   − 3i4  + 12i5 = −30
```
O critério de Sassenfeld dá max β = 0,880 < 1, então a convergência está garantida. O método
convergiu em 18 iterações:
**i1 ≈ 0,1166 · i2 ≈ −3,9269 · i3 ≈ −1,1877 · i4 ≈ −0,5380 · i5 ≈ −4,6666 A**
(sinal negativo = a corrente circula no sentido anti-horário).

### 03.1 – Lei de Moore (reta de mínimos quadrados em log10 N)
**log10 N = −266,9534 + 0,13718·a**, ou seja, **N(a) = 10^(−266,9534 + 0,13718·a)**, com R² = 0,9895.
- **2010: N ≈ 6,08·10⁸ transistores**
- **2020: N ≈ 1,43·10¹⁰ transistores**
- Pelo ajuste, o número de transistores dobra a cada ≈ 26,3 meses (Moore previu 18).

### 04.2 – Área do rio (L = M2 − M1, h = 10 m)
**Trapézio repetido: 2.592,5 m² · Simpson 1/3 repetido: 2.773,0 m²**

## Organização do código
```
main.py                  ponto de entrada
interface.py             menu principal e fluxo de cada questão
entrada.py               leitura validada (números, listas, matrizes)
apresentacao.py          console, formatação brasileira e exibição de sistemas
calculo/diretos.py       eliminacao_de_gauss, residuo_maximo
calculo/iterativos.py    gauss_seidel, criterio_de_sassenfeld, aproximacao_inicial
calculo/ajuste.py        ajustar_reta, erro_quadratico, coeficiente_r2
calculo/integracao.py    trapezio_repetido, simpson_repetido, passo_constante
problemas/               minas, circuito, moore, rio: dados, resolver() e mostrar()
tests/                   testes com pytest
```
