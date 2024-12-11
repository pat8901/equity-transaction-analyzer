class SymbolAnalyzer:
    """
    This is a stripped down version of the Analyzer class with it's bare components.
    Instead of computing all stock symbols, SymbolAnalyzer computes a single stock symbol of your choice.

    The complexity is reduced. Add, Cancel, Execute, and Trade events are printed to the console as they occur.
    This will allow for precise tracking to verify functionality of the core program.
    """

    dataset_path: str = None
    symbol: str = None
    stock_volume: int = 0
    ledger: dict = {}

    def __init__(self, symbol: str, dataset_path):
        self.symbol = symbol
        self.dataset_path = dataset_path

    def read_file(self):
        """Main event loop for a single symbol. This reads the dataset file and
        preform operations to determine a symbols stock volume."""
        with open(self.dataset_path, "r") as file:
            for line in file:
                entry: str = line.strip()
                message_type: str = self.get_message_type(entry)
                message: list = self.parse_order_message(entry, message_type)
                try:
                    message_symbol: str = self.get_message_symbol(message, message_type)
                except:
                    print("Unrecognized message format! Skipping...")
                    continue

                self.compute_message(message, message_type, message_symbol)

    def get_message_type(self, entry: str) -> str:
        """Finds message type and returns it's value."""
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
        """Evaluates message attributes and preforms operations to track order volume for the specified symbol."""
        order_id: str = message[2]

        # Check to see if order is already in the ledger, if not then enter it.
        if order_id not in self.ledger and message_symbol == self.symbol:
            match message_type:
                case "P":
                    current_volume: int = self.stock_volume
                    self.stock_volume = current_volume + int(message[4])
                    print(f"{self.symbol}: {message[2]} {int(message[4])} added to volume")
                case default:
                    print(f"{self.symbol}: {order_id} added to ledger")
                    self.ledger[order_id] = message

        # Update ledger if order message is found in the ledger.
        if order_id in self.ledger:
            old_message: list = self.ledger[order_id]
            match message_type:
                case "X":
                    shares_left: int = int(old_message[4]) - int(message[3])
                    if shares_left == 0:
                        print(f"{self.symbol}: {order_id} canceled")
                        del self.ledger[order_id]
                    else:
                        print(
                            f"{self.symbol}: {order_id} canceled {int(message[3])}, shares Remaining {shares_left}"
                        )
                        old_message[4] = shares_left
                        self.ledger[order_id] = old_message
                case "E":
                    current_volume: int = self.stock_volume
                    self.stock_volume = current_volume + int(message[3])
                    print(f"{self.symbol}: {message[2]} {int(message[3])} added to volume")
                    shares_left: int = int(old_message[4]) - int(message[3])
                    if shares_left == 0:
                        print(f"{self.symbol}: {order_id} removed")
                        del self.ledger[order_id]
                    else:
                        print(f"{self.symbol}: {order_id} shares Remaining {shares_left}")
                        old_message[4] = shares_left
                        self.ledger[order_id] = old_message
                case "P":
                    current_volume: int = self.stock_volume
                    self.stock_volume = current_volume + int(message[4])
                    print(f"{self.symbol}: {message[2]} {int(message[4])} added to volume")
                    shares_left: int = int(old_message[4]) - int(message[4])
                    if shares_left == 0:
                        print(f"{self.symbol}: {order_id} removed")
                        del self.ledger[order_id]
                    else:
                        print(f"{self.symbol}: {order_id} shares Remaining {shares_left}")
                        old_message[4] = shares_left
                        self.ledger[order_id] = old_message

    def print_ledger(self) -> None:
        """Prints out the current state of the ledger which tracks order messages."""
        [print(f"{key}: {value}") for key, value in self.ledger.items()]

    def print_stock_volume(self):
        """Prints out the volume of a given stock."""
        print(f"{self.symbol}: (Total) {self.stock_volume}")
        print("")
