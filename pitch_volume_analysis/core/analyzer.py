import operator
import sys
import traceback


class Analyzer:
    """Analyzer class computes all stock symbols. Scans order messages and computes stock volume.
    Provides a function to display the top ten stock symbols based on volume.
    """

    dataset_path: str = None
    ledger: dict = {}
    symbol_book: dict = {}

    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path

    def read_file(self) -> None:
        """Main event loop. Reads data file and preforms operations to determine stock volume."""
        try:
            with open(self.dataset_path, "r") as file:
                for line in file:
                    entry: str = line.strip()
                    message_type: str = self.get_message_type(entry)
                    message: list[str] = self.parse_order_message(entry, message_type)
                    try:
                        message_symbol: str = self.get_message_symbol(message, message_type)
                    except:
                        print("Unrecognized message format! Skipping...")
                        continue

                    # "X" and "E" messages do not have stock symbols.
                    if message_type != "X" and message_type != "E":
                        self.track_symbol(message)

                    self.compute_message(message, message_type, message_symbol)

        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.dataset_path} not found")
        except IndexError:
            print("Error: Incorrect file format or unrecognized order message")
            sys.exit(1)
        except ValueError:
            print("Value calculation error detected!")
            print(
                "Check the dataset for following proper PITCH transaction rules and/or correctness of math operations within code."
            )
            sys.exit(1)
        except:
            traceback.print_exc()
            sys.exit(1)

    def get_message_type(self, entry: str) -> str:
        """Finds message type and return it's value."""
        return entry[9]

    def get_message_symbol(self, message: list[str], message_type: str) -> str:
        """Parses message and returns it's stock symbol."""
        match message_type:
            case "E":
                symbol = None
            case "X":
                symbol = None
            case default:
                symbol: str = message[5]
        return symbol

    # TODO add more types
    def parse_order_message(self, entry: str, type: str) -> list[str]:
        """Reads in entry string and returns a list called a message.

        The message returned can vary based on message type.
        The list returned contains indexed components based on Cboe PITCH specifications.

        Using a match statement structure, will allow for easy addition of additional PITCH order messages.
        """
        message: list[str] = []
        match (type):
            case "A":  # Add Order (short)
                time_stamp: str = entry[1:9]
                message_type: str = entry[9]
                order_id: str = entry[10:22]
                side_indicator: str = entry[22]
                shares: str = entry[23:29]
                stock_symbol: str = entry[29:35].strip()
                price: str = entry[35:45]
                reserved: str = entry[45]
                message = [
                    time_stamp,
                    message_type,
                    order_id,
                    side_indicator,
                    shares,
                    stock_symbol,
                    price,
                    reserved,
                ]
            case "1":  # Add Order (extended)
                time_stamp: str = entry[1:9]
                message_type: str = entry[9]
                order_id: str = entry[10:22]
                side_indicator: str = entry[22]
                shares: str = entry[23:29]
                stock_symbol: str = entry[29:37].strip()
                price: str = entry[37:51]
                display: str = entry[51]
                participant_id: str = entry[52:56]
                customer_indicator: str = entry[56]
                message = [
                    time_stamp,
                    message_type,
                    order_id,
                    side_indicator,
                    shares,
                    stock_symbol,
                    price,
                    display,
                    participant_id,
                    customer_indicator,
                ]
            case "E":  # Order executed
                time_stamp: str = entry[1:9]
                message_type: str = entry[9]
                order_id: str = entry[10:22]
                executed_shares: str = entry[22:28]
                execution_id: str = entry[28:40]
                message = [time_stamp, message_type, order_id, executed_shares, execution_id]
            case "X":  # Order cancel
                time_stamp: str = entry[1:9]
                message_type: str = entry[9]
                order_id: str = entry[10:22]
                canceled_shares: str = entry[22:28]
                message = [time_stamp, message_type, order_id, canceled_shares]
            case "P":  # Trade (short)
                time_stamp: str = entry[1:9]
                message_type: str = entry[9]
                order_id: str = entry[10:22]
                side_indicator: str = entry[22]
                shares: str = entry[23:29]
                stock_symbol: str = entry[29:35].strip()
                price: str = entry[35:45]
                execution_id: str = entry[45:57]
                message = [
                    time_stamp,
                    message_type,
                    order_id,
                    side_indicator,
                    shares,
                    stock_symbol,
                    price,
                    execution_id,
                ]
        return message

    def compute_message(self, message: list[str], message_type: str, message_symbol: str) -> None:
        """Evaluates message attributes and preforms operations to track order volume in the symbol book."""
        order_id: str = message[2]

        # Check to see if order is already in the ledger, if not then enter it.
        if order_id not in self.ledger:
            match message_type:
                case "P":
                    current_volume: int = self.symbol_book[message_symbol]
                    self.symbol_book[message_symbol] = current_volume + int(message[4])
                case default:
                    self.ledger[order_id] = message

        # Update ledger if order message is found in the ledger.
        elif order_id in self.ledger:
            self.update_ledger_shares(message, message_type, message_symbol, order_id)

    def update_ledger_shares(
        self, message: list[str], message_type: str, message_symbol: str, order_id: str
    ) -> None:
        """Based on message type, this function will preform operations to update shares in the ledger."""
        old_message: list = self.ledger[order_id]
        old_message_symbol: str = old_message[5]

        match message_type:
            case "X":
                shares: str = old_message[4]
                canceled_shares: str = message[3]

                shares_left: int = int(shares) - int(canceled_shares)
                if shares_left == 0:
                    del self.ledger[order_id]
                else:
                    old_message[4] = shares_left
                    self.ledger[order_id] = old_message

            case "E":
                shares: str = old_message[4]
                executed_shares: str = message[3]

                current_volume: int = self.symbol_book[old_message_symbol]
                self.symbol_book[old_message_symbol] = current_volume + int(executed_shares)
                shares_left: int = int(shares) - int(executed_shares)
                if shares_left == 0:
                    del self.ledger[order_id]
                else:
                    old_message[4] = shares_left
                    self.ledger[order_id] = old_message

            case "P":
                shares: str = old_message[4]
                executed_shares: str = message[4]

                current_volume: int = self.symbol_book[message_symbol]
                self.symbol_book[message_symbol] = current_volume + int(executed_shares)
                shares_left: int = int(shares) - int(executed_shares)
                if shares_left == 0:
                    del self.ledger[order_id]
                else:
                    old_message[4] = shares_left
                    self.ledger[order_id] = old_message

    def print_ledger(self) -> None:
        """Prints out the current state of the ledger which tracks order messages."""
        [print(f"{key}: {value}") for key, value in self.ledger.items()]

    def track_symbol(self, message: list) -> None:
        """Determines if the stock symbol is found in symbol dictionary.
        If the symbol is not found, initialize a new one and enter it into the dictionary.
        """
        symbol: str = message[5]
        if symbol not in self.symbol_book:
            self.symbol_book[symbol] = 0

    def print_symbols(self) -> None:
        """Prints out the symbols found in the symbol book."""
        for key, value in self.symbol_book.items():
            print(f"{key}: {value}")

    def get_top_ten_symbols(self) -> None:
        """Get the top ten stocks in descending order based on stock volume."""
        print("*** Top Ten Symbols ***")
        top_ten: dict = dict(
            sorted(self.symbol_book.items(), key=operator.itemgetter(1), reverse=True)[:10]
        )
        for key, value in top_ten.items():
            print(f"{key}: {value}")
        print("")
