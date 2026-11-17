"""Questão 01.3: quantos m³ minerar de cada mina (Eliminação de Gauss)."""

from dataclasses import dataclass

from apresentacao import console, formatar, mostrar_sistema, nova_tabela
from calculo.diretos import eliminacao_de_gauss, residuo_maximo
from entrada import ler_inteiro, ler_lista

TITULO = "01.3 – Mineração de areia e cascalho (Método direto: Gauss)"
ENUNCIADO = """\
Um engenheiro precisa de 4.800, 5.800 e 5.700 m³ de areia, cascalho fino e cascalho grosso.
Composição das minas (%):   Areia  C. fino  C. grosso
                   Mina 1    55      30       15
                   Mina 2    25      45       30
                   Mina 3    25      20       55
Quantos m³ devem ser minerados de cada mina?"""


@dataclass
class DadosMinas:
    materiais: list[str]
    composicao_por_mina: list[list[float]]   # em %
    volumes_necessarios: list[float]


DADOS_DO_ENUNCIADO = DadosMinas(
    materiais=["Areia", "Cascalho fino", "Cascalho grosso"],
    composicao_por_mina=[[55, 30, 15], [25, 45, 30], [25, 20, 55]],
    volumes_necessarios=[4800, 5800, 5700],
)


def montar_sistema(dados: DadosMinas) -> list[list[float]]:
    """Linha i = material i; coluna j = fração do material i na mina j."""
    quantidade = len(dados.materiais)
    return [[mina[i] / 100 for mina in dados.composicao_por_mina] for i in range(quantidade)]


def resolver(dados: DadosMinas) -> list[float]:
    return eliminacao_de_gauss(montar_sistema(dados), dados.volumes_necessarios)


def ler_novos_dados() -> DadosMinas:
    n = ler_inteiro("Quantidade de minas (= quantidade de materiais)", minimo=2)
    materiais = [f"Material {i + 1}" for i in range(n)]
    console.print(f"Digite a composição de cada mina em % ({n} valores, um por material):")
    composicao = [ler_lista(f"  Mina {j + 1}", n) for j in range(n)]
    volumes = ler_lista(f"Volume necessário de cada material em m³ ({n} valores)", n)
    return DadosMinas(materiais, composicao, volumes)


def mostrar(dados: DadosMinas, volumes_por_mina: list[float]) -> None:
    matriz = montar_sistema(dados)
    variaveis = [f"x{j + 1}" for j in range(len(matriz))]
    mostrar_sistema(matriz, dados.volumes_necessarios, variaveis)

    tabela = nova_tabela("Volume a minerar", "Mina", "Volume (m³)")
    for j, volume in enumerate(volumes_por_mina):
        tabela.add_row(f"Mina {j + 1} ({variaveis[j]})", formatar(volume, 2))
    console.print(tabela)

    if any(volume < 0 for volume in volumes_por_mina):
        console.print("[yellow]Atenção: volume negativo — a demanda não é atendível com essas minas.")
    residuo = residuo_maximo(matriz, volumes_por_mina, dados.volumes_necessarios)
    console.print(f"Verificação: max|A·x − b| = {residuo:.2e}")
