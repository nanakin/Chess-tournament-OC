# Chess Tournament Manager

## Preamble
This script was designed for a school project with specific requirements and fixed constraints.
It was developed in a limited period of time and in this context this project is not intended
to evolve that much once "finished". This project is not open to contribution.
The following need is fictive.

## About The Project
![logo](https://user-images.githubusercontent.com/14202917/230413115-25637523-c7ea-4aa5-900e-6430653edb3c.png)

### Project context
A friend of mine is a chess club member. The club is dealing with chess tournament manually.
They would like an offline app to manage their tournaments.

### Screenshots
Tournament registration:
<img width="647" alt="tournament-registration" src="https://user-images.githubusercontent.com/14202917/231799322-4850d8e0-871b-40c4-94fb-e8c5ee89fc29.png">

Tournament management menu:
<img width="645" alt="Screenshot 2023-04-13 at 17 06 57" src="https://user-images.githubusercontent.com/14202917/231803302-79febd00-67b5-494e-a636-7e2c25b60271.png">


### About the application features
- add new players,
- register them to tournaments,
- create tournaments (date, location, number of rounds),
- launch automated and optimal matchmaking,
- start rounds,
- register matches score,
- display reports (list of tournaments, players, matches, etc.) and export them to files, 
- and others.

### About the application design
The application : 
- is designed using the architectural pattern **Model-View-Controller** to have a clear separation between 
the code manipulating data (model) and the one for the user interface (view).
- is solving a **SAT-CP\* model** defined by the **matchmaking constraints** with [ortools](https://pypi.org/project/ortools/). 
(SAT-CP solver = A Constraint Programming (CP) solver that uses satisfiability (SAT) method.)
- is displaying a **pretty and interactive command line** user prompt with [questionary](https://pypi.org/project/questionary/).
- is loading previous data from **JSON files** and is doing **automatic backup** (after each model change). The application does not require internet to work.
- is [flake8](https://flake8.pycqa.org/en/latest/) compliant.


## Technology
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/>

This project is using Python. This application was tested with 3.11 version on Windows, linux and macOS.

Third-party dependencies are : `questionary`, `ortools` and optionally `flake8` (not required by the application).
## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/nanakin/OC-P4-chess-tournament.git chesstournament
   ```
2. Move to the project directory:
     ```sh
      cd chesstournament
      ```
3. Create a virtual environment (optional):
   ```sh
   python3 -m venv venv
   ```
   and activate it:
   ```sh
   .\venv\Scripts\activate  # windows
   source venv/bin/activate  # unix and macOS
   ```
4. Install required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### To launch the Chess Tournament Manager
```sh
python3 main.py
```
#### Option
`--data-path` to specify a backup path.

### To verify flake8 compliance
```sh
flake8 --max-line-length=119 --format=html --htmldir=flake8_rapport --exclude=venv
```

### To format (to be removed from the doc)
```sh
black . --line-length=119
```