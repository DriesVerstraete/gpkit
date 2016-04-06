import numpy.testing as npt
from gpkit import Model
from gpkit.constraints.breakdown import Breakdown
from gpkit.small_scripts import mag
import gpkit

w22value = 2 if not gpkit.units else 0.449617

TEST ={'w': {'w1': {'w11':[3, "N"], 'w12':{'w121':[2, "N"], 'w122':[6, "N"]}},
              'w2': {'w21':[1, "N"], 'w22':[w22value, "lbf"]}, 'w3':[1, "N"]}}


BD = Breakdown(TEST, "N")
m = Model(BD.root, BD)
sol = m.solve()
npt.assert_almost_equal(mag(sol('w')), 15, decimal=5)
npt.assert_almost_equal(mag(sol('w1')), 11, decimal=5)
npt.assert_almost_equal(mag(sol('w2')), 3, decimal=5)
npt.assert_almost_equal(mag(sol('w3')), 1, decimal=5)
npt.assert_almost_equal(mag(sol('w11')), 3, decimal=5)
npt.assert_almost_equal(mag(sol('w12')), 8, decimal=5)
npt.assert_almost_equal(mag(sol('w121')), 2, decimal=5)
npt.assert_almost_equal(mag(sol('w122')), 6, decimal=5)
npt.assert_almost_equal(mag(sol('w21')), 1, decimal=5)
npt.assert_almost_equal(mag(sol('w22')), w22value, decimal=5)

BD.make_diagram(sol)