"""Método iterativo de Gauss-Seidel e critério de convergência de Sassenfeld."""

from dataclasses import dataclass

MAXIMO_DE_ITERACOES = 500


@dataclass
class Iteracao:
    numero: int
    solucao: list[float]
    erro_relativo: float | None


def aproximacao_inicial(matriz: list[list[float]], termos: list[float]) -> list[float]:
    """x⁰ᵢ = bᵢ / aᵢᵢ"""
    return [termos[i] / matriz[i][i] for i in range(len(termos))]


def criterio_de_sassenfeld(matriz: list[list[float]]) -> list[float]:
    """Retorna os βᵢ. Se max(βᵢ) < 1, Gauss-Seidel converge para qualquer x⁰."""
    betas = []
    for i, linha in enumerate(matriz):
        soma = sum(abs(linha[j]) * betas[j] for j in range(i))
        soma += sum(abs(linha[j]) for j in range(i + 1, len(linha)))
        betas.append(soma / abs(linha[i]))
    return betas


def gauss_seidel(matriz: list[list[float]], termos: list[float], solucao_inicial: list[float],
                 precisao: float, maximo_de_iteracoes: int = MAXIMO_DE_ITERACOES) -> list[Iteracao]:
    """Para quando max|xᵏ − xᵏ⁻¹| / max|xᵏ| < precisão. Retorna todas as iterações."""
    if any(matriz[i][i] == 0 for i in range(len(matriz))):
        raise ValueError("Há zero na diagonal principal: reordene as equações.")
    x = solucao_inicial[:]
    historico = [Iteracao(0, x[:], None)]
    for numero in range(1, maximo_de_iteracoes + 1):
        anterior = x[:]
        for i, linha in enumerate(matriz):
            soma = sum(linha[j] * x[j] for j in range(len(x)) if j != i)
            x[i] = (termos[i] - soma) / linha[i]
        erro = _erro_relativo(x, anterior)
        historico.append(Iteracao(numero, x[:], erro))
        if erro < precisao:
            break
    return historico


def _erro_relativo(atual: list[float], anterior: list[float]) -> float:
    maior_diferenca = max(abs(a - b) for a, b in zip(atual, anterior))
    maior_valor = max(abs(a) for a in atual)
    return maior_diferenca / maior_valor if maior_valor else maior_diferenca
