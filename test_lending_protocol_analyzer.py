import unittest
from lending_protocol_analyzer import LendingProtocolAnalyzer


class TestLendingProtocolAnalyzer(unittest.TestCase):

    def setUp(self):
        self.LTV = 70
        self.loans = [
            {
                "id": 1,
                "borrower": "Alice",
                "lender": "Bob",
                "collateral": (1, "ETH"),
                "amountBorrowed": 1000,
                "outputToken": (100, "OUT-1")  # 1 AliceToken = 1/100 ETH = $20
            },

            {
                "id": 2,
                "borrower": "Bob",
                "lender": "Charlie",
                "collateral": (50, "OUT-1"),  # 50 * 20 = $1000
                "amountBorrowed": 400,
                "outputToken": (100, "OUT-2")  # 1000/100 = $10,   1 BobToken = 1/2 AliceToken = 1/200 ETH
            }
        ]
        self.starting_eth_price = 2000
        self.ending_eth_price = 1000
        self.analyzer = LendingProtocolAnalyzer(self.loans)

    def test_get_networths_in_usdc_and_liquidation_with_starting_eth_price(self):
        expected_starting = {'Alice': '1000 USDC', 'Bob': '1400.0 USDC', 'Charlie': '1000.0 USDC', 'liquidations': []}

        result_starting = self.analyzer.get_networths_in_usdc_and_liquidation(self.starting_eth_price, self.LTV)
        self.assertDictEqual(result_starting, expected_starting)

    def test_get_networths_in_usdc_and_liquidation_with_ending_eth_price(self):
        expected_ending = {'Alice': '1000 USDC', 'Bob': '900.0 USDC', 'Charlie': '500.0 USDC', 'liquidations': [0, 1]}

        result_ending = self.analyzer.get_networths_in_usdc_and_liquidation(self.ending_eth_price, self.LTV)
        self.assertDictEqual(result_ending, expected_ending)


if __name__ == '__main__':
    unittest.main()
