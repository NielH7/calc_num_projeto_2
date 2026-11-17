"""Método direto: Eliminação de Gauss com pivoteamento parcial."""

LIMITE_DE_PIVO_NULO = 1e-12


def eliminacao_de_gauss(matriz: list[list[float]], termos: list[float]) -> list[float]:
    aumentada = [linha[:] + [termo] for linha, termo in zip(matriz, termos)]
    n = len(aumentada)
    for coluna in range(n):
        _trocar_pela_linha_de_maior_pivo(aumentada, coluna)
        pivo = aumentada[coluna][coluna]
        if abs(pivo) < LIMITE_DE_PIVO_NULO:
            raise ValueError("Sistema singular: não possui solução única.")
        for linha in range(coluna + 1, n):
            fator = aumentada[linha][coluna] / pivo
            aumentada[linha] = [a - fator * p for a, p in zip(aumentada[linha], aumentada[coluna])]
    return _substituicao_regressiva(aumentada)


def _trocar_pela_linha_de_maior_pivo(aumentada: list[list[float]], coluna: int) -> None:
    linha_do_pivo = max(range(coluna, len(aumentada)), key=lambda i: abs(aumentada[i][coluna]))
    aumentada[coluna], aumentada[linha_do_pivo] = aumentada[linha_do_pivo], aumentada[coluna]


def _substituicao_regressiva(triangular: list[list[float]]) -> list[float]:
    n = len(triangular)
    solucao = [0.0] * n
    for i in reversed(range(n)):
        soma = sum(triangular[i][j] * solucao[j] for j in range(i + 1, n))
        solucao[i] = (triangular[i][n] - soma) / triangular[i][i]
    return solucao


def residuo_maximo(matriz: list[list[float]], solucao: list[float], termos: list[float]) -> float:
    """max |A·x − b|: quanto menor, mais exata a solução."""
    return max(abs(sum(a * x for a, x in zip(linha, solucao)) - b)
               for linha, b in zip(matriz, termos))
