#!/bin/env python3

import argparse
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import windrose
from pathlib import Path
import csv
import numpy as np


plt.rcParams.update({"font.size": 14})


parser = argparse.ArgumentParser(
    description="Plot windrose from CSV file.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
CSV input file should have no header and be comma-separated. First column must be
string, designating wind direction. Possible values of first column:
    - N     (North)
    - NNE   (North North East)
    - NE    (North East)
    - ENE   (East North East)
    - E     (East)
    - ESE   (East South East)
    - SE    (South East)
    - SSE   (South South East)
    - S     (South)
    - SSW   (South South West)
    - SW    (South West)
    - WSW   (West South West)
    - W     (West)
    - WNW   (West Noth West)
    - NW    (North West)
    - NNW   (North North West)

Any other values make input file ill-formed. Second column must be integer value
of windspeed in m/s.

Input file example:
S,5
WNW,1
SSW,4
    """,
)

parser.add_argument(
    "-i",
    "--input",
    type=str,
    required=True,
    help="path of input file",
)

parser.add_argument(
    "-o",
    "--output",
    type=str,
    required=False,
    help="path of output file",
)


def direction_str_to_angle(directionStr):
    step = 22.5
    possible_strings = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    return step * possible_strings.index(directionStr)


def parse_input_file(inputFile):
    directions = []
    speeds = []
    with open(inputFile, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            directions.append(direction_str_to_angle(row[0]))
            speeds.append(int(row[1]))
    return np.array(directions), np.array(speeds)


def plot(directions, speeds):
    fig, ax = plt.subplots(
        figsize=(7, 7), dpi=120, subplot_kw={"projection": "windrose"}
    )
    ax.bar(
        directions,
        speeds,
        normed=True,
        bins=np.arange(0, 10, 2),
        opening=0.8,
        edgecolor="white",
    )
    ax.legend(units="м/с", shadow=False, bbox_to_anchor=(0.95, 0.95))
    xlabels = (
        "В",
        "СВ",
        "С",
        "СЗ",
        "З",
        "ЮЗ",
        "Ю",
        "ЮВ",
    )
    ax.set_xticklabels(xlabels)
    plt.tight_layout()


def main():
    args = parser.parse_args()
    inputFile = Path(args.input)
    assert inputFile.is_file()
    directions, speeds = parse_input_file(inputFile)
    plot(directions, speeds)
    if args.output:
        plt.savefig(args.output, format="png")
    else:
        plt.show()


if __name__ == "__main__":
    main()
