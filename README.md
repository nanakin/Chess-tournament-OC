# Chess Tournament Manager

## Preamble
This script was designed for a school project with specific requirements and fixed constraints.
It was developed in a limited period of time and in this context this project is not intended
to evolve that much once "finished". This project is not open to contribution.
The following need is fictive.

## About The Project
![logo](https://user-images.githubusercontent.com/14202917/230413115-25637523-c7ea-4aa5-900e-6430653edb3c.png)

A friend of mine is a chess club member. The club is dealing with chess tournament manually.
They would like an offline app to manage their tournaments.

![Screenshot of the app](https://user-images.githubusercontent.com/todo.png)

### About the application features
- add new players,
- register them to tournaments,
- create tournaments (date, location, number of rounds),
- launch automated and optimal matchmaking,
- start rounds,
- register matches score,
- display reports (list of tournaments, players, matches, etc.) and export them to files,
and others.

### About the application design
The application : 
- is designed using the architectural pattern **Model-View-Controller** to have a clear separation between 
the code manipulating data (model) and the one for the user interface (view).
- is solving a **SAT-CP\* model** defined by the **matchmaking constraints** with [ortools](https://pypi.org/project/ortools/). 
(SAT-CP solver = A Constraint Programming (CP) solver that uses satisfiability (SAT) method.)
- is displaying a **pretty and interactive command line** user prompt with [questionary](https://pypi.org/project/questionary/).
- is loading previous data from **JSON files** and is doing **automatic backup** (after each model change). The application does not require internet to work.



## Technology
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/>

This project is using Python. This application was tested with 3.11 version on Windows, linux and macOS.

Third-party dependencies are : `questionary` and `ortools`.

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
```sh
python3 main.py
```

The app will auto backup in the given file path
