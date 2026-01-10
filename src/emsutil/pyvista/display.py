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
from .display_settings import PVDisplaySettings, EMergeTheme

import time
import numpy as np
import pyvista as pv
from typing import Literal, Callable, Any
from loguru import logger
from pathlib import Path
from importlib.resources import files
from .utils import determine_projection_data
from ..emdata import FieldPlotData
### Color scale

# Define the colors we want to use
col1 = np.array([57, 179, 227, 255])/255
col2 = np.array([22, 36, 125, 255])/255
col3 = np.array([33, 33, 33, 255])/255
col4 = np.array([173, 76, 7, 255])/255
col5 = np.array([250, 75, 148, 255])/255

cmap_names = Literal['bgy','bgyw','kbc','blues','bmw','bmy','kgy','gray','dimgray','fire','kb','kg','kr',
                     'bkr','bky','coolwarm','gwv','bjy','bwy','cwr','colorwheel','isolum','rainbow','fire',
                     'cet_fire','gouldian','kbgyw','cwr','CET_CBL1','CET_CBL3','CET_D1A']


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

def setdefault(options: dict, **kwargs) -> dict:
    """Shorthand for overwriting non-existent keyword arguments with defaults

    Args:
        options (dict): The kwargs dict

    Returns:
        dict: the kwargs dict
    """
    for key in kwargs.keys():
        if options.get(key,None) is None:
            options[key] = kwargs[key]
    return options

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

def _min_distance(xs, ys, zs):
    """
    Compute the minimum Euclidean distance between any two points
    defined by the 1D arrays xs, ys, zs.
    
    Parameters:
        xs (np.ndarray): x-coordinates of the points
        ys (np.ndarray): y-coordinates of the points
        zs (np.ndarray): z-coordinates of the points
    
    Returns:
        float: The minimum Euclidean distance between any two points
    """
    # Stack the coordinates into a (N, 3) array
    points = np.stack((xs, ys, zs), axis=-1)

    # Compute pairwise squared distances using broadcasting
    diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
    dists_squared = np.sum(diff ** 2, axis=-1)

    # Set diagonal to infinity to ignore zero distances to self
    np.fill_diagonal(dists_squared, np.inf)

    # Get the minimum distance
    min_dist = np.sqrt(np.min(dists_squared))
    return min_dist

def _norm(x, y, z):
    return np.sqrt(np.abs(x)**2 + np.abs(y)**2 + np.abs(z)**2)

class _AnimObject:
    """ A private class containing the required information for plot items in a view
    that can be animated.
    """
    def __init__(self, 
                 field: np.ndarray,
                 T: Callable,
                 grid: pv.Grid,
                 filtered_grid: pv.Grid,
                 actor: pv.Actor,
                 on_update: Callable):
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
        self._facetags: list[int] = []
        self._stop: bool = False
        self._objs: list[_AnimObject] = []
        self._do_animate: bool = False
        self._animate_next: bool = False
        self._closed_via_x: bool = False
        self._Nsteps: int  = 0
        self._fps: int = 25
        self._ruler: ScreenRuler = ScreenRuler(self, 0.001)
        self._selector: ScreenSelector = ScreenSelector(self)
        self._stop = False
        self._objs = []
        self._data_sets: list[pv.DataSet] = []

        self._plot: pv.Plotter | None = None
        self._generate_plotter()
        
        self._ctr: int = 0 
        
        self._isometric: bool = False
        self._bwdrawing: bool = False

        self._bounds: tuple[float, float, float, float, float, float] | None = None
        self._cbar_args: dict = {}
        self._cbar_lim: tuple[float, float] | None = None
        self.camera_position = (1, -1, 1)     # +X, +Z, -Y
        self.__post_init__(*args, **kwargs)
        
        
    def __post_init__(self, *args, **kwargs):
        pass

    def _get_edge_length(self) -> float:
        return 1.0
    ############################################################
    #                        GENERIC METHODS                   #
    ############################################################
    
    def cbar(self, name: str, n_labels: int = 5, interactive: bool = False, clim: tuple[float, float] | None = None ) -> EMergeDisplay:
        self._cbar_args = dict(title=name, n_labels=n_labels, interactive=interactive)
        self._cbar_lim = clim
        return self
    
    def _wrap_plot(self, *args, **kwargs) -> pv.Actor:
        actor = self._plot.add_mesh(*args, **kwargs)
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
        
        self._plot.add_key_event('q', lambda: mark_closed())
    
    @property
    def _colorize(self) -> bool:
        return not self._bwdrawing
    
    @property
    def _camera_distance(self) -> float:
        x,y,z = self._plot.camera.position
        d = (x**2+y**2+z**2)**(0.5)
        return d
    
    def _update_camera(self):
        d = self._camera_distance
        px, py, pz = self.camera_position
        dp = (px**2+py**2+pz**2)**(0.5)
        px, py, pz = px/dp, py/dp, pz/dp
        self._plot.camera.position = (d*px, d*py, d*pz)
    
    def _generate_plotter(self) -> None:
        self._plot = pv.Plotter()

        self._plot.add_key_event("m", self.activate_ruler) # type: ignore
        self._plot.add_key_event("f", self.activate_object) # type: ignore
        self._plot.add_key_event("x", self.view_x)          # type: ignore
        self._plot.add_key_event("y", self.view_y)          # type: ignore
        self._plot.add_key_event("z", self.view_z)          # type: ignore
        self._plot.add_key_event("c", self.toggle_isometric)      # type: ignore
        self._plot.add_key_event("i", self.view_iso)
        
    ############################################################
    #                      KEY PRESS EVENTS                    #
    ############################################################

    def _set_axis_view(self, axis, sign=+1):
        pl = self._plot
        cam = pl.camera

        fp = np.array(cam.focal_point)
        d  = float(self._camera_distance) * sign

        if axis == "x":
            cam.position = (fp[0] + d, fp[1], fp[2])
            cam.up       = (0, 0, 1)
        elif axis == "y":
            cam.position = (fp[0], fp[1] + d, fp[2])
            cam.up       = (0, 0, 1)
        elif axis == "z":
            cam.position = (fp[0], fp[1], fp[2] + d)
            cam.up       = (0, 1, 0)
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

        fp = np.array(cam.focal_point)          # or: np.array(pl.center)
        d  = float(self._camera_distance)

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
        """ Sets the display theme.

        Args:
            theme (EMergeTheme): The theme to set.
        """
        self.set.theme = theme
        
    def show(self):
        """ Shows the Pyvista display. """
        self._ruler.min_length = self._get_edge_length()
        self._update_camera()
        self._add_aux_items()
        self._apply_theme()
        
        if self._do_animate:
            self._wire_close_events()
            self.add_text('Press Q to close!', color='red', position='upper_left')
            self._plot.show(auto_close=False, interactive_update=True, before_close_callback=self._close_callback)
            self._animate()
        else:
            self._plot.show()
        
        self._reset()

    def _get_path(self, filename: str) -> str:
        """Generates a filename for the EMerge package directory in the PyVista folder

        Args:
            filename (str): _description_

        Returns:
            str: _description_
        """
        return str(Path(files('emsutil')) / 'pyvista' / 'textures' / filename)
    
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
            logger.error(f'File {filename} not found. ignoring image')
        return None
        
    def _apply_theme(self):
        picture = self._get_texture('background.png')
        picture.interpolate = True
        picture.mipmap = True
        
        if picture is not None:
            self._plot.set_environment_texture(picture)
        
        if not self.set.theme.render_shadows:
            self._plot.disable_shadows()
            # Turn off directional lighting
            self._plot.remove_all_lights()
        
        if self.set.theme.draw_pvgrid and not self._bwdrawing:
            pv.set_plot_theme('dark')
            bounds = self._bounds
            extra_factor = 0.1
            dx = (bounds[1] - bounds[0])*extra_factor
            dy = (bounds[3] - bounds[2])*extra_factor
            dz = (bounds[5] - bounds[4])*extra_factor
            ds = max(dx, dy, dz)
            bounds = (bounds[0]-ds, bounds[1]+ds, bounds[2]-ds, bounds[3]+ds, bounds[4]-ds, bounds[5]+ds)
            pv.global_theme.font.fmt = "%.3f"
            actor = self._plot.show_grid(
                bounds=bounds,
                color=self.set.theme.text_color,
                fmt="%.3f",
                
            )

        pv.global_theme.font.color = self.set.theme.text_color
        pv.global_theme.colorbar_horizontal.width = 0.4
        pv.global_theme.colorbar_vertical.height = 0.15
        
        if self.set.theme.aa_active:
            self._plot.enable_anti_aliasing(self.set.theme.aa_mode, multi_samples=self.set.theme.aa_samples)
        else:
            self._plot.disable_anti_aliasing()
        self._plot.title = 'EMerge'
        if self._bwdrawing:
            self._plot.set_background('white', top='white') # type: ignore
        else:
            self._plot.set_background(self.set.theme.backgroung_grad_1, top=self.set.theme.backgroung_grad_2) # type: ignore
            
    def _reset(self):
        self._plot.close()
        self._generate_plotter()
        self._stop = False
        self._objs = []
        self._animate_next = False
        self._data_sets = []
        self._bwdrawing = False
        self._reset_cbar()
        self.set.theme.line_cycler.reset()

    def _close_callback(self, arg):
        """The private callback function that stops the animation.
        """
        self._stop = True
        self._reset()

    def _animate(self) -> None:
        """Private function that starts the animation loop.
        """
        
        self._stop = False

        # guard values
        steps = max(1, int(self._Nsteps))
        fps   = max(1, int(self._fps))
        dt    = 1.0 / fps
        next_tick = time.perf_counter()
        step = 0

        while (not self._stop
                and not self._closed_via_x
                and self._plot.render_window is not None):
            # process window/UI events so close button works
            self._plot.update()

            now = time.perf_counter()
            if now >= next_tick:
                step = (step + 1) % steps
                phi = np.exp(1j * (step / steps) * 2*np.pi)

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

    def animate(self, Nsteps: int = 35, fps: int = 25) -> EMergeDisplay:
        """ Turns on the animation mode with the specified number of steps and FPS.

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
        print('If you closed the animation without using (Q) press Ctrl+C to kill the process.')
        self._Nsteps = Nsteps
        self._fps = fps
        self._animate_next = True
        self._do_animate = True
        return self
    
    def drawing_bw(self) -> EMergeDisplay:
        """ Sets the drawing mode to black and white (no colors).

        Args:
            state (bool, optional): Whether to draw in black and white. Defaults to True.
        Returns:

            PVDisplay: The same PVDisplay object
        """
        self._bwdrawing = True
        return self
    
    def _mesh_manual(self, nodes: np.ndarray, tris: np.ndarray) -> pv.UnstructuredGrid:
        ntris = tris.shape[1]
        cells = np.zeros((ntris,4), dtype=np.int64)
        cells[:,1:] = tris.T
        cells[:,0] = 3
        celltypes = np.full(ntris, fill_value=pv.CellType.TRIANGLE, dtype=np.uint8)
        points = nodes.T
        points[:,2] += self.set.z_boost
        return pv.UnstructuredGrid(cells, celltypes, points)
    
    def _add_obj(self,
                 mesh_obj: pv.UnstructuredGrid,
                 obj_dim: int,
                 *args,
                 plot_mesh: bool = False,
                 volume_mesh: bool = True,
                 style: str = 'surface', 
                 metal: bool = False, 
                 metallic: float = None,
                 roughness: float = 0.0,
                 color: str = None, 
                 line_width: float = None, 
                 opacity: float = 1.0, 
                 show_edges: bool = None,
                 texture: str | None = None,
                 **kwargs):
        
        
        style = self.set.theme.render_style
        color = self.set.theme.parse_color(color)
        
        if metallic is None:
            metallic = self.set.theme.render_metal_roughness
            
        if line_width is None:
            line_width = self.set.theme.geo_mesh_width
        
        if color is None:
            color = self.set.theme.geo_edge_color
        
        if show_edges is None:
            show_edges = self.set.theme.render_mesh
        
        edge_color = self.set.theme.geo_mesh_color
        
        if metal and self.set.theme.render_metal:
            pbr = True
            metallic = 0.8
            roughness = self.set.theme.render_metal_roughness
        else:
            pbr = False
            
        # Default keyword arguments when plotting Mesh mode.
        if plot_mesh is True:
            show_edges = True
            opacity = 0.4
            line_width = self.set.theme.geo_mesh_width
            style='wireframe'
            color=next(self.set.theme.line_cycler)
        
        opacity = max(self.set.theme.render_min_opacity, opacity)
        
        # Defining the default keyword arguments for PyVista
        kwargs = setdefault(kwargs, 
                            color=color, 
                            opacity=opacity, 
                            metallic=metallic, 
                            pbr=pbr,
                            roughness=roughness,
                            line_width=line_width, 
                            edge_color=edge_color,
                            show_edges=show_edges, 
                            pickable=True, 
                            smooth_shading=False,
                            split_sharp_edges=True,
                            style=style)
        
        if not self._colorize:
            kwargs['pbr'] = False
            kwargs['roughness'] = 0.0
            kwargs['metallic'] = 0.0
            kwargs['opacity'] = 0.0
            kwargs['color'] = (1,1,1)
            kwargs['silhouette'] = dict(color='black',
                                        line_width=3.0,)
            
        
        if texture is not None and texture != 'None':
            
            tex_image = self._get_texture(texture)
            if tex_image is not None:
                kwargs['texture'] = tex_image
                output = mesh_obj.point_data
                origin = output.dataset.center
                points = output.dataset.points.T
                tris = output.dataset.cells_dict[5].T
                origin, u, v = determine_projection_data(points, tris)
                mesh_obj.texture_map_to_plane(origin=origin, point_u=origin+u, point_v=origin+v, inplace=True)
            
        if plot_mesh is True and volume_mesh is True:
            mesh_obj = mesh_obj.extract_all_edges()
            
        actor = self._wrap_plot(mesh_obj, *args, **kwargs)
        
        # Push 3D Geometries back to avoid Z-fighting with 2D geometries.
        if obj_dim==3:
            mapper = actor.GetMapper()
            mapper.SetResolveCoincidentTopology(1)
            mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(1,0.5)
            
            
    ############################################################
    #                        EMERGE METHODS                    #
    ############################################################
    
    def save_vtk(self, base_path: str) -> None:
        """Saves all the plot object into a directory with the given path to a series of .vtk files.

        Args:
            base_path (str): The base path without extensions.
        """
        if len(self._data_sets)==0:
            logger.error('No VTK objects to save. Make sure to call this method "before" calling .show().')
        base = Path(base_path)
        if base.suffix.lower() == ".vtk":
            base = base.with_suffix("")

        # ensure directory exists
        base.mkdir(parents=True, exist_ok=True)

        logger.info(f'Saving VTK files to {base}')
        # save numbered files
        for idx, vtkobj in enumerate(self._data_sets, start=1):
            filename = base / f"{idx}.vtk"
            vtkobj.save(str(filename))
            logger.debug(f'Saved VTK object to {filename}.')
        logger.info('VTK saving complete!')
        
        
    def add_scatter(self, xs: np.ndarray, ys: np.ndarray, zs: np.ndarray):
        """Adds a scatter point cloud

        Args:
            xs (np.ndarray): The X-coordinate
            ys (np.ndarray): The Y-coordinate
            zs (np.ndarray): The Z-coordinate
        """
        cloud = pv.PolyData(np.array([xs,ys,zs]).T)
        self._data_sets.append(cloud)
        self._plot.add_points(cloud)

    def add_field(self,
                 field: FieldPlotData,
                 scale: Literal['lin','log','symlog'] = 'lin',
                 cmap: cmap_names | None = None,
                 clim: tuple[float, float] | None = None,
                 opacity: float = 1.0,
                 symmetrize: bool = False,
                 _fieldname: str | None = None,
                 **kwargs,) -> pv.DataSet:
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
            symmetrize (bool, optional): If the colorscale should be symmetrized. Defaults to False.
            _fieldname (str | None, optional): A name for the field. Defaults to None.

        Returns:
            pv.DataSet: _description_
        """
        if field.boundary:
            self.add_trisurf(field.x, field.y, field.z, field.F, field.tris,
                                    scale=scale,
                                    cmap=cmap,
                                    clim=clim,
                                    opacity=opacity,
                                    symmetrize=symmetrize,
                                    _fieldname=_fieldname,
                                    **kwargs)
        elif field._is_quiver:
            self.add_quiver(field.x, field.y, field.z, field.vx, field.vy, field.vz, **kwargs)
        else:
            self.add_surf(field.x, field.y, field.z, field.F,
                            scale=scale,
                            cmap=cmap,
                            clim=clim,
                            opacity=opacity,
                            symmetrize=symmetrize,
                            _fieldname=_fieldname,
                            **kwargs)
    def add_surf(self, 
                 x: np.ndarray,
                 y: np.ndarray,
                 z: np.ndarray,
                 field: np.ndarray,
                 scale: Literal['lin','log','symlog'] = 'lin',
                 cmap: cmap_names | None = None,
                 clim: tuple[float, float] | None = None,
                 opacity: float = 1.0,
                 symmetrize: bool = False,
                 _fieldname: str | None = None,
                 **kwargs,) -> pv.DataSet:
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
        
        grid = pv.StructuredGrid(x,y,z)
        field_flat = field.flatten(order='F')
        
        if scale=='log':
            T = lambda x: np.log10(np.abs(x+1e-12))
        elif scale=='symlog':
            T = lambda x: np.sign(x) * np.log10(1 + np.abs(x*np.log(10)))
        else:
            T = lambda x: x
        
        static_field = T(np.real(field_flat))
        
        if _fieldname is None:
            name = 'anim'+str(self._ctr)
        else:
            name = _fieldname
        self._ctr += 1
        
        grid[name] = static_field
        
        grid_no_nan = grid.threshold(scalars=name, all_scalars=True)
        
        default_cmap = self.set.theme.default_amplitude_cmap
        # Determine color limits
        if clim is None:
            if self._cbar_lim is not None:
                clim = self._cbar_lim
            else:
                fmin = np.nanmin(static_field)
                fmax = np.nanmax(static_field)
                clim = (fmin, fmax)
        
        if symmetrize:
            lim = max(abs(clim[0]), abs(clim[1]))
            clim = (-lim, lim)
            default_cmap = self.set.theme.default_wave_cmap
        
        if cmap is None:
            cmap = default_cmap
        else:
            cmap = self.set.theme.parse_cmap_name(cmap)
        
        # Make sure that thresholded cells that are nan are not plotted grey but invisible
        
        kwargs = setdefault(kwargs, cmap=cmap, clim=clim, opacity=opacity, pickable=False, multi_colors=True)
        actor = self._wrap_plot(grid_no_nan, scalars=name, scalar_bar_args=self._cbar_args, **kwargs)
        
        if self._animate_next:
            def on_update(obj: _AnimObject, phi: complex):
                field_anim = obj.T(np.real(obj.field * phi))
                obj.grid[name] = field_anim
                obj.fgrid[name] = obj.grid.threshold(scalars=name)[name]
                #obj.fgrid replace with thresholded scalar data.
            self._objs.append(_AnimObject(field_flat, T, grid, grid_no_nan, actor, on_update))
            self._animate_next = False
        self._reset_cbar()
        return grid_no_nan
    
    def add_trisurf(self, 
                 x: np.ndarray,
                 y: np.ndarray,
                 z: np.ndarray,
                 field: np.ndarray,
                 tris: np.ndarray,
                 scale: Literal['lin','log','symlog'] = 'lin',
                 cmap: cmap_names | None = None,
                 clim: tuple[float, float] | None = None,
                 opacity: float = 1.0,
                 symmetrize: bool = False,
                 _fieldname: str | None = None,
                 **kwargs,):
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
        
        grid = self._mesh_manual(np.array([x,y,z]), tris)
        
        field_flat = field.flatten(order='F')
        
        if scale=='log':
            T = lambda x: np.log10(np.abs(x+1e-12))
        elif scale=='symlog':
            T = lambda x: np.sign(x) * np.log10(1 + np.abs(x*np.log(10)))
        else:
            T = lambda x: x
        
        static_field = T(np.real(field_flat))
        
        if _fieldname is None:
            name = 'anim'+str(self._ctr)
        else:
            name = _fieldname
        self._ctr += 1
        
        grid[name] = static_field
        
        default_cmap = self.set.theme.default_amplitude_cmap
        # Determine color limits
        if clim is None:
            if self._cbar_lim is not None:
                clim = self._cbar_lim
            else:
                fmin = np.nanmin(static_field)
                fmax = np.nanmax(static_field)
                clim = (fmin, fmax)
        
        if symmetrize:
            lim = max(abs(clim[0]), abs(clim[1]))
            clim = (-lim, lim)
            default_cmap = self.set.theme.default_wave_cmap
        
        if cmap is None:
            cmap = default_cmap
        else:
            cmap = self.set.theme.parse_cmap_name(cmap)
            
        kwargs = setdefault(kwargs, cmap=cmap, clim=clim, opacity=opacity, pickable=False, multi_colors=True)
        actor = self._wrap_plot(grid, scalars=name, scalar_bar_args=self._cbar_args, **kwargs)

        if self._animate_next:
            def on_update(obj: _AnimObject, phi: complex):
                field_anim = obj.T(np.real(obj.field * phi))
                obj.grid[name] = field_anim
                #obj.fgrid replace with thresholded scalar data.
            self._objs.append(_AnimObject(field_flat, T, grid, grid, actor, on_update))
            self._animate_next = False
        self._reset_cbar()
        
    def add_title(self, title: str) -> None:
        """Adds a title to the plot

        Args:
            title (str): The title name
        """
        self._plot.add_text(
            title,
            position='upper_edge',
            font_size=18)

    def add_text(self, text: str, 
                 color: str = 'black', 
                 position: Literal['lower_left', 'lower_right', 'upper_left', 'upper_right', 'lower_edge', 'upper_edge', 'right_edge', 'left_edge']='upper_right',
                 abs_position: tuple[float, float, float] | None = None):
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
        
        self._plot.add_text(
            text,
            position=final_position,
            color=color,
            font_size=18,
            viewport=viewport)
        
    def add_quiver(self, 
              x: np.ndarray, y: np.ndarray, z: np.ndarray,
              dx: np.ndarray, dy: np.ndarray, dz: np.ndarray,
              scale: float = 1,
              color: tuple[float, float, float] | None = None,
              cmap: cmap_names | None = None,
              scalemode: Literal['lin','log'] = 'lin'):
        """Add a quiver plot to the display

        Args:
            x (np.ndarray): The X-coordinates
            y (np.ndarray): The Y-coordinates
            z (np.ndarray): The Z-coordinates
            dx (np.ndarray): The arrow X-magnitude
            dy (np.ndarray): The arrow Y-magnitude
            dz (np.ndarray): The arrow Z-magnitude
            scale (float, optional): The arrow scale. Defaults to 1.
            scalemode (Literal['lin','log'], optional): Wether to scale lin or log. Defaults to 'lin'.
        """
        x = x.flatten()
        y = y.flatten()
        z = z.flatten()
        dx = dx.flatten().real
        dy = dy.flatten().real
        dz = dz.flatten().real
        
        ids = np.invert(np.isnan(dx))
        
        if cmap is None:
            cmap = self.set.theme.default_amplitude_cmap
        else:
            cmap = self.set.theme.parse_cmap_name(cmap)

        x, y, z, dx, dy, dz = x[ids], y[ids], z[ids], dx[ids], dy[ids], dz[ids]
        
        dmin = _min_distance(x,y,z)

        dmax = np.max(_norm(dx,dy,dz))
        
        Vec = scale * np.array([dx,dy,dz]).T / dmax * dmin 
        Coo = np.array([x,y,z]).T
        if scalemode=='log':
            dx, dy, dz = _logscale(Vec[:,0], Vec[:,1], Vec[:,2])
            Vec[:,0] = dx
            Vec[:,1] = dy
            Vec[:,2] = dz
        
        kwargs = dict()
        if color is not None:
            kwargs['color'] = color
            
        pl = self._plot.add_arrows(Coo, Vec, scalars=None, clim=None, cmap=cmap, **kwargs)
        self._data_sets.append(pl.mapper.dataset)
        self._reset_cbar()
    
    def add_clip_volume(self,
                     X: np.ndarray,
                     Y: np.ndarray,
                     Z: np.ndarray,
                     V: np.ndarray,
                     scale: Literal['lin','log','symlog'] = 'lin',
                     symmetrize: bool = False,
                     clim: tuple[float, float] | None = None,
                     cmap: cmap_names | None = None,
                     opacity: float = 0.8):
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
        Vf = V.flatten()
        Vf = np.nan_to_num(Vf)
        vmin = np.min(np.real(Vf))
        vmax = np.max(np.real(Vf))
        
        default_cmap = self.set.theme.default_amplitude_cmap
        
        if scale=='log':
            T = lambda x: np.log10(np.abs(x+1e-12))
        elif scale=='symlog':
            T = lambda x: np.sign(x) * np.log10(1 + np.abs(x*np.log(10)))
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
        
        if cmap is None:
            cmap = default_cmap
        else:
            cmap = self.set.theme.parse_cmap_name(cmap)
            
        grid = pv.StructuredGrid(X,Y,Z)
        field = V.flatten(order='F')
        grid['anim'] = T(np.real(field))
        
        
        self._plot.add_mesh_clip_plane(grid, opacity=opacity, cmap=cmap, pickable=False, scalar_bar_args=self._cbar_args)
        #actor = self._wrap_plot(contour, opacity=opacity, cmap=cmap, clim=clim, pickable=False, scalar_bar_args=self._cbar_args)
        
        self._reset_cbar()
        
    def add_contour(self,
                     X: np.ndarray,
                     Y: np.ndarray,
                     Z: np.ndarray,
                     V: np.ndarray,
                     Nlevels: int = 5,
                     scale: Literal['lin','log','symlog'] = 'lin',
                     symmetrize: bool = True,
                     clim: tuple[float, float] | None = None,
                     cmap: cmap_names | None = None,
                     opacity: float = 0.25):
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
        Vf = V.flatten()
        Vf = np.nan_to_num(Vf)
        vmin = np.min(np.real(Vf))
        vmax = np.max(np.real(Vf))
        
        default_cmap = self.set.theme.default_amplitude_cmap
        
        if scale=='log':
            T = lambda x: np.log10(np.abs(x+1e-12))
        elif scale=='symlog':
            T = lambda x: np.sign(x) * np.log10(1 + np.abs(x*np.log(10)))
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
        
        if cmap is None:
            cmap = default_cmap
        else:
            cmap = self.set.theme.parse_cmap_name(cmap)
            
        grid = pv.StructuredGrid(X,Y,Z)
        field = V.flatten(order='F')
        grid['anim'] = T(np.real(field))
        
        levels = list(np.linspace(vmin, vmax, Nlevels))
        contour = grid.contour(isosurfaces=levels)
        
        actor = self._wrap_plot(contour, opacity=opacity, cmap=cmap, clim=clim, pickable=False, scalar_bar_args=self._cbar_args)
        
        if self._animate_next:
            def on_update(obj: _AnimObject, phi: complex):
                new_vals = obj.T(np.real(obj.field * phi))
                obj.grid['anim'] = new_vals
                new_contour = obj.grid.contour(isosurfaces=levels)
                obj.actor.GetMapper().SetInputData(new_contour) # type: ignore
                
            self._objs.append(_AnimObject(field, T, grid, None, actor, on_update)) # type: ignore
            self._animate_next = False
        self._reset_cbar()
        
    def _add_aux_items(self) -> None:
        saved_camera = {
            "position": self._plot.camera.position,
            "focal_point": self._plot.camera.focal_point,
            "view_up": self._plot.camera.up,
            "view_angle": self._plot.camera.view_angle,
            "clipping_range": self._plot.camera.clipping_range
        }
        
        if not self._colorize:
            return
        
        if self._colorize:
            col_x = self.set.theme.axis_x_color
            col_y = self.set.theme.axis_y_color
            col_z = self.set.theme.axis_z_color
        else:
            col_x = 'black'
            col_y = 'black'
            col_z = 'black'
            
        #self._plot.add_logo_widget('src/_img/logo.jpeg',position=(0.89,0.89), size=(0.1,0.1))    
        bounds = self._plot.bounds
        self._bounds = bounds
        
        xmin, xmax, ymin, ymax, zmin, zmax = self._plot.bounds
        
        max_size = max([abs(dim) for dim in [bounds.x_max, bounds.x_min, bounds.y_max, bounds.y_min, bounds.z_max, bounds.z_min]])
        
        length = self.set.plane_ratio*max_size
        
        if self.set.theme.draw_xplane:
            plane = pv.Plane(
                center=(0, 0, 0),
                direction=(1, 0, 0),    # normal vector pointing along +X
                i_size=length, # type: ignore
                j_size=length, # type: ignore
                i_resolution=1,
                j_resolution=1
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
                style='wireframe',
                pickable=False,
            )
            
        if self.set.theme.draw_yplane:
            plane = pv.Plane(
                center=(0, 0, 0),
                direction=(0, 1, 0),    # normal vector pointing along +X
                i_size=length, # type: ignore
                j_size=length, # type: ignore
                i_resolution=1,
                j_resolution=1
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
                style='wireframe',
                pickable=False,
            )
        if self.set.theme.draw_zplane:
            plane = pv.Plane(
                center=(0, 0, 0),
                direction=(0, 0, 1),    # normal vector pointing along +X
                i_size=length, # type: ignore
                j_size=length, # type: ignore
                i_resolution=1,
                j_resolution=1
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
                style='wireframe',
                pickable=False,
            )
        # Draw X-axis
        if self.set.theme.draw_xax:
            x_line = pv.Line(
                pointa=(-length, 0, 0),
                pointb=(length, 0, 0),
            )
            self._plot.add_mesh(
                x_line,
                color=col_x,
                line_width=self.set.axis_line_width,
                pickable=False,
            )

        # Draw Y-axis
        if self.set.theme.draw_yax:
            y_line = pv.Line(
                pointa=(0, -length, 0),
                pointb=(0, length, 0),
            )
            self._plot.add_mesh(
                y_line,
                color=col_y,
                line_width=self.set.axis_line_width,
                pickable=False,
            )

        # Draw Z-axis
        if self.set.theme.draw_zax:
            z_line = pv.Line(
                pointa=(0, 0, -length),
                pointb=(0, 0, length),
            )
            self._plot.add_mesh(
                z_line,
                color=col_z,
                line_width=self.set.axis_line_width,
                pickable=False,
            )

        exponent = np.floor(np.log10(length))
        gs = 10 ** exponent
        
        nextra = 1
        
        Nxmin, Nxmax, Nymin, Nymax, Nzmin, Nzmax = [np.sign(val)*max(1,np.ceil(np.abs(val)/gs)) for val in [xmin, xmax, ymin, ymax, zmin, zmax]]
        
        x_vals = np.arange(Nxmin, Nxmax+1)*gs
        y_vals = np.arange(Nymin, Nymax+1)*gs
        z_vals = np.arange(Nzmin, Nzmax+1)*gs
        
        
        xmin = Nxmin*gs
        xmax = Nxmax*gs
        ymin = Nymin*gs
        ymax = Nymax*gs
        zmin = Nzmin*gs
        zmax = Nzmax*gs
        
        
        # XY grid at Z=0
        if self.set.theme.draw_zgrid:
            
            # lines parallel to X
            for y in y_vals:
                line = pv.Line(
                    pointa=(xmin, y, zmin),
                    pointb=(xmax, y, zmin)
                )
                self._plot.add_mesh(line, color=self.set.theme.grid_color, line_width=self.set.theme.grid_width, opacity=0.5, edge_opacity=0.5,pickable=False)
    
            # lines parallel to Y
            for x in x_vals:
                line = pv.Line(
                    pointa=(x, ymin, zmin),
                    pointb=(x, ymax, zmin)
                )
                self._plot.add_mesh(line, color=self.set.theme.grid_color, line_width=self.set.theme.grid_width, opacity=0.5, edge_opacity=0.5,pickable=False)


        # YZ grid at X=0
        if self.set.theme.draw_xgrid:
            
            # lines parallel to Y
            for z in z_vals:
                line = pv.Line(
                    pointa=(xmin, ymin, z),
                    pointb=(xmin, ymax, z)
                )
                self._plot.add_mesh(line, color=self.set.theme.grid_color, line_width=self.set.theme.grid_width, opacity=0.5, edge_opacity=0.5, pickable=False)

            # lines parallel to Z
            for y in y_vals:
                line = pv.Line(
                    pointa=(xmin, y, zmin),
                    pointb=(xmin, y, zmax)
                )
                self._plot.add_mesh(line, color=self.set.theme.grid_color, line_width=self.set.theme.grid_width, opacity=0.5, edge_opacity=0.5, pickable=False)


        # XZ grid at Y=0
        if self.set.theme.draw_ygrid:
            
            # lines parallel to X
            for z in z_vals:
                line = pv.Line(
                    pointa=(xmin, ymin, z),
                    pointb=(xmax, ymin, z)
                )
                self._plot.add_mesh(line, color=self.set.theme.grid_color, line_width=self.set.theme.grid_width, opacity=0.5, edge_opacity=0.5, pickable=False)

            # lines parallel to Z
            for x in x_vals:
                line = pv.Line(
                    pointa=(x, ymin, zmin),
                    pointb=(x, ymin, zmax)
                )
                self._plot.add_mesh(line, color=self.set.theme.grid_color, line_width=self.set.theme.grid_width, opacity=0.5, edge_opacity=0.5, pickable=False)
        
        if self.set.add_light:
            light = pv.Light()
            light.set_direction_angle(*self.set.light_angle) # type: ignore
            self._plot.add_light(light)

        
        self._plot.add_axes(color=self.set.theme.text_color,
                            x_color=col_x,
                            y_color=col_y,
                            z_color=col_z) # type: ignore

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
                cells = np.zeros((ntris,4), dtype=np.int64)
                cells[:,1:] = self.disp._mesh.tris[:,tris].T
                cells[:,0] = 3
                nodes = np.unique(self.disp._mesh.tris[:,tris].flatten())
                celltypes = np.full(ntris, fill_value=pv.CellType.TRIANGLE, dtype=np.uint8)
                points = self.disp._mesh.nodes.T
                grid = pv.UnstructuredGrid(cells, celltypes, points)
                grid._tag = key # type: ignore
                self.grids.append(grid)
                self.surfs[key] = points[nodes,:].T
        
        self.select_actors = []
        for grid in self.grids:
            actor = self.disp._plot.add_mesh(grid, opacity=0.001, color='red', pickable=True, name=f'FaceTag_{grid._tag}')
            self.select_actors.append(actor)

        def callback(actor: pv.Actor):
            key = int(actor.name.split('_')[1])
            points = self.surfs[key]
            xs = points[0,:]
            ys = points[1,:]
            zs = points[2,:]
            meanx = np.mean(xs)
            meany = np.mean(ys)
            meanz = np.mean(zs)
            data = (meanx, meany, meanz, min(xs), min(ys), min(zs), max(xs), max(ys), max(zs))
            encoded = self.encoder(data) #type: ignore
            print(f'Face code key={key}: ', encoded)

        self.disp._plot.enable_mesh_picking(callback, style='surface', left_clicking=True, use_actor=True)
    
    def turn_off(self) -> None:
        for actor in self.select_actors:
            self.disp._plot.remove_actor(actor) # type: ignore
        self.select_actors = []
        for actor in self.original_actors:
            if isinstance(actor, pv.Text):
                continue
            actor.pickable = True

        
class ScreenRuler:

    def __init__(self, display: EMergeDisplay, min_length: float):
        self.disp: EMergeDisplay = display
        self.points: list[tuple] = [(0,0,0),(0,0,0)]
        self.text: pv.Text | None = None
        self.ruler: Any = None
        self.state: bool = False
        self.min_length: float = min_length
    
    @freeze
    def toggle(self):
        if not self.state:
            self.state = True
            self.disp._plot.enable_point_picking(self._add_point, left_clicking=True, tolerance=self.min_length)
        else:
            self.state = False
            self.disp._plot.disable_picking()

    @freeze
    def turn_off(self):
        self.state = False
        self.disp._plot.disable_picking()
    
    @property
    def dist(self) -> float:
        p1, p2 = self.points
        return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)**(0.5)
    
    @property
    def middle(self) -> tuple[float, float, float]:
        p1, p2 = self.points
        return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2)
    
    @property
    def measurement_string(self) -> str:
        dist = self.dist
        p1, p2 = self.points
        dx = p2[0]-p1[0]
        dy = p2[1]-p1[1]
        dz = p2[2]-p1[2]
        return f'{dist*1000:.2f}mm (dx={1000.*dx:.4f}mm, dy={1000.*dy:.4f}mm, dz={1000.*dz:.4f}mm)'
    
    def set_ruler(self) -> None:
        if self.ruler is None:
            self.ruler = self.disp._plot.add_ruler(self.points[0], self.points[1], title=f'{1000*self.dist:.2f}mm') # type: ignore
        else:
            p1 = self.ruler.GetPositionCoordinate()
            p2 = self.ruler.GetPosition2Coordinate()
            p1.SetValue(*self.points[0])
            p2.SetValue(*self.points[1])
            self.ruler.SetTitle(f'{1000*self.dist:.2f}mm')
    
    @freeze
    def _add_point(self, point: tuple[float, float, float]):
        self.points = [point,self.points[0]]
        self.text = self.disp._plot.add_text(self.measurement_string, self.middle, name='RulerText')
        self.set_ruler()