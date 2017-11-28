#!/usr/bin/env python3
# -*-coding:utf-8 -*

import unittest

from eccw.physics.eccw_compute import EccwCompute


class TestEccwCompute(unittest.TestCase):

    def test_compression(self):
        foo = EccwCompute(phiB=30, phiD=10, beta=0, alpha=3.43653, context="c")
        a1, a2 = foo.compute("alpha")
        self.assertAlmostEqual(a1, 3.4365, places=3)
        self.assertAlmostEqual(a2, 23.9463, places=3)
        b1, b2 = foo.compute("beta")
        self.assertAlmostEqual(b1, 0.0000, places=3)
        self.assertAlmostEqual(b2, 69.6780, places=3)
        phiB1, phiB2 = foo.compute("phiB")
        self.assertAlmostEqual(phiB1, 30.000, places=3)
        self.assertEqual(phiB2, None)
        phiD1, phiD2 = foo.compute("phiD")
        self.assertAlmostEqual(phiD1, 10.000, places=3)
        self.assertAlmostEqual(phiD2, 1.1494, places=3)

    def test_compression_off_domain(self):
        foo = EccwCompute(phiB=30, phiD=10, beta=-20, alpha=31, context="c")
        a1, a2 = foo.compute("alpha")
        self.assertEqual(a1, None)
        self.assertEqual(a2, None)
        b1, b2 = foo.compute("beta")
        self.assertEqual(b1, None)
        self.assertEqual(b2, None)
        phiB1, phiB2 = foo.compute("phiB")
        self.assertEqual(phiB1, None)
        self.assertEqual(phiB2, None)
        phiD1, phiD2 = foo.compute("phiD")
        self.assertEqual(phiD1, None)
        self.assertEqual(phiD2, None)

    def test_compression_fluids(self):
        foo = EccwCompute(phiB=30, phiD=10, beta=0, alpha=3.8353, context="c",
                          rho_f=1000, rho_sr=3500,
                          delta_lambdaB=0.5, delta_lambdaD=0.3)
        a1, a2 = foo.compute("alpha")
        self.assertAlmostEqual(a1, 3.8353, places=3)
        self.assertAlmostEqual(a2, 6.7608, places=3)
        b1, b2 = foo.compute("beta")
        self.assertAlmostEqual(b1, 0., places=3)
        self.assertAlmostEqual(b2, 58.9149, places=3)
        phiB1, phiB2 = foo.compute("phiB")
        self.assertAlmostEqual(phiB1, 30.000, places=3)
        # TODO: is this results meaningfull ?? 
        # There is no possible value with these parameters in the normal domain
        self.assertAlmostEqual(phiB2, 30.000, places=3)
        phiD1, phiD2 = foo.compute("phiD")
        self.assertAlmostEqual(phiD1, 10.000, places=3)
        self.assertAlmostEqual(phiD2, 5.3915, places=3)

    # def test_extension(self):
    #     foo = EccwCompute(phiB=30, phiD=10, beta=20, alpha=9.4113, context="e")
    #     a1, a2 = foo.compute("alpha")
    #     self.assertAlmostEqual(a1,  -16.2620, places=3)
    #     self.assertAlmostEqual(a2, 9.4112, places=3)
    #     b1, b2 = foo.compute("beta")
    #     self.assertAlmostEqual(b1, 20.0000, places=3)
    #     self.assertAlmostEqual(b2, 89.6779, places=3)
    #     phiB1, phiB2 = foo.compute("phiB")
    #     self.assertEqual(phiB1, None)
    #     self.assertAlmostEqual(phiB2, 30.0, places=3)
    #     phiD1, phiD2 = foo.compute("phiD")
    #     self.assertAlmostEqual(phiD1, 29.6651, places=3)
    #     self.assertAlmostEqual(phiD2, 10.0, places=3)

    # def test_change_params(self):
    #     foo = EccwCompute(phiB=30, phiD=10, beta=0, alpha=3.43653, context="c")
    #     foo.context = "e"
    #     foo.beta = 20
    #     foo.alpha = 9.4113
    #     a1, a2 = foo.compute("alpha")
    #     self.assertAlmostEqual(a1,  -16.2620, places=3)
    #     self.assertAlmostEqual(a2, 9.4112, places=3)
    #     b1, b2 = foo.compute("beta")
    #     self.assertAlmostEqual(b1, 20.0000, places=3)
    #     self.assertAlmostEqual(b2, 89.6779, places=3)
    #     phiB1, phiB2 = foo.compute("phiB")
    #     self.assertEqual(phiB1, None)
    #     self.assertAlmostEqual(phiB2, 30.0, places=3)
    #     phiD1, phiD2 = foo.compute("phiD")
    #     self.assertAlmostEqual(phiD1, 29.6651, places=3)
    #     self.assertAlmostEqual(phiD2, 10.0, places=3)

if __name__ == '__main__':
    unittest.main()
