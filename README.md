# Pitch Volume Analysis

Reads PITCH data from standard input and shows a table of the top ten symbols by executed volume.

## Project Organization

```
├── data                    <- Dataset and log files are stored here
│   ├── logs                    <- Holds profiling log results
│   └── raw                     <- The original, immutable data dump
│
│
├── pitch_volume_analysis   <- Source code for use in this project
│    │
│    ├── core                   <- Houses the program core
│    │      │ 
│    │      ├── __init__.py                 <- Makes core a Python module
│    │      ├── analyzer.py                 <- Class and functions to analyze order messages for multiple symbols
│    │      ├── main.py                     <- Program entry point
│    │      └── symbol_analyzer.py          <- Class and functions to analyze order messages for a single symbol
│    │
│    ├── tests                  <- Logic to run testing suites
│    │      │ 
│    │      ├── __init__.py                 <- Makes tests a Python module
│    │      ├── test_analyzer.py            <- Unit tests for analyzer.py
│    │      ├── test_main.py                <- Unit tests for main.py
│    │      └── test_symbol_analyzer.py     <- Unit tests for symbol_analyzer.py
│    │    
│    └── __init__.py            <- Makes pitch_volume_analysis a Python module
│
├── references              <- Data dictionaries, manuals, and all other explanatory materials
│
│
├── dev-requirements.txt    <- The requirements file for reproducing the dev environment
|
├── LICENSE                 <- Open-source license
│
│
├── pyproject.toml          <- Project configuration file with package metadata for pitch_volume_analysis
│                              and configuration for additional core packages needed to run this program
│
├── README.md               <- The top-level README for developers using this project
│
│
└── setup.cfg               <- Configuration file for flake8
```

## How to Run
#### 1. Create and activate a virtual environment inside project root directory: 
```
    python -m venv venv

    Windows:
        .\venv\Scripts\activate
    *nix:
        . venv/bin/activate
```

#### 2. (In project root) install the package within the virtual environment (must install as editable -e):
```
    python -m pip install -e .

    Optional:   To install additional dev dependencies install dev-requirements.txt
                pip install -r dev-requirements.txt
```

#### 3. Run the program 
```
    After installing the pitch_volume_analysis package you will have access to the command "pva"

    1. To run the program run the following command:
        pva

    Optional:   Alternatively you can also run the program at it's entry point (main.py) located at
                "pitch_volume_analysis/pitch_volume_analysis/core/main.py"
```

## How to Uninstall
```
    To uninstall run the following command:
    pip uninstall pitch_volume_analysis
```

## Optional Flags

There are several flags that you can use when calling pva from the command line

#### -h, --help
```
    Will return general help message showing the commands available to you.
```

#### -f FILE, --file File
```
    Using this flag allows the user to input a path to another dataset they would like to use.

    If this flag is not invoked then a built-in default dataset will be used instead. 
    The default dataset will also be used when the user inputted a dataset that does not exist. 

    Using this flag enables the user to not have to manually place and swap the dataset
    in the project file system.

    Examples: 
            pva -f path/to/dataset.txt
            pva --file path/to/dataset.txt
```

#### -p, --profile
```
    The flag -p, --profile allows the developers to profile the main program. This will give insight into 
    what files and functions are taking up the most resources.

    Examples:
            pva -p
            pva --profile
```

#### -d DEBUG, --debug DEBUG
```
    The -d, --debug flag runs an extra program after the execution of the main program. 

    This extra program is a stripped down version of the main application. It's purpose is to 
    follow a single symbol that is specified by the user. 

    It will print to the console the full transaction history for this single symbol. 
    This will help developers verify proper functionality of the main program.

    The bare bones program will provide step by step transactions showing the developers how 
    the program came to the concluded stock volume. 

    Examples:  
            pva -d AAPL
            pva --debug DIA
```

## How to Run Tests
#### pytest
```
    To unit test implemented functions you can use the command pytest.
    In the project root directory just type pytest and the testing suite will run.

    These test will verify if any modifications/optimizations done to the code base 
    still produce expected results.

    Example:
            pytest

```

## Using Tuna to Visualize Profiling Reports
```
    When the command "pva -p" is ran the profiler will generate a file called "results.prof".
    You can find this file at "pitch_volume_analysis/data/logs/results.prof".

    Tuna can then be used to view "results.prof".

    Tuna is a modern, lightweight Python profile viewer inspired by SnakeViz. 
    It handles runtime and import profiles, has minimal dependencies, uses d3 and bootstrap, 
    and avoids certain errors present in SnakeViz and is faster, too.
```

#### Calling Tuna 
```
    To use Tuna make sure your environment is activated with Tuna already installed.
    Tuna should have been automatically installed via the pyproject.toml file when the package was installed.

    In case it wasn't, use the following command to install Tuna:   
    pip install tuna
       
    To use Tuna type the following:    
    tuna path/to/results.prof
   
    Tuna will then open in the browser at localhost:8000 displaying "results.prof".
```

--------

