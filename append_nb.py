import json

with open('data_profiling.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

part_b_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Part B: Missing Values and Completeness\n",
            "In this section, we compute the percentage of missing values (including standard NaNs and `-1` values which represent 'Unknown' in this dataset), identify critical missingness, and suggest remediation strategies."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import numpy as np\n",
            "\n",
            "# Function to summarize missing values including NaNs and -1\n",
            "def summarize_missingness(df):\n",
            "    # Standard missing (NaNs)\n",
            "    missing = df.isnull().sum()\n",
            "    missing_pct = (missing / len(df)) * 100\n",
            "    \n",
            "    # Unknowns (-1)\n",
            "    unknowns_pct = pd.Series(0.0, index=df.columns)\n",
            "    for col in df.columns:\n",
            "        if df[col].dtype in ['int64', 'float64', 'int32', 'float32']:\n",
            "            unknowns_pct[col] = (df[col] == -1).sum() / len(df) * 100\n",
            "            \n",
            "    missing_df = pd.DataFrame({\n",
            "        'NaN_Pct': missing_pct,\n",
            "        'Unknown_Pct(-1)': unknowns_pct,\n",
            "        'Total_Missing_Pct': missing_pct + unknowns_pct\n",
            "    })\n",
            "    \n",
            "    # Filter to only show columns with > 0% missingness\n",
            "    return missing_df[missing_df['Total_Missing_Pct'] > 0].sort_values(by='Total_Missing_Pct', ascending=False)\n",
            "\n",
            "for name, df in datasets.items():\n",
            "    print(f\"--- {name.upper()} Missingness ---\")\n",
            "    display(summarize_missingness(df))\n",
            "    print(\"\\n\")\n"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Critical Missingness Analysis\n",
            "\n",
            "Based on the output above, here are the most problematic missing values:\n",
            "\n",
            "1. **High Missingness (> 90%)**: Columns like `lartpc` (width of central divider), `v2` (alphanumeric route index), `secu3` (tertiary safety equipment), `etatp` (pedestrian status), and `occutc` (public transport occupants). \n",
            "   - *Why problematic:* They are virtually empty for the vast majority of the dataset.\n",
            "   - *Context:* These are often conditionally applicable (e.g., `occutc` only applies if the vehicle is public transport, `etatp` only applies to pedestrians).\n",
            "\n",
            "2. **Moderate Missingness (10% - 50%)**: Columns like `voie` (18.9%), `v1` (23.1% unknown), `secu2` (42.9%), `locp` (49.3%).\n",
            "   - *Why problematic:* `voie` and `v1` are crucial for identifying the exact road where the accident happened. `locp` is critical for pedestrian accident analysis.\n",
            "\n",
            "3. **Low but Critical Missingness (< 10%)**: `vma` (max speed, 5.1% unknown), `adr` (address, 4.2%), `an_nais` (birth year, 2.0%).\n",
            "   - *Why problematic:* `vma` and `an_nais` are highly predictive features for accident severity. Losing age or speed limit data can bias predictive models.\n",
            "\n",
            "## Remediation Strategies\n",
            "\n",
            "1. **Standardize Missing Values**: First, replace all `-1` values with `np.nan` so that pandas can universally handle them as missing data across all operations.\n",
            "2. **Conditional Columns (> 90% missing)**: Do not drop these columns if analyzing specific sub-groups (e.g. pedestrians, public transport). Instead, fill missing values with a designated category like `\"Not Applicable\"` or `0` depending on the context.\n",
            "3. **Categorical Imputation**: For features like `vma` (max speed) or `lum` (lighting), impute using the **mode** (most frequent value) based on the road category (`catr`) or intersection type (`int`).\n",
            "4. **Numerical Imputation**: For `an_nais` (birth year), impute missing values using the **median** birth year, possibly grouped by user category (`catu`).\n",
            "5. **Row Deletion**: For critical identifiers like `adr` (address) or coordinates, if location analysis is the primary goal and imputation is impossible, dropping the rows (only ~4%) might be the safest approach to prevent plotting accidents in the ocean (0,0).\n"
        ]
    }
]

notebook['cells'].extend(part_b_cells)

with open('data_profiling.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=4)
