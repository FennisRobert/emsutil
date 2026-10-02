# EMerge is an open source Python based FEM EM simulation module.
# Copyright (C) 2025  Robert Fennis.

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, see
# <https://www.gnu.org/licenses/>.

from __future__ import annotations

import time
from importlib.resources import files
from pathlib import Path
from typing import Any, Callable, Literal

import numpy as np
import pyvista as pv
from loguru import logger

from ..emdata import DataStructure, FieldPlotData
from .display_settings import EMergeTheme, PVDisplaySettings
from .utils import determine_projection_data

### Color scale

# Define the colors we want to use
col1 = np.array([57, 179, 227, 255]) / 255
col2 = np.array([22, 36, 125, 255]) / 255
col3 = np.array([33, 33, 33, 255]) / 255
col4 = np.array([173, 76, 7, 255]) / 255
col5 = np.array([250, 75, 148, 255]) / 255

cmap_names = Literal[
    "bgy",
    "bgyw",
    "kbc",
    "blues",
    "bmw",
    "bmy",
    "kgy",
    "gray",
    "dimgray",
    "fire",
    "kb",
    "kg",
    "kr",
    "bkr",
    "bky",
    "coolwarm",
    "gwv",
    "bjy",
    "bwy",
    "cwr",
    "colorwheel",
    "isolum",
    "rainbow",
    "fire",
    "cet_fire",
    "gouldian",
    "kbgyw",
    "cwr",
    "CET_CBL1",
    "CET_CBL3",
    "CET_D1A",
]


def nanminmax(arr):
    valid = arr[~np.isnan(arr)]
    return valid.min(), valid.max()


# Data processing

from scipy.spatial import KDTree


def _min_distance(xs, ys, zs):
    """Finds the single smallest distance between any two points in a point cloud

    using an efficient O(N log N) KD-Tree approach.

    Parameters:
    -----------
    points : np.ndarray
        An (N, 2) or (N, 3) array of coordinates.

    Returns:
    --------
    float
        The minimum distance between the two closest points in the dataset.
    """
    points = np.array([xs, ys, zs]).T

    if len(points) < 2:
        return 0.0

    tree = KDTree(points)
    distances, _ = tree.query(points, k=2)

    closest_neighbor_distances = distances[:, 1]
    return float(np.min(closest_neighbor_distances))

def ruler_snap_points(datasets):
    """Collect vertices along sharp edges and boundaries."""
    chunks = []

    for mesh in datasets:
        if mesh.n_points == 0:
            continue

        surface = mesh.extract_surface(algorithm="dataset_surface").clean()

        if surface.n_cells == 0:
            points = surface.points
        else:
            edges = surface.extract_feature_edges(
                feature_angle=30,
                boundary_edges=True,
                non_manifold_edges=True,
                feature_edges=True,
                manifold_edges=False,
            )
            points = edges.points

        if len(points):
            chunks.append(np.asarray(points))

    if not chunks:
        return np.empty((0, 3))

    return np.unique(np.vstack(chunks), axis=0)

class _RunState:
    def __init__(self):
        self.state: bool = False
        self.ctr: int = 0

    def run(self):
        self.state = True
        self.ctr = 0

    def stop(self):
        self.state = False
        self.ctr = 0

    def step(self):
        self.ctr += 1


ANIM_STATE = _RunState()


def _logscale(dx, dy, dz):
    """
    Logarithmically scales vector magnitudes so that the largest remains unchanged
    and others are scaled down logarithmically.

    Parameters:
        dx, dy, dz (np.ndarray): Components of vectors.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: Scaled dx, dy, dz arrays.
    """
    dx = np.asarray(dx)
    dy = np.asarray(dy)
    dz = np.asarray(dz)

    # Compute original magnitudes
    mags = np.sqrt(dx**2 + dy**2 + dz**2)
    mags_nonzero = np.where(mags == 0, 1e-10, mags)  # avoid log(0)

    # Logarithmic scaling (scaled to max = original max)
    log_mags = np.log10(mags_nonzero)
    log_min = np.min(log_mags)
    log_max = np.max(log_mags)

    if log_max == log_min:
        # All vectors have the same length
        return dx, dy, dz

    # Normalize log magnitudes to [0, 1]
    log_scaled = (log_mags - log_min) / (log_max - log_min)

    # Scale back to original max magnitude
    max_mag = np.max(mags)
    new_mags = log_scaled * max_mag

    # Compute unit vectors
    unit_dx = dx / mags_nonzero
    unit_dy = dy / mags_nonzero
    unit_dz = dz / mags_nonzero

    # Apply scaled magnitudes
    scaled_dx = unit_dx * new_mags
    scaled_dy = unit_dy * new_mags
    scaled_dz = unit_dz * new_mags

    return scaled_dx, scaled_dy, scaled_dz


def _norm(x, y, z):
    return np.sqrt(np.abs(x) ** 2 + np.abs(y) ** 2 + np.abs(z) ** 2)


class _AnimObject:
    """A private class containing the required information for plot items in a view
    that can be animated.
    """

    def __init__(
        self,
        field: np.ndarray,
        T: Callable,
        grid: pv.Grid,
        filtered_grid: pv.Grid,
        actor: pv.Actor,
        on_update: Callable,
    ):
        self.field: np.ndarray = field
        self.T: Callable = T
        self.grid: pv.Grid = grid
        self.fgrid: pv.Grid = filtered_grid
        self.actor: pv.Actor = actor
        self.on_update: Callable = on_update

    def update(self, phi: complex):
        self.on_update(self, phi)


class EMergeDisplay:
    def __init__(self, *args, **kwargs):

        self.set: PVDisplaySettings = PVDisplaySettings()

        # Animation options
        self._facetags: dict[int, str] = dict()
        self._stop: bool = False
        self._objs: list[_AnimObject] = []
        self._do_animate: bool = False
        self._animate_next: bool = False
        self._closed_via_x: bool = False
        self._Nsteps: int = 0
        self._fps: int = 25
        self._ruler: ScreenRuler = ScreenRuler(self)
        self._selector: ScreenSelector = ScreenSelector(self)
        self._stop = False
        self._objs = []
        self._data_sets: list[pv.DataSet] = []

        self._plot: pv.Plotter | None = None
        self._generate_plotter()

        self._ctr: int = 0

        self._isometric: bool = False
        self._bwdrawing: bool = False

        self.highlight_actor = None
        self.highlight_text_actor = None
        self._cycle_pos: int = 0
        self._obj_cycler: list[str] = []
        self._selectable_objects: dict[str:dict] = dict()

        self._bounds: tuple[float, float, float, float, float, float] | None = None
        self._cbar_args: dict = {}
        self._cbar_lim: tuple[float, float] | None = None
        self.camera_position = (1, -1, 1)  # +X, +Z, -Y

        self._plot.track_click_position(
            callback=self._on_click, side="right", viewport=True
        )

        self.__post_init__(*args, **kwargs)

    def __post_init__(self, *args, **kwargs):
        pass

    def _get_edge_length(self) -> float:
        return 1.0

    @staticmethod
    def _def_if_none(value, default):
        if value is None:
            return default
        return value

    def parse_opacity(
        self, value: float | str | None, default: float | str, minimize: bool = False
    ) -> float:
        """Picks the provided value or parses the default. If minimize is true it will pick the lowest of the value and the default opacity.

        Args:
            value (float | str): The opacity as float, string or even None
            default (float | str): The default value
            minimize (bool, optional): If the output should be the minimum of both. Defaults to False.

        Returns:
            float: _description_
        """
        default = self.set.theme.parse_opacity(default)
        if value is None:
            return default
        if minimize:
            return min(self.set.theme.parse_opacity(value), default)
        else:
            return self.set.theme.parse_opacity(value)

    @staticmethod
    def _append_with_defaults(values: dict, *defaults: dict) -> dict:
        """Append with default. Overwrites detault dict entries with values"""
        out = dict()
        for default in defaults:
            out.update(default)
        out.update(values)
        return out

    ############################################################
    #                        GENERIC METHODS                   #
    ############################################################

    def cbar(
        self,
        name: str,
        n_labels: int = 5,
        interactive: bool = False,
        clim: tuple[float, float] | None = None,
    ) -> EMergeDisplay:
        """Configure the colorbar settings for the next plot call to be made.

        Args:
            name (str): The name of the field quantity (shared between multiple plots of the same name)
            n_labels (int, optional): The number of color-bar value labels. Defaults to 5.
            interactive (bool, optional): If the colorbar should be set to interactive mode. Defaults to False.
            clim (tuple[float, float] | None, optional): The color-limits (manual overwrite). Defaults to None.

        Returns:
            EMergeDisplay: This same object instance
        """
        self._cbar_args = dict(
            title=name,
            n_labels=n_labels,
            interactive=interactive,
            title_font_size=26,
            label_font_size=25,
            unconstrained_font_size=True,
        )
        self._cbar_lim = clim
        return self

    def _cbar_defaults(self, **kwargs):
        """overwrite Defaults kwargs for _cbar_args."""
        defaults = dict(
            title_font_size=26,
            label_font_size=24,
            color=self.set.theme.text_color,
            unconstrained_font_size=True,
        )
        defaults.update(kwargs)

        self._cbar_args = self._append_with_defaults(self._cbar_args, defaults)

    def _wrap_plot(self, *args, **kwargs) -> pv.Actor:
        """Performs plot operations to handle Pyvistas behavior better"""

        # Scalar bars are handled separately in order to make font size changes work
        if "scalar_bar_args" in kwargs and kwargs.get("show_scalar_bar", True):
            sbarargs = kwargs.pop("scalar_bar_args")
        else:
            sbarargs = None

        # Make the plot call without scalar bar
        kwargs["show_scalar_bar"] = False
        actor = self._plot.add_mesh(*args, **kwargs)

        # Add the scalar bar separately.
        if sbarargs is not None:
            self._plot.add_scalar_bar(**sbarargs)
        self._data_sets.append(actor.mapper.dataset)
        return actor

    def _reset_cbar(self) -> None:
        self._cbar_args: dict = {}
        self._cbar_lim: tuple[float, float] | None = None

    def _wire_close_events(self):
        self._closed = False

        def mark_closed(*_):
            self._closed = True
            self._stop = True

        self._plot.add_key_event("q", lambda: mark_closed())

    @property
    def _colorize(self) -> bool:
        return not self._bwdrawing

    @property
    def _camera_distance(self) -> float:
        x, y, z = self._plot.camera.position
        d = (x**2 + y**2 + z**2) ** (0.5)
        return d

    def _update_camera(self):
        d = self._camera_distance
        px, py, pz = self.camera_position
        dp = (px**2 + py**2 + pz**2) ** (0.5)
        px, py, pz = px / dp, py / dp, pz / dp
        self._plot.camera.position = (d * px, d * py, d * pz)

    def _apply_lighting(self) -> None:
        # Applies default lighting
        lights = []

        lights.append(pv.Light(position=(-1, 1, 1), color="white", intensity=0.3))
        lights.append(pv.Light(position=(1, -1, -1), color="white", intensity=0.3))
        for light in lights:
            self._plot.add_light(light)

    def _generate_plotter(self) -> None:
        self._plot = pv.Plotter()

        self._plot.add_key_event("m", self.activate_ruler)  # type: ignore
        self._plot.add_key_event("g", self.activate_object)  # type: ignore
        self._plot.add_key_event("x", self.view_x)  # type: ignore
        self._plot.add_key_event("y", self.view_y)  # type: ignore
        self._plot.add_key_event("z", self.view_z)  # type: ignore
        self._plot.add_key_event("c", self.toggle_isometric)  # type: ignore
        self._plot.add_key_event("i", self.view_iso)
        self._plot.add_key_event("Right", self._on_next_obj)
        self._plot.add_key_event("Left", self._on_prev_obj)

    def _on_click(self, click_pos):
        x, y = click_pos

        # Get the underlying VTK renderer
        renderer = self._plot.renderer

        # Convert the 2D screen click into a 3D point on the near clipping plane
        renderer.SetDisplayPoint(x, y, 0.0)
        renderer.DisplayToWorld()
        ray_start = np.array(renderer.GetWorldPoint()[:3])

        # Convert the 2D screen click into a 3D point on the far clipping plane
        renderer.SetDisplayPoint(x, y, 1.0)
        renderer.DisplayToWorld()
        ray_end = np.array(renderer.GetWorldPoint()[:3])

        hits = []
        for name, info in self._selectable_objects.items():
            mesh = info["mesh"]
            actor = info["actor"]
            if not isinstance(mesh, pv.PolyData):
                surface = mesh.extract_surface(algorithm="dataset_surface")
            else:
                surface = mesh

            points, cells = surface.ray_trace(ray_start, ray_end)
            if len(points) > 0:
                point = points[0, :]
                distance = np.linalg.norm(point - ray_start)
                hits.append((distance, name))

        hits.sort(key=lambda x: x[0])

        self._cycle_pos = 0
        self._obj_cycler = []
        if hits:
            for dist, name in hits:
                print(f" -> {name} (distance: {dist:.2f})")
                self._obj_cycler.append(name)

        self._highlight_object()

    def _on_prev_obj(self):
        self._cycle_pos += 1
        self._highlight_object()

    def _on_next_obj(self):
        self._cycle_pos -= 1
        self._highlight_object()

    def _clear_highlight(self) -> None:
        "Clears the highlightable objects and selection text."
        if self.highlight_actor is not None:
            self._plot.remove_actor(self.highlight_actor)
            self.highlight_actor = None

        self._clear_highlight_text()

    def _highlight_object(self) -> None:
        """Removes the old highlight and draws a new glowing edge outline around the selected mesh."""

        if len(self._obj_cycler) == 0:
            return

        name = self._obj_cycler[self._cycle_pos % len(self._obj_cycler)]
        mesh_data = self._selectable_objects[name]["mesh"]

        self._clear_highlight()

        if mesh_data is not None:
            # 2. Extract edges to create a wireframe outline outline
            # For UnstructuredGrids, extract_surface ensures extract_edges works perfectly
            surface = (
                mesh_data.extract_surface(algorithm="dataset_surface")
                if not isinstance(mesh_data, pv.PolyData)
                else mesh_data
            )

            self.highlight_actor = self._plot.add_mesh(
                surface,
                style="surface",
                color=self.set.theme.parse_color_name("EMERGE-SELECT"),
                line_width=5,  # Makes lines look thicker and cleaner
                opacity=self.parse_opacity(
                    "EMERGE-SELECT", self.set.theme.default_opacity
                ),
            )
            self._set_highlight_text(name)

        # 4. Force the plotter to re-render the scene immediately
        self._plot.render()

    ############################################################
    #                      KEY PRESS EVENTS                    #
    ############################################################

    def _set_axis_view(self, axis, sign=+1):
        pl = self._plot
        cam = pl.camera

        fp = np.array(cam.focal_point)
        d = float(self._camera_distance) * sign

        if axis == "x":
            cam.position = (fp[0] + d, fp[1], fp[2])
            cam.up = (0, 0, 1)
        elif axis == "y":
            cam.position = (fp[0], fp[1] + d, fp[2])
            cam.up = (0, 0, 1)
        elif axis == "z":
            cam.position = (fp[0], fp[1], fp[2] + d)
            cam.up = (0, 1, 0)
        else:
            raise ValueError("axis must be 'x', 'y', or 'z'")

        cam.focal_point = tuple(fp)

        pl.reset_camera_clipping_range()
        pl.render()

    def view_x(self):
        self._set_axis_view("x", +1)

    def view_y(self):
        self._set_axis_view("y", +1)

    def view_z(self):
        self._set_axis_view("z", +1)

    def view_iso(self):
        pl = self._plot
        cam = pl.camera

        fp = np.array(cam.focal_point)  # or: np.array(pl.center)
        d = float(self._camera_distance)

        # Typical "technical drawing" 3D view: from +X,+Y,+Z
        v = np.array([1.0, 1.0, 1.0])
        v /= np.linalg.norm(v)

        cam.position = tuple(fp + d * v)
        cam.focal_point = tuple(fp)

        # Keep +Z vertical on screen (common convention)
        cam.up = (0, 0, 1)

        # If you want no vanishing points (orthographic)
        cam.parallel_projection = True  # or: pl.enable_parallel_projection()

        pl.reset_camera_clipping_range()
        pl.render()

    def toggle_isometric(self):
        if self._isometric:
            self._isometric = False
            self._plot.disable_parallel_projection()
        else:
            self._isometric = True
            self._plot.enable_parallel_projection()
        self._plot.render()

    def activate_ruler(self):
        self._plot.disable_picking()
        self._selector.turn_off()
        self._ruler.toggle()

    def activate_object(self):
        self._plot.disable_picking()
        self._ruler.turn_off()
        self._selector.toggle()

    def set_theme(self, theme: EMergeTheme) -> None:
        """Sets the display theme.

        Args:
            theme (EMergeTheme): The theme to set.
        """
        self.set.theme = theme

    def show(self, screenshot: str | None = None, off_screen: bool = False):
        """Shows the Pyvista display."""

        self._plot.off_screen = off_screen
        pv.OFF_SCREEN = off_screen

        self._update_camera()
        self._add_aux_items()
        self._apply_theme()

        if self._do_animate and screenshot is None:
            self._wire_close_events()
            self.add_text("Press Q to close!", color="red", position="upper_left")
            self._plot.show(
                auto_close=False,
                interactive_update=True,
                before_close_callback=self._close_callback,
            )
            self._animate()
        else:
            if screenshot is not None:
                self._plot.show(screenshot=screenshot, auto_close=True)
            else:
                self._plot.show()

        self._reset()

    def _parse_cmap_name(self, cmap: str, default: str | None = None) -> str:
        """Universal pipeline for cmap parsing

        Args:
            cmap (str): _description_

        Returns:
            str: _description_
        """
        if default is None:
            default = self.set.theme.default_amplitude_cmap
        if cmap is None:
            cmap = default
        elif isinstance(cmap, str):
            cmap = self.set.theme.parse_cmap_name(cmap)
        return cmap

    def _parse_field_data(self, 
                          V: np.ndarray, 
                          value_scale: Literal['lin','log','symlog'], 
                          symmetrize: bool, 
                          clim: tuple[float, float] | None = None,
                          clim_crop_factor: float = 1.0) -> tuple[tuple[float, float], str, Callable]:
        """Does common processing operations amongst plot functions
        including:
         - Computing color limits
         - Defining the default colormap
         - Defining the quantity transformation T: R -> R

        Args:
            V (np.ndarray): _description_
            symmetrize (bool): _description_

        Returns:
            tuple[np.ndarray, str]: _description_
        """

        # Sanitize and flatten
        Vf = np.nan_to_num(V.flatten())

        # Extract min and max
        vmin, vmax = nanminmax(Vf.real)
        vmin = vmin * clim_crop_factor
        vmax = vmax * clim_crop_factor

        default_cmap = self.set.theme.default_amplitude_cmap

        if value_scale == "log":
            T = lambda x: np.log10(np.abs(x + 1e-12))
        elif value_scale == "symlog":
            T = lambda x: np.sign(x) * np.log10(1 + np.abs(x * np.log(10)))
        else:
            T = lambda x: x

        if symmetrize:
            level = np.max(np.abs(Vf))
            vmin, vmax = (-level, level)
            default_cmap = self.set.theme.default_wave_cmap

        if clim is None:
            if self._cbar_lim is not None:
                clim = self._cbar_lim
                vmin, vmax = clim
            else:
                clim = (vmin, vmax)

        return clim, default_cmap, T

    def _get_path(self, filename: str) -> str:
        """Generates a filename for the EMerge package directory in the PyVista folder

        Args:
            filename (str): _description_

        Returns:
            str: _description_
        """
        return str(Path(files("emsutil")) / "pyvista" / "textures" / filename)

    def _get_texture(self, filename: str) -> pv.Texture | None:
        """Returns a PyVista Texture object for a filename in the EMerge directlry

        Args:
            filename (str): The filename without path

        Returns:
            pv.Texture | None: _description_
        """
        try:
            tex = pv.read_texture(self._get_path(filename))
            return tex
        except FileNotFoundError:
            logger.error(f"File {filename} not found. ignoring image")
        return None

    def _apply_theme(self):
        picture = self._get_texture("background.png")
        picture.interpolate = True
        picture.mipmap = True

        if picture is not None:
            self._plot.set_environment_texture(picture)

        if not self.set.theme.render_shadows:
            self._plot.disable_shadows()
            # Turn off directional lighting
            self._plot.remove_all_lights()
        else:
            self._apply_lighting()

        if self.set.theme.draw_pvgrid and not self._bwdrawing:
            pv.set_plot_theme("dark")
            bounds = self._bounds
            extra_factor = 0.1
            dx = (bounds[1] - bounds[0]) * extra_factor
            dy = (bounds[3] - bounds[2]) * extra_factor
            dz = (bounds[5] - bounds[4]) * extra_factor
            ds = max(dx, dy, dz)
            bounds = (
                bounds[0] - ds,
                bounds[1] + ds,
                bounds[2] - ds,
                bounds[3] + ds,
                bounds[4] - ds,
                bounds[5] + ds,
            )
            pv.global_theme.font.fmt = "%.3f"
            actor = self._plot.show_grid(
                bounds=bounds, color=self.set.theme.text_color, fmt="%.3f"
            )

        pv.global_theme.font.color = self.set.theme.text_color
        pv.global_theme.font.size = self.set.theme.text_size
        pv.global_theme.colorbar_horizontal.width = 0.4
        pv.global_theme.colorbar_vertical.height = 0.15

        if self.set.theme.aa_active:
            self._plot.enable_anti_aliasing(
                self.set.theme.aa_mode, multi_samples=self.set.theme.aa_samples
            )
        else:
            self._plot.disable_anti_aliasing()
        self._plot.title = "EMerge"

        if self._bwdrawing:
            self._plot.set_background("white", top="white")  # type: ignore
        else:
            self._plot.set_background(
                self.set.theme.backgroung_grad_1, top=self.set.theme.backgroung_grad_2
            )  # type: ignore

    def _reset(self):
        self._ctr = 0
        self._plot.close()
        self._generate_plotter()
        self._clear_highlight()
        self._stop = False
        self._objs = []
        self._animate_next = False
        self._data_sets = []
        self._bwdrawing = False
        self._reset_cbar()
        self.set.theme.line_cycler.reset()
        self._plot.off_screen = False
        self._cycle_pos: int = 0
        self._obj_cycler: list[str] = []
        self._selectable_objects: dict[str:dict] = dict()
        pv.OFF_SCREEN = False

    def _close_callback(self, arg):
        """The private callback function that stops the animation."""
        self._stop = True
        self._reset()

    def _animate(self) -> None:
        """Private function that starts the animation loop."""
        self._stop = False

        # guard values
        steps = max(1, int(self._Nsteps))
        fps = max(1, int(self._fps))
        dt = 1.0 / fps
        next_tick = time.perf_counter()
        step = 0

        while (
            not self._stop
            and not self._closed_via_x
            and self._plot.render_window is not None
        ):
            # process window/UI events so close button works
            self._plot.update()

            now = time.perf_counter()
            if now >= next_tick:
                step = (step + 1) % steps
                phi = np.exp(1j * (step / steps) * 2 * np.pi)

                # update all animated objects
                for aobj in self._objs:
                    aobj.update(phi)

                # draw one frame
                self._plot.render()

                # schedule next frame; catch up if we fell behind
                next_tick += dt
                if now > next_tick + dt:
                    next_tick = now + dt

            # be kind to the CPU
            time.sleep(0.001)
        # ensure cleanup pathway runs once
        self._close_callback(None)

    def _get_fieldname(self) -> str:
        """
        Generates a unique field name for color bar separation."""
        name = f"Field{self._ctr}"
        self._ctr += 1
        return name

    def animate(self, Nsteps: int = 35, fps: int = 25) -> EMergeDisplay:
        """Turns on the animation mode with the specified number of steps and FPS.

        All subsequent plot calls will automatically be animated. This method can be
        method chained.

        Args:
            Nsteps (int, optional): The number of frames in the loop. Defaults to 35.
            fps (int, optional): The number of frames per seocond, Defaults to 25

        Returns:
            PVDisplay: The same PVDisplay object

        Example:
        >>> display.animate().surf(...)
        >>> display.show()
        """
        print(
            "If you closed the animation without using (Q) press Ctrl+C to kill the process."
        )
        self._Nsteps = Nsteps
        self._fps = fps
        self._animate_next = True
        self._do_animate = True
        return self

    def drawing_bw(self) -> EMergeDisplay:
        """Sets the drawing mode to black and white (no colors).

        Args:
            state (bool, optional): Whether to draw in black and white. Defaults to True.
        Returns:

            PVDisplay: The same PVDisplay object
        """
        self._bwdrawing = True
        return self

    def _mesh_manual(self, nodes: np.ndarray, tris: np.ndarray) -> pv.UnstructuredGrid:
        ntris = tris.shape[1]
        cells = np.zeros((ntris, 4), dtype=np.int64)
        cells[:, 1:] = tris.T
        cells[:, 0] = 3
        celltypes = np.full(ntris, fill_value=pv.CellType.TRIANGLE, dtype=np.uint8)
        points = nodes.T
        points[:, 2] += self.set.z_boost
        return pv.UnstructuredGrid(cells, celltypes, points)

    def _add_selectable(self, mesh: pv.UnstructuredGrid, actor: pv.Actor, name: str):
        """Add a mesh and actor as selectable item."""
        self._selectable_objects[name] = dict(mesh=mesh, actor=actor)

    def _clear_highlight_text(self) -> None:
        if self.highlight_text_actor is not None:
            self._plot.remove_actor(self.highlight_text_actor)
            self.highlight_text_actor = None

    def _set_highlight_text(self, text: str) -> None:
        self._clear_highlight_text()
        self.highlight_text_actor = self.add_text(text, abs_position=(0.5,0.85,0), center=True)

    def _add_obj(
        self,
        mesh_obj: pv.UnstructuredGrid,
        obj_dim: int,
        *args,
        plot_mesh: bool = False,
        volume_mesh: bool = True,
        style: str = "surface",
        metal: bool = False,
        metallic: float = None,
        roughness: float = 0.0,
        color: str = None,
        line_width: float = None,
        opacity: float = 1.0,
        show_edges: bool = None,
        texture: str | None = None,
        allow_pbr: bool = True,
        smooth_shading: bool = False,
        **kwargs,
    ) -> pv.Actor:

        style = self.set.theme.render_style
        color = self.set.theme.parse_color(color)
        opacity = self.set.theme.parse_opacity(opacity)

        # Default rendering settings
        specular = self.set.theme.render_specular
        diffuse = self.set.theme.render_diffuse
        ambient = self.set.theme.render_ambient
        edge_color = self.set.theme.geo_mesh_color

        # If no metallic render style is explicitly specified, pick the theme choice
        if metallic is None:
            metallic = self.set.theme.render_metal_roughness

        # Same for line width
        if line_width is None:
            line_width = self.set.theme.geo_mesh_width

        # Same for edge color
        if color is None:
            color = self.set.theme.geo_edge_color

        # Same for show edges
        if show_edges is None:
            show_edges = self.set.theme.render_mesh

        # If Physics based rendering is allowed
        if metal and self.set.theme.render_pbr:
            pbr = allow_pbr
            metallic = self.set.theme.render_metallic
            roughness = self.set.theme.render_metal_roughness
        else:
            pbr = False

        # Default keyword arguments when plotting Mesh mode.
        if plot_mesh is True:
            show_edges = True
            opacity = 0.4
            line_width = self.set.theme.geo_mesh_width
            style = "wireframe"
            color = next(self.set.theme.line_cycler)

        # Don't know why I made this but in case, you can specify a minimum
        # rendering opacity
        opacity = max(self.set.theme.render_min_opacity, opacity)

        # Defining the default keyword arguments for PyVista
        kwargs = self._append_with_defaults(
            kwargs,
            dict(
                color=color,
                opacity=opacity,
                metallic=metallic,
                pbr=pbr,
                roughness=roughness,
                line_width=line_width,
                edge_color=edge_color,
                show_edges=show_edges,
                pickable=False,
                smooth_shading=smooth_shading,
                split_sharp_edges=True,
                specular=specular,
                ambient=ambient,
                diffuse=diffuse,
                style=style,
            )
        )

        # Treat as black and white
        if not self._colorize:
            kwargs["pbr"] = False
            kwargs["roughness"] = 0.0
            kwargs["metallic"] = 0.0
            kwargs["opacity"] = 0.0
            kwargs["color"] = (1, 1, 1)
            kwargs["silhouette"] = dict(color="black", line_width=3.0)

        # Add a texture if it is specified
        if texture is not None and texture != "None":
            tex_image = self._get_texture(texture)
            if tex_image is not None:
                kwargs["texture"] = tex_image
                output = mesh_obj.point_data
                origin = output.dataset.center
                points = output.dataset.points.T
                tris = output.dataset.cells_dict[5].T
                origin, u, v = determine_projection_data(points, tris)
                mesh_obj.texture_map_to_plane(
                    origin=origin, point_u=origin + u, point_v=origin + v, inplace=True
                )

        # Replace the mesh object with an edge mesh object.
        if plot_mesh is True and volume_mesh is True:
            mesh_obj = mesh_obj.extract_all_edges()

        # If Physics based rendering is active and edges are desired
        # make a separate plot call for the edges.
        if kwargs["pbr"] and kwargs["show_edges"]:
            kwargs2 = kwargs.copy()
            kwargs2["style"] = "wireframe"
            kwargs2["pbr"] = False
            kwargs2["show_edges"] = False
            kwargs2["color"] = edge_color
            kwargs2["edge_color"] = edge_color
            kwargs2["line_width"] = 1
            kwargs2["lighting"] = True
            kwargs2["ambient"] = 0.6
            kwargs2["opacity"] = opacity
            kwargs2["render_lines_as_tubes"] = False

            kwargs["show_edges"] = False

            actor = self._wrap_plot(mesh_obj, *args, **kwargs2)

        # Finally plot the mesh object.
        actor = self._wrap_plot(mesh_obj, *args, **kwargs)

        # Push 3D Geometries back to avoid Z-fighting with 2D geometries.
        if obj_dim == 3:
            mapper = actor.GetMapper()
            mapper.SetResolveCoincidentTopology(1)
            mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(1, 0.5)

        return actor

    ############################################################
    #                        EMERGE METHODS                    #
    ############################################################

    def save_vtk(self, base_path: str) -> None:
        """Saves all the plot object into a directory with the given path to a series of .vtk files.

        Args:
            base_path (str): The base path without extensions.
        """
        if len(self._data_sets) == 0:
            logger.error(
                'No VTK objects to save. Make sure to call this method "before" calling .show().'
            )
        base = Path(base_path)
        if base.suffix.lower() == ".vtk":
            base = base.with_suffix("")

        # ensure directory exists
        base.mkdir(parents=True, exist_ok=True)

        logger.info(f"Saving VTK files to {base}")
        # save numbered files
        for idx, vtkobj in enumerate(self._data_sets, start=1):
            filename = base / f"{idx}.vtk"
            vtkobj.save(str(filename))
            logger.debug(f"Saved VTK object to {filename}.")
        logger.info("VTK saving complete!")

    def add_scatter(self, xs: np.ndarray, ys: np.ndarray, zs: np.ndarray):
        """Adds a scatter point cloud

        Args:
            xs (np.ndarray): The X-coordinate
            ys (np.ndarray): The Y-coordinate
            zs (np.ndarray): The Z-coordinate
        """
        cloud = pv.PolyData(np.array([xs, ys, zs]).T)
        self._data_sets.append(cloud)
        self._plot.add_points(cloud)

    def add_field(
        self,
        field: FieldPlotData,
        scale: Literal["lin", "log", "symlog"] = "lin",
        cmap: cmap_names | None = None,
        clim: tuple[float, float] | None = None,
        opacity: float = None,
        voltype: Literal["cloud", "contour", "clip"] = "cloud",
        clim_crop_factor: float = 1.0,
        symmetrize: bool = False,
        _fieldname: str | None = None,
        smooth_shading: bool = False,
        **kwargs,
    ) -> pv.DataSet:
        """A generic method to add a field plot to the display. Depending on the field type, it will call the appropriate method.

        Example:
        >>> display.add_field(myfield.cutplane(...).scalar('Ex','real'),...)
        >>> display.add_field(myfield.grid(...).vector('E'),...)

        Args:
            field (FieldPlotData): The field to plot
            scale (Literal["lin","log","symlog"], optional): . Defaults to 'lin'.
            cmap (cmap_names | None, optional): The colormap. Defaults to None.
            clim (tuple[float, float] | None, optional): The color limit scale (min, max). Defaults to None.
            opacity (float, optional): The plot opacity. Defaults to 1.0.
            clipplane (bool, optional): If a 3D grid plot should be done including a clip plane. Defaults to false.
            clim_crop_factor (float, optional): A multiplier for the default clim limits. If this value is 0.5, the clim limits will be divided by half to zoom in on the color range.
            symmetrize (bool, optional): If the colorscale should be symmetrized. Defaults to False.
            _fieldname (str | None, optional): A name for the field. Defaults to None.

        Returns:
            pv.DataSet: _description_
        """

        if "title" not in self._cbar_args:
            self._cbar_args["title"] = field.name

        if self._do_animate:
            smooth_shading = False

        if field.structure == DataStructure.TRISURF:
            self.add_trisurf(
                field.x,
                field.y,
                field.z,
                field.F,
                field.tris,
                scale=scale,
                cmap=cmap,
                clim=clim,
                opacity=opacity,
                symmetrize=symmetrize,
                clim_crop_factor=clim_crop_factor,
                _fieldname=_fieldname,
                smooth_shading=smooth_shading,
                **kwargs,
            )
            return
        if field._is_quiver:
            self.add_quiver(
                field.x,
                field.y,
                field.z,
                field.vx,
                field.vy,
                field.vz,
                scalemode=scale,
                **kwargs,
            )
            return
        if field.structure == DataStructure.GRID2D:
            self.add_surf(
                field.x,
                field.y,
                field.z,
                field.F,
                scale=scale,
                cmap=cmap,
                clim=clim,
                opacity=opacity,
                symmetrize=symmetrize,
                clim_crop_factor=clim_crop_factor,
                _fieldname=_fieldname,
                smooth_shading=smooth_shading,
                **kwargs,
            )
            return
        if field.structure == DataStructure.GRID3D:
            if voltype == "clip":
                self.add_clip_volume(
                    field.x,
                    field.y,
                    field.z,
                    field.F,
                    scale=scale,
                    cmap=cmap,
                    opacity=opacity,
                    symmetrize=symmetrize,
                    clim_crop_factor=clim_crop_factor,
                    clim=clim,
                    _fieldname=_fieldname,
                    **kwargs,
                )
            elif voltype == "contour":
                self.add_contour(
                    field.x,
                    field.y,
                    field.z,
                    field.F,
                    scale=scale,
                    cmap=cmap,
                    opacity=opacity,
                    symmetrize=symmetrize,
                    clim_crop_factor=clim_crop_factor,
                    clim=clim,
                    _fieldname=_fieldname,
                    **kwargs,
                )
            elif voltype == "cloud":
                self.add_cloud(
                    field.x,
                    field.y,
                    field.z,
                    field.F,
                    scale=scale,
                    cmap=cmap,
                    opacity=opacity,
                    symmetrize=symmetrize,
                    clim_crop_factor=clim_crop_factor,
                    clim=clim,
                    _fieldname=_fieldname,
                    **kwargs,
                )
            return
        raise Exception(
            f"I have no clue how to plot dataset {field} with structure {field.structure}"
        )

    def add_surf(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        field: np.ndarray,
        scale: Literal["lin", "log", "symlog"] = "lin",
        cmap: cmap_names | None = None,
        clim: tuple[float, float] | None = None,
        opacity: float | None = None,
        symmetrize: bool = False,
        clim_crop_factor: float = 1.0,
        _fieldname: str | None = None,
        **kwargs,
    ) -> pv.DataSet:
        """Add a surface plot to the display
        The X,Y,Z coordinates must be a 2D grid of data points. The field must be a real field with the same size.

        Args:
            x (np.ndarray): The X-grid array
            y (np.ndarray): The Y-grid array
            z (np.ndarray): The Z-grid array
            field (np.ndarray): The scalar field to display
            scale (Literal["lin","log","symlog"], optional): The colormap scaling¹. Defaults to 'lin'.
            cmap (cmap_names, optional): The colormap. Defaults to 'coolwarm'.
            clim (tuple[float, float], optional): Specific color limits (min, max). Defaults to None.
            opacity (float, optional): The opacity of the surface. Defaults to 1.0.
            symmetrize (bool, optional): Wether to force a symmetrical color limit (-A,A). Defaults to True.

        (¹): lin: f(x)=x, log: f(x)=log₁₀(|x|), symlog: f(x)=sgn(x)·log₁₀(1+|x·ln(10)|)
        """

        clim, default_cmap, T = self._parse_field_data(field, scale, symmetrize, clim, clim_crop_factor)

        # Extract the fieldname
        name = self._get_fieldname() if _fieldname is None else _fieldname

        # Create the structured grid objects
        grid = pv.StructuredGrid(x, y, z)
        field_flat = field.flatten(order="F")

        # Generate and transform the dataset
        static_field = T(np.real(field_flat))

        # Set the scalar field as grid and apply a NaN removal
        # Nans are used to remove plots outside the simulation domain.
        grid[name] = static_field
        grid_no_nan = grid.threshold(scalars=name, all_scalars=True)

        cmap = self._parse_cmap_name(cmap, default=default_cmap)

        # Set default plot argument settings
        kwargs = self._append_with_defaults(
            kwargs,
            self.set.theme.surf_kwargs,
            dict(
                cmap=cmap,
                clim=clim,
                opacity=self.parse_opacity(opacity, "EMERGE-SURF"),
                pickable=False,
                multi_colors=True,
            )
        )

        # Overwrite the color bar Title if no title exists
        self._cbar_defaults(title=name)

        # Generate the plot
        actor = self._wrap_plot(
            grid_no_nan, scalars=name, scalar_bar_args=self._cbar_args, **kwargs
        )

        # Animation settings
        if self._animate_next:

            def on_update(obj: _AnimObject, phi: complex):
                field_anim = obj.T(np.real(obj.field * phi))
                obj.grid[name] = field_anim
                obj.fgrid[name] = obj.grid.threshold(scalars=name, all_scalars=True)[
                    name
                ]

            self._objs.append(
                _AnimObject(field_flat, T, grid, grid_no_nan, actor, on_update)
            )
            self._animate_next = False
        self._reset_cbar()
        return grid_no_nan

    def add_trisurf(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        field: np.ndarray,
        tris: np.ndarray,
        scale: Literal["lin", "log", "symlog"] = "lin",
        cmap: cmap_names | None = None,
        clim: tuple[float, float] | None = None,
        opacity: float = 1.0,
        symmetrize: bool = False,
        clim_crop_factor: float = 1.0,
        _fieldname: str | None = None,
        **kwargs,
    ):
        """Adds a triangular surface plot to the display

        The X,Y,Z coordinates must be a 2D grid of data points. The field must be a real field with the same size.

        Example:
        >>> display.add_boundary_field(xs, ys, zs, field, tris, ...)

        Args:
            x (np.ndarray): The X-grid array
            y (np.ndarray): The Y-grid array
            z (np.ndarray): The Z-grid array
            field (np.ndarray): The scalar field to display
            tris (np.ndarray): The triangle indices array
            scale (Literal["lin","log","symlog"], optional): The colormap scaling
            cmap (cmap_names, optional): The colormap. Defaults to 'coolwarm'.
            clim (tuple[float, float], optional): Specific color limits (min, max).
            opacity (float, optional): The opacity of the surface. Defaults to 1.0.
            symmetrize (bool, optional): Wether to force a symmetrical color limit (-A,A). Defaults to True.


        (¹): lin: f(x)=x, log: f(x)=log₁₀(|x|), symlog: f(x)=sgn(x)·log₁₀(1+|x·ln(10)|)
        """

        clim, default_cmap, T = self._parse_field_data(field, scale, symmetrize, clim, clim_crop_factor)
        name = self._get_fieldname() if _fieldname is None else _fieldname

        grid = self._mesh_manual(np.array([x, y, z]), tris)
        field_flat = field.flatten(order="F")
        static_field = T(np.real(field_flat))
        grid[name] = static_field

        cmap = self._parse_cmap_name(cmap, default_cmap)

        kwargs = self._append_with_defaults(
            kwargs,
            self.set.theme.surf_kwargs,
            dict(
                cmap=cmap,
                clim=clim,
                opacity=opacity,
                pickable=False,
                multi_colors=True,
            )
        )

        self._cbar_defaults(title=name)
        actor = self._wrap_plot(
            grid,
            scalars=name,
            scalar_bar_args=self._cbar_args,
            backface_culling=False,
            **kwargs,
        )

        if self._animate_next:

            def on_update(obj: _AnimObject, phi: complex):
                field_anim = obj.T(np.real(obj.field * phi))
                obj.grid[name] = field_anim
                # obj.fgrid replace with thresholded scalar data.

            self._objs.append(_AnimObject(field_flat, T, grid, grid, actor, on_update))
            self._animate_next = False
        self._reset_cbar()

    def add_title(self, title: str, color: str = "EMERGE-TEXT") -> None:
        """Adds a title to the plot

        Args:
            title (str): The title name
        """
        self._plot.add_text(
            title,
            position="upper_edge",
            font_size=18,
            color=self.set.theme.parse_color(color),
        )

    def add_text(
        self,
        text: str,
        color: str = "EMERGE-TEXT",
        position: Literal[
            "lower_left",
            "lower_right",
            "upper_left",
            "upper_right",
            "lower_edge",
            "upper_edge",
            "right_edge",
            "left_edge",
        ] = "upper_right",
        center: bool = False,
        abs_position: tuple[float, float, float] | None = None,
    ):
        """Adds text to the plot at a given position

        position options:
            'lower_left', 'lower_right', 'upper_left', 'upper_right',
            'lower_edge', 'upper_edge', 'right_edge', 'left_edge'

        Args:
            text (str): The text to place
            color (str, optional): The color of the text. Defaults to 'black'.
            position (str, optional): The position of the text. Defaults to 'upper_right'.
            abs_position (tuple[float, float, float] | None, optional): The absolute position. Defaults to None.
        """
        viewport = False
        if abs_position is not None:
            final_position = abs_position
            viewport = True
        else:
            final_position = position
        kwargs = self.set.theme.text_kwarg
        actor = self._plot.add_text(
            text,
            position=final_position,
            color=self.set.theme.parse_color_name(color),
            font_size=18,
            viewport=viewport,
            **kwargs,
        )
        if center:
            prop = actor.GetTextProperty()
            prop.SetJustificationToCentered()
            prop.SetVerticalJustificationToCentered()
        return actor

    def add_quiver(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        dx: np.ndarray,
        dy: np.ndarray,
        dz: np.ndarray,
        scale: float = 1,
        color: tuple[float, float, float] | None = None,
        cmap: cmap_names | None = None,
        scalemode: Literal["lin", "log"] = "lin",
        _fieldname: str = "",
    ):
        x = x.flatten()
        y = y.flatten()
        z = z.flatten()
        # Keep the complex components alive for animation; only take .real
        # once we've decided which frame's instantaneous value we want.
        dx_c = dx.flatten()
        dy_c = dy.flatten()
        dz_c = dz.flatten()

        ids = np.invert(np.isnan(dx_c.real))
        
        x, y, z = x[ids], y[ids], z[ids]
        dx_c, dy_c, dz_c = dx_c[ids], dy_c[ids], dz_c[ids]

        dmin = _min_distance(x, y, z)

        def build_vectors(dxr, dyr, dzr):
            """Turns instantaneous real component arrays into scaled arrow vectors."""
            dxr, dyr, dzr = dxr.copy(), dyr.copy(), dzr.copy()
            if scalemode == "log":
                dxr, dyr, dzr = _logscale(dxr, dyr, dzr)
            dmax = np.max(_norm(dxr, dyr, dzr))
            dmax = dmax if dmax != 0 else 1e-30
            return scale * np.array([dxr, dyr, dzr]) / dmax * dmin * 2

        Vec = build_vectors(dx_c.real, dy_c.real, dz_c.real)

        kwargs = dict()

        # Turn Scalar bars off if a uniform color was supplied. Unique to Add Quiver.
        if color is not None:
            kwargs["color"] = self.set.theme.parse_color_name(color)
            kwargs["show_scalar_bar"] = False

        cmap = self._parse_cmap_name(cmap)

        self._cbar_defaults(title=_fieldname)

        arrow_obj = pv.Arrow(**self.set.theme.quiver_kwargs)
        grid = pv.StructuredGrid(x, y, z)
        grid.point_data["vectors"] = np.column_stack(Vec)
        grid.set_active_vectors("vectors")
        arrows = grid.glyph(orient="vectors", scale="vectors", geom=arrow_obj, factor=0.5)

        actor = self._wrap_plot(
            arrows,
            clim=None,
            cmap=cmap,
            scalar_bar_args=self._cbar_args,
            **kwargs,
        )

        self._data_sets.append(actor.mapper.dataset)
        self._reset_cbar()

        if self._animate_next:

            def on_update(obj: _AnimObject, phi: complex):
                dxr = (dx_c * phi).real
                dyr = (dy_c * phi).real
                dzr = (dz_c * phi).real
                Vec_t = build_vectors(dxr, dyr, dzr)
                obj.grid.point_data["vectors"] = np.column_stack(Vec_t)
                obj.grid.set_active_vectors("vectors")
                new_arrows = obj.grid.glyph(
                    orient="vectors", scale="vectors", geom=arrow_obj, factor=0.5
                )
                obj.actor.GetMapper().SetInputData(new_arrows)
                obj.actor.GetMapper().Modified()

            # field slot is unused here (T slot too) — kept only to match _AnimObject's signature
            self._objs.append(_AnimObject(None, None, grid, None, actor, on_update))
            self._animate_next = False

    def add_clip_volume(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        Z: np.ndarray,
        V: np.ndarray,
        scale: Literal["lin", "log", "symlog"] = "lin",
        symmetrize: bool = False,
        clim_crop_factor: float = 1.0,
        clim: tuple[float, float] | None = None,
        cmap: cmap_names | None = None,
        opacity: float = 1.0,
        _fieldname: str | None = None,
    ):
        """Adds a 3D volumetric plot with clip plane based on a 3D grid of X,Y,Z and field values

        Args:
            X (np.ndarray): A 3D Grid of X-values
            Y (np.ndarray): A 3D Grid of Y-values
            Z (np.ndarray): A 3D Grid of Z-values
            V (np.ndarray): The scalar quantity to plot ()
            Nlevels (int, optional): The number of contour levels. Defaults to 5.
            symmetrize (bool, optional): Wether to symmetrize the countour levels (-V,V). Defaults to True.
            cmap (str, optional): The color map. Defaults to 'viridis'.
        """

        
        clim, default_cmap, T = self._parse_field_data(V, scale, symmetrize, clim, clim_crop_factor)
        
        name = self._get_fieldname() if _fieldname is None else _fieldname
        cmap = self._parse_cmap_name(cmap, default_cmap)

        grid = pv.StructuredGrid(X, Y, Z)
        field = V.flatten(order="F")
        grid[name] = T(np.real(field))

        kwargs = self._append_with_defaults(dict(), self.set.theme.surf_kwargs)

        self._plot.add_mesh_clip_plane(
            grid,
            opacity=opacity,
            cmap=cmap,
            clim=clim,
            pickable=False,
            scalar_bar_args=self._cbar_args,
            **kwargs,
        )

        self._reset_cbar()

    def add_contour(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        Z: np.ndarray,
        V: np.ndarray,
        Nlevels: int = 5,
        scale: Literal["lin", "log", "symlog"] = "lin",
        symmetrize: bool = True,
        clim_crop_factor: float = 1.0,
        clim: tuple[float, float] | None = None,
        cmap: cmap_names | None = None,
        _fieldname: str | None = None,
        opacity: float = 0.25,
    ):
        """Adds a 3D volumetric contourplot based on a 3D grid of X,Y,Z and field values

        Args:
            X (np.ndarray): A 3D Grid of X-values
            Y (np.ndarray): A 3D Grid of Y-values
            Z (np.ndarray): A 3D Grid of Z-values
            V (np.ndarray): The scalar quantity to plot ()
            Nlevels (int, optional): The number of contour levels. Defaults to 5.
            symmetrize (bool, optional): Wether to symmetrize the countour levels (-V,V). Defaults to True.
            cmap (str, optional): The color map. Defaults to 'viridis'.
        """
        clim, default_cmap, T = self._parse_field_data(V, scale, symmetrize, clim, clim_crop_factor)
        name = self._get_fieldname() if _fieldname is None else _fieldname
        cmap = self._parse_cmap_name(cmap, default_cmap)

        grid = pv.StructuredGrid(X, Y, Z)
        field = V.flatten(order="F")
        grid[name] = T(np.real(field))

        self._cbar_defaults(title=name)

        levels = list(np.linspace(clim[0], clim[1], Nlevels))
        contour = grid.contour(isosurfaces=levels)

        kwargs = self.set.theme.contour_kwargs

        actor = self._wrap_plot(
            contour,
            opacity=opacity,
            cmap=cmap,
            clim=clim,
            pickable=False,
            scalar_bar_args=self._cbar_args,
            **kwargs,
        )

        if self._animate_next:

            def on_update(obj: _AnimObject, phi: complex):
                new_vals = obj.T(np.real(obj.field * phi))
                obj.grid[name] = new_vals
                new_contour = obj.grid.contour(isosurfaces=levels)
                obj.actor.GetMapper().SetInputData(new_contour)  # type: ignore

            self._objs.append(_AnimObject(field, T, grid, None, actor, on_update))  # type: ignore
            self._animate_next = False
        self._reset_cbar()

    def add_cloud(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        Z: np.ndarray,
        V: np.ndarray,
        scale: Literal["lin", "log", "symlog"] = "lin",
        symmetrize: bool = True,
        clim_crop_factor: float = 1.0,
        clim: tuple[float, float] | None = None,
        cmap: cmap_names | None = None,
        opacity: float | None = None,
        _fieldname: str | None = None,
    ):
        """Adds a 3D volumetric cloud volume plot based on a 3D grid of X,Y,Z and field values

        Args:
            X (np.ndarray): A 3D Grid of X-values
            Y (np.ndarray): A 3D Grid of Y-values
            Z (np.ndarray): A 3D Grid of Z-values
            V (np.ndarray): The scalar quantity to plot ()
            symmetrize (bool, optional): Wether to symmetrize the countour levels (-V,V). Defaults to True.
            cmap (str, optional): The color map. Defaults to 'viridis'.
        """

        clim, default_cmap, T = self._parse_field_data(V, scale, symmetrize, clim, clim_crop_factor)
        name = self._get_fieldname() if _fieldname is None else _fieldname
        cmap = self._parse_cmap_name(cmap, default_cmap)

        # Create opacity scales
        if opacity is None:
            if symmetrize:
                opacity_array = 255 * np.abs(
                    1 - np.cos(np.linspace(-np.pi / 2, np.pi / 2, 256))
                )
            else:
                opacity_array = np.linspace(0, 256, 256)
                opacity_array = 256 * (opacity_array/256)**2
        else:
            opacity_array = opacity

        x_coords = X[0, :, 0]  # Assuming X varies along first axis
        y_coords = Y[:, 0, 0]  # Y varies along second axis
        z_coords = Z[0, 0, :]  # Z varies along third axis

        grid = pv.ImageData(
            dimensions=(len(x_coords), len(y_coords), len(z_coords)),
            spacing=(
                x_coords[1] - x_coords[0],
                y_coords[1] - y_coords[0],
                z_coords[1] - z_coords[0],
            ),
            origin=(x_coords[0], y_coords[0], z_coords[0]),
        )
        
        V = np.nan_to_num(V, nan=0.0)
        field = V.transpose(1, 0, 2).flatten(order="F")
        grid[name] = T(np.real(field))

        self._cbar_defaults(title=name)
        kwargs = self.set.theme.cloud_kwargs

        # Add to the plot
        actor = self._plot.add_volume(
            grid,
            scalars=name,
            opacity=opacity_array,
            clim=clim,
            cmap=cmap,
            pickable=False,
            scalar_bar_args=self._cbar_args,
            **kwargs,
        )
        actor.prop.interpolation_type = "linear"

        if self._animate_next:

            def on_update(obj: _AnimObject, phi: complex):
                field_anim = obj.T(np.real(obj.field * phi))
                obj.grid[name] = field_anim
                obj.actor.GetMapper().SetInputData(obj.grid)
                obj.actor.GetMapper().Modified()
                obj.actor.Modified()

            self._objs.append(_AnimObject(field, T, grid, None, actor, on_update))  # type: ignore
            self._animate_next = False
        self._reset_cbar()

    def add_streamline(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        Z: np.ndarray,
        vx: np.ndarray,
        vy: np.ndarray,
        vz: np.ndarray,
        source_points: np.ndarray | None = None,
        scale: Literal["lin", "log", "symlog"] = "lin",
        clim: tuple[float, float] | None = None,
        clim_crop_factor: float = 1.0,
        cmap: cmap_names | None = None,
        opacity: float = 0.25,
        _fieldname: str | None = 'RTData',
    ):
        """Adds a 3D volumetric cloud volume plot based on a 3D grid of X,Y,Z and field values

        Args:
            X (np.ndarray): A 3D Grid of X-values
            Y (np.ndarray): A 3D Grid of Y-values
            Z (np.ndarray): A 3D Grid of Z-values
            V (np.ndarray): The scalar quantity to plot ()
            cmap (str, optional): The color map. Defaults to 'viridis'.
        """

        # Data Pre Processing
        vx = vx.flatten()
        vx = np.nan_to_num(vx)
        vy = vy.flatten()
        vy = np.nan_to_num(vy)
        vz = vz.flatten()
        vz = np.nan_to_num(vz)
        norm = (np.abs(vx) ** 2 + np.abs(vy) ** 2 + np.abs(vz) ** 2) ** 0.5

        # Creating defaults
        clim, default_cmap, T = self._parse_field_data(norm, scale, False, clim, clim_crop_factor)
        name = self._get_fieldname() if _fieldname is None else _fieldname
        cmap = self._parse_cmap_name(cmap, default_cmap)

        # Data processing for plotting
        x_coords = X[0, :, 0]  # Assuming X varies along first axis
        y_coords = Y[:, 0, 0]  # Y varies along second axis
        z_coords = Z[0, 0, :]  # Z varies along third axis

        grid = pv.ImageData(
            dimensions=(len(x_coords), len(y_coords), len(z_coords)),
            spacing=(
                x_coords[1] - x_coords[0],
                y_coords[1] - y_coords[0],
                z_coords[1] - z_coords[0],
            ),
            origin=(x_coords[0], y_coords[0], z_coords[0]),
        )

        vectors = np.empty((grid.n_points, 3))
        vectors[:, 0] = vx.flatten(order="F")
        vectors[:, 1] = vy.flatten(order="F")
        vectors[:, 2] = vz.flatten(order="F")

        grid["vectors"] = vectors

        if source_points is not None:
            source_points = np.array(source_points)
            if source_points.shape[1] == 3:
                source_points = source_points.T
            source_center = np.mean(source_points, axis=1)
            source_radius = np.max(
                np.linalg.norm(source_points - source_center[:, np.newaxis], axis=0)
            )
        else:
            source_center = None
            source_radius = None
            
        sl = grid.streamlines(
            "vectors",
            n_points=200,
            source_center=source_center,
            source_radius=source_radius,
        )
        self._cbar_defaults(title=name)
        kwargs = self.set.theme.streamline_kwarg

        actor = self._wrap_plot(
            sl,
            cmap=cmap,
            pickable=False,
            scalar_bar_args=self._cbar_args**kwargs,
        )

        self._reset_cbar()

    def _add_aux_items(self) -> None:
        saved_camera = {
            "position": self._plot.camera.position,
            "focal_point": self._plot.camera.focal_point,
            "view_up": self._plot.camera.up,
            "view_angle": self._plot.camera.view_angle,
            "clipping_range": self._plot.camera.clipping_range,
        }

        if not self._colorize:
            return

        if self._colorize:
            col_x = self.set.theme.axis_x_color
            col_y = self.set.theme.axis_y_color
            col_z = self.set.theme.axis_z_color
        else:
            col_x = "black"
            col_y = "black"
            col_z = "black"

        bounds = self._plot.bounds
        self._bounds = bounds

        xmin, xmax, ymin, ymax, zmin, zmax = self._plot.bounds

        max_size = max(
            [
                abs(dim)
                for dim in [
                    bounds.x_max,
                    bounds.x_min,
                    bounds.y_max,
                    bounds.y_min,
                    bounds.z_max,
                    bounds.z_min,
                ]
            ]
        )

        length = self.set.plane_ratio * max_size

        if self.set.theme.draw_xplane:
            plane = pv.Plane(
                center=(0, 0, 0),
                direction=(1, 0, 0),  # normal vector pointing along +X
                i_size=length,  # type: ignore
                j_size=length,  # type: ignore
                i_resolution=1,
                j_resolution=1,
            )
            self._plot.add_mesh(
                plane,
                color=col_x,
                opacity=self.set.plane_opacity,
                show_edges=False,
                pickable=False,
            )
            self._plot.add_mesh(
                plane,
                edge_opacity=1.0,
                edge_color=col_x,
                color=col_x,
                line_width=self.set.plane_edge_width,
                style="wireframe",
                pickable=False,
            )

        if self.set.theme.draw_yplane:
            plane = pv.Plane(
                center=(0, 0, 0),
                direction=(0, 1, 0),  # normal vector pointing along +X
                i_size=length,  # type: ignore
                j_size=length,  # type: ignore
                i_resolution=1,
                j_resolution=1,
            )
            self._plot.add_mesh(
                plane,
                color=col_y,
                opacity=self.set.plane_opacity,
                show_edges=False,
                pickable=False,
            )
            self._plot.add_mesh(
                plane,
                edge_opacity=1.0,
                edge_color=col_y,
                color=col_y,
                line_width=self.set.plane_edge_width,
                style="wireframe",
                pickable=False,
            )
        if self.set.theme.draw_zplane:
            plane = pv.Plane(
                center=(0, 0, 0),
                direction=(0, 0, 1),  # normal vector pointing along +X
                i_size=length,  # type: ignore
                j_size=length,  # type: ignore
                i_resolution=1,
                j_resolution=1,
            )
            self._plot.add_mesh(
                plane,
                color=col_z,
                opacity=self.set.plane_opacity,
                show_edges=False,
                pickable=False,
            )
            self._plot.add_mesh(
                plane,
                edge_opacity=1.0,
                edge_color=col_z,
                color=col_z,
                line_width=self.set.plane_edge_width,
                style="wireframe",
                pickable=False,
            )
        # Draw X-axis
        tlrat = 0.05
        srrat = 0.001
        trad = 0.006
        lrat = 1.1
        if self.set.theme.draw_xax:
            x_line = pv.Arrow(
                start=(0, 0, 0),
                direction=(length * lrat, 0, 0),
                shaft_radius=srrat,
                tip_length=tlrat,
                tip_radius=trad,
                scale="auto",
            )
            self._plot.add_mesh(
                x_line,
                color=col_x,
                ambient=0.5,
                line_width=self.set.axis_line_width,
                pickable=False,
            )

        # Draw Y-axis
        if self.set.theme.draw_yax:
            y_line = pv.Arrow(
                start=(0, 0, 0),
                direction=(0, length * lrat, 0),
                shaft_radius=srrat,
                tip_length=tlrat,
                tip_radius=trad,
                scale="auto",
            )
            self._plot.add_mesh(
                y_line,
                color=col_y,
                ambient=0.5,
                line_width=self.set.axis_line_width,
                pickable=False,
            )

        # Draw Z-axis
        if self.set.theme.draw_zax:
            z_line = pv.Arrow(
                start=(0, 0, 0),
                direction=(0, 0, length * lrat),
                tip_length=tlrat,
                shaft_radius=srrat,
                tip_radius=trad,
                scale="auto",
            )
            self._plot.add_mesh(
                z_line,
                color=col_z,
                ambient=0.5,
                line_width=self.set.axis_line_width,
                pickable=False,
            )

        exponent = np.floor(np.log10(length))
        gs = 10**exponent

        Nxmin, Nxmax, Nymin, Nymax, Nzmin, Nzmax = [
            np.sign(val) * max(1, np.ceil(np.abs(val) / gs))
            for val in [xmin, xmax, ymin, ymax, zmin, zmax]
        ]

        x_vals = np.arange(Nxmin, (Nxmax + 1)) * gs
        y_vals = np.arange(Nymin, (Nymax + 1)) * gs
        z_vals = np.arange(Nzmin, (Nzmax + 1)) * gs

        xmin = Nxmin * gs
        xmax = Nxmax * gs
        ymin = Nymin * gs
        ymax = Nymax * gs
        zmin = Nzmin * gs
        zmax = Nzmax * gs

        def get_mult(val: float) -> float:
            if abs(val) < 1e-9:
                return 2.0
            return 1.0

        # XY grid at Z=0
        if self.set.theme.draw_zgrid:
            # lines parallel to X
            for y in y_vals:
                line = pv.Line(pointa=(xmin, y, 0), pointb=(xmax, y, 0))
                self._plot.add_mesh(
                    line,
                    color=self.set.theme.grid_color,
                    line_width=self.set.theme.grid_width * get_mult(y),
                    opacity=0.5,
                    edge_opacity=0.5,
                    pickable=False,
                )

            # lines parallel to Y
            for x in x_vals:
                line = pv.Line(pointa=(x, ymin, 0), pointb=(x, ymax, 0))
                self._plot.add_mesh(
                    line,
                    color=self.set.theme.grid_color,
                    line_width=self.set.theme.grid_width * get_mult(x),
                    opacity=0.5,
                    edge_opacity=0.5,
                    pickable=False,
                )

        # YZ grid at X=0
        if self.set.theme.draw_xgrid:
            # lines parallel to Y
            for z in z_vals:
                line = pv.Line(pointa=(0, ymin, z), pointb=(0, ymax, z))
                self._plot.add_mesh(
                    line,
                    color=self.set.theme.grid_color,
                    line_width=self.set.theme.grid_width * get_mult(z),
                    opacity=0.5,
                    edge_opacity=0.5,
                    pickable=False,
                )

            # lines parallel to Z
            for y in y_vals:
                line = pv.Line(pointa=(0, y, zmin), pointb=(0, y, zmax))
                self._plot.add_mesh(
                    line,
                    color=self.set.theme.grid_color,
                    line_width=self.set.theme.grid_width * get_mult(y),
                    opacity=0.5,
                    edge_opacity=0.5,
                    pickable=False,
                )

        # XZ grid at Y=0
        if self.set.theme.draw_ygrid:
            # lines parallel to X
            for z in z_vals:
                line = pv.Line(pointa=(xmin, 0, z), pointb=(xmax, 0, z))
                self._plot.add_mesh(
                    line,
                    color=self.set.theme.grid_color,
                    line_width=self.set.theme.grid_width * get_mult(z),
                    opacity=0.5,
                    edge_opacity=0.5,
                    pickable=False,
                )

            # lines parallel to Z
            for x in x_vals:
                line = pv.Line(pointa=(x, 0, zmin), pointb=(x, 0, zmax))
                self._plot.add_mesh(
                    line,
                    color=self.set.theme.grid_color,
                    line_width=self.set.theme.grid_width * get_mult(x),
                    opacity=0.5,
                    edge_opacity=0.5,
                    pickable=False,
                )

        if self.set.add_light:
            light = pv.Light()
            light.set_direction_angle(*self.set.light_angle)  # type: ignore
            self._plot.add_light(light)

        self._plot.add_axes(
            color=self.set.theme.text_color, x_color=col_x, y_color=col_y, z_color=col_z
        )  # type: ignore

        self._plot.camera.position = saved_camera["position"]
        self._plot.camera.focal_point = saved_camera["focal_point"]
        self._plot.camera.up = saved_camera["view_up"]
        self._plot.camera.view_angle = saved_camera["view_angle"]
        self._plot.camera.clipping_range = saved_camera["clipping_range"]


def freeze(function):

    def new_function(self, *args, **kwargs):
        cam = self.disp._plot.camera_position[:]
        self.disp._plot.suppress_rendering = True
        function(self, *args, **kwargs)
        self.disp._plot.camera_position = cam
        self.disp._plot.suppress_rendering = False
        self.disp._plot.render()

    return new_function


class ScreenSelector:
    def __init__(self, display: EMergeDisplay):
        self.encoder: Callable | None = None
        self.disp: EMergeDisplay = display
        self.original_actors: list[pv.Actor] = []
        self.select_actors: list[pv.Actor] = []
        self.grids: list[pv.UnstructuredGrid] = []
        self.surfs: dict[int, np.ndarray] = dict()
        self.state = False

    def _set_encoder_function(self, encoder: Callable) -> None:
        self.encoder = encoder

    def toggle(self):
        if self.state:
            self.turn_off()
        else:
            self.activate()

    def activate(self):
        self.original_actors = list(self.disp._plot.actors.values())

        for actor in self.original_actors:
            if isinstance(actor, pv.Text):
                continue
            actor.pickable = False

        if len(self.grids) == 0:
            for key in self.disp._facetags:
                tris = self.disp._mesh.get_triangles(key)
                ntris = tris.shape[0]
                cells = np.zeros((ntris, 4), dtype=np.int64)
                cells[:, 1:] = self.disp._mesh.tris[:, tris].T
                cells[:, 0] = 3
                nodes = np.unique(self.disp._mesh.tris[:, tris].flatten())
                celltypes = np.full(
                    ntris, fill_value=pv.CellType.TRIANGLE, dtype=np.uint8
                )
                points = self.disp._mesh.nodes.T
                grid = pv.UnstructuredGrid(cells, celltypes, points)
                grid._tag = key  # type: ignore
                self.grids.append(grid)
                self.surfs[key] = points[nodes, :].T

        self.select_actors = []
        for grid in self.grids:
            actor = self.disp._plot.add_mesh(
                grid,
                opacity=0.001,
                color="blue",
                pickable=True,
                name=f"FaceTag_{grid._tag}",
            )
            self.select_actors.append(actor)

        def callback(actor: pv.Actor):
            key = int(actor.name.split("_")[1])
            self.disp._set_highlight_text(self.disp._facetags.get(key, 'Unknown?'))

        self.disp._plot.enable_mesh_picking(
            callback, style="surface", color=self.disp.set.theme.parse_color_name('EMERGE-SELECT'), opacity=0.25, left_clicking=True, use_actor=True
        )

    def turn_off(self) -> None:
        for actor in self.select_actors:
            self.disp._plot.remove_actor(actor)  # type: ignore
        self.select_actors = []
        for actor in self.original_actors:
            if isinstance(actor, pv.Text):
                continue
            actor.pickable = True


def _do_nothing(*args):
    pass


class ScreenRuler:
    def __init__(self, display: EMergeDisplay):
        self.disp: EMergeDisplay = display
        self.points: list[tuple] = [(0, 0, 0), (0, 0, 0)]
        self.text: pv.Text | None = None
        self.ruler: Any = None
        self.state: bool = False
        self._call_coords: Callable = _do_nothing
        self._snap_actor = None

    @freeze
    def toggle(self):
        if not self.state:
            self.turn_on()
        else:
            self.turn_off()

    @freeze
    def turn_on(self):
        if self.state:
            return

        pl = self.disp._plot
        points = ruler_snap_points(
            info["mesh"]
            for info in self.disp._selectable_objects.values()
            if info["actor"].GetVisibility()
        )

        if not len(points):
            logger.info("No ruler snap points found.")
            return

        # Use add_mesh directly: don't register the snap cloud in _data_sets.
        self._snap_actor = pl.add_mesh(
            pv.PolyData(points),
            name="_ruler_snap_points",
            style="points",
            color="orange",
            point_size=12,
            render_points_as_spheres=True,
            lighting=False,
            pickable=True,
            reset_camera=False,
        )

        pl.enable_point_picking(
            callback=self._add_point_callback,
            picker="point",
            left_clicking=True,
            tolerance=0.01,
            show_point=False,
            show_message=False,
            pickable_window=False,
        )

        # Only the snap cloud participates, even if other actors are pickable.
        picker = pl.iren.picker
        picker.InitializePickList()
        picker.AddPickList(self._snap_actor)
        picker.PickFromListOn()

        self.state = True


    @freeze
    def turn_off(self):
        pl = self.disp._plot
        pl.disable_picking()

        if self._snap_actor is not None:
            pl.remove_actor(self._snap_actor, reset_camera=False)
            self._snap_actor = None

        self.state = False

    @property
    def dist(self) -> float:
        p1, p2 = self.points
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2) ** (
            0.5
        )

    @property
    def middle(self) -> tuple[float, float, float]:
        p1, p2 = self.points
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2)

    @property
    def measurement_string(self) -> str:
        dist = self.dist
        p1, p2 = self.points
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dz = p2[2] - p1[2]
        lines = [
            f"p1 = ({p1[0] * 1000:.2f}, {p1[1] * 1000:.2f}, {p1[2] * 1000:.2f})",
            f"p2 = ({p2[0] * 1000:.2f}, {p2[1] * 1000:.2f}, {p2[2] * 1000:.2f})",
            f"{dist * 1000:.2f}mm (dx={1000.0 * dx:.4f}mm, dy={1000.0 * dy:.4f}mm, dz={1000.0 * dz:.4f}mm)",
        ]
        return "\n".join(lines)

    def set_ruler(self) -> None:
        if self.ruler is None:
            self.ruler = self.disp._plot.add_ruler(
                self.points[0], self.points[1], title=f"{1000 * self.dist:.2f}mm"
            )  # type: ignore
        else:
            p1 = self.ruler.GetPositionCoordinate()
            p2 = self.ruler.GetPosition2Coordinate()
            p1.SetValue(*self.points[0])
            p2.SetValue(*self.points[1])
            self.ruler.SetTitle(f"{1000 * self.dist:.2f}mm")
            x1, y1, z = self.points[0]
            x2, y2, z = self.points[1]
            self._call_coords(x1, y1, x2, y2, z)

    @freeze
    def _add_point_callback(self, point: tuple[float, float, float]):
        self.points = [point, self.points[0]]
        self.text = self.disp._plot.add_text(
            self.measurement_string, 
            position=self.middle, 
            name="RulerText",
        )
        self.set_ruler()

        color = pv.Color(self.disp.set.theme.text_color).float_rgb
        self.ruler.GetTitleTextProperty().SetColor(*color)
        self.ruler.GetLabelTextProperty().SetColor(*color)