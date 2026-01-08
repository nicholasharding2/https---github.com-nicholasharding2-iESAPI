import streamlit as st

# local imports
from helper import margin_group, get_roi_types
from commands import (
    build_margin_command,
    build_crop_command,
    build_extract_wall_command,
    build_bool_command,
    build_copy_command
)

# initilise commands once
if "commands" not in st.session_state:
    st.session_state.commands = []

st.title("Interactive ESAPI Automation Code Generator")

tab_structures, tab_plan = st.tabs(["Auto Structure", "Auto Plan"])

with tab_structures:
    st.header("Create list of structure generation commands")

    st.write("Define automation instruction")
    # Command selection
    command_options = [
        "Margin for Structure",
        "Extract Wall",
        "Crop",
        "Boolean",
        "Copy",
        "Remove"
    ]
    st.divider()
    chosen_command = st.selectbox("Choose a command", command_options)
    # final target ID
    target_structure = st.text_input("Final Target Structure ID", max_chars=32, key = "target_id")
    
    dicom_roi_options = get_roi_types()
    dicom_roi_choice = st.selectbox("Choose Final Target ROI type (if requried)", dicom_roi_options, key="dicom_roi", index=None)
    st.divider()
    # Original structure ID
    orig_structure = st.text_input("Original Structure ID", max_chars=32, key = "original_id")

    

    # add some validation for the add command button later
    can_add = False
    validation_errors = []

    if chosen_command == "Margin for Structure":
        # Geometry choice
        outer_or_inner = st.radio("Outer or inner margin", ["outer", "inner"])

        symmetric = st.checkbox("Use symmetrical margin", value=True)

        # Symmetric checkbox
        #sym_margin = st.checkbox("Use symmetrical margin", value=True, key="sym_margin")

         # Labels and keys
        margins_labels = [
            "Lat Left (cm)",
            "Lat Right (cm)",
            "Vert Up (cm)",
            "Vert Down (cm)",
            "Long Sup (cm)",
            "Long Inf (cm)"
        ]

        margins = margin_group(
            base_key = "structure_margin",
            labels = margins_labels,
            symmetric=symmetric
            )
        
        margin_avoid = st.checkbox("Avoid structure?", key="Margin_Avoid")
        if margin_avoid:
            avoid_id = st.text_input("Avoid Structure ID", max_chars=32)
        else:
            avoid_id=""

        # button validation
        can_add = (
            isinstance(orig_structure, str)
            and isinstance(target_structure, str)
            and orig_structure.strip() != ""
            and target_structure.strip() != ""
        )
        if not can_add:
            validation_errors.append("Original and output structure IDs are required.")



    elif chosen_command == "Extract Wall":
        outer_wall_margin = st.number_input(
            "Outer wall margin (cm)",
            key = "Outer Wall Margin",
            min_value=-5.0,
            max_value=5.0,
            step=0.1,
            format="%0.1f",
            value=0.0
            )
        inner_wall_margin = st.number_input(
            "Inner wall margin (cm)",
            key = "Inner Wall Margin",
            min_value=-5.0,
            max_value=5.0,
            step=0.1,
            format="%0.1f",
            value=0.0
            )
        # button validation
        can_add = (
            isinstance(orig_structure, str)
            and isinstance(target_structure, str)
            and orig_structure.strip() != ""
            and target_structure.strip() != ""
        )
        if not can_add:
            validation_errors.append("Original and output structure IDs are required.")

    elif chosen_command == "Crop":
        crop_direction = st.radio("Remove part extending",["outside","inside"])
        st.write("crop structure.")
        crop_structure = st.text_input("Crop Structure ID", max_chars=32)

        crop_avoid = st.checkbox("Additional margin?", key="Crop_Margin")
        if crop_avoid:
            #avoid_id = st.text_input("Avoid Structure ID", max_chars=32)
            additional_margin = st.number_input(
            "Additional margin (cm)",
            min_value=0.0,
            max_value=5.0,
            step=0.1,
            format="%0.1f",
            value=0.0
            )

        else:
            additional_margin=0.0
        
        # button validation
        can_add = (
            isinstance(orig_structure, str)
            and isinstance(target_structure, str)
            and isinstance(crop_structure, str)
            and orig_structure.strip() != ""
            and target_structure.strip() != ""
            and crop_structure.strip() != ""
        )
        if not can_add:
            validation_errors.append("Original, output and crop structure IDs are required.")

        
        
    elif chosen_command == "Boolean":
        boolean_options = ["OR","AND","SUB","XOR"]
        boolean_choice = st.pills("Operator",boolean_options)
        if boolean_choice == "OR":
            st.image("images/boolean_or.png", caption="Union (OR)", width=75)
        elif boolean_choice == "AND":
            st.image("images/boolean_and.png", caption="Intersection (AND)", width=75)
        elif boolean_choice == "SUB":
            st.image("images/boolean_sub.png", caption="Subtraction (SUB)", width=75)
        elif boolean_choice == "XOR":
            st.image("images/boolean_xor.png", caption="Exclusive OR (XOR)", width=75)

        second_structure = st.text_input("Second Structure ID", max_chars=32)

        # add some validation logic before allowing button to be pressed
        can_add = (
            isinstance(orig_structure, str)
            and isinstance(target_structure, str)
            and isinstance(second_structure, str)
            and orig_structure.strip() != ""
            and target_structure.strip() != ""
            and second_structure.strip() != ""
            and boolean_choice in boolean_options
        )
        if not can_add:
            validation_errors.append("A boolean operator and all of original, target and second structures required.")
    elif chosen_command == "Copy":
        st.write("Note that this is only needed for explicit copy only actions.")
        st.write("All other commands automatically copy structures as required.")
        #copy_dicom_roi_options = get_roi_types()
        #copy_dicom_roi_choice = st.selectbox("Choose an ROI type", copy_dicom_roi_options, key="copy_dicom_roi")
        # validation
        can_add = (
            isinstance(orig_structure, str)
            and isinstance(target_structure, str)
            and orig_structure.strip() != ""
            and target_structure.strip() != ""
            #and copy_dicom_roi_choice in copy_dicom_roi_options
        )
        if not can_add:
            validation_errors.append("A DICOM ROI, original and target structure are required.")
    
    #can_add = (
     #   isinstance(orig_structure, str)
      #  and isinstance(target_structure, str)
       # and orig_structure.strip() != ""
        #and target_structure.strip() != ""
    #)
    if not can_add:
        for msg in validation_errors:
            st.warning(msg)
    
 

    # Submit button
    #submit = st.button("Add command")

    if st.button("Add command", disabled=not can_add):
        if chosen_command == "Margin for Structure":
            entry = build_margin_command(
                original_structure_id=orig_structure,
                output_structure_id=target_structure,
                symmetric=symmetric,
                margins=margins,
                outer_or_inner=outer_or_inner,
                margin_avoid_enabled=margin_avoid,
                avoid_structure_id=avoid_id
            )
        elif chosen_command == "Extract Wall":
            entry = build_extract_wall_command(
                original_structure_id=orig_structure,
                output_structure_id=target_structure,
                margins=[outer_wall_margin,inner_wall_margin]
            )
        elif chosen_command == "Crop":
            entry = build_crop_command(
                original_structure_id=orig_structure,
                output_structure_id=target_structure,
                outside_or_inside=crop_direction,
                crop_structure_id=crop_structure,
                additional_margin_enabled=crop_avoid,
                additional_margin=additional_margin
            )
        elif chosen_command == "Boolean":
            entry = build_bool_command(
                original_structure_id=orig_structure,
                output_structure_id=target_structure,
                second_structure_id=second_structure,
                operator=boolean_choice
            )
        elif chosen_command == "Copy":
            entry = build_copy_command(
                original_structure_id=orig_structure,
                output_structure_id=target_structure,
                dicom_roi_type=dicom_roi_choice
            )

        st.session_state.commands.append(entry)
        st.success(f"{chosen_command} command added.")
        #st.write(f"Command submitted: {chosen_command}")
        #if chosen_command == "Margin for Structure":
            #st.write("Margins:", margins)

    

    # make a place for queued commands
    st.divider()
    st.subheader("Queued Commands")
    if not st.session_state.commands:
        st.info("No commands added yet.")
    else:
        header = st.columns([1,7,1])
        header[0].write("No.")
        header[1].write("Command")
        header[2].write("")

        to_delete = None

        for i, cmd in enumerate(st.session_state.commands):
            cols = st.columns([1,7,1])

            #cols[1].write(cmd["command"])
            #cols[2].write(cmd.get("input_structure", ""))

            cols[0].write(i+1)
            #cols[1].write(cmd['readable_command'])
            cols[1].write(cmd.get("readable_command",""))
            if cols[2].button("X", key=f"del_{cmd['id']}"):
                to_delete = i

            if to_delete is not None:
                st.session_state.commands.pop(to_delete)
                st.rerun()
    # to develop further
    make_json = st.button("Make JSON File (in dev - disabled)", disabled=True)

with tab_plan:
    st.write("In development")