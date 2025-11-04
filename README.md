# Gravitational Wave Animation

This project renders a 3D visualization of a spacetime grid distorted by gravitational waves emitted by two orbiting masses. The script generates an animation and saves it as an MP4 file.

## Prerequisites

- Python 3.10 or newer
- FFmpeg available on the system path (required by Matplotlib for MP4 export)

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

Run the animation script from the project root. The rendered movie is written to `outputs/gravitational_wave.mp4`.

```powershell
python src\gravitational_wave_animation.py
```

## Project Structure

- `src/`: Main Python source files.
- `assets/`: Placeholder for future textures or simulation assets.
- `outputs/`: Animation renders exported by the script.

## Notes

- Adjust simulation parameters in `src/gravitational_wave_animation.py` to explore different source masses, separations, and wave amplitudes.
- If FFmpeg is not available, update the writer configuration in the script to another supported backend (for example, PillowWriter for GIF output).
