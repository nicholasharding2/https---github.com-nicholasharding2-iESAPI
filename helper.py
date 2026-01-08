import streamlit as st

def margin_group(base_key, labels, symmetric=False):
    vals = []

    top_val = st.number_input(
        labels[0],
        key=f"{base_key}_0",
        min_value=0.0,
        max_value=5.0,
        step=0.1,
        format="%0.1f",
    )
    vals.append(top_val)

    for i in range(1, len(labels)):
        if symmetric:
            st.number_input(
                labels[i],
                key=f"{base_key}_{i}",
                value=top_val,
                disabled=True,
                min_value=0.0,
                max_value=5.0,
                step=0.1,
                format="%0.1f",
            )
            vals.append(top_val)
        else:
            v = st.number_input(
                labels[i],
                key=f"{base_key}_{i}",
                min_value=0.0,
                max_value=5.0,
                step=0.1,
                format="%0.1f",
            )
            vals.append(v)

    return vals

def get_roi_types():


    dicom_roi_types = [
        "None",
        "GTV",
        "CTV",
        "PTV",
        "Avoidance",
        "Organ",
        "Treated Volume",
        "Irrad Volume",
        "Contrast Agent",
        "Cavity",
        "Support",
        "Fixation",
        "Dose Region",
        "Control",
        "Dose Measurement"
    ]
    return dicom_roi_types

def valid_roi(roi_type: str):
    return True if roi_type in get_roi_types() else False