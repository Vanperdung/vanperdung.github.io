import numpy as np
import matplotlib.pyplot as plt

def compute_fft(signal, N):
    spectrum  = np.fft.rfft(signal)
    freqs     = np.fft.rfftfreq(N)
    magnitude = 2 * np.abs(spectrum) / N
    return freqs, magnitude

def plot_windowing_demo(signal_freq=5.0, num_cycles=5.3):
    N  = 4096
    T  = num_cycles / signal_freq
    t  = np.linspace(0, T, N, endpoint=False)
    fs = N / T  # sample rate

    raw     = np.sin(2 * np.pi * signal_freq * t)
    window  = np.hanning(N)
    windowed = raw * window

    freqs_raw, mag_raw = compute_fft(raw, N)
    freqs_win, mag_win = compute_fft(windowed, N)
    freq_axis_raw = freqs_raw * fs
    freq_axis_win = freqs_win * fs

    GREEN  = "#1D9E75"
    ORANGE = "#E24B4A"
    PURPLE = "#7F77DD"
    BLUE   = "#3266ad"
    GRAY   = "#888780"

    fig, axes = plt.subplots(3, 2, figsize=(14, 11))
    fig.suptitle(
        f"Windowing Demo — f = {signal_freq} Hz, {num_cycles} cycles (non-integer)\n"
        "Left: No window (Rectangular)    Right: Hanning Window applied",
        fontsize=13, fontweight="bold"
    )

    max_plot_freq = signal_freq * 5

    # ── Row 0: raw signal vs windowed signal ───────────────────────────────
    ax = axes[0, 0]
    ax.plot(t, raw, color=ORANGE, linewidth=1.2, label="Raw signal")
    ax.axvline(0,  color=GRAY, linewidth=0.8, linestyle="--", alpha=0.5)
    ax.axvline(T,  color=GRAY, linewidth=0.8, linestyle="--", alpha=0.5, label="Window boundary")
    ax.annotate(
        "Discontinuity!",
        xy=(T, raw[-1]), xytext=(T * 0.70, 1.2),
        arrowprops=dict(arrowstyle="->", color=ORANGE),
        color=ORANGE, fontsize=9
    )
    ax.set_title("Time Domain — No window (Rectangular)", fontsize=10)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_ylim(-1.6, 1.6)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)

    ax = axes[0, 1]
    ax.plot(t, raw,      color=ORANGE, linewidth=0.8, alpha=0.35, label="Raw signal")
    ax.plot(t, windowed, color=GREEN,  linewidth=1.2, label="Windowed signal")
    ax.fill_between(t, windowed, alpha=0.08, color=GREEN)
    ax.set_title("Time Domain — Hanning window applied", fontsize=10)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_ylim(-1.6, 1.6)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)

    # ── Row 1: the window function itself ──────────────────────────────────
    ax = axes[1, 0]
    rect = np.ones(N)
    ax.plot(t, rect, color=ORANGE, linewidth=1.4, label="Rectangular window")
    ax.set_title("Window Function — Rectangular (box)", fontsize=10)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Weight")
    ax.set_ylim(-0.1, 1.3)
    ax.fill_between(t, rect, alpha=0.12, color=ORANGE)
    ax.annotate("Sharp edges →\nartificial discontinuity",
                xy=(T, 1.0), xytext=(T * 0.55, 1.1),
                arrowprops=dict(arrowstyle="->", color=ORANGE),
                color=ORANGE, fontsize=9)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)

    ax = axes[1, 1]
    ax.plot(t, window, color=PURPLE, linewidth=1.4, label="Hanning window")
    ax.fill_between(t, window, alpha=0.12, color=PURPLE)
    ax.annotate("Tapers to zero\nat both ends",
                xy=(0, 0), xytext=(T * 0.08, 0.55),
                arrowprops=dict(arrowstyle="->", color=PURPLE),
                color=PURPLE, fontsize=9)
    ax.set_title("Window Function — Hanning (smooth taper)", fontsize=10)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Weight")
    ax.set_ylim(-0.1, 1.3)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)

    # ── Row 2: FFT spectra comparison ──────────────────────────────────────
    mask_r = freq_axis_raw <= max_plot_freq
    mask_w = freq_axis_win <= max_plot_freq
    bw = freq_axis_raw[1] - freq_axis_raw[0]

    ax = axes[2, 0]
    colors_raw = [
        GREEN if abs(f - signal_freq) < signal_freq * 0.12 else ORANGE
        for f in freq_axis_raw[mask_r]
    ]
    ax.bar(freq_axis_raw[mask_r], mag_raw[mask_r], width=bw,
           color=colors_raw, align="center")
    ax.axvline(signal_freq, color=BLUE, linewidth=1.2, linestyle="--",
               label=f"True freq: {signal_freq} Hz")
    ax.text(signal_freq * 1.08, mag_raw[np.argmax(mag_raw)] * 0.6,
            "Energy leaks\ninto neighbors", color=ORANGE, fontsize=8)
    ax.set_title("FFT Spectrum — No window  ⚠  Spectral leakage", fontsize=10, color=ORANGE)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2, axis="y")

    ax = axes[2, 1]
    colors_win = [
        GREEN if abs(f - signal_freq) < signal_freq * 0.12 else "#1D9E7540"
        for f in freq_axis_win[mask_w]
    ]
    ax.bar(freq_axis_win[mask_w], mag_win[mask_w], width=bw,
           color=colors_win, align="center")
    ax.axvline(signal_freq, color=BLUE, linewidth=1.2, linestyle="--",
               label=f"True freq: {signal_freq} Hz")
    ax.text(signal_freq * 1.08, mag_win[np.argmax(mag_win)] * 0.6,
            "Leakage\nsuppressed", color=GREEN, fontsize=8)
    ax.set_title("FFT Spectrum — Hanning window  ✓  Leakage reduced", fontsize=10, color=GREEN)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2, axis="y")

    plt.tight_layout()
    plt.savefig("spectral_leakage.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("Saved → spectral_leakage.png")


if __name__ == "__main__":
    plot_windowing_demo(signal_freq=5, num_cycles=5.3)