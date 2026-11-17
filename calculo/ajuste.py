"""Mínimos quadrados: ajuste de uma reta y = b0 + b1·x."""


def ajustar_reta(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Resolve as equações normais e retorna (b0, b1)."""
    n = len(xs)
    if n < 2 or len(set(xs)) < 2:
        raise ValueError("São necessários pelo menos 2 valores de x diferentes.")
    soma_x, soma_y = sum(xs), sum(ys)
    soma_xx = sum(x * x for x in xs)
    soma_xy = sum(x * y for x, y in zip(xs, ys))
    b1 = (n * soma_xy - soma_x * soma_y) / (n * soma_xx - soma_x ** 2)
    b0 = (soma_y - b1 * soma_x) / n
    return b0, b1


def erro_quadratico(ys: list[float], ajustados: list[float]) -> float:
    """Σ [yᵢ − g(xᵢ)]²"""
    return sum((y - g) ** 2 for y, g in zip(ys, ajustados))


def coeficiente_r2(ys: list[float], ajustados: list[float]) -> float:
    media = sum(ys) / len(ys)
    variacao_total = sum((y - media) ** 2 for y in ys)
    return 1 - erro_quadratico(ys, ajustados) / variacao_total
