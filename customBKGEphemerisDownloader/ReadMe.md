# BKG Ephemeris Downloader

A Python utility to download and process GNSS broadcast ephemeris (BRDC) files from the BKG FTP server. This tool is designed to resolve missing ephemeris errors in GNSS analysis workflows.

---

## ⚠️ Important Note

This script **ONLY works with the BKG FTP server**:

```
https://igs.bkg.bund.de/root_ftp/IGS/BRDC/
```

It **DOES NOT support NASA CDDIS files**, such as:

```
hour1110.26n.gz
```

If you see errors related to missing BRDC files in your GNSS analysis tool, this script helps you fetch them.

---

## What This Script Does

* Downloads missing BRDC ephemeris files from BKG server
* Extracts `.gz` compressed files
* Converts mixed RINEX files into constellation-specific files using `gfzrnx`
* Saves output in the same directory as the script

---

## Requirements

* Python 3.x
* Internet connection

Directory structure:

```
customBKGEphemerisDownloader/
├── customBKGEphemerisDownloader.py
├── bin/
│   └── gfzrnx.exe
```

---

## Usage

### 1. Run the Script

```bash
python customBKGEphemerisDownloader.py
```

---

### 2. Enter File Names

Provide the required BRDC filenames.

Supported formats:

#### Option 1: Comma-separated

```
BRDC00WRD_R_20261090000_01D_EN.rnx.gz, BRDC00WRD_R_20261090000_01D_CN.rnx.gz, -1
```

#### Option 2: Space-separated

```
BRDC00WRD_R_20261090000_01D_EN.rnx.gz BRDC00WRD_R_20261090000_01D_CN.rnx.gz -1
```

#### Option 3: Line-by-line input

```
BRDC00WRD_R_20261090000_01D_EN.rnx.gz
BRDC00WRD_R_20261090000_01D_CN.rnx.gz
-1
```

### Termination

* Enter `-1` to finish input

---

## Processing Steps

For each file:

1. Extracts year and GPS week from filename
2. Downloads the corresponding **Mixed (M)** ephemeris file
3. Extracts `.gz` file
4. Converts to constellation-specific RINEX using:

```bash
gfzrnx.exe -finp input -fout output -satsys <CONST>
```

---

## Supported Constellations

| Code | Constellation |
| ---- | ------------- |
| G    | GPS           |
| R    | GLONASS       |
| E    | Galileo       |
| C    | BeiDou        |
| J    | QZSS          |
| I    | IRNSS         |
| S    | SBAS          |
| M    | Mixed         |

---

## Output

* Extracted `.rnx` files
* Converted constellation-specific RINEX files
* Stored in the same folder as the script

---

## Final Step

After execution:

1. Copy the generated ephemeris files
2. Paste them into your GNSS analysis folder
   (where your GNSSLogger raw `.txt` file is located)

---

## Example Workflow

```
|- Enter filenames:
|-> BRDC00WRD_R_20261090000_01D_EN.rnx.gz BRDC00WRD_R_20261090000_01D_CN.rnx.gz -1

[Downloading Files....]
|- Downloaded successfully
|- extracted Filename: BRDC00WRD_R_20261090000_01D_MN.rnx

-> RINEX file for 'GPS (G)' has been generated
-> RINEX file for 'BeiDou (C)' has been generated
```

---

## Common Issues

### ❌ Invalid filename format

Ensure filenames follow:

```
BRDCXXXXX_R_YYYYDDD0000_01D_<CONST>N.rnx.gz
```

### ❌ Missing gfzrnx

Ensure:

```
bin/gfzrnx.exe
```

exists

### ❌ Download failure

Check:

* Internet connection

---

##
