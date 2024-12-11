from pitch_volume_analysis.core.analyzer import Analyzer
import pytest
from pathlib import Path


@pytest.fixture
def my_analyzer() -> Analyzer:
    CURRENT_FILE_PATH: Path = Path(__file__).resolve()
    PROJECT_ROOT: Path = CURRENT_FILE_PATH.parents[2]
    DATASET_PATH: Path = Path(PROJECT_ROOT, "data", "raw", "pitch_example_data")
    return Analyzer(DATASET_PATH)


@pytest.fixture
def get_entries() -> list[str]:
    """Catalog of all possible entries that the program can encounter.
    Returns a list that can be iterated through by tests.
    This allows for the automated process of testing not just one message type, but multiple.
    """
    add_order_short: str = "S28800011AAK27GA0000DTS000100SH    0000619200Y"
    cancel_order: str = "S28800181X1K27GA00000Y000100"
    return [add_order_short, cancel_order]


@pytest.fixture
def my_message(my_analyzer) -> list[str]:
    entry: str = "S28800011AAK27GA0000DTS000100SH    0000619200Y"
    type: str = "A"
    message: list[str] = my_analyzer.parse_order_message(entry, type)
    return message


@pytest.fixture
def my_message_type(my_analyzer) -> str:
    type: str = my_analyzer.get_message_type("S28800011AAK27GA0000DTS000100SH    0000619200Y")
    return type


@pytest.fixture
def my_message_symbol(my_analyzer, my_message, my_message_type) -> str:
    symbol: str = my_analyzer.get_message_symbol(my_message, my_message_type)
    return symbol


def test_read_file_can_open_file_unsuccessfully():
    with pytest.raises(FileNotFoundError) as e_info:
        CURRENT_FILE_PATH: Path = Path(__file__).resolve()
        PROJECT_ROOT: Path = CURRENT_FILE_PATH.parents[2]
        DATASET_PATH: Path = Path(PROJECT_ROOT, "data", "raw", "file_does_not_exist_data")
        my_analyzer = Analyzer(DATASET_PATH)
        my_analyzer.read_file()
    assert str(e_info.value) == f"File {DATASET_PATH} not found"


def test_get_message_type(get_entries, my_message_type):
    assert my_message_type == get_entries[0][9]


def test_parse_order_message(my_message):
    assert len(my_message) == 8


def test_get_message_symbol(my_message_symbol):
    assert my_message_symbol == "SH"


def test_compute_message(my_analyzer, my_message, my_message_type, my_message_symbol):
    order_id: str = my_message[2]
    my_analyzer.compute_message(my_message, my_message_type, my_message_symbol)
    assert my_analyzer.ledger[order_id] == my_message


def test_update_ledger_shares(my_analyzer, my_message, my_message_type, my_message_symbol):
    order_id: str = my_message[2]
    my_analyzer.compute_message(my_message, my_message_type, my_message_symbol)
    cancel_entry: str = "S28858232XAK27GA0000DT000100"
    cancel_message: list[str] = my_analyzer.parse_order_message(cancel_entry, "X")
    my_analyzer.update_ledger_shares(cancel_message, "X", my_message_symbol, order_id)
    assert my_analyzer.ledger.get(order_id) == None


def test_track_symbol(my_analyzer, my_message):
    symbol: str = my_message[5]
    my_analyzer.track_symbol(my_message)
    assert symbol in my_analyzer.symbol_book


def test_get_top_ten_symbols():
    pass
