import pytest

from problemas import circuito, minas, moore, rio


def test_minas():
    assert minas.resolver(minas.DADOS_DO_ENUNCIADO) == pytest.approx([2416.67, 9193.33, 4690.0], abs=0.01)


def test_circuito():
    final = circuito.resolver(circuito.DADOS_DO_ENUNCIADO)[-1].solucao
    assert final == pytest.approx([0.1162, -3.9276, -1.1881, -0.5384, -4.6671], abs=1e-3)


def test_moore():
    ajuste = moore.resolver(moore.DADOS_DO_ENUNCIADO)
    assert ajuste.b1 == pytest.approx(0.13718, abs=1e-5)
    assert ajuste.prever(2010) == pytest.approx(6.08e8, rel=1e-2)
    assert ajuste.prever(2020) == pytest.approx(1.43e10, rel=1e-2)


def test_rio():
    area = rio.resolver(rio.DADOS_DO_ENUNCIADO)
    assert area.trapezio == pytest.approx(2592.5)
    assert area.simpson == pytest.approx(2773.0)
