import unittest

from pymaze.solver import Solver


class TestSolver(unittest.TestCase):
    def test_ctor(self):
        solver = Solver("", "", False)

        self.assertEqual(solver.name, "")
        self.assertEqual(solver.quiet_mode, False)


if __name__ == "__main__":
    unittest.main()
