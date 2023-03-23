# LendingProtocolAnalyzer


This project involves analyzing lending protocols, a popular protocol in the DeFi space. Borrowers deposit collateral to receive USDC loans from lenders who obtain tokens representing the value of the deposited collateral. It incorporates a liquidation system to protect lenders from losses due to price volatility. If the loan-to-value ratio of a position goes above 70%, the collateral is sold at face value and given to the lender.

The task is to write logic that takes in the starting and ending prices of ETH in USD and a list of triples containing information about loans. The function should output the initial and final net worths of users in terms of USD and an array indicating which loans get liquidated.



## Running Unit Tests
To run the unit tests for the LendingProtocolAnalyzer, execute the following command in the terminal:


```
python test_lending_protocol_analyzer.py

```

This will run the test suite and output the results. Make sure that the file `lending_protocol_analyzer.py` is in the same directory as `test_lending_protocol_analyzer.py` before running the command.

You can also view the test cases in the `test_lending_protocol_analyzer.py` file and modify them as needed.
