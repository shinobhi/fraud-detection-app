import unittest

from src.fraud_rules import derive_signals


class DeriveSignalsTests(unittest.TestCase):
    def test_derives_all_configured_signals(self):
        signals = derive_signals(
            {
                "country": "US",
                "ip_country": "RO",
                "card_country": "CA",
                "prior_accounts_from_ip": 8,
                "payment_attempts_last_hour": 5,
            }
        )

        self.assertEqual(len(signals), 4)
        self.assertIn("IP country (RO) does not match account country (US).", signals)
        self.assertIn("Card country (CA) does not match account country (US).", signals)

    def test_returns_no_signals_at_thresholds(self):
        signals = derive_signals(
            {
                "country": "US",
                "ip_country": "US",
                "card_country": "US",
                "prior_accounts_from_ip": 4,
                "payment_attempts_last_hour": 4,
            }
        )

        self.assertEqual(signals, [])


if __name__ == "__main__":
    unittest.main()
