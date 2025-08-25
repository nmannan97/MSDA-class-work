import numpy as np

# Set print options
np.set_printoptions(suppress=True, linewidth=150)

# File path to the uploaded loan data CSV
file_path = "DATA-200/loan-data.csv"

# Load full raw data as strings to handle corrupted characters and separate types
raw_data_np = np.genfromtxt(file_path, delimiter=';', skip_header=1, dtype=str, encoding="cp855")

# Extract header row
header_full = np.genfromtxt(file_path, delimiter=';', max_rows=1, dtype=str, encoding="cp855")

# Identify numeric columns by trying to convert each column
num_cols = []
str_cols = []

# Check each column to see if it can be converted to float
for i in range(raw_data_np.shape[1]):
    try:
        # Try converting entire column to float
        col_as_float = raw_data_np[:, i].astype(np.float64)
        num_cols.append(i)
    except ValueError:
        str_cols.append(i)

# Separate arrays
loan_data_strings = raw_data_np[:, str_cols]
loan_data_numeric_raw = raw_data_np[:, num_cols]

# Try converting numeric data with bad entries to NaN
loan_data_numeric = np.full_like(loan_data_numeric_raw, np.nan, dtype=np.float64)

for i in range(loan_data_numeric_raw.shape[1]):
    for j in range(loan_data_numeric_raw.shape[0]):
        try:
            loan_data_numeric[j, i] = float(loan_data_numeric_raw[j, i])
        except ValueError:
            continue  # Leave as NaN

# Extract headers
header_strings = header_full[str_cols]
header_numeric = header_full[num_cols]

# Save cleaned arrays to checkpoint
np.savez("E:\\Masters Data Analytics\\MSDA-class-work\\DATA-200\\loan_data_cleaned_checkpoint.npz",
         loan_data_strings=loan_data_strings,
         loan_data_numeric=loan_data_numeric,
         header_strings=header_strings,
         header_numeric=header_numeric)

print("Data preprocessing complete.")
print("String data shape:", loan_data_strings.shape)
print("Numeric data shape:", loan_data_numeric.shape)
