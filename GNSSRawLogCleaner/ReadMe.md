# GNSS Raw Log Cleaner

A lightweight Python command-line utility to clean Android GNSS raw log files (`.txt`). The script filters satellite observations based on constellation selection and Carrier-to-Noise ratio (C/N₀).

---

## Features

- **Constellation Filtering**  
  Remove data from selected GNSS constellations:
  - GPS (G)
  - SBAS (S)
  - GLONASS (R)
  - QZSS (J)
  - BeiDou (C)
  - Galileo (E)
  - IRNSS (I)

- **C/N₀ Threshold Filtering**  
  Discard measurements below a user-defined threshold (in dB-Hz)

- **Safe Output Generation**  
  Generates a new cleaned file without modifying the original input

---

## Requirements

- Python 3.x
- No external libraries required (uses only standard library)

---

## Usage

### 1. Run the Script

```bash
python cleanRaw.py
```

### 2. Provide Input File

- Enter the absolute path to a `.txt` GNSS raw log file
- Example:

```
C:\Users\Dheeraj\Downloads\gnss_log.txt
```

### 3. Select Constellations to Remove

- Enter constellation characters in any format:

```
G R
G,R
G, R
GR
```

- Leave blank to keep all constellations

### 4. Set C/N₀ Threshold

- Enter a numeric value (e.g., `25`)
- Press **Enter** to use default: `20 dB-Hz`

#### Notes

- Values `< 10` may include noisy data
- Values `> 40` may remove most satellite observations

---

## Output

- Output file is saved in the same directory as the input file
- Naming convention:

```
cleaned_<original_filename>.txt
```

### Example

```
Input:  gnss_log.txt
Output: cleaned_gnss_log.txt
```

---

## How It Works

- Reads the file line-by-line
- Processes only lines starting with `"Raw"`
- Extracts:
  - C/N₀ → column index `16` (0 - based indexing)
  - Constellation ID → column index `28`(0 - based indexing)
- Filters data based on:
  - Selected constellations
  - C/N₀ threshold
- Writes valid lines to the output file

---

## Constellation Mapping

| Character | Constellation | ID |
|----------|--------------|----|
| G        | GPS          | 1  |
| S        | SBAS         | 2  |
| R        | GLONASS      | 3  |
| J        | QZSS         | 4  |
| C        | BeiDou       | 5  |
| E        | Galileo      | 6  |
| I        | IRNSS        | 7  |

---

## Example Workflow

```
|- Enter the absolute path of the raw (.txt) log file to be cleaned:
|-> C:\logs\gnss.txt

|- Enter constellations to remove:
|-> GR

|- Enter C/N0 threshold:
|-> 25

[Processing...]

-> Cleaned file saved: C:\logs\cleaned_gnss.txt
-> Constellations present: ['E', 'C']
```

