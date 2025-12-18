import streamlit as st

# local imports
from helper import margin_group
from commands import build_margin_command

# initilise commands once
if "commands" not in st.session_state:
    st.session_state.commands = []

st.title("Interactive ESAPI Automation Code Generator")

tab_structures, tab_plan = st.tabs(["Auto Structure", "Auto Plan"])

with tab_structures:
    st.header("Create list of structure generation commands")

    st.write("Define automation instruction")

    # Original structure ID
    orig_structure = st.text_input("Original Structure ID", max_chars=32, key = "original_id")
    
    # Command selection
    command_options = [
        "Margin for Structure",
        "Extract Wall",
        "Crop",
        "Boolean"
    ]
    chosen_command = st.selectbox("Choose a command", command_options)

    target_structure = st.text_input("Target Structure ID", max_chars=32, key = "target_id")

    if chosen_command == "Margin for Structure":
        # Geometry choice
        outer_or_inner = st.radio("Geometry [cm]", ["Create outer margin", "Create inner margin"])

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
    elif chosen_command == "Crop":
        crop_direction = st.radio("Remove part",["extending outside","extending inside"])
        crop_structure = st.text_input("Crop Fodder Structure ID", max_chars=32)
        additional_margin = st.number_input(
            "Additional margin (cm)",
            min_value=0.0,
            max_value=5.0,
            step=0.1,
            format="%0.1f",
            value=0.0
        )
    elif chosen_command == "Boolean":
        boolean_options = ["OR","AND","SUB","XOR"]
        boolean_choice = st.pills("Operator",boolean_options)
        second_structure = st.text_input("Second Structure ID", max_chars=32)
 

    # ✅ Submit button
    submit = st.button("Add command")

    if submit:
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

        st.session_state.commands.append(entry)
        st.success("Margin commands added.")
        #st.write(f"Command submitted: {chosen_command}")
        #if chosen_command == "Margin for Structure":
            #st.write("Margins:", margins)

    # to develop further
    make_json = st.button("Make JSON File", disabled=True)

    # make a place for queued commands
    st.divider()
    st.subheader("Queued Commands")
    if not st.session_state.commands:
        st.info("No commands added yet.")
    else:
        header = st.columns([1,2,3,3,1])
        header[0].write("No.")
        header[1].write("Command")
        header[2].write("Input")
        header[3].write("Output")
        header[4].write("")

        to_delete = None

        for i, cmd in enumerate(st.session_state.commands):
            cols = st.columns([1,5,1])

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

with tab_plan:
    st.write("In development")