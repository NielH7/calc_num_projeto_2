"""Questão 03.1: Lei de Moore (mínimos quadrados em log10 N)."""

import math
from dataclasses import dataclass
from pathlib import Path

from apresentacao import console, formatar, formatar_cientifico, nova_tabela
from calculo.ajuste import ajustar_reta, coeficiente_r2, erro_quadratico
from entrada import ler_lista

TITULO = "03.1 – Lei de Moore (Mínimos quadrados)"
ENUNCIADO = """\
Número de transistores N por ano de lançamento a (4004 em 1971 … Pentium 4 em 2000).
Transformando N em log10(N), os pontos ficam alinhados: log10(N) = b0 + b1·a,
logo N(a) = 10^(b0 + b1·a). Previsão para 2010 e 2020."""

PASTA_DE_GRAFICOS = Path("graficos")


@dataclass
class DadosMoore:
    anos: list[float]
    transistores: list[float]
    anos_para_prever: list[float]


@dataclass
class AjusteMoore:
    b0: float
    b1: float
    r2: float
    erro_quadratico: float

    def prever(self, ano: float) -> float:
        return 10 ** (self.b0 + self.b1 * ano)

    def meses_para_dobrar(self) -> float:
        return math.log10(2) / self.b1 * 12


DADOS_DO_ENUNCIADO = DadosMoore(
    anos=[1971, 1972, 1974, 1978, 1982, 1986, 1989, 1993, 1997, 1999, 2000],
    transistores=[2_250, 3_300, 6_000, 29_000, 134_000, 275_000, 1_200_000,
                  3_100_000, 7_500_000, 9_500_000, 42_000_000],
    anos_para_prever=[2010, 2020],
)


def resolver(dados: DadosMoore) -> AjusteMoore:
    if any(n <= 0 for n in dados.transistores):
        raise ValueError("O número de transistores deve ser positivo (log10).")
    logs = [math.log10(n) for n in dados.transistores]
    b0, b1 = ajustar_reta(dados.anos, logs)
    ajustados = [b0 + b1 * a for a in dados.anos]
    return AjusteMoore(b0, b1, coeficiente_r2(logs, ajustados), erro_quadratico(logs, ajustados))


def ler_novos_dados() -> DadosMoore:
    anos = ler_lista("Anos (separados por espaço)")
    transistores = ler_lista(f"Número de transistores ({len(anos)} valores, ex.: 42e6)", len(anos))
    previsoes = ler_lista("Anos para previsão (separados por espaço)", minimo=1)
    return DadosMoore(anos, transistores, previsoes)


def mostrar(dados: DadosMoore, ajuste: AjusteMoore) -> None:
    tabela = nova_tabela("Dados e ajuste", "Ano", "N real", "log10(N)", "log10 ajustado", "N ajustado")
    for ano, n in zip(dados.anos, dados.transistores):
        tabela.add_row(f"{ano:.0f}", formatar_cientifico(n), formatar(math.log10(n)),
                       formatar(ajuste.b0 + ajuste.b1 * ano), formatar_cientifico(ajuste.prever(ano)))
    console.print(tabela)

    console.print(f"Reta ajustada:  log10(N) = {formatar(ajuste.b0)} + {formatar(ajuste.b1, 5)}·a")
    console.print(f"Função:         N(a) = 10^({formatar(ajuste.b0)} + {formatar(ajuste.b1, 5)}·a)")
    console.print(f"R² = {formatar(ajuste.r2)}   Erro quadrático Σ\\[log10 N − g(a)]² = {formatar(ajuste.erro_quadratico)}")
    console.print(f"O número de transistores dobra a cada {formatar(ajuste.meses_para_dobrar(), 1)} meses "
                  "(Moore previu 18 meses).\n")
    for ano in dados.anos_para_prever:
        console.print(f"[bold green]Previsão {ano:.0f}: N ≈ {formatar_cientifico(ajuste.prever(ano))} transistores")
    console.print(f"Gráfico salvo em: {gerar_grafico(dados, ajuste)}")


def gerar_grafico(dados: DadosMoore, ajuste: AjusteMoore) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    inicio = min(dados.anos)
    fim = max(dados.anos + dados.anos_para_prever)
    anos_da_curva = [inicio + (fim - inicio) * k / 100 for k in range(101)]

    figura, eixo = plt.subplots(figsize=(8, 5))
    eixo.semilogy(dados.anos, dados.transistores, "o", label="Dados")
    eixo.semilogy(anos_da_curva, [ajuste.prever(a) for a in anos_da_curva], "-",
                  label=f"N = 10^({ajuste.b0:.3f} + {ajuste.b1:.5f}·a)")
    eixo.semilogy(dados.anos_para_prever, [ajuste.prever(a) for a in dados.anos_para_prever],
                  "s", color="red", label="Previsões")
    eixo.set(xlabel="Ano", ylabel="Transistores (escala log)", title="Lei de Moore – mínimos quadrados")
    eixo.grid(True, which="both", alpha=0.3)
    eixo.legend()

    PASTA_DE_GRAFICOS.mkdir(exist_ok=True)
    caminho = PASTA_DE_GRAFICOS / "moore.png"
    figura.savefig(caminho, dpi=120, bbox_inches="tight")
    plt.close(figura)
    return caminho
