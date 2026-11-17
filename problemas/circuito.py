"""Questão 02.3: correntes de malha de um circuito (Gauss-Seidel)."""

from dataclasses import dataclass

from apresentacao import console, formatar, mostrar_sistema, nova_tabela
from calculo.iterativos import (Iteracao, aproximacao_inicial, criterio_de_sassenfeld,
                                gauss_seidel)
from entrada import ler_inteiro, ler_lista, ler_matriz, ler_numero

TITULO = "02.3 – Correntes de malha em um circuito (Método iterativo: Gauss-Seidel)"
ENUNCIADO = """\
Lei das malhas de Kirchhoff (todas as correntes no sentido horário, ΣRi = ΣE):
  Malha 1:  5i1 + 2,5(i1 − i2) + 2(i1 − i4)              =  12
  Malha 2:  2,5(i2 − i1) + 3,5(i2 − i3) + 5(i2 − i5)      = −16
  Malha 3:  3,5(i3 − i2) + 8i3 + 4(i3 − i5)               =  14
  Malha 4:  2(i4 − i1) + 3(i4 − i5) + 2i4                 =  10
  Malha 5:  5(i5 − i2) + 4(i5 − i3) + 3(i5 − i4)          = −30
x⁰ = bᵢ/aᵢᵢ e precisão 0,0001."""


@dataclass
class DadosCircuito:
    matriz: list[list[float]]
    termos: list[float]
    precisao: float


DADOS_DO_ENUNCIADO = DadosCircuito(
    matriz=[[9.5, -2.5, 0, -2, 0],
            [-2.5, 11, -3.5, 0, -5],
            [0, -3.5, 15.5, 0, -4],
            [-2, 0, 0, 7, -3],
            [0, -5, -4, -3, 12]],
    termos=[12, -16, 14, 10, -30],
    precisao=1e-4,
)


def resolver(dados: DadosCircuito) -> list[Iteracao]:
    inicial = aproximacao_inicial(dados.matriz, dados.termos)
    return gauss_seidel(dados.matriz, dados.termos, inicial, dados.precisao)


def ler_novos_dados() -> DadosCircuito:
    n = ler_inteiro("Número de malhas", minimo=2)
    console.print("Coeficientes de cada equação de malha (resistências):")
    matriz = ler_matriz(n, "Malha")
    termos = ler_lista(f"Termos independentes – tensões ({n} valores)", n)
    precisao = ler_numero("Precisão (ex.: 0,0001)", positivo=True)
    return DadosCircuito(matriz, termos, precisao)


def mostrar(dados: DadosCircuito, historico: list[Iteracao]) -> None:
    n = len(dados.termos)
    nomes = [f"i{k + 1}" for k in range(n)]
    mostrar_sistema(dados.matriz, dados.termos, nomes)
    _mostrar_criterio(dados.matriz)

    tabela = nova_tabela("Iterações de Gauss-Seidel", "k", *nomes, "Erro relativo")
    for iteracao in historico:
        erro = "—" if iteracao.erro_relativo is None else f"{iteracao.erro_relativo:.2e}"
        tabela.add_row(str(iteracao.numero), *(formatar(v) for v in iteracao.solucao), erro)
    console.print(tabela)

    final = historico[-1]
    if final.erro_relativo is not None and final.erro_relativo < dados.precisao:
        console.print(f"[green]Convergiu em {final.numero} iterações.")
    else:
        console.print("[red]Não convergiu no máximo de iterações.")
    for nome, corrente in zip(nomes, final.solucao):
        sentido = "anti-horário" if corrente < 0 else "horário"
        console.print(f"  {nome} = {formatar(corrente)} A  ({formatar(abs(corrente))} A no sentido {sentido})")


def _mostrar_criterio(matriz: list[list[float]]) -> None:
    betas = criterio_de_sassenfeld(matriz)
    texto = ", ".join(f"β{i + 1}={formatar(b, 3)}" for i, b in enumerate(betas))
    if max(betas) < 1:
        console.print(f"Critério de Sassenfeld: {texto} → max β < 1, [green]convergência garantida[/].\n")
    else:
        console.print(f"Critério de Sassenfeld: {texto} → [yellow]convergência não garantida[/].\n")
