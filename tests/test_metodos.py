import pytest

from calculo.ajuste import ajustar_reta, erro_quadratico
from calculo.diretos import eliminacao_de_gauss
from calculo.integracao import passo_constante, simpson_repetido, trapezio_repetido
from calculo.iterativos import aproximacao_inicial, criterio_de_sassenfeld, gauss_seidel


def test_gauss_resolve_sistema_2x2():
    assert eliminacao_de_gauss([[2, 1], [1, 3]], [5, 10]) == pytest.approx([1, 3])


def test_gauss_precisa_de_pivoteamento():
    assert eliminacao_de_gauss([[0, 1], [1, 0]], [2, 3]) == pytest.approx([3, 2])


def test_gauss_rejeita_sistema_singular():
    with pytest.raises(ValueError):
        eliminacao_de_gauss([[1, 2], [2, 4]], [3, 6])


def test_gauss_seidel_converge_para_solucao():
    matriz, termos = [[4, 1], [2, 5]], [9, 13]
    historico = gauss_seidel(matriz, termos, aproximacao_inicial(matriz, termos), 1e-8)
    assert historico[-1].solucao == pytest.approx([1.777777, 1.888888], abs=1e-5)


def test_sassenfeld():
    assert max(criterio_de_sassenfeld([[4, 1], [2, 5]])) < 1


def test_reta_exata():
    assert ajustar_reta([0, 1, 2], [1, 3, 5]) == pytest.approx((1, 2))
    assert erro_quadratico([1, 3, 5], [1, 3, 5]) == 0


def test_integracao_de_x_ao_quadrado():
    xs = [0, 0.5, 1, 1.5, 2]
    ys = [x ** 2 for x in xs]
    assert simpson_repetido(ys, 0.5) == pytest.approx(8 / 3)
    assert trapezio_repetido(ys, 0.5) == pytest.approx(2.75)


def test_simpson_rejeita_subintervalos_impares():
    with pytest.raises(ValueError):
        simpson_repetido([1, 2, 3, 4], 1)


def test_passo_constante_rejeita_pontos_desiguais():
    with pytest.raises(ValueError):
        passo_constante([0, 1, 3])
