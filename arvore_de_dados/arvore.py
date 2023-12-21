class No:
    def __init__(self, valor, filhos=None):
        self.valor = valor
        if filhos is None:
            filhos = []
        self.filhos = filhos

def busca(no, valor):
    if no is None:
        return None
    if no.valor == valor:
        return no
    for filho in no.filhos:
        resultado = busca(filho, valor)
        if resultado is not None:
            return resultado
    return None

def remove(no_pai, no_filho):
    no_pai = busca(raiz, no_pai)
    no_filho = busca(raiz, no_filho)
    if no_pai is not None and no_filho is not None:
        no_pai.filhos.remove(no_filho)

def busca_profundidade(no):
    if no is None:
        return
    print(no.valor)
    for filho in no.filhos:
        busca_profundidade(filho)

import unittest

class TestNo(unittest.TestCase):
    def setUp(self):
        self.no_d = No("D")
        self.no_e = No("E")
        self.no_f = No("F")
        self.no_b = No("B", [self.no_d, self.no_e])
        self.no_c = No("C", [self.no_f])
        self.no_a = No("A", [self.no_b, self.no_c])

        self.raiz = self.no_a

    def test_valor(self):
        self.assertEqual(self.raiz.valor, "A")
        self.assertEqual(self.raiz.filhos[0].valor, "B")
        self.assertEqual(self.raiz.filhos[1].valor, "C")

    def test_filhos(self):
        self.assertEqual(self.raiz.filhos, [self.no_b, self.no_c])
        self.assertEqual(self.no_b.filhos, [self.no_d, self.no_e])
        self.assertEqual(self.no_c.filhos, [self.no_f])

    def test_busca_profundidade(self):
        visitados = []
        def visitar(no):
            print(no.valor)
            visitados.append(no.valor)
        busca_profundidade(self.raiz, visitar)
        self.assertEqual(visitados, ["A", "B", "D", "E", "C", "F"])

    def test_insercao(self):
        no_g = No("G")
        inserir("C", no_g)
        self.assertIn(no_g, self.no_c.filhos)

    def test_remocao(self):
        remove("C", "G")
        self.assertNotIn(self.no_g, self.no_c.filhos)
