import streamlit as st

def margin_group(
    key_prefix: str,
    labels: list[str],
    min_value: float = 0.0,
    max_value: float = 5.0,
    step: float = 0.1,
    sym_default: bool = True,
):
    """
    Creates six margin inputs with optional symmetry.
    
    Returns:
        List of six floats in the same order as labels.
    """

    # --- symmetry toggle ---
    sym_key = f"{key_prefix}_sym"
    sym = st.checkbox("Use symmetrical margin", value=sym_default, key=sym_key)

    # Generate 6 keys
    keys = [f"{key_prefix}_{i}" for i in range(6)]

    # Ensure keys exist BEFORE widgets are drawn
    for k in keys:
        st.session_state.setdefault(k, 0.0)

    # --- Apply mirroring BEFORE widget creation ---
    if sym:
        top = st.session_state[keys[0]]
        for k in keys[1:]:
            st.session_state[k] = top

    # --- Draw widgets ---
    for i, label in enumerate(labels):
        st.number_input(
            label,
            min_value=min_value,
            max_value=max_value,
            step=step,
            key=keys[i],
            disabled=(sym and i > 0),
            format="%0.1f",
        )

    # Return values in order
    return [st.session_state[k] for k in keys]
