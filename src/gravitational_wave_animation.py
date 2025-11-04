"""Render a 3D gravitational wave animation and save it as an MP4 file."""

from pathlib import Path
from typing import Tuple

import numpy as np
from matplotlib import animation
from matplotlib import cm
from matplotlib import pyplot as plt

# Simulation constants
FPS = 30
DURATION = 12  # seconds
TOTAL_FRAMES = FPS * DURATION
SPACE_EXTENT = 6.0
GRID_POINTS = 60
WAVE_SPEED = 1.0
WAVE_AMPLITUDE = 0.6
WAVE_NUMBER = 2.0
GAUSSIAN_FALLOFF = 18.0
ORBITAL_RADIUS = 1.4
ORBITAL_PERIOD = 4.0  # seconds
# Colors chosen to contrast strongly with Viridis surface
MASS_COLORS = ("#ff1744", "#f5f5f5")
MASS_HEIGHT_OFFSET = 0.9
# Save destination
OUTPUT_FILE = Path(__file__).resolve().parents[1] / "outputs" / "gravitational_wave.mp4"


def _build_grid() -> Tuple[np.ndarray, np.ndarray]:
    """Prepare the spacetime mesh grid."""
    axis = np.linspace(-SPACE_EXTENT, SPACE_EXTENT, GRID_POINTS)
    return np.meshgrid(axis, axis)


def _mass_positions(time_seconds: float) -> Tuple[np.ndarray, np.ndarray]:
    """Compute the planar positions of the two orbiting masses."""
    angular_velocity = 2.0 * np.pi / ORBITAL_PERIOD
    angle = angular_velocity * time_seconds
    offset = ORBITAL_RADIUS
    first = np.array([offset * np.cos(angle), offset * np.sin(angle)])
    second = np.array([-offset * np.cos(angle), -offset * np.sin(angle)])
    return first, second


def _wave_displacement_at(x_coord: float, y_coord: float, time_seconds: float) -> float:
    """Return the wave displacement at a single coordinate."""
    radius = np.sqrt(x_coord**2 + y_coord**2) + 1e-6
    phase = WAVE_NUMBER * radius - (2.0 * np.pi / ORBITAL_PERIOD) * time_seconds * WAVE_SPEED
    polarization = (x_coord**2 - y_coord**2) / (SPACE_EXTENT**2)
    envelope = np.exp(-radius**2 / GAUSSIAN_FALLOFF)
    return WAVE_AMPLITUDE * np.sin(phase) * polarization * envelope


def _wave_deformation(x_grid: np.ndarray, y_grid: np.ndarray, time_seconds: float) -> np.ndarray:
    """Calculate wave displacement for each grid point."""
    r = np.sqrt(x_grid**2 + y_grid**2) + 1e-6
    phase = WAVE_NUMBER * r - (2.0 * np.pi / ORBITAL_PERIOD) * time_seconds * WAVE_SPEED
    polarization = (x_grid**2 - y_grid**2) / (SPACE_EXTENT**2)
    envelope = np.exp(-r**2 / GAUSSIAN_FALLOFF)
    return WAVE_AMPLITUDE * np.sin(phase) * polarization * envelope


def _setup_axes(ax: plt.Axes) -> None:
    ax.set_xlim(-SPACE_EXTENT, SPACE_EXTENT)
    ax.set_ylim(-SPACE_EXTENT, SPACE_EXTENT)
    ax.set_zlim(-1.5, 1.5)
    ax.set_box_aspect((1, 1, 0.5))
    ax.set_xlabel("x (space)")
    ax.set_ylabel("y (space)")
    ax.set_zlabel("z (strain)")
    ax.view_init(elev=30, azim=45)
    ax.set_title("Gravitational Wave Distortion")


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    x_grid, y_grid = _build_grid()

    fig = plt.figure(figsize=(8, 6), constrained_layout=True)
    ax = fig.add_subplot(111, projection="3d")
    _setup_axes(ax)

    surface = [None]
    masses = [None]

    def init():
        ax.clear()
        _setup_axes(ax)
        z_grid = _wave_deformation(x_grid, y_grid, 0.0)
        surface[0] = ax.plot_surface(x_grid, y_grid, z_grid, cmap=cm.viridis, linewidth=0, antialiased=True, alpha=0.85)
        first, second = _mass_positions(0.0)
        first_z = _wave_displacement_at(first[0], first[1], 0.0) + MASS_HEIGHT_OFFSET
        second_z = _wave_displacement_at(second[0], second[1], 0.0) + MASS_HEIGHT_OFFSET
        masses[0] = ax.scatter(
            [first[0], second[0]],
            [first[1], second[1]],
            [first_z, second_z],
            c=list(MASS_COLORS),
            s=150,            # Increased size
            edgecolors="black", # Added for crisp border
            alpha=1.0,          # Ensure full opacity
            depthshade=False,   # Stop depth-based dimming
            zorder=10            # Draw on top of the surface
        )
        return surface[0], masses[0]

    def update(frame_index: int):
        time_seconds = frame_index / FPS
        ax.clear()
        _setup_axes(ax)

        z_grid = _wave_deformation(x_grid, y_grid, time_seconds)
        surface[0] = ax.plot_surface(x_grid, y_grid, z_grid, cmap=cm.viridis, linewidth=0, antialiased=True, alpha=0.85)

        first, second = _mass_positions(time_seconds)
        first_z = _wave_displacement_at(first[0], first[1], time_seconds) + MASS_HEIGHT_OFFSET
        second_z = _wave_displacement_at(second[0], second[1], time_seconds) + MASS_HEIGHT_OFFSET
        masses[0] = ax.scatter(
            [first[0], second[0]],
            [first[1], second[1]],
            [first_z, second_z],
            c=list(MASS_COLORS),
            s=150,            # Increased size
            edgecolors="black",
            alpha=1.0,          # Ensure full opacity
            depthshade=False,   # Stop depth-based dimming
            zorder=10            # Draw on top of the surface
        )

        ax.contour(
            x_grid,
            y_grid,
            z_grid,
            levels=8,
            zdir="z",
            offset=-1.5,
            cmap="plasma",
            linewidths=0.6,
        )
        return surface[0], masses[0]

    anim = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=TOTAL_FRAMES,
        interval=1000 / FPS,
        blit=False,
    )

    writer = animation.FFMpegWriter(fps=FPS, bitrate=1800, metadata={"artist": "GitHub Copilot"})
    print(f"Saving animation to {OUTPUT_FILE}")
    anim.save(OUTPUT_FILE, writer=writer, dpi=160)
    plt.close(fig)
    print("Render complete.")


if __name__ == "__main__":
    main()
