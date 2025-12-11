import streamlit as st

st.title("Interactive ESAPI Automation Code Generator")

tab_structures, tab_plan = st.tabs(["Auto Structure", "Auto Plan"])

with tab_structures:
    st.header("Create list of structure generation commands")


    st.write("Define automation instruction")

    # Original structure ID
    orig_structure = st.text_input("Original Structure ID", max_chars=32)
    target_structure = st.text_input("Target Structure ID", max_chars=32)

    # Command selection
    command_options = [
        "Margin for Structure",
        "Extract Wall",
        "Crop",
        "Boolean",
        "Boolean AND",
        "Boolean SUB",
        "Boolean OR",
        "Boolean XOR"
    ]
    chosen_command = st.selectbox("Choose a command", command_options)

    if chosen_command == "Margin for Structure":
        # Geometry choice
        st.radio("Geometry [cm]", ["Create outer margin", "Create inner margin"])

        # Symmetric checkbox
        sym_margin = st.checkbox("Use symmetrical margin", value=True)

         # Labels and keys
        margins_labels = [
            "Lat Left (cm)",
            "Lat Right (cm)",
            "Vert Up (cm)",
            "Vert Down (cm)",
            "Long Sup (cm)",
            "Long Inf (cm)"
        ]
        margins_keys = [
            "Margin X1", "Margin X2", "Margin Y1",
            "Margin Y2", "Margin Z1", "Margin Z2"
        ]

        # Determine initial values
        #top_val = float(st.session_state.get(margins_keys[0], 0.0))
        top_val = st.number_input(
            margins_labels[0],
            key = margins_keys[0],
            min_value=0.0,
            max_value=5.0,
            step=0.1,
            format="%0.1f",
            value=float(st.session_state.get(margins_keys[0], 0.0))
        )

        #if sym_margin:
         #   margins_values = [top_val] * 6
        #else:
            # Keep previous values if they exist
         #   margins_values = [float(st.session_state.get(k, 0.0)) for k in margins_keys]
         # if sym update other session state values before creating the widgets
        if sym_margin:
            for i in range(1,6):
                st.session_state[margins_keys[i]] = top_val
         

        # now Render remaining inputs
        for i in range(1,6):
            #value = top_val if sym_margin else float(st.session_state.get(margins_keys[i],0.0))
            st.number_input(
                margins_labels[i],
                key=margins_keys[i],
                value=float(st.session_state.get(margins_keys[i],0.0)),
                min_value=0.0,
                max_value=5.0,
                step=0.1,
                format="%0.1f",
                disabled=(sym_margin)
            )

        # Collect final margins
        final_margins = [st.session_state[k] for k in margins_keys]

        margin_avoid = st.checkbox("Avoid structure", key="Margin_Avoid")
        if not margin_avoid:
            # Original structure ID
            st.text_input("Avoid Structure ID", max_chars=32)


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
    submit = st.button("Run")

    if submit:
        st.write(f"Command submitted: {chosen_command}")
        if chosen_command == "Margin for Structure":
            st.write("Margins:", final_margins)

with tab_plan:
    st.write("In development")