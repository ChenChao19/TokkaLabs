import asyncio

from service.TransactionProcessSubscriber import TransactionProcessSubscriber
from service.dataLoader.binance.binance import BinanceLoader
from service.dataLoader.etherscan.etherscan import EtherscanLoader
from util.logger import setup_logger

async def main():
    setup_logger("main.log")
    # Initialize both loaders
    binance_loader = BinanceLoader()
    etherscan_loader = EtherscanLoader()
    transaction_process_subscriber = TransactionProcessSubscriber()

    # Run both loaders concurrently
    # This will run both the Binance and Etherscan loaders indefinitely
    await asyncio.gather(
        binance_loader.run_forever(),
        etherscan_loader.run_forever(),
        transaction_process_subscriber.run_forever()
    )

if __name__ == "__main__":
    asyncio.run(main())