from .pyvista.display_settings import EMergeTheme


class _VaporWave(EMergeTheme):
    """A custom EMerge Vaportwave theme with many strong Neon city light colors."""

    def define(self):
        self.backgroung_grad_1 = "#200B44"
        self.backgroung_grad_2 = "#6A0572"
        self.grid_color = "#C280FF9A"
        self.brightness = 1.0

        self.geo_edge_color = "#B3FFE9"
        self.label_color = "#18172C"
        self.text_color = "#FFFFFF"

        self.bleding_sequence = [("overlay", "#c760ff", 0.5)]
        # The amlitude colormap goes through Neon colors (HSV like) and the Wave is an anti-symmetirc one with 0.49 and 0.51 in the middle with 0 alpha
        # going from neon pink to neon green
        self.colormaps = {
            "amplitude": (
                (
                    "#200B44",
                    "#6A0572",
                    "#C280FF",
                    "#FF6EC4",
                    "#FFABAB",
                    "#B5FFFC",
                    "#6AFFE1",
                    "#20FF9D",
                    "#20B486",
                ),
                (0.0, 0.1429, 0.2857, 0.4286, 0.5714, 0.7143, 0.8571, 0.95, 1.0),
            ),
            "wave": (
                (
                    "#FF6EC4",
                    "#FFABAB",
                    "#B5FFFD00",
                    "#6AFFE100",
                    "#1BAA6C",
                    "#00FF80AC",
                ),
                (0.0, 0.25, 0.49, 0.51, 0.75, 1.0),
            ),
        }

        # Line colors are like technical neon colors with 0.5 alpha

        self.line_color_cycle = [
            "#FF6EC49A",
            "#FFABAB9A",
            "#B5FFFC9A",
            "#6AFFE19A",
            "#20FF9D9A",
            "#20B4869A",
        ]


class _Vintage(EMergeTheme):
    """A custom EMerge theme."""

    def define(self):
        self.backgroung_grad_1 = "#000000"
        self.backgroung_grad_2 = "#000000"
        self.grid_color = "#FFFFFFFF"
        self.brightness = 1.0
        self.mix_color = "#0827f5ff"
        self.geo_edge_color = "#FFFFFF"
        self.label_color = "#000000"
        self.text_color = "#FFFFFF"
        self.render_pbr = False

        # 8 Bit axis colors

        self.axis_x_color = "#FF0000FF"
        self.axis_y_color = "#00FF00FF"
        self.axis_z_color = "#0000FFFF"

        self.aa_active = False
        self.aa_samples = 0
        self.cmap_npts = 16

        self.render_shadows = False
        self.render_style = "wireframe"
        self.render_min_opacity = 0.5
        # * bit amplitude color map scales
        self.colormaps = {
            "amplitude": (
                (
                    "#000000",
                    "#0000FF",
                    "#00FFFF",
                    "#00FF00",
                    "#FFFF00",
                    "#FF0000",
                    "#FFFFFF",
                ),
                (0.0, 0.1667, 0.3333, 0.5, 0.6667, 0.8333, 1.0),
            ),
            "wave": (
                (
                    "#FF0000",
                    "#FFFF00",
                    "#00FF00",
                    "#00FFFF",
                    "#0000FF",
                    "#FF00FF",
                    "#FF0000",
                ),
                (0.0, 0.1667, 0.3333, 0.5, 0.6667, 0.8333, 1.0),
            ),
        }

        self.bleding_sequence = [("8bit", "#ffffff", 1.0)]

        # Line color cycle is a goofy 8 bit sequency
        self.line_color_cycle = [
            "#FF0000FF",
            "#00FF00FF",
            "#0000FFFF",
            "#FFFF00FF",
            "#FF00FFFF",
            "#00FFFFFF",
        ]


class _Tron(EMergeTheme):
    """A custom EMerge theme."""

    def define(self):
        self.backgroung_grad_1 = "#001622"
        self.backgroung_grad_2 = "#000F25"
        self.grid_color = "#00FFEEFF"
        self.brightness = 1.0
        self.geo_edge_color = "#00FFEEFF"
        self.render_mesh = True
        self.label_color = "#000000"
        self.text_color = "#00FFEEFF"
        self.render_pbr = True
        self.geo_edge_width = 3.0
        self.geo_mesh_width = 13.0
        self.geo_mesh_color = "#00CCFFFF"
        self.bleding_sequence = [
            ("color", "#00ffae", 0.3),
            ("luminosity", "#00ffae", 0.7),
        ]

        self.axis_x_color = "#FFFF00FF"
        self.axis_y_color = "#00FFFFFF"
        self.axis_z_color = "#FF00FFFF"
        self.draw_pvaxes = True
        self.aa_active = True
        self.aa_samples = 5
        self.cmap_npts = 32
        self.colormaps = {
            "amplitude": (
                ("#8C0000", "#FFBB00", "#6FD600", "#2BFFCD", "#00FFC8"),
                (0.0, 0.25, 0.5, 0.75, 1.0),
            ),
            "wave": (
                (
                    "#95FF00",
                    "#00A727ff",
                    "#00A72700",
                    "#0059FF00",
                    "#0059FFFF",
                    "#00D9FF",
                ),
                (0.0, 0.25, 0.49, 0.51, 0.75, 1.0),
            ),
        }

        self.render_style = "surface"
        self.line_color_cycle = [
            "#00FFEEFF",
            "#FF00FFFF",
            "#FFFF00FF",
            "#FF00AAFF",
            "#AA00FFFF",
            "#00AAFFFF",
        ]


class _Document(EMergeTheme):
    """A custom EMerge theme."""

    def define(self):
        self.backgroung_grad_1 = "#FFFFFF"
        self.backgroung_grad_2 = "#FFFFFF"
        self.grid_color = "#676767FF"
        self.brightness = 1.0

        self.label_color = "#FFFFFF"
        self.text_color = "#000000FF"
        self.render_pbr = False
        self.line_width = 3.0

        self.geo_edge_width = 3.0
        self.geo_edge_color = "#000000ff"

        self.bleding_sequence = [("ansi", "#000000", 1.0)]

        self.draw_xax = False
        self.draw_yax = False
        self.draw_zax = False
        self.draw_xplane = False
        self.draw_yplane = False
        self.draw_zplane = False
        self.draw_xgrid = False
        self.draw_ygrid = False
        self.draw_zgrid = False

        self.axis_x_color = "#FF0000FF"
        self.axis_y_color = "#00FF00FF"
        self.axis_z_color = "#0000FFFF"

        self.aa_active = True
        self.aa_samples = 5
        self.cmap_npts = 64

        # Basic clear academic scales
        # Amplitude is Jet
        # Wave is blue to transparent to red

        self.colormaps = {
            "amplitude": (
                ("#0000FF", "#00FFFF", "#00FF00", "#FFFF00", "#FF0000"),
                (0.0, 0.25, 0.5, 0.75, 1.0),
            ),
            "wave": (
                ("#FF0000", "#FFAAAA00", "#0000FF00", "#0000FF"),
                (0.0, 0.49, 0.51, 1.0),
            ),
        }

        self.render_style = "surface"

        # Clear high contrast matlab colors for paper
        self.line_color_cycle = [
            "#0072BDFF",
            "#D95319FF",
            "#EDB120FF",
            "#7E2F8EFF",
            "#77AC30FF",
            "#4DBEEEFF",
        ]


class _Stylish(EMergeTheme):
    """A custom EMerge theme."""

    def define(self):
        self.backgroung_grad_1 = "#FFFFFF"
        self.backgroung_grad_2 = "#FFFFFF"
        self.grid_color = "#676767FF"
        self.brightness = 1.0

        self.label_color = "#FFFFFF"
        self.text_color = "#000000FF"
        self.render_pbr = True
        self.line_width = 3.0

        self.geo_edge_width = 3.0
        self.geo_edge_color = "#000000ff"

        self.draw_xax = False
        self.draw_yax = False
        self.draw_zax = False
        self.draw_xplane = False
        self.draw_yplane = False
        self.draw_zplane = False
        self.draw_xgrid = False
        self.draw_ygrid = False
        self.draw_zgrid = False

        self.axis_x_color = "#FF0000FF"
        self.axis_y_color = "#00FF00FF"
        self.axis_z_color = "#0000FFFF"

        self.aa_active = True
        self.aa_samples = 5
        self.cmap_npts = 64

        self.draw_pvgrid = False
        self.render_shadows = True
        # Basic clear academic scales
        # Amplitude is Jet
        # Wave is blue to transparent to red

        self.colormaps = {
            "amplitude": (
                ("#0000FF", "#00FFFF", "#00FF00", "#FFFF00", "#FF0000"),
                (0.0, 0.25, 0.5, 0.75, 1.0),
            ),
            "wave": (
                ("#FF0000", "#FFAAAA00", "#0000FF00", "#0000FF"),
                (0.0, 0.49, 0.51, 1.0),
            ),
        }

        self.render_style = "surface"

        # Clear high contrast matlab colors for paper
        self.line_color_cycle = [
            "#003E67FF",
            "#7F2600FF",
            "#5B09A7FF",
            "#0C5D14FF",
            "#A35100FF",
            "#6C006AFF",
        ]


class _GigawaveStudio(EMergeTheme):
    def define(self):

        # Generic Controls
        self.aa_active: bool = True
        self.aa_mode = "msaa"
        self.aa_samples: int = 8

        # Background
        self.backgroung_grad_1: str = "#ffffff"
        self.backgroung_grad_2: str = "#a6acba"

        # Axis and Grids
        self.draw_xplane: bool = False
        self.draw_yplane: bool = False
        self.draw_zplane: bool = False
        self.draw_xgrid: bool = False
        self.draw_ygrid: bool = False
        self.draw_zgrid: bool = True
        self.draw_xax: bool = False
        self.draw_yax: bool = False
        self.draw_zax: bool = False
        self.draw_pvgrid: bool = False
        self.draw_pvaxes: bool = True

        self.axis_color: str = "#000000"
        self.axis_x_color: str = "#ff0000"
        self.axis_y_color: str = "#00ff00"
        self.axis_z_color: str = "#0000ff"

        # Grids
        self.grid_color: str = "#8e8e8e"
        self.grid_width: float = 2

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
        self.render_pbr: bool = False
        self.render_style = "surface"
        self.render_mesh: bool = False
        self.render_metal_roughness: float = 0.3
        self.render_min_opacity: float = 0.0

        # Color modifiers
        self.brightness: float = 1.0
        self.bleding_sequence: list[tuple[str, str, float]] = []

        # Colormaps
        self.cmap_npts: int = 16
        self.default_amplitude_colormap: str = "amplitude"
        self.default_wave_colormap: str = "wave"

        self.colormaps: dict[str, tuple[list[str], list[float]]] = {
            "amplitude": (
                ["#0000ff", "#00ffff", "#00ff00", "#ffff00", "#ff0000"],
                (0.0, 0.25, 0.5, 0.75, 0.99),
            ),
            "wave": (
                ["#0000ff", "#00ffff", "#00ff00", "#ffff00", "#ff0000"],
                (0.0, 0.25, 0.5, 0.75, 0.99),
            ),
        }

        self.line_color_cycle = [
            "#0000aa",
            "#aa0000",
            "#009900",
            "#990099",
            "#994400",
            "#005588",
        ]

        self.color_name_map = {
            "EMERGE-PEC": "#ffff18",
            "EMERGE-DIEL": "#e7c8b4",
            "EMERGE-COPPER": "#ffff18",
            "EMERGE-SELECT": "#ff0000",
            "EMERGE-AIR": "#ffffff",
        }
        self.opacity_codes = {
            "EMERGE-CONDUCTOR": 1.0,
            "EMEREG-DIEL": 1.0,
            "EMERGE-AIR": 0.001,
            "EMERGE-SELECT": 0.5,
            "EMERGE-FFSURF": 0.6,
        }


class _LFSS(EMergeTheme):
    def define(self):

        # Generic Controls
        self.aa_active: bool = True
        self.aa_mode = "msaa"
        self.aa_samples: int = 8

        # Background
        self.backgroung_grad_1: str = "#ffffff"
        self.backgroung_grad_2: str = "#ffffff"

        # Axis and Grids
        self.draw_xplane: bool = False
        self.draw_yplane: bool = False
        self.draw_zplane: bool = False
        self.draw_xgrid: bool = False
        self.draw_ygrid: bool = False
        self.draw_zgrid: bool = True
        self.draw_xax: bool = True
        self.draw_yax: bool = True
        self.draw_zax: bool = True
        self.draw_pvgrid: bool = False
        self.draw_pvaxes: bool = True

        self.axis_color: str = "#000000"
        self.axis_x_color: str = "#ff0000"
        self.axis_y_color: str = "#00ff00"
        self.axis_z_color: str = "#0000ff"

        # Grids
        self.grid_color: str = "#8e8e8e"
        self.grid_width: float = 2

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
        self.render_pbr: bool = False
        self.render_style = "surface"
        self.render_mesh: bool = False
        self.render_metal_roughness: float = 0.3
        self.render_min_opacity: float = 0.0

        # Color modifiers
        self.brightness: float = 1.0
        self.bleding_sequence: list[tuple[str, str, float]] = []

        # Colormaps
        self.cmap_npts: int = 16
        self.default_amplitude_colormap: str = "amplitude"
        self.default_wave_colormap: str = "wave"

        self.colormaps: dict[str, tuple[list[str], list[float]]] = {
            "amplitude": (
                ["#0000ff", "#00ffff", "#00ff00", "#ffff00", "#ff0000"],
                (0.0, 0.25, 0.5, 0.75, 0.99),
            ),
            "wave": (
                ["#0000ff", "#00ffff", "#00ff00", "#ffff00", "#ff0000"],
                (0.0, 0.25, 0.5, 0.75, 0.99),
            ),
        }

        self.line_color_cycle = [
            "#0000aa",
            "#aa0000",
            "#009900",
            "#990099",
            "#994400",
            "#005588",
        ]

        self.color_name_map = {
            "EMERGE-PEC": "#f69754",
            "EMERGE-DIEL": "#abc0ab",
            "EMERGE-COPPER": "#f69754",
            "EMERGE-SELECT": "#ff00ff",
            "EMERGE-AIR": "#ffffff",
        }
        self.opacity_codes = {
            "EMERGE-CONDUCTOR": 1.0,
            "EMEREG-DIEL": 1.0,
            "EMERGE-AIR": 0.001,
            "EMERGE-SELECT": 1.0,
            "EMERGE-FFSURF": 1.0,
            "EMERGE-SURF": 1.0,
        }


class _EMV3(EMergeTheme):
    def define(self):

        # Generic Controls
        self.aa_active: bool = True
        self.aa_mode = "msaa"
        self.aa_samples: int = 8

        # Background
        self.backgroung_grad_1: str = "#373956"
        self.backgroung_grad_2: str = "#0f0e0e"

        # Axis and Grids
        self.draw_xplane: bool = False
        self.draw_yplane: bool = False
        self.draw_zplane: bool = False
        self.draw_xgrid: bool = False
        self.draw_ygrid: bool = False
        self.draw_zgrid: bool = True
        self.draw_xax: bool = True
        self.draw_yax: bool = True
        self.draw_zax: bool = True
        self.draw_pvgrid: bool = False
        self.draw_pvaxes: bool = True

        self.axis_color: str = "#8CCFFF"
        self.axis_x_color: str = "#f93c12"
        self.axis_y_color: str = "#a2fb12"
        self.axis_z_color: str = "#3b62ff"

        # Grids
        self.grid_color: str = "#d17711"
        self.grid_width: float = 2

        # Labels
        self.label_color: str = "#4B4B4B"
        self.text_color: str = "#ACCDE5"

        # Geometry
        self.geo_edge_color: str = "#90C0FF"
        self.geo_edge_width: float = 2.0
        self.geo_mesh_width: float = 1.0
        self.geo_mesh_color: str = "#005CD4"

        # Materials and rendering
        self.render_shadows: bool = True
        self.render_pbr: bool = True
        self.render_style = "surface"
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
            "amplitude": (
                ("#30123B", "#28BBEC", "#A2FC3C", "#FF8426", "#E80D09"),
                (0.0, 0.25, 0.5, 0.75, 1.0),
            ),
            "wave": (
                (
                    "#FF8426",
                    "#eb1c1cb6",
                    "#FF000000",
                    "#006EFF00",
                    "#006EFFB7",
                    "#28DFFF",
                ),
                (0.0, 0.4, 0.49, 0.51, 0.6, 1.0),
            ),
        }

        self.line_color_cycle = [
            "#8484ff",
            "#ff7d7d",
            "#73FF73",
            "#FF5E94",
            "#FFB06F",
            "#65E8FF",
        ]

        self.color_name_map = {
            "EMERGE-PEC": "#C14D0A",
            "EMERGE-DIEL": "#55C955",
            "EMERGE-COPPER": "#bb5710",
            "EMERGE-SELECT": "#33a7ff",
            "EMERGE-AIR": "#DEEBF400",
            "EMERGE-TEXT": "#ACCDE5",
        }
        self.opacity_codes = {
            "EMERGE-CONDUCTOR": 1.0,
            "EMEREG-DIEL": 0.8,
            "EMERGE-AIR": 0.01,
            "EMERGE-SELECT": 0.8,
            "EMERGE-SURF": 1.0,
            "EMEREG-FFSURF": 1.0,
        }

        self.obj_3d_kwarg = dict()
        self.farfield_3d_kwarg = dict(
            lighting=True, smooth_shading=True, specular=0.7, diffuse=0.75, ambient=0.2
        )
        self.surf_kwargs = dict(lighting=True, diffuse=0.75, ambient=0.2, specular=0.7)
        self.quiver_kwargs = dict(
            tip_length=1.0,
            tip_radius=0.1,
        )


VaporWave = _VaporWave()
Vintage = _Vintage()
Tron = _Tron()
Document = _Document()
Stylish = _Stylish()
GigawaveStudio = _GigawaveStudio()
LFSS = _LFSS()
EMV3 = _EMV3()
