from collections import defaultdict


class LendingProtocolAnalyzer:
    def __init__(self, loans):
        self.loans = loans
        self.individual_balances = self._calculate_balances()
        self.token_to_eth_conversion = self._token_to_eth()

    def _calculate_balances(self):
        balance = defaultdict(lambda: defaultdict(lambda: 0))
        for loan in self.loans:
            borrower_name = loan["borrower"]
            balance[borrower_name]["USDC"] += loan["amountBorrowed"]
            collateral_amount, collateral_token = loan["collateral"]
            output_amount, output_token = loan["outputToken"]
            lender_name = loan["lender"]
            balance[borrower_name][collateral_token] -= int(collateral_amount)  # outputToken/ethprice
            balance[lender_name][output_token] += int(output_amount)
        return balance

    def _token_to_eth(self):
        token_to_eth_conversion = {}

        for loan in self.loans:
            output_amount, output_token = loan["outputToken"]
            collateral_amount, collateral_token = loan["collateral"]

            if collateral_token == "ETH":
                token_to_eth_conversion[output_token] = collateral_amount / output_amount
            else:
                if collateral_token not in token_to_eth_conversion:
                    raise Exception("collateral token conversion unavailable")
                collateral_token_in_eth = token_to_eth_conversion[collateral_token] * collateral_amount
                token_to_eth_conversion[output_token] = collateral_token_in_eth / output_amount
        return token_to_eth_conversion

    def calculate_networths_in_usdc(self, eth_price):
        networths = defaultdict(lambda: 0)

        for individual, balances in self.individual_balances.items():
            for token, balance in balances.items():
                if token == "USDC":
                    networths[individual] += balance
                elif token == "ETH":
                    continue  # hardcoded to skip since the initial borrower's collateral isn't considered in this question
                else:
                    networths[individual] += balance * self.token_to_eth_conversion[token] * eth_price
        return networths

    def calculate_liquidation(self, target_ltv, eth_price):
        liquidations = []
        for i, loan in enumerate(self.loans):
            collateral_amount, collateral_token = loan["collateral"]
            if collateral_token != "ETH":
                collateral_amount = float(collateral_amount) * self.token_to_eth_conversion[collateral_token]

            borrowed_amount = int(loan["amountBorrowed"])

            ltv = borrowed_amount / (float(collateral_amount) * eth_price) * 100  # higher is worse
            if ltv > target_ltv:
                liquidations.append(i)
        return liquidations

    def get_networths_in_usdc_and_liquidation(self, eth_price, target_ltv):
        networths_and_liquidation_output = {}
        networths_dict = self.calculate_networths_in_usdc(eth_price)
        for individual, networth in networths_dict.items():
            networths_and_liquidation_output[individual] = str(networth) + " USDC"

        networths_and_liquidation_output["liquidations"] = self.calculate_liquidation(target_ltv, eth_price)

        return networths_and_liquidation_output
