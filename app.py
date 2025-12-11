import streamlit as st

st.title("Interactive ESAPI Automation Code Generator")

tab_structures, tab_plan = st.tabs(["Auto Structure", "Auto Plan"])

with tab_structures:
    st.header("Create list of structure generation commands")
    st.form("autoStructureForm", clear_on_submit=True)
    with st.form("autoStructureForm"):
        st.write("Define automation instruction")
        
        # consider if want to limit max characters in text_input? Set at 32 
        # for no real reason other than to stop them being really long?
        # TG263 suggests 16 but I don't think Eclipse stops it
        st.text_input("Original Structure ID", max_chars=32)
        
        # now add a combo box to choose the type of command
        # potential options are: margin (uniform), margin (assymmetric), extract wall, crop, booleans
        # booleans are AND SUB OR XOR
        command_options = [
            "Margin for Structure",
            "Extract Wall",
            "Crop",
            "Boolean AND",
            "Boolean SUB",
            "Boolean OR",
            "Boolean XOR"
            ]
        chosen_command = st.selectbox("Choose a command", command_options)
        

        if chosen_command == "Margin for Structure":
            # st.write("Not implemented yet")
            st.radio("Geometry [cm]",["Create outer margin","Create inner margin"])
            sym_margin = st.checkbox("Use symmetrical margin", value=True)

            vals = []
            # keys list
            margins_keys = ["Margin X1","Margin X2","Margin Y1","Margin Y2","Margin Z1","Margin Z2"]
            margins_labels = [
                "Lat Left (cm)",
                "Lat right (cm)",
                "Vert up (cm)",
                "Vert down (cm)",
                "Long sup (cm)",
                "Long inf (cm)"
            ]
            # always render the six inputs
            for i in range(6):
                v = st.number_input(
                    margins_labels[i],
                    key = margins_keys[i],
                    min_value=0.0,
                    max_value=5.0,
                    value=float,
                    format="%0.1f",
                    step=0.1,
                    disabled=(sym_margin and i>0) # only top active in sym mode
                )
                vals.append(v)

            # if sym then force all six values to match the top
            if sym_margin:
                top = vals[0]
                for i in range(1,6):
                    st.session_state[margins_keys[i]] = top
            margins = [st.session_state[margins_keys[i] for i in range(6)]]





            #if (sym_margin):
             #   x1 = st.number_input("Lat Left (cm)", min_value=0.0, max_value=5.0, value=float, format="%0.1f", step=0.1, key="Margin x1")

            


        elif chosen_command == "Extract Wall":
            st.write("Not implemented yet")
        else:
            st.write("Not implemented yet.")




        # every form needs a submit button
        submitted = st.form_submit_button("Submit")
        if submitted:
            # TODO: pass stuff over here
            pass

with tab_plan:
    st.write("To be developed.")

