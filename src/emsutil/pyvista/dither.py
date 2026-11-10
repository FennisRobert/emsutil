"""Screen-space ordered dithering for 1-bit (pure black and white) rendering.

The fragment shader of an actor is extended so that every pixel is turned into
black or white by comparing its brightness against a 4x4 Bayer threshold matrix.
The matrix is indexed by window pixel position (gl_FragCoord), so the dot
pattern is fixed on screen and the geometry only masks it. Transparency is
rendered the same way (screen-door): a pixel is either drawn or dropped.
"""

from __future__ import annotations

import pyvista as pv

_DECLARATIONS = """//VTK::Light::Dec
const float _bayer4[16] = float[16](
     0.0,  8.0,  2.0, 10.0,
    12.0,  4.0, 14.0,  6.0,
     3.0, 11.0,  1.0,  9.0,
    15.0,  7.0, 13.0,  5.0);
"""

_IMPLEMENTATION = """//VTK::Light::Impl
{
    float lum = dot(gl_FragData[0].rgb, vec3(0.299, 0.587, 0.114));
    float density = 1.0 - clamp(lum, 0.0, 1.0);
    if (dither_levels > 0) {
        density = floor(density * float(dither_levels) + 0.5) / float(dither_levels);
    }
    ivec2 p = ivec2(mod(floor(gl_FragCoord.xy / dither_cell), 4.0));
    float threshold = (_bayer4[p.y * 4 + p.x] + 0.5) / 16.0;

    // Screen-door transparency: drop pixels instead of blending them into grey.
    // The transposed matrix keeps this pattern from lining up with the density dots.
    float coverage = (_bayer4[p.x * 4 + p.y] + 0.5) / 16.0;
    if (gl_FragData[0].a < coverage) {
        discard;
    }

    float v = density > threshold ? 0.0 : 1.0;
    gl_FragData[0] = vec4(v, v, v, 1.0);
}
"""


def apply_dither(actor: pv.Actor, cell: int = 4, levels: int = 0) -> None:
    """Renders an actor as a black and white dot pattern.

    The dot density follows the brightness of the actor's lit colour, so darker
    materials, shadowed faces and darker colormap values get denser dots.

    Args:
        actor (pv.Actor): The actor to dither.
        cell (int, optional): Size of one pattern dot in pixels. Defaults to 4.
        levels (int, optional): Quantize the density to this many steps (e.g. 4 gives
            0, 25, 50, 75 and 100% black). 0 keeps all 17 Bayer levels. Defaults to 0.
    """
    sp = actor.GetShaderProperty()
    sp.ClearAllFragmentShaderReplacements()
    sp.AddFragmentShaderReplacement("//VTK::Light::Dec", True, _DECLARATIONS, False)
    sp.AddFragmentShaderReplacement("//VTK::Light::Impl", True, _IMPLEMENTATION, False)

    uniforms = sp.GetFragmentCustomUniforms()
    uniforms.SetUniformf("dither_cell", float(max(1, cell)))
    uniforms.SetUniformi("dither_levels", int(max(0, levels)))
