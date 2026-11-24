# Parked features

Taken out of Wicktest on Nov 24, 2026 to be reworked later:

- **Line Art / Color Art inside each layer** (with the bucket filling Color Art by default and a switch to turn that off). Ran into problems in testing; plan to re-implement.
- **Textured brushes** (crayon, chalk, charcoal, spray with rough edges).

`parked-textures-and-line-color-art.patch` has the code for both, as differences from the current Wicktest source:
`engine/src` (ArtLayers.js, BrushTextures.js, Brush, FillBucket, Tool, Path, View.Frame, View.Path, Layer.erase, ToolSettings, gulpfile),
`src/Editor` (ArtLayerSwitch, Toolbox, ToolSettings, ToolIcon) and the built `wickengine.js`.
The brush texture icons are the PNG files in this folder.
