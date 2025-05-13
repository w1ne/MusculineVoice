# Masculine Voice Analysis Script

## Overview

I built this script to measure my own voice qualities, to improve resonance, depness, and warmness.

This script analyzes the masculine characteristics of a given audio file (voice recording) and visualizes key metrics such as pitch, formants, spectral tilt, and harmonics-to-noise ratio (HNR). It also provides a clear, structured report of the analyzed voice features.

## Features

* Supports both **WAV** and **M4A** audio file formats (for standard Android recorder).
* Visualizes the following metrics:

  * Pitch contour (Time vs Hertz)
  * Spectral tilt (dB/octave)
  * Formant frequencies (F1, F2)
* Generates a detailed report table with the following metrics:

  * Average Pitch (F0)
  * Pitch Variability (95%)
  * Formant 1 (F1)
  * Formant 2 (F2)
  * Spectral Tilt
  * Harmonics-to-Noise Ratio (HNR)
* Saves the visualization as a PNG file, named after the input file.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/username/masculine-voice-analysis.git
   cd masculine-voice-analysis
   ```

2. Set up a Python virtual environment (recommended):

   ```bash
   python3 -m venv voice_env
   source voice_env/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

* Python 3.8+
* parselmouth
* numpy
* librosa
* matplotlib
* scipy
* pydub

## Usage

Run the script from the command line:

```bash
python voice_analyzer.py /path/to/audio.m4a
```

Example:

```bash
python voice_analyzer.py "Sunday at 11-46 PM.m4a"
```

## Output

The script will:

1. Display three plots:

   * Pitch contour (Time vs Hertz)
   * Spectral tilt (dB/octave)
   * Formant frequencies (F1, F2)
2. Print a structured analysis report in the terminal.
3. Save the visualization as a PNG file named after the input file (e.g., `Sunday at 11-46 PM_plot.png`).

## License

MIT License

