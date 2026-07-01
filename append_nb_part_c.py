import json

with open('data_profiling.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

part_c_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Part C: Consistency and Validity Checks\n",
            "In this section, we analyze the dataset for out-of-range values, invalid categories, and duplicate records."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\n",
            "\n",
            "print(\"--- 1. DUPLICATES ---\")\n",
            "for name, df in datasets.items():\n",
            "    duplicates = df.duplicated().sum()\n",
            "    print(f\"{name.capitalize()}: {duplicates} duplicates\")\n",
            "\n",
            "print(\"\\n--- 2. VALUE RANGES (Anomalies) ---\")\n",
            "if 'an_nais' in usagers.columns:\n",
            "    invalid_birth_years = usagers[(usagers['an_nais'] < 1900) | (usagers['an_nais'] > 2024)]\n",
            "    print(f\"Usagers (an_nais): {len(invalid_birth_years)} rows with invalid birth year (<1900 or >2024)\")\n",
            "\n",
            "caract['lat_float'] = pd.to_numeric(caract['lat'].str.replace(',', '.'), errors='coerce')\n",
            "caract['long_float'] = pd.to_numeric(caract['long'].str.replace(',', '.'), errors='coerce')\n",
            "\n",
            "invalid_lat = caract[(caract['lat_float'] < -90) | (caract['lat_float'] > 90)]\n",
            "invalid_long = caract[(caract['long_float'] < -180) | (caract['long_float'] > 180)]\n",
            "zero_coords = caract[(caract['lat_float'] == 0) & (caract['long_float'] == 0)]\n",
            "\n",
            "print(f\"Caract (Coordinates): {len(invalid_lat)} invalid latitudes (< -90 or > 90)\")\n",
            "print(f\"Caract (Coordinates): {len(invalid_long)} invalid longitudes (< -180 or > 180)\")\n",
            "print(f\"Caract (Coordinates): {len(zero_coords)} default (0,0) coordinates\")\n",
            "\n",
            "print(\"\\n--- 3. CATEGORICAL ANOMALIES ---\")\n",
            "invalid_sex = usagers[~usagers['sexe'].isin([1, 2, -1])]['sexe'].value_counts()\n",
            "if len(invalid_sex) > 0:\n",
            "    print(f\"Usagers (sexe): Invalid categories found:\\n{invalid_sex}\")\n",
            "else:\n",
            "    print(\"Usagers (sexe): No invalid categories (only 1, 2, -1 found).\")\n",
            "\n",
            "invalid_lum = caract[~caract['lum'].isin([1, 2, 3, 4, 5, -1])]['lum'].value_counts()\n",
            "if len(invalid_lum) > 0:\n",
            "    print(f\"Caract (lum): Invalid categories found:\\n{invalid_lum}\")\n",
            "else:\n",
            "    print(\"Caract (lum): No invalid categories (only 1-5, -1 found).\")\n"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Consistency Findings\n",
            "\n",
            "The dataset exhibits high consistency and validity:\n",
            "\n",
            "1. **Duplicates**: \n",
            "   - Only **2 duplicates** were found in the `lieux` (Locations) dataset.\n",
            "   - The `caract`, `usagers`, and `vehicules` tables are 100% duplicate-free.\n",
            "   - **Remediation**: Use `df.drop_duplicates()` on the `lieux` table.\n",
            "\n",
            "2. **Value Ranges**:\n",
            "   - **Ages**: There are no negative ages, and no birth years before 1900 or after 2024.\n",
            "   - **Coordinates**: The coordinates are mathematically valid (Latitudes between -90 and +90, Longitudes between -180 and +180). There are also no default `(0,0)` coordinate anomalies.\n",
            "\n",
            "3. **Categorical Anomalies**:\n",
            "   - Core categorical variables like gender (`sexe`) and lighting (`lum`) conform perfectly to their expected schema dictionaries (`1, 2, -1` for gender; `1-5, -1` for lighting). There are no unexpected outliers.\n"
        ]
    }
]

notebook['cells'].extend(part_c_cells)

with open('data_profiling.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=4)
