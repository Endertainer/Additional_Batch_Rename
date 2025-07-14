import bpy


#━━━━━━━━━━━━━━
#     Main     
#━━━━━━━━━━━━━━

class ADD_BatchRename(bpy.types.Operator):
    """Additional Batch rename operators."""
    bl_idname = "add.batchrename"
    bl_label = "Additional Batch Rename"
    bl_options = {'REGISTER', 'UNDO'}

    # -------------------
    #     Properties     
    # -------------------

    # Enum property to select the type of batch renaming to perform (Modifier/Constraints or Vertex Groups)
    operator_type: bpy.props.EnumProperty(
        name="Operator",
        items=[
            ('MODCON', "Modifiers/Constraints", ""),
            ('VERTGROUP', "Vertex Groups", "")
        ],
        default='MODCON',
        description="Select the type of batch renaming operator"
    )

    # Enum property to select the type of data to rename (Modifiers or Constraints)
    data_type: bpy.props.EnumProperty(
        name="Data",
        items=[
            ('MODIFIERS', "Modifiers", ""),
            ('CONSTRAINTS', "Constraints", "")
        ],
        default='MODIFIERS',
        description="Select whether to rename modifiers or constraints"
    )

    # Enum property to select the target (Objects or Bones)
    target_type: bpy.props.EnumProperty(
        name="Target",
        items=[
            ('OBJECTS', "Objects", ""),
            ('BONES', "Bones", "")
        ],
        default='OBJECTS',
        description="Select whether to target objects or bones"
    )

    # Enum property to select the scope of operation (Selected or All)
    scope_type: bpy.props.EnumProperty(
        name="Scope",
        items=[
            ('SELECTED', "Selected", ""),
            ('ALL', "All", "")
        ],
        default='SELECTED',
        description="Select whether to apply to selected items or all items (For bones only on active armature)"
    )

    # Enum property to select the type of operation (Find & Replace, Prefix, Suffix)
    operation_type: bpy.props.EnumProperty(
        name="Operation",
        items=[
            ('FIND_REPLACE', "Find & Replace", ""),
            ('PREFIX', "Prefix", ""),
            ('SUFFIX', "Suffix", "")
        ],
        default='FIND_REPLACE',
        description="Select the type of renaming operation"
    )

    # String property for the string to find (used in Find & Replace)
    find_str: bpy.props.StringProperty(
        name="Find",
        default="",
        description="String to find for replacement"
    )

    # String property for the replacement string (used in Find & Replace)
    replace_str: bpy.props.StringProperty(
        name="Replace",
        default="",
        description="Replacement string for Find & Replace"
    )

    # String property for the prefix (used in Prefix)
    prefix_str: bpy.props.StringProperty(
        name="Prefix",
        default="",
        description="Prefix to add to names"
    )

    # String property for the suffix (used in Suffix)
    suffix_str: bpy.props.StringProperty(
        name="Suffix",
        default="",
        description="Suffix to add to names"
    )

    # Bool property for exact matching search
    exact_match: bpy.props.BoolProperty(
        name='Exact Match',
        default=False,
        description="If enabled, find only string with exact matches"
    )

    # ------------------
    #     Interface     
    # ------------------

    # Invoke the operator and display the dialog
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    # Draw the operator panel in the Blender UI
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "operator_type")

        # If operator_type is MODCON, show Modifiers and Constraints settings
        if self.operator_type == 'MODCON':

            layout.prop(self, "target_type", expand=True)

             # If BONES are targeted, force data type to CONSTRAINTS and display a message
            if self.target_type == 'BONES':
                self.data_type = 'CONSTRAINTS'
                layout.label(text="Data type is set to constraints for bones.", icon= 'INFO_LARGE')
            else:

                # Display data type (Modifiers/Constraints) for objects
                layout.prop(self, "data_type", expand=True)

            layout.prop(self, "scope_type", expand=True)

            # If BONES are targeted and scope is ALL, show a warning about armature
            if self.target_type == 'BONES' and self.scope_type == 'ALL':
                layout.label(text="Only rename all bones on active armature.", icon= 'WARNING_LARGE')

            # Set input based on operation type
            layout.prop(self, "operation_type", expand=True)
            if self.operation_type == 'FIND_REPLACE':
                layout.prop(self, "find_str")
                layout.prop(self, "replace_str")
                layout.prop(self, "exact_match")
            elif self.operation_type == 'PREFIX':
                layout.prop(self, "prefix_str")
            elif self.operation_type == 'SUFFIX':
                layout.prop(self, "suffix_str")
        
        # If operator_type is VERTGROUP, show Vertex Groups settings
        elif self.operator_type == 'VERTGROUP':
            
            layout.prop(self, "scope_type", expand=True)
            layout.prop(self, "operation_type", expand=True)

            # Set input based on operation type
            if self.operation_type == 'FIND_REPLACE':
                layout.prop(self, "find_str")
                layout.prop(self, "replace_str")
                layout.prop(self, "exact_match")
            elif self.operation_type == 'PREFIX':
                layout.prop(self, "prefix_str")
            elif self.operation_type == 'SUFFIX':
                layout.prop(self, "suffix_str")

    # ------------------
    #     Functions     
    # ------------------

    # Process modifiers for renaming and returns the number of modifiers renamed
    def process_modifiers(self, modifiers):

        # Counter for successfully renamed modifiers
        renamed = 0

        for mod in modifiers:
            if self.operation_type == 'FIND_REPLACE':
                if self.exact_match:

                    # Check for an exact match of the modifier's name
                    if mod.name == self.find_str:
                        mod.name = self.replace_str
                        renamed += 1

                else:

                    # Check if the 'find_str' is a substring within the modifier's name
                    if self.find_str in mod.name:
                        mod.name = mod.name.replace(self.find_str, self.replace_str)
                        renamed += 1

            elif self.operation_type == 'PREFIX':

                # Add the specified prefix to the modifier's name
                mod.name = f"{self.prefix_str}{mod.name}"
                renamed += 1

            elif self.operation_type == 'SUFFIX':

                # Add the specified suffix to the modifier's name
                mod.name = f"{mod.name}{self.suffix_str}"
                renamed += 1
        
        # Return the total count of renamed modifiers
        return renamed

    # Process constraints for renaming and returns the number of constraints renamed
    def process_constraints(self, constraints):

        # Counter for successfully renamed constraints
        renamed = 0

        for con in constraints:
            if self.operation_type == 'FIND_REPLACE':
                if self.exact_match:

                    # Check for an exact match of the constraint's name
                    if con.name == self.find_str:
                        con.name = self.replace_str
                        renamed += 1

                else:

                    # Check if the 'find_str' is a substring within the constraint's name
                    if self.find_str in con.name:
                        con.name = con.name.replace(self.find_str, self.replace_str)
                        renamed += 1

            elif self.operation_type == 'PREFIX':

                # Add the specified prefix to the constraint's name
                con.name = f"{self.prefix_str}{con.name}"
                renamed += 1

            elif self.operation_type == 'SUFFIX':

                # Add the specified suffix to the constraint's name
                con.name = f"{con.name}{self.suffix_str}"
                renamed += 1

        # Return the total count of renamed constraints
        return renamed

    # Process vertex groups for renaming and returns the number of vertex groups renamed
    def process_vertex_groups(self, vertex_groups):

        # Counter for successfully renamed vertex groups
        renamed = 0

        for vg in vertex_groups:
            if self.operation_type == 'FIND_REPLACE':
                if self.exact_match:

                    # Check for an exact match of the vertex group's name
                    if vg.name == self.find_str:
                        vg.name = self.replace_str
                        renamed += 1
                
                else:

                    # Check if the 'find_str' is a substring within the vertex group's name
                    if self.find_str in vg.name:
                        vg.name = vg.name.replace(self.find_str, self.replace_str)
                        renamed += 1

            elif self.operation_type == 'PREFIX':

                # Add the specified prefix to the vertex group's name
                vg.name = f"{self.prefix_str}{vg.name}"
                renamed += 1

            elif self.operation_type == 'SUFFIX':

                # Add the specified suffix to the vertex group's name
                vg.name = f"{vg.name}{self.suffix_str}"
                renamed += 1

        # Return the total count of renamed vertex groups
        return renamed

    # ------------------
    #     Execution     
    # ------------------

    # Execute the batch rename operation based on the selected parameters
    def execute(self, context):

        # Initialize counters for renamed and failed operations
        renamed_count = 0
        failed_count = 0

        # If operator_type is MODCON, do Modifiers and Constraints batch renaming
        if self.operator_type == 'MODCON':
            
            # List to store the actual objects or bones to process
            items = []

            # Determine the items to process based on target_type and scope_type
            if self.target_type == 'OBJECTS':
                if self.scope_type == 'SELECTED':
                    items = context.selected_objects

                    # Stop if no objects are selected
                    if not items:
                        self.report({'INFO'}, "No object(s) selected.")
                        return {'CANCELLED'}
                else:

                    # Get all objects in the current Blender file
                    items = bpy.data.objects

            elif self.target_type == 'BONES':
                if self.scope_type == 'SELECTED':
                    
                    # Iterate through selected objects to find armatures and their selected bones
                    for obj in context.selected_objects:
                        if obj.type == 'ARMATURE':
                            pose_bones = obj.pose.bones
                            selected_bones = [pb for pb in pose_bones if pb.bone.select]
                            items.extend(selected_bones)
                    
                    # Stop if no bones are selected
                    if not items:
                        self.report({'INFO'}, "No bone(s) selected.")
                        return {'CANCELLED'}
                else:
                    active_object = context.active_object

                    # Get all bones from the active armature
                    if active_object and active_object.type == 'ARMATURE':
                        items = active_object.pose.bones

                    else:

                        # Stop if no armature is active
                        self.report({'INFO'}, "No active armature.")
                        return {'CANCELLED'}
            
            # If target_type is BONES, enforce data_type to CONSTRAINTS
            if self.target_type == 'BONES':
                self.data_type = 'CONSTRAINTS'

            # Process each item based on data_type
            for item in items:
                if self.data_type == 'MODIFIERS':

                    # Check if the item has a 'modifiers' collection
                    if hasattr(item, 'modifiers'):

                        # Check if the item has a 'modifiers' collection
                        renamed_count += self.process_modifiers(item.modifiers)

                    else:

                        # Increment failed count if no modifiers found
                        failed_count += 1

                else:

                    # Check if the item has a 'constraints' collection
                    if hasattr(item, 'constraints'):

                        # Process constraints
                        renamed_count += self.process_constraints(item.constraints)

                    else:
                        
                        # Specific warning for armatures with no bones (which would have no constraints)
                        if self.target_type == 'BONES':
                            self.report({'WARNING'}, "Armature has no bones or selected bones have no constraints.")

                        # Increment failed count if no constraints found
                        failed_count += 1

            # Report the results of the Modifiers/Constraints renaming operation
            if renamed_count > 0:
                self.report({'INFO'}, f"Renamed {renamed_count} {self.data_type.lower()}.")
            if failed_count > 0:
                if renamed_count == 0:
                    self.report({'WARNING'}, f"No {self.data_type.lower()} renamed.")
        
        # If operator_type is VERTGROUP, do Vertex Groups batch renaming
        elif self.operator_type == 'VERTGROUP':
            
            # List to store objects to process for vertex groups
            objects = []

            # Determine the objects to process based on scope_type
            if self.scope_type == 'SELECTED':

                # Get currently selected objects
                objects = context.selected_objects
                if not objects:
                    self.report({'INFO'}, "No object(s) selected.")
                    return {'CANCELLED'}
            else:

                # Get all objects in the current Blender file
                objects = bpy.data.objects
                if not objects:
                    self.report({'INFO'}, "No objects in the scene.")
                    return {'CANCELLED'}

            # Iterate through the determined objects and process their vertex groups
            for obj in objects:

                # Only process objects that typically have vertex groups
                if obj.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'ARMATURE', 'LATTICE']:

                    # Check if the object has vertex groups
                    if obj.vertex_groups:

                        # Process vertex groups
                        renamed_count += self.process_vertex_groups(obj.vertex_groups)

                    else:

                        # Increment failed count if no vertex groups found
                        failed_count += 1

            # Report the results of the Vertex Groups renaming operation
            if renamed_count > 0:
                self.report({'INFO'}, f"Renamed {renamed_count} Vertex Group(s).")
            if failed_count > 0:
                if renamed_count == 0:
                    self.report({'WARNING'}, f"No Vertex Group(s) renamed.")

        return {'FINISHED'}


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     Register & Unregister     
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Function to draw the operator in the context menu
def draw_context_menu(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.separator()
    self.layout.operator(ADD_BatchRename.bl_idname, text="Additional Batch Rename")

# Register the classes and append the context menu to Blender's UI
def register():
    bpy.utils.register_class(ADD_BatchRename)
    
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_context_menu)
    bpy.types.VIEW3D_MT_pose_context_menu.append(draw_context_menu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(draw_context_menu)

# Unregister the classes and remove the context menu from Blender's UI
def unregister():
    bpy.utils.unregister_class(ADD_BatchRename)
    
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_context_menu)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(draw_context_menu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_context_menu)

if __name__ == "__main__":
    register()