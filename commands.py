import uuid

def build_margin_command(structure_id, symmetric, margins, outer_or_inner):
    """
    Build a clean schema entry for a margin command.

    structure_id: string (e.g. "CTV")
    symmetric: bool
    margins: list of 6 numbers [L, R, U, D, S, I]
    outer_or_inner: "outer" or "inner"
    """
    return {
        "id": str(uuid.uuid4()),
        "command": "margin",
        "input_structure": structure_id,
        "parameters": {
            "outer_or_inner": outer_or_inner,
            "symmetric": symmetric,
            "margins_cm": {
                "lat_left": margins[0],
                "lat_right": margins[1],
                "vert_up": margins[2],
                "vert_down": margins[3],
                "long_sup": margins[4],
                "long_inf": margins[5]
            }
        }
    }
