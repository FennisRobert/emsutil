from typing import Literal
from .cmap_maker import make_colormap, LinearSegmentedColormap
import json


class _Cycler:
    """Like itertools.cycle(iterable) but with reset(). Materializes the iterable."""
    def __init__(self, iterable):
        self._data = list(iterable)
        self._n = len(self._data)
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._n == 0:
            raise StopIteration
        item = self._data[self._i]
        self._i += 1
        if self._i == self._n:
            self._i = 0
        return item

    def reset(self):
        self._i = 0
        
class EMergeTheme:
    
    def __init__(self):
        
        
        # Generic Controls
        self.aa_active: bool = True
        self.aa_mode: Literal['msaa', 'fxaa', 'ssaa'] = "msaa"
        self.aa_samples: int = 8
        
        # Background
        self.backgroung_grad_1: str = "#a8c4e7"
        self.backgroung_grad_2: str = "#dbe5f6"
        
        # Axis and Grids
        self.draw_xplane: bool = False
        self.draw_yplane: bool = False
        self.draw_zplane: bool = False
        self.draw_xgrid: bool = False
        self.draw_ygrid: bool = False
        self.draw_zgrid: bool = False
        self.draw_xax: bool = False
        self.draw_yax: bool = False
        self.draw_zax: bool = False
        self.draw_pvgrid: bool = True
        self.draw_pvaxes: bool = True
        
        self.axis_color: str = "#000000"
        self.axis_x_color: str = "#ff007b"
        self.axis_y_color: str = "#88ff00"
        self.axis_z_color: str = "#003cff"
       
        # Grids
        self.grid_color: str = "#8e8e8e"
        self.grid_width: float = 0.5
        
        # Labels
        self.label_color: str = "#FFFFFF"
        self.text_color: str = "#000000"
        
        # Geometry
        self.geo_edge_color: str = "#000000"
        self.geo_edge_width: float = 2.0
        self.geo_mesh_width: float = 1.0
        self.geo_mesh_color: str = "#000000"
        
        # Materials and rendering
        self.render_shadows: bool = True
        self.render_metal: bool = True
        self.render_style: Literal['surface', 'wireframe', 'points'] = 'surface'
        self.render_mesh: bool = False
        self.render_metal_roughness: float = 0.3
        self.render_min_opacity: float = 0.0
        
        # Color modifiers
        self.brightness: float = 1.0
        self.bleding_sequence: list[tuple[str, str, float]] = []
        
        # Colormaps
        self.cmap_npts: int = 256
        self.default_amplitude_colormap: str = "amplitude"
        self.default_wave_colormap: str = "wave"
        
        self.colormaps: dict[str, tuple[list[str], list[float]]] = {
            'amplitude': (["#1F0061","#4218c0","#2849db", "#ff007b", "#ff7c51"], (0.0, 0.15, 0.3, 0.7, 0.95)),
            'wave': (["#4ab9ff","#0510B2B8","#0511B200","#CC095400","#CC0954B9","#ff9036"], (0.0, 0.25, 0.49,0.51, 0.75, 1.0))
        }
        
        self.line_color_cycle = [
            "#0000aa",
            "#aa0000",
            "#009900",
            "#990099",
            "#994400",
            "#005588"
        ]
        
        self.line_cycler: _Cycler = None
        
        self.define()
        self._init()
    
    def define(self):
        """This function is caller after a theme's default initialization to allow customization.
        """
        pass

    def _init(self):
        self.line_cycler = _Cycler(self.line_color_cycle)
    
    @staticmethod
    def load_from_json(json_path: str):
        """ Loads a theme from a JSON file. """
        theme = EMergeTheme()
        with open(json_path, 'r') as f:
            data = json.load(f)
            for key, value in data.items():
                if hasattr(theme, key):
                    setattr(theme, key, value)
        theme._init()
        return theme
        
    def parse_cmap_name(self, name: str) -> LinearSegmentedColormap | str:
        """ Returns a colormap by name if it exists. """
        if name not in self.colormaps:
            return name
        return make_colormap(*self.colormaps[name], N=self.cmap_npts)
    
    @property
    def get_line_cyler(self) -> _Cycler:
        return _Cycler(self.line_color_cycle)
    
    @property
    def default_wave_cmap(self) -> LinearSegmentedColormap:
        return self.parse_cmap_name(self.default_wave_colormap)
    
    @property
    def default_amplitude_cmap(self) -> LinearSegmentedColormap:
        return self.parse_cmap_name(self.default_amplitude_colormap)
    
    @staticmethod
    def color_hex_to_tuple(hex_color: str) -> tuple[float, float, float, float]:
        """ Converts a hex color string to an Red Green Blue Alpha tuple with values between 0 and 1. """
        hex_color = hex_color.lstrip('#')
        lv = len(hex_color)
        has_alpha = lv == 8
        if has_alpha:
            r, g, b, a = tuple(int(hex_color[i:i + 2], 16) for i in range(0, lv, 2))
            return (r / 255.0, g / 255.0, b / 255.0, a / 255.0)
        else:
            r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in range(0, lv, 2))
            return (r / 255.0, g / 255.0, b / 255.0, 1.0)
        
    @staticmethod
    def color_tuple_to_hex(color_tuple: tuple[float, float, float, float]) -> str:
        """ Converts an RGB tuple with values between 0 and 1 to a hex color string. """
        if len(color_tuple) == 4:
            return '#%02x%02x%02x%02x' % tuple(int(c * 255) for c in color_tuple)
        return '#%02x%02x%02x' % tuple(int(c * 255) for c in color_tuple)
    
    def _apply_color_blend(self, 
                          base_rgba: tuple[float, float, float, float],
                          blending_mode: str,
                          mix_color: str,
                          alpha: float) -> tuple[float, float, float, float]:
          
        """ Applies a blending mode to a base color with a mix color and alpha value. """
        mix_rgba = self.color_hex_to_tuple(mix_color)
        mr, mg, mb, _ = mix_rgba
        br, bg, bb, _ = base_rgba
        
        #print(f"start = {br:2f}, {bg:.2f}, {bb:.2f} ")
        if blending_mode == 'normal':
            r = (1 - alpha) * br + alpha * mr
            g = (1 - alpha) * bg + alpha * mg
            b = (1 - alpha) * bb + alpha * mb
        elif blending_mode == 'multiply':
            r = br * ((1 - alpha) + alpha * mr)
            g = bg * ((1 - alpha) + alpha * mg)
            b = bb * ((1 - alpha) + alpha * mb)
        elif blending_mode == 'screen':
            r = 1 - (1 - br) * (1 - (alpha * mr + (1 - alpha)))
            g = 1 - (1 - bg) * (1 - (alpha * mg + (1 - alpha)))
            b = 1 - (1 - bb) * (1 - (alpha * mb + (1 - alpha)))
        elif blending_mode == 'overlay':
            def overlay_channel(bc, mc):
                if bc < 0.5:
                    return 2 * bc * (alpha * mc + (1 - alpha))
                else:
                    return 1 - 2 * (1 - bc) * (1 - (alpha * mc + (1 - alpha)))
            r = overlay_channel(br, mr)
            g = overlay_channel(bg, mg)
            b = overlay_channel(bb, mb)
        elif blending_mode == 'darken':
            r = min(br, alpha * mr + (1 - alpha))
            g = min(bg, alpha * mg + (1 - alpha))
            b = min(bb, alpha * mb + (1 - alpha))
        elif blending_mode == 'lighten':
            r = max(br, alpha * mr + (1 - alpha))
            g = max(bg, alpha * mg + (1 - alpha))
            b = max(bb, alpha * mb + (1 - alpha))
        elif blending_mode == 'color_dodge':
            def color_dodge_channel(bc, mc):
                if mc == 1.0:
                    return 1.0
                return min(1.0, bc / (1 - (alpha * mc + (1 - alpha))))
            r = color_dodge_channel(br, mr)
            g = color_dodge_channel(bg, mg)
            b = color_dodge_channel(bb, mb)
        elif blending_mode == 'color_burn':
            def color_burn_channel(bc, mc):
                if mc == 0.0:
                    return 0.0
                return max(0.0, 1 - (1 - bc) / (alpha * mc + (1 - alpha)))
            r = color_burn_channel(br, mr)
            g = color_burn_channel(bg, mg)
            b = color_burn_channel(bb, mb)
        elif blending_mode == 'hard_light':
            def hard_light_channel(bc, mc):
                if (alpha * mc + (1 - alpha)) < 0.5:
                    return 2 * bc * (alpha * mc + (1 - alpha))
                else:
                    return 1 - 2 * (1 - bc) * (1 - (alpha * mc + (1 - alpha)))
            r = hard_light_channel(br, mr)
            g = hard_light_channel(bg, mg)
            b = hard_light_channel(bb, mb)
        elif blending_mode == 'soft_light':
            def soft_light_channel(bc, mc):
                return (1 - 2 * (alpha * mc + (1 - alpha))) * bc * bc + 2 * (alpha * mc + (1 - alpha)) * bc
            r = soft_light_channel(br, mr)
            g = soft_light_channel(bg, mg)
            b = soft_light_channel(bb, mb)
        elif blending_mode == 'difference':
            r = abs(br - (alpha * mr + (1 - alpha)))
            g = abs(bg - (alpha * mg + (1 - alpha)))
            b = abs(bb - (alpha * mb + (1 - alpha)))
        elif blending_mode == 'exclusion':
            r = br + (alpha * mr + (1 - alpha)) - 2 * br * (alpha * mr + (1 - alpha))
            g = bg + (alpha * mg + (1 - alpha)) - 2 * bg * (alpha * mg + (1 - alpha))
            b = bb + (alpha * mb + (1 - alpha)) - 2 * bb * (alpha * mb + (1 - alpha))
        elif blending_mode == 'luminosity':
            # Convert to grayscale for luminosity
            lum = 0.21 * mr + 0.72 * mg + 0.07 * mb
            r = br + (lum - (0.21 * br + 0.72 * bg + 0.07 * bb)) * alpha
            g = bg + (lum - (0.21 * br + 0.72 * bg + 0.07 * bb)) * alpha
            b = bb + (lum - (0.21 * br + 0.72 * bg + 0.07 * bb)) * alpha
        elif blending_mode == "8bit":
            # Apply 8Bit retro color scales ignoring the mxing color
            r = round(br * 31) / 31.0
            g = round(bg * 63) / 63.0
            b = round(bb * 31) / 31.0
        elif blending_mode == 'ansi':
            # Approximate ANSI color blending
            r = round(br * 5) / 5.0
            g = round(bg * 5) / 5.0
            b = round(bb * 5) / 5.0
        else:
            # Default to normal blending if unknown mode
            r = (1 - alpha) * br + alpha * mr
            g = (1 - alpha) * bg + alpha * mg
            b = (1 - alpha) * bb + alpha * mb
        #print(f"end = {r:2f}, {g:.2f}, {b:.2f} ")
        r = min(1.0, max(0.0, r))
        g = min(1.0, max(0.0, g))
        b = min(1.0, max(0.0, b))
        a = min(1.0, max(0.0, base_rgba[3]))
        return (r, g, b, a)

    def parse_color(self, color: str | tuple[float, float, float]) -> tuple[float, float, float]:
        """ Parses a color input which can be either a hex string or an RGB tuple. """
        
        colstr = False
        if isinstance(color, str):
            col = self.color_hex_to_tuple(color)
            colstr = True
        else:
            if len(color) == 3:
                col = (color[0], color[1], color[2], 1.0)
            else:
                col = color
        
        # apply a brightness modifier to the RGB values (without A channel)
        col = tuple([min(1.0, c * self.brightness) for c in col[:3]]) + (col[3],)
        
        # mix the color with the mix_color by alpha blending
        
        for blending_mode, mix_color, alpha in self.bleding_sequence:
            col = self._apply_color_blend(col, blending_mode, mix_color, alpha)
        
        # Parse back
        if colstr:
            return self.color_tuple_to_hex(col)
        
        # remove alpha channel if it is 100%
        if col[3] == 1.0:
            return col[:3]
        
        return col

class PVDisplaySettings:

    def __init__(self):
        
        self.plane_ratio: float = 0.5
        self.plane_opacity: float = 0.00
        self.plane_edge_width: float = 1.0
        self.axis_line_width: float = 1.5
        self.add_light: bool = False
        self.light_angle: tuple[float, float] = (20., -20.)
        self.z_boost: float = 0.0
        self.depth_peeling: bool = True
        
        self.theme = EMergeTheme()