import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import spectrogram

def generate_fsk_waveform(data, fs=1000, f0=100, f1=200, bit_duration=1):
    t = np.arange(0, bit_duration * len(data), 1/fs)
    waveform = np.zeros_like(t)
    for i, bit in enumerate(data):
        freq = f1 if bit else f0
        idx_start = int(i * bit_duration * fs)
        idx_end = int((i + 1) * bit_duration * fs)
        waveform[idx_start:idx_end] = np.cos(2 * np.pi * freq * t[idx_start:idx_end])
    return t, waveform

def generate_fm_waveform(data, fs=1000, f0=100, f1=200, bit_duration=1):
    # FM view of FSK waveform, raised to the 2^2 power (4)
    t, fsk_wave = generate_fsk_waveform(data, fs, f0, f1, bit_duration)
    fm_wave = np.sign(fsk_wave) * np.abs(fsk_wave) ** 4  # 2^2 = 4
    return t, fm_wave

class ModulateApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FSK & FM Modulation Viewer")
        self.geometry("1800x950")

        # Parameters
        self.fs = 1000
        self.default_settings = {
            "fsk_f0": 100,
            "fsk_f1": 200,
            "fm_index": 2,
            "fm_carrier": 10,
            "fm_mod": 3,
            "bit_duration": 0.1,
            "data": "1011001",
            "cmap": "viridis",
            "log_power": True,
            "view1": "FSK Time Domain",
            "view2": "FM Time Domain"
        }

        # Controls
        control_frame = ttk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="FSK f0:").pack(side=tk.LEFT)
        self.fsk_f0 = tk.DoubleVar(value=self.default_settings["fsk_f0"])
        self.fsk_f0_scale = ttk.Scale(control_frame, from_=50, to=300, variable=self.fsk_f0, orient=tk.HORIZONTAL, length=120, command=self.update_plot)
        self.fsk_f0_scale.pack(side=tk.LEFT)

        ttk.Label(control_frame, text="FSK f1:").pack(side=tk.LEFT)
        self.fsk_f1 = tk.DoubleVar(value=self.default_settings["fsk_f1"])
        self.fsk_f1_scale = ttk.Scale(control_frame, from_=100, to=400, variable=self.fsk_f1, orient=tk.HORIZONTAL, length=120, command=self.update_plot)
        self.fsk_f1_scale.pack(side=tk.LEFT)

        ttk.Label(control_frame, text="FM Index:").pack(side=tk.LEFT)
        self.fm_index = tk.DoubleVar(value=self.default_settings["fm_index"])
        self.fm_index_scale = ttk.Scale(control_frame, from_=0.5, to=10, variable=self.fm_index, orient=tk.HORIZONTAL, length=120, command=self.update_plot)
        self.fm_index_scale.pack(side=tk.LEFT)

        ttk.Label(control_frame, text="FM Carrier:").pack(side=tk.LEFT)
        self.fm_carrier = tk.DoubleVar(value=self.default_settings["fm_carrier"])
        self.fm_carrier_scale = ttk.Scale(control_frame, from_=1, to=50, variable=self.fm_carrier, orient=tk.HORIZONTAL, length=120, command=self.update_plot)
        self.fm_carrier_scale.pack(side=tk.LEFT)

        ttk.Label(control_frame, text="FM Mod Freq:").pack(side=tk.LEFT)
        self.fm_mod = tk.DoubleVar(value=self.default_settings["fm_mod"])
        self.fm_mod_scale = ttk.Scale(control_frame, from_=1, to=20, variable=self.fm_mod, orient=tk.HORIZONTAL, length=120, command=self.update_plot)
        self.fm_mod_scale.pack(side=tk.LEFT)

        ttk.Label(control_frame, text="Bit Duration:").pack(side=tk.LEFT)
        self.bit_duration = tk.DoubleVar(value=self.default_settings["bit_duration"])
        self.bit_duration_scale = ttk.Scale(control_frame, from_=0.01, to=0.5, variable=self.bit_duration, orient=tk.HORIZONTAL, length=120, command=self.update_plot)
        self.bit_duration_scale.pack(side=tk.LEFT)

        ttk.Label(control_frame, text="FSK Data:").pack(side=tk.LEFT)
        self.data_entry = ttk.Entry(control_frame, width=10)
        self.data_entry.insert(0, self.default_settings["data"])
        self.data_entry.pack(side=tk.LEFT)
        self.data_entry.bind("<Return>", self.update_plot)

        # Colormap selection
        ttk.Label(control_frame, text="Colormap:").pack(side=tk.LEFT)
        self.cmap = tk.StringVar(value=self.default_settings["cmap"])
        cmap_box = ttk.Combobox(control_frame, textvariable=self.cmap, values=["viridis", "plasma", "inferno", "magma", "cividis"], width=8)
        cmap_box.pack(side=tk.LEFT)
        cmap_box.bind("<<ComboboxSelected>>", self.update_plot)

        # Log scale toggle
        self.log_scale = tk.BooleanVar(value=self.default_settings["log_power"])
        ttk.Checkbutton(control_frame, text="Log Power", variable=self.log_scale, command=self.update_plot).pack(side=tk.LEFT)

        # Reset button
        ttk.Button(control_frame, text="Reset to Default", command=self.reset_defaults).pack(side=tk.LEFT, padx=10)

        # View selection buttons (3 per line for each view)
        view_frame = ttk.Frame(self)
        view_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.view1 = tk.StringVar(value=self.default_settings["view1"])
        self.view2 = tk.StringVar(value=self.default_settings["view2"])
        view_options = [
            "FSK Time Domain",
            "FSK Power Spectrum",
            "FSK 2D Spectrogram",
            "FSK 3D Spectrogram",
            "FM Time Domain",
            "FM Power Spectrum",
            "FM 2D Spectrogram",
            "FM 3D Spectrogram"
        ]

        # Split view_options into two lists for each view
        view1_options = view_options[:4]
        view2_options = view_options[4:]

        # View 1 buttons (3 per line)
        ttk.Label(view_frame, text="View 1:").grid(row=0, column=0, sticky="w")
        for i, v in enumerate(view1_options):
            row = 1 + i // 3
            col = i % 3
            btn = ttk.Button(view_frame, text=v, command=lambda vv=v: self.set_view(self.view1, vv))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")

        # View 2 buttons (3 per line)
        ttk.Label(view_frame, text="View 2:").grid(row=0, column=4, sticky="w")
        for i, v in enumerate(view2_options):
            row = 1 + i // 3
            col = 4 + (i % 3)
            btn = ttk.Button(view_frame, text=v, command=lambda vv=v: self.set_view(self.view2, vv))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")

        # Figure and Canvas (two axes used)
        self.fig = Figure(figsize=(16, 7), dpi=100)
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Connect mouse click event for markers
        self.canvas.mpl_connect("button_press_event", self.on_click)

        # Zoom and pan controls for each axis
        zoom_frame = ttk.Frame(self)
        zoom_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        ttk.Label(zoom_frame, text="Zoom/Pan View 1:").grid(row=0, column=0, sticky="w")
        ttk.Button(zoom_frame, text="X+", command=lambda: self.zoom_axis(self.ax1, 'x', 0.8)).grid(row=0, column=1)
        ttk.Button(zoom_frame, text="X-", command=lambda: self.zoom_axis(self.ax1, 'x', 1.2)).grid(row=0, column=2)
        ttk.Button(zoom_frame, text="Y+", command=lambda: self.zoom_axis(self.ax1, 'y', 0.8)).grid(row=0, column=3)
        ttk.Button(zoom_frame, text="Y-", command=lambda: self.zoom_axis(self.ax1, 'y', 1.2)).grid(row=0, column=4)
        ttk.Button(zoom_frame, text="Pan X+", command=lambda: self.pan_axis(self.ax1, 'x', 0.2)).grid(row=0, column=5)
        ttk.Button(zoom_frame, text="Pan X-", command=lambda: self.pan_axis(self.ax1, 'x', -0.2)).grid(row=0, column=6)
        ttk.Button(zoom_frame, text="Pan Y+", command=lambda: self.pan_axis(self.ax1, 'y', 0.2)).grid(row=0, column=7)
        ttk.Button(zoom_frame, text="Pan Y-", command=lambda: self.pan_axis(self.ax1, 'y', -0.2)).grid(row=0, column=8)
        ttk.Button(zoom_frame, text="Reset", command=lambda: self.reset_axis(self.ax1)).grid(row=0, column=9)

        ttk.Label(zoom_frame, text="Zoom/Pan View 2:").grid(row=1, column=0, sticky="w")
        ttk.Button(zoom_frame, text="X+", command=lambda: self.zoom_axis(self.ax2, 'x', 0.8)).grid(row=1, column=1)
        ttk.Button(zoom_frame, text="X-", command=lambda: self.zoom_axis(self.ax2, 'x', 1.2)).grid(row=1, column=2)
        ttk.Button(zoom_frame, text="Y+", command=lambda: self.zoom_axis(self.ax2, 'y', 0.8)).grid(row=1, column=3)
        ttk.Button(zoom_frame, text="Y-", command=lambda: self.zoom_axis(self.ax2, 'y', 1.2)).grid(row=1, column=4)
        ttk.Button(zoom_frame, text="Pan X+", command=lambda: self.pan_axis(self.ax2, 'x', 0.2)).grid(row=1, column=5)
        ttk.Button(zoom_frame, text="Pan X-", command=lambda: self.pan_axis(self.ax2, 'x', -0.2)).grid(row=1, column=6)
        ttk.Button(zoom_frame, text="Pan Y+", command=lambda: self.pan_axis(self.ax2, 'y', 0.2)).grid(row=1, column=7)
        ttk.Button(zoom_frame, text="Pan Y-", command=lambda: self.pan_axis(self.ax2, 'y', -0.2)).grid(row=1, column=8)
        ttk.Button(zoom_frame, text="Reset", command=lambda: self.reset_axis(self.ax2)).grid(row=1, column=9)

        # Marker controls
        marker_frame = ttk.Frame(self)
        marker_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        ttk.Label(marker_frame, text="Marker 1 (X):").grid(row=0, column=0)
        self.marker1_x = tk.DoubleVar(value=0.0)
        marker1_entry = ttk.Entry(marker_frame, textvariable=self.marker1_x, width=10)
        marker1_entry.grid(row=0, column=1)
        ttk.Label(marker_frame, text="Marker 2 (X):").grid(row=0, column=2)
        self.marker2_x = tk.DoubleVar(value=0.0)
        marker2_entry = ttk.Entry(marker_frame, textvariable=self.marker2_x, width=10)
        marker2_entry.grid(row=0, column=3)
        ttk.Button(marker_frame, text="Update Markers", command=self.update_plot).grid(row=0, column=4)
        ttk.Button(marker_frame, text="Reset Markers", command=self.reset_markers).grid(row=0, column=5, padx=5)
        self.marker_label = ttk.Label(marker_frame, text="")
        self.marker_label.grid(row=0, column=6, padx=10)

        self._axis_limits = {}  # Store default axis limits for reset
        self._next_marker = 1   # Track which marker to set next on click
        self.update_plot()

    def set_view(self, view_var, view_name):
        view_var.set(view_name)
        self.update_plot()

    def reset_defaults(self):
        self.fsk_f0.set(self.default_settings["fsk_f0"])
        self.fsk_f1.set(self.default_settings["fsk_f1"])
        self.fm_index.set(self.default_settings["fm_index"])
        self.fm_carrier.set(self.default_settings["fm_carrier"])
        self.fm_mod.set(self.default_settings["fm_mod"])
        self.bit_duration.set(self.default_settings["bit_duration"])
        self.data_entry.delete(0, tk.END)
        self.data_entry.insert(0, self.default_settings["data"])
        self.cmap.set(self.default_settings["cmap"])
        self.log_scale.set(self.default_settings["log_power"])
        self.view1.set(self.default_settings["view1"])
        self.view2.set(self.default_settings["view2"])
        self.marker1_x.set(0.0)
        self.marker2_x.set(0.0)
        self._next_marker = 1
        self.update_plot()

    def update_plot(self, event=None):
        # Get parameters
        f0 = self.fsk_f0.get()
        f1 = self.fsk_f1.get()
        mod_index = self.fm_index.get()
        f_carrier = self.fm_carrier.get()
        f_mod = self.fm_mod.get()
        bit_duration = self.bit_duration.get()
        cmap = self.cmap.get()
        log_power = self.log_scale.get()
        view1 = self.view1.get()
        view2 = self.view2.get()
        marker1_x = self.marker1_x.get()
        marker2_x = self.marker2_x.get()

        # Get data sequence
        try:
            data_str = self.data_entry.get()
            data = [int(b) for b in data_str if b in "01"]
            if not data:
                data = [1, 0, 1, 1, 0, 0, 1]
        except Exception:
            data = [1, 0, 1, 1, 0, 0, 1]
        self.data = data

        # FSK
        t_fsk, modulated_waveform = generate_fsk_waveform(self.data, fs=self.fs, f0=f0, f1=f1, bit_duration=bit_duration)
        freqs_fsk = np.fft.rfftfreq(len(modulated_waveform), d=1/self.fs)
        power_spectrum_fsk = np.abs(np.fft.rfft(modulated_waveform))**2
        f_fsk, tt_fsk, Sxx_fsk = spectrogram(modulated_waveform, self.fs)

        # FM (2^2 power view of FSK)
        t_fm, fm_waveform = generate_fm_waveform(self.data, fs=self.fs, f0=f0, f1=f1, bit_duration=bit_duration)
        freqs_fm = np.fft.rfftfreq(len(fm_waveform), d=1/self.fs)
        power_spectrum_fm = np.abs(np.fft.rfft(fm_waveform))**2
        f_fm, tt_fm, Sxx_fm = spectrogram(fm_waveform, self.fs)

        # Clear axes
        self.fig.clf()
        ax1_is_3d = "3D" in view1
        ax2_is_3d = "3D" in view2
        self.ax1 = self.fig.add_subplot(121, projection='3d' if ax1_is_3d else None)
        self.ax2 = self.fig.add_subplot(122, projection='3d' if ax2_is_3d else None)

        # Helper for plotting
        def plot_view(ax, view, marker_xs):
            marker_vals = []
            marker_labels = ["Marker 1", "Marker 2"]
            if view == "FSK Time Domain":
                ax.plot(t_fsk, modulated_waveform)
                ax.set_title("FSK Time Domain")
                ax.set_xlabel("Time [s]")
                ax.set_ylabel("Amplitude")
                for i, mx in enumerate(marker_xs):
                    idx = (np.abs(t_fsk - mx)).argmin()
                    val = modulated_waveform[idx] if 0 <= idx < len(modulated_waveform) else None
                    if val is not None:
                        ax.axvline(mx, color='r', linestyle='--')
                        ax.plot(mx, val, 'ro')
                        ax.annotate(marker_labels[i], xy=(mx, val), xytext=(5, 5), textcoords='offset points', color='red', fontsize=10, fontweight='bold')
                        marker_vals.append((mx, val))
            elif view == "FSK Power Spectrum":
                y_fsk = 10 * np.log10(power_spectrum_fsk) if log_power else power_spectrum_fsk
                ax.plot(freqs_fsk, y_fsk)
                ax.set_title("FSK Power Spectrum")
                ax.set_xlabel("Frequency [Hz]")
                ax.set_ylabel("Power [dB]" if log_power else "Power")
                for i, mx in enumerate(marker_xs):
                    idx = (np.abs(freqs_fsk - mx)).argmin()
                    val = y_fsk[idx] if 0 <= idx < len(y_fsk) else None
                    if val is not None:
                        ax.axvline(mx, color='r', linestyle='--')
                        ax.plot(mx, val, 'ro')
                        ax.annotate(marker_labels[i], xy=(mx, val), xytext=(5, 5), textcoords='offset points', color='red', fontsize=10, fontweight='bold')
                        marker_vals.append((mx, val))
            elif view == "FSK 2D Spectrogram":
                Sxx_fsk_plot = 10 * np.log10(Sxx_fsk) if log_power else Sxx_fsk
                pcm = ax.pcolormesh(tt_fsk, f_fsk, Sxx_fsk_plot, shading='gouraud', cmap=cmap)
                ax.set_title("FSK 2D Spectrogram")
                ax.set_xlabel("Time [s]")
                ax.set_ylabel("Frequency [Hz]")
                self.fig.colorbar(pcm, ax=ax, label='Power [dB]' if log_power else 'Power')
                for i, mx in enumerate(marker_xs):
                    ax.axvline(mx, color='r', linestyle='--')
                    ax.annotate(marker_labels[i], xy=(mx, f_fsk[-1]), xytext=(5, -15), textcoords='offset points', color='red', fontsize=10, fontweight='bold')
                    marker_vals.append((mx, None))
            elif view == "FSK 3D Spectrogram":
                T_fsk, F_fsk = np.meshgrid(tt_fsk, f_fsk)
                Z_fsk = 10 * np.log10(Sxx_fsk) if log_power else Sxx_fsk
                ax.plot_surface(T_fsk, F_fsk, Z_fsk, cmap=cmap)
                ax.set_title("FSK 3D Spectrogram")
                ax.set_xlabel("Time [s]")
                ax.set_ylabel("Frequency [Hz]")
                ax.set_zlabel("Power [dB]" if log_power else "Power")
                # Default 3D controls (no markers, no zoom/pan)
            elif view == "FM Time Domain":
                ax.plot(t_fm, fm_waveform)
                ax.set_title("FM Time Domain")
                ax.set_xlabel("Time [s]")
                ax.set_ylabel("Amplitude")
                for i, mx in enumerate(marker_xs):
                    idx = (np.abs(t_fm - mx)).argmin()
                    val = fm_waveform[idx] if 0 <= idx < len(fm_waveform) else None
                    if val is not None:
                        ax.axvline(mx, color='r', linestyle='--')
                        ax.plot(mx, val, 'ro')
                        ax.annotate(marker_labels[i], xy=(mx, val), xytext=(5, 5), textcoords='offset points', color='red', fontsize=10, fontweight='bold')
                        marker_vals.append((mx, val))
            elif view == "FM Power Spectrum":
                y_fm = 10 * np.log10(power_spectrum_fm) if log_power else power_spectrum_fm
                ax.plot(freqs_fm, y_fm)
                ax.set_title("FM Power Spectrum")
                ax.set_xlabel("Frequency [Hz]")
                ax.set_ylabel("Power [dB]" if log_power else "Power")
                for i, mx in enumerate(marker_xs):
                    idx = (np.abs(freqs_fm - mx)).argmin()
                    val = y_fm[idx] if 0 <= idx < len(y_fm) else None
                    if val is not None:
                        ax.axvline(mx, color='r', linestyle='--')
                        ax.plot(mx, val, 'ro')
                        ax.annotate(marker_labels[i], xy=(mx, val), xytext=(5, 5), textcoords='offset points', color='red', fontsize=10, fontweight='bold')
                        marker_vals.append((mx, val))
            elif view == "FM 2D Spectrogram":
                Sxx_fm_plot = 10 * np.log10(Sxx_fm) if log_power else Sxx_fm
                pcm = ax.pcolormesh(tt_fm, f_fm, Sxx_fm_plot, shading='gouraud', cmap=cmap)
                ax.set_title("FM 2D Spectrogram")
                ax.set_xlabel("Time [s]")
                ax.set_ylabel("Frequency [Hz]")
                self.fig.colorbar(pcm, ax=ax, label='Power [dB]' if log_power else 'Power')
                for i, mx in enumerate(marker_xs):
                    ax.axvline(mx, color='r', linestyle='--')
                    ax.annotate(marker_labels[i], xy=(mx, f_fm[-1]), xytext=(5, -15), textcoords='offset points', color='red', fontsize=10, fontweight='bold')
                    marker_vals.append((mx, None))
            elif view == "FM 3D Spectrogram":
                T_fm, F_fm = np.meshgrid(tt_fm, f_fm)
                Z_fm = 10 * np.log10(Sxx_fm) if log_power else Sxx_fm
                ax.plot_surface(T_fm, F_fm, Z_fm, cmap=cmap)
                ax.set_title("FM 3D Spectrogram")
                ax.set_xlabel("Time [s]")
                ax.set_ylabel("Frequency [Hz]")
                ax.set_zlabel("Power [dB]" if log_power else "Power")
                # Default 3D controls (no markers, no zoom/pan)
            return marker_vals

        marker_vals1 = plot_view(self.ax1, self.view1.get(), [self.marker1_x.get(), self.marker2_x.get()])
        marker_vals2 = plot_view(self.ax2, self.view2.get(), [self.marker1_x.get(), self.marker2_x.get()])

        # Store default axis limits for reset
        self._axis_limits[self.ax1] = self.ax1.axis()
        self._axis_limits[self.ax2] = self.ax2.axis()

        # Display marker values
        marker_text = f"View 1 Markers: {marker_vals1} | View 2 Markers: {marker_vals2}"
        self.marker_label.config(text=marker_text)

        self.fig.tight_layout()
        self.canvas.draw()

    def zoom_axis(self, ax, axis, factor):
        # Get current limits
        if axis == 'x':
            xmin, xmax = ax.get_xlim()
            xmid = (xmin + xmax) / 2
            xlen = (xmax - xmin) * factor / 2
            ax.set_xlim(xmid - xlen, xmid + xlen)
        elif axis == 'y':
            ymin, ymax = ax.get_ylim()
            ymid = (ymin + ymax) / 2
            ylen = (ymax - ymin) * factor / 2
            ax.set_ylim(ymid - ylen, ymid + ylen)
        self.canvas.draw()

    def pan_axis(self, ax, axis, frac):
        # Pan axis by fraction of current range
        if axis == 'x':
            xmin, xmax = ax.get_xlim()
            xlen = xmax - xmin
            ax.set_xlim(xmin + frac * xlen, xmax + frac * xlen)
        elif axis == 'y':
            ymin, ymax = ax.get_ylim()
            ylen = ymax - ymin
            ax.set_ylim(ymin + frac * ylen, ymax + frac * ylen)
        self.canvas.draw()

    def reset_axis(self, ax):
        # Reset to stored default axis limits
        if ax in self._axis_limits:
            ax.axis(self._axis_limits[ax])
            self.canvas.draw()

    def on_click(self, event):
        # Only respond to clicks inside axes
        if event.inaxes is None:
            return
        # Determine which axis was clicked
        if event.inaxes == self.ax1:
            # Alternate between marker 1 and marker 2
            if self._next_marker == 1:
                self.marker1_x.set(event.xdata)
                self._next_marker = 2
            else:
                self.marker2_x.set(event.xdata)
                self._next_marker = 1
            self.update_plot()
        elif event.inaxes == self.ax2:
            # Alternate between marker 1 and marker 2
            if self._next_marker == 1:
                self.marker1_x.set(event.xdata)
                self._next_marker = 2
            else:
                self.marker2_x.set(event.xdata)
                self._next_marker = 1
            self.update_plot()

    def reset_markers(self):
        self.marker1_x.set(0.0)
        self.marker2_x.set(0.0)
        self._next_marker = 1

if __name__ == "__main__":
    app = ModulateApp()
    app.mainloop()