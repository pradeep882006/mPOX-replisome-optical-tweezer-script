# C-trap DNA Unwinding Analysis

Python scripts for analyzing DNA unwinding by a viral helicase from single-molecule
optical-tweezers (C-trap) data collected on the **LUMICKS** platform.

Raw traces are read from LUMICKS `.h5` files, the trap-to-trap distance is converted
into **nucleotides (nt) unwound**, and the resulting time traces are plotted, exported,
and (optionally) analyzed for **unwinding length** and **pausing behavior**. Raw traces for testing the script can be found here : **https://doi.org/10.5281/zenodo.21363054**. 


---

## What the scripts do

| Script | Purpose |
| --- | --- |
| `Marker_Data_analysis_Ctrap_1.py` | Load `.h5` files from a folder, convert distance → nt unwound, plot distance vs. time, and batch-export the plots as PDFs. |
| `PauseAndFinalUnwindingLegnth_forSpecificTime.py` | For each trace, smooth the signal, measure the total nt unwound at a fixed time point (default 60 s), and estimate the fraction of the trace spent paused. |

---

## Requirements

- Python 3.9+
- [`lumicks.pylake`](https://lumicks-pylake.readthedocs.io/) — reading `.h5` files
- `numpy`
- `pandas`
- `matplotlib`
- `scipy` — Savitzky–Golay / median smoothing
- `pyperclip` — used by the pause script to read the folder path from the clipboard

Install everything with:

```bash
pip install lumicks.pylake numpy pandas matplotlib scipy pyperclip
```

> **Note:** The scripts were written to run interactively (e.g. in Spyder or a
> Jupyter/IPython session). `Marker_Data_analysis_Ctrap_1.py` uses the IPython
> magic `%matplotlib auto` and cell markers (`#%%`), and the pause script assumes
> `numpy`, `pandas`, `matplotlib.pyplot`, and `lumicks.pylake` are already imported
> in the session. If you run them as plain `.py` files, add the standard imports at
> the top (see below).

---



## Usage

### 1. Plot and export traces — `Marker_Data_analysis_Ctrap_1.py`

1. Set the folder that contains your `.h5` files. In the script this is the `path`
   variable used in `os.chdir(path)` — assign it before running the file-listing cell,
   e.g.:

   ```python
   path = r"C:\path\to\your\h5\folder"
   ```

2. Run the file-listing cell. It collects every `.h5` file in the folder and prints
   them as a table.

3. **Inspect a single file:** set `k` to the index of the file you want and run the
   selection cell to plot distance (nt) vs. time (s).

4. **Batch export:** run the final cell to loop over every file in the folder and save
   each trace as `<filename>Dist.pdf` in the same folder. The y-axis is fixed to
   `[-50, 500]` nt for the batch plots — adjust `axs.set_ylim([...])` if your traces
   fall outside that range.

### 2. Measure unwinding length and pausing — `PauseAndFinalUnwindingLegnth_forSpecificTime.py`

1. **Copy the folder path** containing your `.h5` files to the clipboard. The script
   reads it with `pyperclip.paste()`, so no editing is needed — just copy the path
   before running.

2. Run the script. For every trace **longer than 60 s** it will:
   - Smooth the signal with a Savitzky–Golay filter
     (`window_length=51`, `polyorder=2`).
   - Record the nt unwound at the target time (`target_t = 60` s) →
     appended to `finalUnwindingLength`.
   - Compute the instantaneous rate (slope) and classify each point as *paused* when
     `|slope| < flat_threshold` (default `2.0` nt/s).
   - Append the paused fraction (%) of the trace to `finalPauseDuration` and print it.
   - Plot the smoothed trace (black) with paused points highlighted (yellow).

3. Results accumulate across all files in the two arrays:
   - `finalUnwindingLength` — nt unwound at 60 s for each qualifying trace
   - `finalPauseDuration` — percentage of the trace spent paused

**Parameters you may want to tune:**

| Parameter | Default | Meaning |
| --- | --- | --- |
| `target_t` | `60` | Time point (s) at which unwinding length is measured. |
| `time[-1] > 60` | `60` | Minimum trace duration (s) required for a file to be analyzed. |
| `window_length` / `polyorder` | `51` / `2` | Savitzky–Golay smoothing window and polynomial order. |
| `flat_threshold` | `2.0` | Rate (nt/s) below which the helicase is considered paused. |

---

## Suggested imports (for standalone runs)

If you run the scripts outside of an interactive session where these are already
loaded, add the following at the top of each file:

```python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import lumicks.pylake as lk
from scipy.signal import medfilt, savgol_filter
import pyperclip   # pause script only
```

---

## Data assumptions

- Input files are LUMICKS `.h5` files containing a `distance1` channel.
- Distance is read via `file.distance1.data` and time via `file.distance1.seconds`.
- All `.h5` files in the selected folder belong to the same substrate/calibration
  (they share the conversion constants).

---

## Output

- **`Marker_Data_analysis_Ctrap_1.py`** — one PDF per trace (distance in nt vs. time)
  saved alongside the source `.h5` files.
- **`PauseAndFinalUnwindingLegnth_forSpecificTime.py`** — in-session plots plus the
  `finalUnwindingLength` and `finalPauseDuration` arrays for downstream analysis or
  export.

---

