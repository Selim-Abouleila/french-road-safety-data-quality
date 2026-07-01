import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Part A: Dataset Structure\n",
                "## 1. Data Loading & Column Inventory\n",
                "Loading the datasets to inspect their shape, columns, and data types."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import os\n",
                "\n",
                "# Load datasets\n",
                "caract = pd.read_csv('caract-2024.csv', sep=';')\n",
                "lieux = pd.read_csv('lieux-2024.csv', sep=';')\n",
                "usagers = pd.read_csv('usagers-2024.csv', sep=';')\n",
                "vehicules = pd.read_csv('vehicules-2024.csv', sep=';')\n",
                "\n",
                "datasets = {'caract': caract, 'lieux': lieux, 'usagers': usagers, 'vehicules': vehicules}\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "for name, df in datasets.items():\n",
                "    print(f\"--- {name.upper()} ---\")\n",
                "    print(f\"Shape: {df.shape}\")\n",
                "    print(\"\\nData Types:\")\n",
                "    print(df.dtypes)\n",
                "    print(\"\\n\")\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Semantic Meaning\n",
                "### Characteristics (`caract-2024.csv`)\n",
                "- `Num_Acc`: Unique accident identifier\n",
                "- `jour`, `mois`, `an`: Date of the accident\n",
                "- `hrmn`: Time of accident\n",
                "- `lum`: Lighting conditions\n",
                "- `dep`, `com`: Department and Municipality\n",
                "- `agg`: Location type (built-up area vs out)\n",
                "- `int`: Intersection type\n",
                "- `atm`: Atmospheric conditions\n",
                "- `col`: Collision type\n",
                "- `adr`, `lat`, `long`: Address and coordinates\n",
                "\n",
                "### Locations (`lieux-2024.csv`)\n",
                "- `Num_Acc`: Unique accident identifier\n",
                "- `catr`: Road category\n",
                "- `voie`, `v1`, `v2`: Route/Road identifiers\n",
                "- `circ`: Traffic regime\n",
                "- `nbv`: Number of lanes\n",
                "- `vosp`: Reserved lanes\n",
                "- `prof`, `plan`: Road profile and plan\n",
                "- `pr`, `pr1`: Home reference point\n",
                "- `lartpc`, `larrout`: Road width\n",
                "- `surf`: Surface condition\n",
                "- `infra`, `situ`: Infrastructure and situation\n",
                "- `vma`: Max speed\n",
                "\n",
                "### Users (`usagers-2024.csv`)\n",
                "- `Num_Acc`, `id_usager`, `id_vehicule`, `num_veh`: IDs\n",
                "- `place`: Seat position\n",
                "- `catu`: User category (driver, passenger, pedestrian)\n",
                "- `grav`: Severity of injury\n",
                "- `sexe`, `an_nais`: Gender and birth year\n",
                "- `trajet`: Reason for travel\n",
                "- `secu1`, `secu2`, `secu3`: Safety equipment\n",
                "- `locp`, `actp`, `etatp`: Pedestrian info\n",
                "\n",
                "### Vehicles (`vehicules-2024.csv`)\n",
                "- `Num_Acc`, `id_vehicule`, `num_veh`: IDs\n",
                "- `senc`: Direction of travel\n",
                "- `catv`: Vehicle category\n",
                "- `obs`, `obsm`: Obstacles hit\n",
                "- `choc`: Initial point of impact\n",
                "- `manv`: Main maneuver\n",
                "- `motor`: Motorization type\n",
                "- `occutc`: Number of occupants (public transport)"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('data_profiling.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=4)
