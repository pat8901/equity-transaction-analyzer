import pitch_volume_analysis.core.main as main
import pytest
from pathlib import Path
import argparse


@pytest.fixture
def my_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", type=Path, help="Enter file path to preform pitch volume analysis"
    )
    parser.add_argument("-p", "--profile", action="store_true", help="Enables profiler mode")
    parser.add_argument(
        "-d",
        "--debug",
        type=str,
        help="Enables debug mode to finely track a symbol",
    )
    args = parser.parse_args()
    return args


def test_add_flags(my_args):
    assert my_args is not None and type(my_args) == argparse.Namespace


def test_start_program():
    CURRENT_FILE_PATH: Path = Path(__file__).resolve()
    PROJECT_ROOT: Path = CURRENT_FILE_PATH.parents[2]
    DATASET_PATH: Path = Path(PROJECT_ROOT, "data", "raw", "pitch_example_data")
    result = main.start_program(DATASET_PATH)
    assert result == True


def test_start_symbol_program():
    CURRENT_FILE_PATH: Path = Path(__file__).resolve()
    PROJECT_ROOT: Path = CURRENT_FILE_PATH.parents[2]
    DATASET_PATH: Path = Path(PROJECT_ROOT, "data", "raw", "pitch_example_data")
    result = main.start_symbol_program(DATASET_PATH, "AAPL")
    assert result == True
