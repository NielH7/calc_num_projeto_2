"""Regras do Trapézio e de Simpson 1/3 repetidas para pontos igualmente espaçados."""


def trapezio_repetido(ys: list[float], h: float) -> float:
    """h/2 · [y₀ + 2(y₁ + … + yₙ₋₁) + yₙ]"""
    if len(ys) < 2:
        raise ValueError("São necessários pelo menos 2 pontos.")
    return h / 2 * (ys[0] + 2 * sum(ys[1:-1]) + ys[-1])


def simpson_repetido(ys: list[float], h: float) -> float:
    """h/3 · [y₀ + 4(ímpares) + 2(pares internos) + yₙ]"""
    subintervalos = len(ys) - 1
    if subintervalos < 2 or subintervalos % 2:
        raise ValueError("Simpson 1/3 exige número par de subintervalos (número ímpar de pontos).")
    return h / 3 * (ys[0] + 4 * sum(ys[1:-1:2]) + 2 * sum(ys[2:-1:2]) + ys[-1])


def passo_constante(xs: list[float]) -> float:
    """Retorna h e confere se os pontos são igualmente espaçados."""
    h = xs[1] - xs[0]
    if h <= 0 or any(abs((b - a) - h) > 1e-9 * abs(h) for a, b in zip(xs, xs[1:])):
        raise ValueError("Os valores de x devem ser crescentes e igualmente espaçados.")
    return h
