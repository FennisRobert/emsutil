from .pyvista.display_settings import EMergeTheme


class _VaporWave(EMergeTheme):
    """ A custom EMerge Vaportwave theme with many strong Neon city light colors. """
    def define(self):
        self.backgroung_grad_1 = "#200B44"
        self.backgroung_grad_2 = "#6A0572"
        self.grid_color = "#C280FF9A"
        self.brightness = 1.0
        
        self.geo_edge_color = "#B3FFE9"
        self.label_color = "#18172C"
        self.text_color = "#FFFFFF"
        
        self.bleding_sequence = [
            ('overlay',"#c760ff", 0.5)
        ]
        # The amlitude colormap goes through Neon colors (HSV like) and the Wave is an anti-symmetirc one with 0.49 and 0.51 in the middle with 0 alpha
        # going from neon pink to neon green
        self.colormaps = {
            'amplitude': (("#200B44", "#6A0572", "#C280FF", "#FF6EC4", "#FFABAB", "#B5FFFC", "#6AFFE1", "#20FF9D", "#20B486"), (0.0, 0.1429, 0.2857, 0.4286, 0.5714, 0.7143, 0.8571, 0.95, 1.0)),
            'wave': (("#FF6EC4", "#FFABAB", "#B5FFFD00", "#6AFFE100", "#1BAA6C", "#00FF80AC"), (0.0, 0.25, 0.49, 0.51, 0.75, 1.0)),
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
    """ A custom EMerge theme. """
    def define(self):
        self.backgroung_grad_1 = "#000000"
        self.backgroung_grad_2 = "#000000"
        self.grid_color = "#FFFFFFFF"
        self.brightness = 1.0
        self.mix_color = "#0827f5ff"
        self.geo_edge_color = "#FFFFFF"
        self.label_color = "#000000"
        self.text_color = "#FFFFFF"
        self.render_metal = False

        # 8 Bit axis colors
        
        self.axis_x_color = "#FF0000FF"
        self.axis_y_color = "#00FF00FF"
        self.axis_z_color = "#0000FFFF"
        
        self.aa_active = False
        self.aa_samples = 0
        self.cmap_npts = 16
        
        self.render_shadows = False
        self.render_style = 'wireframe'
        self.render_min_opacity = 0.5
        # * bit amplitude color map scales
        self.colormaps = {
            'amplitude': (("#000000", "#0000FF", "#00FFFF", "#00FF00", "#FFFF00", "#FF0000", "#FFFFFF"),(0.0, 0.1667, 0.3333, 0.5, 0.6667, 0.8333, 1.0)),
            'wave': (("#FF0000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF", "#FF0000"), (0.0, 0.1667, 0.3333, 0.5, 0.6667, 0.8333, 1.0)),
        }
        
        self.bleding_sequence = [
            ('8bit',"#ffffff", 1.0)
        ]
        
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
    """ A custom EMerge theme. """
    def define(self):
        self.backgroung_grad_1 = "#001622"
        self.backgroung_grad_2 = "#000F25"
        self.grid_color = "#00FFEEFF"
        self.brightness = 1.0
        self.geo_edge_color = "#00FFEEFF"
        self.render_mesh = True
        self.label_color = "#000000"
        self.text_color = "#00FFEEFF"
        self.render_metal = True
        self.geo_edge_width = 3.0
        self.geo_mesh_width = 3.0
        self.geo_mesh_color = "#00CCFFFF"
        self.bleding_sequence = [
            ('color',"#00ffae", 0.3),
            ('luminosity',"#00ffae", 0.7)
        ]
        

        self.axis_x_color = "#FFFF00FF"
        self.axis_y_color = "#00FFFFFF"
        self.axis_z_color = "#FF00FFFF"
        self.draw_pvaxes = True
        self.aa_active = True
        self.aa_samples = 5
        self.cmap_npts = 32
        self.colormaps = {
            'amplitude': (("#8C0000", "#FFBB00", "#6FD600", "#2BFFCD", "#00FFC8"),(0.0, 0.25, 0.5, 0.75, 1.0)),
            'wave': (("#95FF00", "#00A727ff", "#00A72700","#0059FF00", "#0059FFFF", "#00D9FF"), (0.0, 0.25, 0.49, 0.51, 0.75, 1.0)),
        }
        
        self.render_style = 'surface'
        self.line_color_cycle = [
            "#00FFEEFF",
            "#FF00FFFF",
            "#FFFF00FF",
            "#FF00AAFF",
            "#AA00FFFF",
            "#00AAFFFF",
        ]

class _Document(EMergeTheme):
    """ A custom EMerge theme. """
    def define(self):
        self.backgroung_grad_1 = "#FFFFFF"
        self.backgroung_grad_2 = "#FFFFFF"
        self.grid_color = "#676767FF"
        self.brightness = 1.0
        
        self.label_color = "#FFFFFF"
        self.text_color = "#000000FF"
        self.render_metal = False
        self.line_width = 3.0
        
        self.geo_edge_width = 3.0
        self.geo_edge_color = "#000000ff"
        
        self.bleding_sequence = [
            ('ansi',"#000000", 1.0)
        ]

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
            'amplitude': (("#0000FF", "#00FFFF", "#00FF00", "#FFFF00", "#FF0000"),(0.0, 0.25, 0.5, 0.75, 1.0)),
            'wave': (("#FF0000", "#FFAAAA00","#0000FF00", "#0000FF"), (0.0, 0.49, 0.51, 1.0)),
        }
        
        self.render_style = 'surface'
        
        # Clear high contrast matlab colors for paper
        self.line_color_cycle = [
            "#0072BDFF",
            "#D95319FF",
            "#EDB120FF",
            "#7E2F8EFF",
            "#77AC30FF",
            "#4DBEEEFF",
        ]


VaporWave = _VaporWave()
Vintage = _Vintage()
Tron = _Tron()
Document = _Document()
