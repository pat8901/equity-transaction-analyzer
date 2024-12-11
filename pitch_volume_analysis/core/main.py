from pathlib import Path
from pitch_volume_analysis.core.analyzer import Analyzer
from pitch_volume_analysis.core.symbol_analyzer import SymbolAnalyzer
import sys
import traceback
import typing
import cProfile
import pstats
import argparse


def main():
    # Adding optional argument flags.
    args = add_flags()

    # Setting base directory.
    try:
        CURRENT_FILE_PATH: Path = Path(__file__).resolve()
        PROJECT_ROOT: Path = CURRENT_FILE_PATH.parents[2]
        DATASET_PATH: Path = Path(PROJECT_ROOT, "data", "raw", "pitch_example_data")
        LOG_PATH: Path = Path(PROJECT_ROOT, "data", "logs")
    except:
        print("Directories and/or dataset not found!")
        # traceback.print_exc()
        sys.exit(1)

    # Checking for file flag.
    if args.file is not None:

        NEW_DATASET_PATH: Path = Path(args.file)
        file_exist: bool = NEW_DATASET_PATH.exists()

        if file_exist:
            DATASET_PATH = NEW_DATASET_PATH
        else:
            print("File does not exist!")
            print("Will use the default file instead.\n")

    # Checking for profile flag.
    if args.profile:
        print("Running profiler...")
        with cProfile.Profile() as profile:
            start_program(DATASET_PATH)
            profiler = pstats.Stats(profile)
            profiler.sort_stats(pstats.SortKey.TIME)
            profiler.print_stats()
            profiler.dump_stats(Path(LOG_PATH, "results.prof"))
    else:
        start_program(DATASET_PATH)

    # Checking for debug flag.
    if args.debug is not None:
        SYMBOL: str = args.debug
        start_symbol_program(DATASET_PATH, SYMBOL.upper())


def add_flags():
    """Adds optional command line arguments enabling additional features."""
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


def start_program(DATASET_PATH: Path) -> bool:
    """Initializes base program to compute stock volumes."""
    my_analyzer = Analyzer(DATASET_PATH)
    my_analyzer.read_file()
    my_analyzer.get_top_ten_symbols()
    # my_analyzer.print_symbols()
    return True


def start_symbol_program(DATASET_PATH: Path, SYMBOL: str) -> bool:
    """Initializes debug program to find the volume of a single stock symbol."""
    print(f"*** Running Debug Test ***")
    symbol_analyzer = SymbolAnalyzer(SYMBOL, DATASET_PATH)
    symbol_analyzer.read_file()
    symbol_analyzer.print_stock_volume()
    return True


if __name__ == "__main__":
    main()
