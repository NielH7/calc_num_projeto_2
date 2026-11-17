"""Questão 04.2: área da superfície de um rio (Trapézio e Simpson 1/3 repetidos)."""

from dataclasses import dataclass
from pathlib import Path

from apresentacao import console, formatar, nova_tabela
from calculo.integracao import passo_constante, simpson_repetido, trapezio_repetido
from entrada import ler_lista

TITULO = "04.2 – Área da superfície de um rio (Integração numérica)"
ENUNCIADO = """\
Distâncias (m) entre uma linha de referência e as margens M1 e M2:
   x      0      10     20     30     40
   M1   50,8   86,2   136    72,8   51
   M2  113,6  144,5   185   171,2   95,3
Área = ∫ [M2(x) − M1(x)] dx em [0, 40], pelas regras do Trapézio e de Simpson repetidas."""

PASTA_DE_GRAFICOS = Path("graficos")


@dataclass
class DadosRio:
    xs: list[float]
    margem_1: list[float]
    margem_2: list[float]


@dataclass
class AreaDoRio:
    larguras: list[float]
    h: float
    trapezio: float
    simpson: float | None   # None quando o número de subintervalos é ímpar


DADOS_DO_ENUNCIADO = DadosRio(
    xs=[0, 10, 20, 30, 40],
    margem_1=[50.8, 86.2, 136, 72.8, 51],
    margem_2=[113.6, 144.5, 185, 171.2, 95.3],
)


def resolver(dados: DadosRio) -> AreaDoRio:
    h = passo_constante(dados.xs)
    larguras = [m2 - m1 for m1, m2 in zip(dados.margem_1, dados.margem_2)]
    simpson = simpson_repetido(larguras, h) if (len(larguras) - 1) % 2 == 0 else None
    return AreaDoRio(larguras, h, trapezio_repetido(larguras, h), simpson)


def ler_novos_dados() -> DadosRio:
    xs = ler_lista("Valores de x igualmente espaçados (separados por espaço)")
    n = len(xs)
    margem_1 = ler_lista(f"Distâncias até a margem M1 ({n} valores)", n)
    margem_2 = ler_lista(f"Distâncias até a margem M2 ({n} valores)", n)
    return DadosRio(xs, margem_1, margem_2)


def mostrar(dados: DadosRio, area: AreaDoRio) -> None:
    tabela = nova_tabela("L(x) = M2(x) − M1(x)", "x (m)", "M1 (m)", "M2 (m)", "L (m)")
    for linha in zip(dados.xs, dados.margem_1, dados.margem_2, area.larguras):
        tabela.add_row(*(formatar(v, 1) for v in linha))
    console.print(tabela)

    subintervalos = len(area.larguras) - 1
    console.print(f"h = {formatar(area.h, 2)} m, {subintervalos} subintervalos\n")
    console.print(f"[bold green]Trapézio repetido:   A ≈ {formatar(area.trapezio, 2)} m²")
    if area.simpson is None:
        console.print("[yellow]Simpson 1/3 repetido: não se aplica (número ímpar de subintervalos).")
    else:
        console.print(f"[bold green]Simpson 1/3 repetido: A ≈ {formatar(area.simpson, 2)} m²")
        diferenca = abs(area.simpson - area.trapezio)
        console.print(f"Diferença entre as regras: {formatar(diferenca, 2)} m² "
                      "(Simpson aproxima por parábolas, em geral é mais preciso).")
    console.print(f"Gráfico salvo em: {gerar_grafico(dados)}")


def gerar_grafico(dados: DadosRio) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    figura, eixo = plt.subplots(figsize=(8, 5))
    eixo.plot(dados.xs, dados.margem_1, "o-", label="Margem M1")
    eixo.plot(dados.xs, dados.margem_2, "o-", label="Margem M2")
    eixo.fill_between(dados.xs, dados.margem_1, dados.margem_2, alpha=0.3, label="Superfície do rio")
    eixo.set(xlabel="x (m)", ylabel="y (m)", title="Área da superfície do rio")
    eixo.grid(True, alpha=0.3)
    eixo.legend()

    PASTA_DE_GRAFICOS.mkdir(exist_ok=True)
    caminho = PASTA_DE_GRAFICOS / "rio.png"
    figura.savefig(caminho, dpi=120, bbox_inches="tight")
    plt.close(figura)
    return caminho
