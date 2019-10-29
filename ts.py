import unittest
from pattern import Card


class TestCard(unittest.TestCase):
    def test_is_tcpair(self):
        cards = [(1, 2), (1, 2), (1, 3), (0, 3), (2, 5)]
        c = Card(cards)
        self.assertEqual(c.is_tcpair(), 3)

    def test_is_pair(self):
        cards = [(1, 2), (1, 2), (1, 3), (0, 4), (2, 5)]
        c = Card(cards)
        self.assertEqual(c.is_pair(), 2)
        cards2 = [(1, 2), (1, 9), (1, 3), (0, 4), (2, 5)]
        c = Card(cards2)
        self.assertFalse(c.is_tcpair())

    def test_is_triple(self):
        cards = [(1, 2), (1, 2), (1, 2), (0, 5), (3, 8)]
        c = Card(cards)
        self.assertEqual(c.is_triple(), 2)


if __name__ == '__main__':
    unittest.main()
