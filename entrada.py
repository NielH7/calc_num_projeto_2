"""Leitura validada de números, listas e matrizes. Aceita vírgula decimal (0,55)."""

import math

from apresentacao import console


def converter_numero(texto: str) -> float:
    valor = float(texto.strip().replace(",", "."))
    if not math.isfinite(valor):
        raise ValueError
    return valor


def ler_numero(pergunta: str, positivo: bool = False) -> float:
    while True:
        try:
            valor = converter_numero(console.input(f"{pergunta}: "))
            if positivo and valor <= 0:
                raise ValueError
            return valor
        except ValueError:
            console.print("[red]Digite um número válido" + (" e positivo." if positivo else "."))


def ler_inteiro(pergunta: str, minimo: int = 1) -> int:
    while True:
        texto = console.input(f"{pergunta}: ").strip()
        if texto.isdigit() and int(texto) >= minimo:
            return int(texto)
        console.print(f"[red]Digite um inteiro maior ou igual a {minimo}.")


def ler_lista(pergunta: str, tamanho: int | None = None, minimo: int = 2) -> list[float]:
    """Valores separados por espaço ou ';'. Ex.: 0,55 0,25 0,25"""
    while True:
        texto = console.input(f"{pergunta}: ").replace(";", " ")
        try:
            valores = [converter_numero(parte) for parte in texto.split()]
        except ValueError:
            console.print("[red]Há um valor inválido. Separe os números por espaço ou ';'.")
            continue
        if tamanho is not None and len(valores) != tamanho:
            console.print(f"[red]Digite exatamente {tamanho} valores (você digitou {len(valores)}).")
        elif len(valores) < minimo:
            console.print(f"[red]Digite pelo menos {minimo} valor(es).")
        else:
            return valores


def ler_matriz(n: int, nome_da_linha: str = "Equação") -> list[list[float]]:
    return [ler_lista(f"  {nome_da_linha} {i + 1} ({n} coeficientes)", n) for i in range(n)]


def ler_opcao(pergunta: str, opcoes: set[str]) -> str:
    while True:
        opcao = console.input(f"{pergunta} ").strip()
        if opcao in opcoes:
            return opcao
        console.print(f"[red]Opção inválida. Escolha entre: {', '.join(sorted(opcoes))}.")
