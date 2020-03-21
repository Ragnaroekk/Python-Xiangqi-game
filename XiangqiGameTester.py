# Author: Ray Franklin
# Date: 03/01/2020
# Description: a file that contains unit tests for the XiangqiGame.py file.

import unittest
import XiangqiGame as Game


class TestStore(unittest.TestCase):
    """Contains unit tests for the Xiangqi.py file"""

    def test_1(self):
        """A test to ensure you can't move from and to the same location."""
        g1 = Game.XiangqiGame()
        self.assertFalse(g1.make_move("a1", "a1"))

    def test_2(self):
        """A test to ensure the wrong player can't move the other's piece."""
        g1 = Game.XiangqiGame()
        self.assertFalse(g1.make_move("e10", "e9"))

    def test_3(self):
        """A test to confirm a piece was moved to the new location."""
        g1 = Game.XiangqiGame()
        piece = g1.get_game_board().get_game_piece_by_location(9, 4)
        g1.make_move("e1", "e2")
        self.assertEqual(g1.get_game_board().get_game_piece_by_location(8, 4), piece)

    def test_4(self):
        """A test to ensure you can't land on your own piece"""
        g1 = Game.XiangqiGame()
        g1.make_move("e1", "d1")
        with self.subTest():
            self.assertEqual(g1.make_move("e1", "d1"), False)
        with self.subTest():
            self.assertEqual(g1.get_game_board().get_game_piece_color_by_location(9, 4), "Red")

    def test_5(self):
        """A test to ensure the General can't move outside of its moveset"""
        g1 = Game.XiangqiGame()
        g1.make_move("e4", "e5")  # red moves
        g1.make_move("e10", "e9")  # black moves
        g1.make_move("e1", "e2")  # red moves
        g1.make_move("e9", "f9")  # black moves
        g1.make_move("e2", "e3")  # red moves
        with self.subTest():
            self.assertEqual(g1.make_move("f9", "g9"), False)  # black moves
            g1.make_move("f9", "e9")  # black moves
        with self.subTest():
            self.assertEqual(g1.make_move("e3", "e4"), False)  # red moves

    def test_6(self):
        """A test to ensure the Advisor can't move outside of its moveset"""
        g1 = Game.XiangqiGame()
        g1.make_move("e4", "e5")  # red moves
        g1.make_move("d10", "e9")  # black moves
        g1.make_move("f1", "e2")  # red moves
        g1.make_move("e9", "d8")  # black moves
        g1.make_move("e2", "f3")  # red moves
        with self.subTest():
            self.assertEqual(g1.make_move("d8", "c9"), False)  # black moves
            g1.make_move("d8", "e9")  # black moves
        with self.subTest():
            self.assertEqual(g1.make_move("f3", "e4"), False)  # red moves

    def test_7(self):
        """A test to ensure the Elephant can't move outside of its moveset"""
        g1 = Game.XiangqiGame()
        g1.make_move("c1", "e3")  # red moves
        g1.make_move("c10", "e8")  # black moves
        g1.make_move("e3", "c5")  # red moves
        g1.make_move("e8", "g6")  # black moves
        with self.subTest():
            self.assertEqual(g1.make_move("c5", "e7"), False)  # red moves
            g1.make_move("c5", "e3")  # red moves
        with self.subTest():
            self.assertEqual(g1.make_move("g6", "i4"), False)  # black moves

    def test_8(self):
        """A test to ensure the Soldier can't move outside of its moveset"""
        g1 = Game.XiangqiGame()
        with self.subTest():
            self.assertEqual(g1.make_move("e4", "e3"), False)  # red moves
        with self.subTest():
            self.assertEqual(g1.make_move("e4", "f4"), False)  # red moves

    def test_9(self):
        """A test to ensure the General can't move beyond 1 space"""
        g1 = Game.XiangqiGame()
        with self.subTest():
            self.assertEqual(g1.make_move("e1", "e3"), False)  # red moves
        with self.subTest():
            self.assertEqual(g1.make_move("e4", "d2"), False)  # red moves

    def test_10(self):
        """A test to see if the elephant is blocked correctly, upper right"""
        g1 = Game.XiangqiGame()
        g1.make_move("c1", "e3")  # red
        g1.make_move("h8", "f8")  # black
        g1.make_move("e1", "e2")  # red
        g1.make_move("f8", "f4")  # black
        with self.subTest():
            self.assertNotIn("g5", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())
        with self.subTest():
            self.assertNotIn("g1", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())
        with self.subTest():
            self.assertIn("c5", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())
        with self.subTest():
            self.assertIn("c1", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())

    def test_11(self):
        """A test to see if the elephant is blocked correctly, upper left"""
        g1 = Game.XiangqiGame()
        g1.make_move("c1", "e3")  # red
        g1.make_move("b8", "d8")  # black
        g1.make_move("e1", "e2")  # red
        g1.make_move("d8", "d4")  # black
        with self.subTest():
            self.assertNotIn("c5", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())
        with self.subTest():
            self.assertNotIn("g1", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())
        with self.subTest():
            self.assertIn("g5", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())
        with self.subTest():
            self.assertIn("c1", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())

    def test_12(self):
        """A test to see if the elephant is blocked correctly, lower left"""
        g1 = Game.XiangqiGame()
        g1.make_move("c1", "e3")  # red
        g1.make_move("b8", "d8")  # black
        g1.make_move("e1", "e2")  # red
        g1.make_move("d8", "d2")  # black
        with self.subTest():
            self.assertNotIn("c1", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())
        with self.subTest():
            self.assertNotIn("g1", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())
        with self.subTest():
            self.assertIn("g5", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())
        with self.subTest():
            self.assertIn("c5", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())

    def test_13(self):
        """A test to see if the elephant is blocked correctly, upper right"""
        g1 = Game.XiangqiGame()
        g1.make_move("c1", "e3")  # red
        g1.make_move("h8", "f8")  # black
        g1.make_move("e1", "e2")  # red
        g1.make_move("f8", "f2")  # black
        with self.subTest():
            self.assertNotIn("g1", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())
        with self.subTest():
            self.assertIn("g5", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())
        with self.subTest():
            self.assertIn("c5", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())
        with self.subTest():
            self.assertIn("c1", g1.get_game_board().get_game_piece_by_location(7, 4).get_legal_moves())

    def test_14(self):
        """A test to see if the horse is blocked correctly"""
        g1 = Game.XiangqiGame()
        g1.make_move("b1", "c3")  # red
        g1.make_move("b8", "c8")  # black
        g1.make_move("h3", "d3")  # red
        g1.make_move("c8", "b8")  # black
        g1.make_move("a1", "a2")  # red
        g1.make_move("b8", "c8")  # black
        g1.make_move("a2", "c2")  # red
        self.assertEqual([], g1.get_game_board().get_game_piece_by_location(7, 2).get_legal_moves())

    def test_15(self):
        """A test to check if chariot can attack correctly and move correctly"""
        g1 = Game.XiangqiGame()
        g1.make_move("a1", "a2")  # red
        g1.make_move("a10", "a9")  # black
        g1.make_move("e1", "e2")  # red
        g1.make_move("a9", "f9")  # black
        g1.make_move("a2", "d2")
        g1.make_move("a7", "a6")
        g1.make_move("d2", "d9")
        g1.make_move("b8", "b9")
        with self.subTest():
            self.assertEqual(['d8', 'd7', 'd6', 'd5', 'd4', 'd3', 'd2', 'c9', 'e9', 'b9', 'f9', 'd10'],
                             g1.get_game_board().get_game_piece_by_location(1, 3).get_legal_moves())
        with self.subTest():
            self.assertEqual(['f8', 'f7', 'f6', 'f5', 'f4', 'f3', 'f2', 'e9', 'g9', 'h9', 'i9', 'd9', 'f1'],
                             g1.get_game_board().get_game_piece_by_location(1, 5).get_legal_moves())

    def test_16(self):
        """A test to check if the cannon can attack correctly and move correctly"""
        g1 = Game.XiangqiGame()
        g1.make_move("h3", "f3")  # red moves
        g1.make_move("h8", "h7")  # black moves
        g1.make_move("f3", "f7")  # red moves
        g1.make_move("b8", "f8")  # black moves
        g1.make_move("b3", "f3")  # red moves
        with self.subTest():
            self.assertEqual(['h9', 'h8', 'h6', 'h5', 'h4', 'h3', 'h2', 'f7'],
                             g1.get_game_board().get_game_piece_by_location(3, 7).get_legal_moves())
        with self.subTest():
            self.assertEqual(['f9', 'a8', 'b8', 'c8', 'd8', 'e8', 'g8', 'h8', 'i8', 'f6', 'f5', 'f4', 'f3'],
                             g1.get_game_board().get_game_piece_by_location(2, 5).get_legal_moves())
        with self.subTest():
            self.assertEqual(['f6', 'f5', 'f4', 'd7', 'c7', 'h7', 'f9', 'f10', 'f2'],
                             g1.get_game_board().get_game_piece_by_location(3, 5).get_legal_moves())
        with self.subTest():
            self.assertEqual(['f6', 'f5', 'f4', 'f2', 'a3', 'b3', 'c3', 'd3', 'e3', 'g3', 'h3', 'i3', 'f8'],
                             g1.get_game_board().get_game_piece_by_location(7, 5).get_legal_moves())

    def test_17(self):
        """A test to check soldier movement before and after the final row"""
        g1 = Game.XiangqiGame()
        g1.make_move("c4", "c5")  # red moves
        g1.make_move("g7", "g6")  # black moves
        g1.make_move("c5", "c6")  # red moves
        g1.make_move("g6", "g5")  # black moves
        g1.make_move("c6", "c7")  # red moves
        g1.make_move("g5", "g4")  # black moves
        g1.make_move("c7", "c8")  # red moves
        g1.make_move("g4", "g3")  # black moves
        g1.make_move("c8", "c9")  # red moves
        g1.make_move("g3", "g2")  # black moves
        g1.make_move("c9", "c10")  # red moves
        with self.subTest():
            self.assertEqual(['d10', 'b10'], g1.get_game_board().get_game_piece_by_location(0, 2).get_legal_moves())
        with self.subTest():
            self.assertEqual(['h2', 'f2', 'g1'], g1.get_game_board().get_game_piece_by_location(8, 6).get_legal_moves())

    def test_18(self):
        """A test to check the flying general rules"""
        g1 = Game.XiangqiGame()
        g1.make_move("e1", "e2")  # red moves
        g1.make_move("e10", "e9")  # black moves
        g1.make_move("e2", "d2")  # red moves
        with self.subTest():
            self.assertEqual(['d8', 'd9'],
                             g1.get_game_board().get_game_piece_by_location(8, 3).get_flying_moves())
        with self.subTest():
            self.assertEqual(['f9', 'e8', 'e10'],
                             g1.get_game_board().get_game_piece_by_location(1, 4).get_legal_moves())

    def test_19(self):
        """A test to check the General's check status"""
        g1 = Game.XiangqiGame()
        g1.make_move("b3", "e3")  # red moves
        g1.make_move("a10", "a9")  # black moves
        g1.make_move("e3", "e7")  # red moves
        g1.make_move("a9", "e9")  # black moves
        g1.make_move("e7", "d7")  # red moves
        g1.make_move("e9", "e4")  # black moves
        g1.make_move("a1", "a2")  # red moves
        with self.subTest():
            self.assertEqual(True, g1.is_in_check("Red"))
        with self.subTest():
            self.assertEqual(False, g1.is_in_check("Black"))

    def test_20(self):
        """A test to check if red won is correct"""
        g1 = Game.XiangqiGame()
        g1.make_move("a1", "a2")  # red
        g1.make_move("a10", "a9")  # black
        g1.make_move("e1", "e2")  # red
        g1.make_move("a9", "a10")  # black
        g1.make_move("a2", "d2")  # red
        g1.make_move("a7", "a6")
        g1.make_move("d2", "d9")  # red
        g1.make_move("b8", "b9")
        g1.make_move("e2", "d2")  # red
        g1.make_move("b9", "b8")
        g1.make_move("d9", "d10")  # red
        g1.make_move("b8", "b9")
        g1.make_move("e4", "e5")  # red
        g1.make_move("b9", "b8")
        g1.make_move("e5", "e6")  # red
        g1.make_move("b8", "b9")
        g1.make_move("e6", "e7")  # red
        g1.make_move("b9", "b8")
        g1.make_move("b3", "e3")
        self.assertEqual("RED_WON", g1.get_game_state())
