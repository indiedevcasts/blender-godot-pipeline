# blender-godot-pipeline

A Blender add-on to save you time when exporting glTF assets and modeling game maps. **This add-on only works with mesh
objects**.

## Developer note

This Blender add-on is under development. While it can be used if you find it helpful it might be bugged and not easy
to install.

## How to install

- Clone this repository
- Edit > Preferences > Add-ons
- On the top-right you should have a dropdown menu (arrow). Expand it and click on "Install from disk"
- Add the `blender-godot-pipeline.py` file
- Enable (check) the add-on "Blender Godot Pipeline"

## Usage

- Select one or several objects from the hierarchy
- File > Export > glTF 2.0
- Then expand the panel "Export with Reset Options" at the bottom-left
- Check the options as you prefer and add the path of your exported asset(s)
- Click the button "Export with Godot Workflow" (not the built-in export button")

**Note**: You inherit the operator presets from the built-in glTF exporter. So you can check `Transform > +Y Up` and other
options.

**Tip**: You can use the file explorer from the official built-in window and just copy/paste the path in the "Export with
Reset Options" panel.

### Reset options

When working in Blender you might need to change the location and rotation of your assets especially if you are working with a map or putting together multiple objects. If you don't want to keep the location and rotation changes, you can
check `Reset Location` and `Reset Rotation`. This is very handy if you want to update glb scenes (prefabs).

### Godot suffix

At the moment this add-on only supports the Godot suffix `-onlycol`. When you select your objects to export, the add-on
will duplicate them and suffix the name with `-onlycol` so Godot receive this suffix hint and will generate a separate
mesh collider. To avoid polluting your hierarchy in Blender, these duplicated objects are automatically removed once the
export is complete.

## Troubleshooting

### Failed loading resource

> modules/gltf/gltf_document.cpp:552 - Condition "!scene_dict.has("nodes")" is true. Returning: ERR_UNAVAILABLE
> Make sure resources have been imported by opening the project in the editor at least once.

If you get similar messages this is just because the add-on requires at least one object from the hierarchy. Better
error handling will be added later.

## Next features

This add-on will provide a pipeline to make game-ready assets while designing a map. The main objective is to gain
as much time as possible by reducing the manual tasks for the developer.

When you design a map it's a time saver if you can place real assets on it but export them to Godot as prefabs by
resetting their Transform information. This way you can manage prefabs in Godot, have LOD and other improvements, while designing your game map with static assets directly in Blender.

The next big feature will be the ability to generate markers (empty objects) inheriting asset properties
(location, rotation, ...) and linking prefabs (with name conventions) to these markers in Godot.



