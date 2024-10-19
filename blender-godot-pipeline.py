bl_info = {
    "name": "Blender Godot Pipeline",
    "blender": (4, 2),
    "category": "Export",
    "description": "A workflow tailored for Godot where you can reset the location and the rotation and use Godot suffix to generate colliders.",
    "author": "Julian - @theredfish - indiedevcasts.com",
    "version": (0, 1, 0),
}

import bpy
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExportPipeline(bpy.types.Operator):
    bl_idname = "export.godot_workflow"
    bl_label = "Export for Godot workflow"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        logger.info("[Blender Godot Pipeline] Exporting selected objects")

        # Dic to store original transforms to restore them later
        original_transforms = {}
        # Array of colliders generated in the scene for export purpose that
        # should be removed after to keep a clean scene.
        colliders = []
        selected_objects = context.selected_objects

        # UI elements
        reset_location = context.scene.reset_location
        reset_rotation = context.scene.reset_rotation
        add_suffix = context.scene.add_suffix
        gltf_export_path = context.scene.gltf_export_path

        for obj in selected_objects:
            if obj.type == "MESH":

                # Save the original location and rotation
                original_transforms[obj.name] = {
                    "location": obj.location.copy(),
                    "rotation": obj.rotation_euler.copy()
                }

                if reset_location:
                    obj.location = (0, 0, 0)
                if reset_rotation:
                    obj.rotation_euler = (0, 0, 0)
                if add_suffix:
                    logger.debug(f"Creating the mesh collider for {obj.name}")
                    collider = obj.copy()
                    collider.name += "_colonly"
                    context.collection.objects.link(collider)
                    colliders.append(collider)

        # Proceed with the gltf export with the configured preset attributes
        bpy.ops.export_scene.gltf(filepath=gltf_export_path, use_selection=True)

        # Restore the original location and rotation if needed
        for obj in selected_objects:
            if obj.type == 'MESH':
                if reset_location:
                    obj.location = original_transforms[obj.name]["location"]
                if reset_rotation:
                    obj.rotation_euler = original_transforms[obj.name]["rotation"]

        # Remove the generated collider objects since they are generated during
        # the export.
        for collider in colliders:
            bpy.data.objects.remove(collider, do_unlink=True)

        return {'FINISHED'}

class ExportPanel(bpy.types.Panel):
    bl_label = "Export with Reset Options"
    bl_idname = "EXPORT_GLTFSCRIPT_PT_panel"
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "reset_location")
        layout.prop(scene, "reset_rotation")
        layout.prop(scene, "add_suffix")
        layout.prop(scene, "gltf_export_path")
        layout.operator("export.godot_workflow", text="Export with Godot Workflow")


def register():
    bpy.utils.register_class(ExportPipeline)
    bpy.utils.register_class(ExportPanel)
    bpy.types.Scene.reset_location = bpy.props.BoolProperty(name="Reset Location", default=True)
    bpy.types.Scene.reset_rotation = bpy.props.BoolProperty(name="Reset Rotation", default=True)
    bpy.types.Scene.add_suffix = bpy.props.BoolProperty(name="Add Godot Suffix", default=True)
    bpy.types.Scene.gltf_export_path = bpy.props.StringProperty(
        name="Export File Path",
        default="",
        description="Path to export the GLTF file"
    )

def unregister():
    bpy.utils.unregister_class(ExportPipeline)
    bpy.utils.unregister_class(ExportPanel)

    del bpy.types.Scene.reset_location
    del bpy.types.Scene.reset_rotation
    del bpy.types.Scene.add_suffix
    del bpy.types.Scene.gltf_export_path

if __name__ == "__main__":
    register()
