import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    # ------------------------------------------------------------------
    # Standard service (existing behaviour must be preserved)
    # ------------------------------------------------------------------
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_standard_explicit_keyword(self):
        self.assertEqual(shipping_quote(2, "local", service="standard"), 8.0)

    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            shipping_quote(0, "local")

    # ------------------------------------------------------------------
    # Express service
    # ------------------------------------------------------------------
    def test_express_local(self):
        # express = standard + $7 surcharge
        self.assertEqual(shipping_quote(2, "local", service="express"), 15.0)

    def test_express_regional(self):
        self.assertEqual(shipping_quote(2, "regional", service="express"), 18.0)

    def test_express_different_weight(self):
        # 5 kg local standard = 5 + 7.5 = 12.5; express = 12.5 + 7 = 19.5
        self.assertEqual(shipping_quote(5, "local", service="express"), 19.5)

    def test_express_weight_must_be_positive(self):
        with self.assertRaises(ValueError):
            shipping_quote(0, "local", service="express")

    # ------------------------------------------------------------------
    # Unknown / invalid inputs
    # ------------------------------------------------------------------
    def test_unknown_zone(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "international")

    def test_unknown_service(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "local", service="overnight")
