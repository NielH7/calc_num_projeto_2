"""Menu principal e fluxo de cada questão."""

from rich.panel import Panel

from apresentacao import console
from entrada import ler_opcao
from problemas import circuito, minas, moore, rio

QUESTOES = {"1": minas, "2": circuito, "3": moore, "4": rio}
OPCAO_SOBRE = "5"
OPCAO_SAIR = "0"

TEXTO_SOBRE_OS_METODOS = """\
[bold]Eliminação de Gauss (direto)[/] – zera os elementos abaixo da diagonal e resolve por
  substituição regressiva. Pivoteamento parcial: usa como pivô o maior |aᵢₖ| da coluna.

[bold]Gauss-Seidel (iterativo)[/] – xᵢ⁽ᵏ⁺¹⁾ = (bᵢ − Σⱼ≠ᵢ aᵢⱼxⱼ) / aᵢᵢ, já usando os valores novos.
  Para quando max|xᵏ − xᵏ⁻¹| / max|xᵏ| < ε. Converge se max βᵢ < 1 (Sassenfeld).

[bold]Mínimos quadrados[/] – reta y = b0 + b1·x que minimiza Σ[yᵢ − g(xᵢ)]².
  Para crescimento exponencial, ajusta-se a reta em log10(y).

[bold]Trapézio repetido[/] – A ≈ h/2·[y₀ + 2(y₁+…+yₙ₋₁) + yₙ]
[bold]Simpson 1/3 repetido[/] – A ≈ h/3·[y₀ + 4(ímpares) + 2(pares) + yₙ], n par."""


def executar() -> None:
    try:
        _menu_principal()
    except (KeyboardInterrupt, EOFError):
        console.print()
    console.print("[bold]Até logo![/]")


def _menu_principal() -> None:
    console.print(Panel.fit("[bold]Atividade Complementar – Cálculo Numérico 2026.2[/]\n"
                            "Questões 01.3 · 02.3 · 03.1 · 04.2", border_style="cyan"))
    while True:
        console.print("\n[bold]Menu principal[/]")
        for numero, questao in QUESTOES.items():
            console.print(f"  {numero}) {questao.TITULO}")
        console.print(f"  {OPCAO_SOBRE}) Sobre os métodos\n  {OPCAO_SAIR}) Sair")
        opcao = ler_opcao("Escolha:", set(QUESTOES) | {OPCAO_SOBRE, OPCAO_SAIR})
        if opcao == OPCAO_SAIR:
            return
        if opcao == OPCAO_SOBRE:
            console.print(Panel(TEXTO_SOBRE_OS_METODOS, title="Métodos", border_style="cyan"))
        elif not _executar_questao(QUESTOES[opcao]):
            return


def _executar_questao(questao) -> bool:
    """Retorna False quando o usuário escolhe sair do programa."""
    while True:
        console.print(Panel(questao.ENUNCIADO, title=questao.TITULO, border_style="cyan"))
        console.print("  1) Usar os dados do enunciado\n  2) Digitar novos dados")
        if ler_opcao("Escolha:", {"1", "2"}) == "1":
            dados = questao.DADOS_DO_ENUNCIADO
        else:
            dados = questao.ler_novos_dados()
        try:
            questao.mostrar(dados, questao.resolver(dados))
        except (ValueError, ZeroDivisionError, OverflowError) as erro:
            console.print(f"[red]Não foi possível calcular: {erro}")

        console.print("\n  1) Novo cálculo  2) Voltar ao menu  0) Sair")
        acao = ler_opcao("Escolha:", {"1", "2", "0"})
        if acao != "1":
            return acao == "2"
