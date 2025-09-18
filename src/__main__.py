# src/__main__.py

import argparse
import importlib

#from src.optimizer import run_optimizer
from src.runs.sim import flightsim


def main():
    parser = argparse.ArgumentParser(description="Rocket design and simulation tool")
    parser.add_argument(
        "input_file",
        type=str,
        help="Name of the input file (inside src/inputs/, without .py)"
    )
    args = parser.parse_args()

    # Dynamically import input file (must define desvars, mission, constraints)
    program_input = importlib.import_module(f"src.inputs.{args.input_file}")

    print("\nSelect run mode:")
    print("1 --> Single Run")
    print("2 --> Optimization")
    user_input = input("Enter number: ")

    if user_input == "1":
        results = flightsim(program_input.desvars, program_input.mission_reqs)
        print("Single run finished. Results:")
        print(results)

    elif user_input == "2":
        program_input.desvars, program_input.mission
        """
        results = run_optimizer(config, program_input.constraints)
        print("Optimization finished. Best result:")
        print(results)
        """

    else:
        print("Invalid selection.")


if __name__ == "__main__":
    main()
