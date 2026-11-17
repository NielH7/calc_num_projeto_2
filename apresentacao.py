"""Console, formatação de números e exibição de sistemas lineares."""

from rich.console import Console
from rich.table import Table

console = Console()


def formatar(valor: float, casas: int = 4) -> str:
    """Formata no padrão brasileiro: 1234.5 -> 1.234,5000"""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


def formatar_cientifico(valor: float) -> str:
    return f"{valor:.3e}".replace(".", ",")


def nova_tabela(titulo: str, *colunas: str) -> Table:
    tabela = Table(title=titulo, title_style="bold cyan", header_style="bold")
    for coluna in colunas:
        tabela.add_column(coluna, justify="right")
    return tabela


def mostrar_sistema(matriz: list[list[float]], termos: list[float], variaveis: list[str]) -> None:
    console.print("[bold]Sistema linear:[/]")
    for linha, termo in zip(matriz, termos):
        parcelas = [_parcela(coeficiente, variavel, primeira=(j == 0))
                    for j, (coeficiente, variavel) in enumerate(zip(linha, variaveis))]
        console.print("  " + "".join(parcelas) + f" = {formatar(termo, 2)}")
    console.print()


def _parcela(coeficiente: float, variavel: str, primeira: bool) -> str:
    if coeficiente == 0:
        return " " * (len(variavel) + 11)
    sinal = "−" if coeficiente < 0 else ("" if primeira else "+")
    return f"{sinal:>2}{formatar(abs(coeficiente), 2):>7}{variavel} "
