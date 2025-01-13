# Traveling Salesperson Problem (TSP) Evolutionary Algorithms

## Project Overview:

This project implements evolutionary algorithms for solving the Traveling Salesperson Problem (TSP). The aim is to find a minimal-cost tour that visits each city exactly once and returns to the origin. The project includes modules for representing the TSP problem, individuals, populations, variation operators (mutation and crossover), and selection methods.

Implemented three evolutionary algorithms using different crossover, mutation, and selection methods:

1. **Order Crossover (OX)** + Insert Mutation + Fitness-Proportional Selection + Elitism.
2. **Partially Mapped Crossover (PMX)** + Swap Mutation + Elitism.
3. **Edge Recombination Crossover (ERX)** + Inversion Mutation + Tournament Selection.

All programs are set to terminate after 2 hours of execution.

---

## Instructions to Run the Code:

### 1. Requirements:
   - Python 3.x or above
   - Required Python libraries (install via pip):
     ```bash
     pip install numpy matplotlib pandas jupyterlab
     ```

### 2. Running the Code:
To run each evolutionary algorithm:

- **Order Crossover (OX)**:
   ```bash
   python3 alg_oxrun.py eil51 100 10000 0.1
   ```
   This runs the OX algorithm with a population of 100 individuals, for 10000 generations, with a mutation rate of 0.1. The program outputs results to `result_eil51_pop_gen.txt`. Previous test runs are saved in the `ox_results` folder.

- **Partially Mapped Crossover (PMX)**:
   ```bash
   python3 alg_pmx.py eil51 100 10000 0.1
   ```
   This runs the PMX algorithm, outputting results to `pmx_results.txt`.
    - Previous run results in **results_pmx.txt**
    - Debug mode is activated by adding "debug" e.g. *python alg_pmx.py eil51 10 5000 debug*
    - Possesses an implementation to help you execute the algorithm 

- **Edge Recombination Crossover (ERX)**:
   ```bash
   python3 alg_erx.py eil51 100 10000 0.1
   ```
   This runs the ERX algorithm, outputting results to `erx_results.txt`.

---

## File Outputs:
- **OX Results**: Stored in `result_eil51_pop_gen.txt` (historical runs are in the `ox_results` folder).
- **PMX Results**: Stored in `pmx_results.txt`.
- **ERX Results**: Stored in `erx_results.txt`.

---

## File Descriptions:

- **TSPProblem.py**: Defines the `TSPProblem` class, which represents TSP instances from TSPlib.
- **Individual.py**: Represents a TSP solution as a permutation of cities.
- **Population.py**: Manages a population of individuals and their fitness.
- **Mutation.py**: Implements mutation operators (insert, swap, inversion, scramble).
- **Crossover.py**: Implements crossover operators (OX, PMX, Cycle, Edge Recombination).
- **ElitismSelection.py**: Implements elitism selection in the evolutionary algorithm.
- **FitnessProp.py**: Implements fitness-proportional selection.
- **IndieMute.py**: Handles individual mutation operations.
- **InverOverMain.py & InverOverOperator.py**: Implements the Inver-over operator for the TSP, based on research.
- **PopMute.py**: Handles population-wide mutation operations.
- **TournamentSelection.py**: Implements tournament selection.
- **alg_ox.py**: Runs the OX crossover algorithm.
- **alg_pmx.py**: Runs the PMX crossover algorithm.
- **alg_erx.py**: Runs the ERX crossover algorithm.

---

## Known Issues or Assumptions:

- For large instances like `USA13509`, the algorithm may not complete within 2 hours. Partial results will be reported if the time limit is reached.
- The algorithms may require significant computational resources for larger TSP instances.

---
## Group:
- **Benjamin Signorelli**
- **Tianyue Chu**
- **Charles Lynch**
- **Daniel Manka**
- **Tate Manning**
- **Qiyang Shi**
---
