import argparse
import parselmouth
from parselmouth.praat import call
import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy.signal import welch
from pydub import AudioSegment

def convert_m4a_to_wav(file_path):
    if file_path.lower().endswith(".m4a"):
        sound = AudioSegment.from_file(file_path, format="m4a")
        wav_path = file_path.replace(".m4a", ".wav")
        sound.export(wav_path, format="wav")
        return wav_path
    return file_path


def print_analysis_table(mean_pitch, std_pitch, f1, f2, tilt, hnr):
    print("\nMasculine Voice Analysis Report:")
    print(f"{'Metric':<25}{'Current Value':<20}{'Target Range'}")
    print("-" * 70)
    print(f"{'Avg. Pitch (F0)':<25}{mean_pitch:.2f} Hz{'90–115 Hz':>20}")
    print(f"{'Pitch Variability (95%)':<25}{std_pitch:.2f} Hz{'30–45 Hz':>20}")
    print(f"{'Formant 1 (F1)':<25}{f1:.2f} Hz{'300–700 Hz':>20}")
    print(f"{'Formant 2 (F2)':<25}{f2:.2f} Hz{'800–1500 Hz':>20}")
    print(f"{'Spectral Tilt':<25}{tilt:.2f} dB/oct{'-10 to -5 dB/octave':>20}")
    print(f"{'HNR (Harmonics-to-Noise)':<25}{hnr:.2f} dB{'15–20 dB':>20}")
    print("-" * 70)
def analyze_voice(file_path):
    file_path = convert_m4a_to_wav(file_path)

    snd = parselmouth.Sound(file_path)
    pitch = snd.to_pitch()
    mean_pitch = call(pitch, "Get mean", 0, 0, "Hertz")
    std_pitch = call(pitch, "Get standard deviation", 0, 0, "Hertz")
    harmonicity = snd.to_harmonicity_cc()
    hnr = call(harmonicity, "Get mean", 0, 0)

    formant = snd.to_formant_burg(time_step=0.025, max_number_of_formants=5, maximum_formant=5000)
    f1 = formant.get_value_at_time(1, 0.5)
    f2 = formant.get_value_at_time(2, 0.5)

    y, sr = librosa.load(file_path, sr=None)
    freqs, psd = welch(y, sr, nperseg=1024)
    tilt = np.polyfit(np.log(freqs[1:]), 10 * np.log10(psd[1:]), 1)[0]

    plt.figure(figsize=(14, 10))

    plt.subplot(3, 1, 1)
    pitch_values = pitch.selected_array["frequency"]
    pitch_values[pitch_values == 0] = np.nan
    pitch_values[pitch_values > 300] = np.nan
    plt.plot(pitch.xs(), pitch_values, label="Pitch contour", color="blue")
    plt.title("Pitch Contour (Time vs Hertz)")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")

    plt.subplot(3, 1, 2)
    plt.semilogx(freqs, 10 * np.log10(psd), label="Spectral Tilt", color="green")
    plt.title(f"Spectral Tilt: {tilt:.2f} dB/octave")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power (dB)")

    plt.subplot(3, 1, 3)
    bars = plt.bar([1, 2], [f1, f2], tick_label=["F1", "F2"], color="orange")
    plt.title("Formant Frequencies (F1, F2)")
    plt.xlabel("Formant")
    plt.ylabel("Frequency (Hz)")
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 20, f'{yval:.1f}', ha='center', va='bottom')

    plt.tight_layout()
    output_path = file_path.replace('.wav', '_plot.png').replace('.m4a', '_plot.png')
    plt.savefig(output_path)
    print(f"Plot saved as {output_path}")
    plt.show()
    print("Plot saved as voice_analysis_improved.png")

    print_analysis_table(mean_pitch, std_pitch, f1, f2, tilt, hnr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Masculine Voice Analysis Script")
    parser.add_argument("file", help="Path to the audio file (WAV or M4A)")
    args = parser.parse_args()
    analyze_voice(args.file)

