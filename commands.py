import uuid

def build_margin_command(
    original_structure_id: str,
    output_structure_id: str,
    symmetric: bool,
    margins: list[float],
    outer_or_inner: str,
    margin_avoid_enabled: bool = False,
    avoid_structure_id: str = ""
)-> dict:
    """
    Build a schema entry for a Margin command.

    Parameters
    ----------
    original_structure_id : str
        Source structure ID
    output_structure_id : str
        Resulting structure ID
    symmetric : bool
        Whether margins are symmetric
    margins : list of 6 floats
        [lat_left, lat_right, vert_up, vert_down, long_sup, long_inf]
    outer_or_inner : str
        "outer" or "inner"
    margin_avoid_enabled : bool
        Whether margin avoid is used
    avoid_structure_id : string
        Structure ID to avoid if used (otherwise "")
    """
    # add validation
    if len(margins) !=6:
        raise ValueError("margins must be a list of six floats")
    
    if outer_or_inner not in ["outer","inner"]:
        raise ValueError("outer_or_inner must be 'outer' or 'inner'")
    
    lat_l, lat_r, vert_u, vert_d, long_s, long_i = margins

    if symmetric:
        readable = (
            f"Grow a symmetric {outer_or_inner} margin of"
            f"{lat_l:.1f} cm from {original_structure_id} into {output_structure_id}"
        )
    else:
        readable = (
            f"Grow asymmetric margin {outer_or_inner} margins"
            f"Lat L {lat_l:.1f}, Lat R {lat_r:.1f}"
            f"Vert U {vert_u:.1f}, Vert I {vert_d:.1f}"
            f"Long S {long_s:.1f}, Long I {long_i:.1f} cm"
            f"from {original_structure_id} into {output_structure_id}"
        )

    
    if margin_avoid_enabled:
        readable += f" avoiding {avoid_structure_id}."
    else:
        readable_command += "."
    
    return {
        "id": str(uuid.uuid4()),
        "command": "Margin",
        "input_structure": original_structure_id,
        "output_structure": output_structure_id,
        "readable_command":readable,
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
            },
            "margin_avoid_enabled": margin_avoid_enabled,
            "avoid_structure_id": avoid_structure_id if margin_avoid_enabled else ""
        }
    }

def build_old_command(
    
    original_structure_id: str,
    output_structure_id: str,
    symmetric: bool,
    margins: list[float],
    outer_or_inner: str,
    margin_avoid_enabled: bool = False,
    avoid_structure_id: str = ""
):
    """
    Build a schema entry for a generic command.

    Parameters
    ----------
    original_structure_id : str
        Source structure ID
    output_structure_id : str
        Resulting structure ID
    symmetric : bool
        Whether margins are symmetric
    margins : list of 6 floats
        [lat_left, lat_right, vert_up, vert_down, long_sup, long_inf]
    outer_or_inner : str
        "outer" or "inner"
    margin_avoid_enabled : bool
        Whether margin avoid is used
    avoid_structure_id : string
        Structure ID to avoid if used (otherwise "")
    """
    return {
        "id": str(uuid.uuid4()),
        "command": "margin",
        "input_structure": original_structure_id,
        "output_structure": output_structure_id,
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
            },
            "margin_avoid_enabled": margin_avoid_enabled,
            "avoid_structure_id": avoid_structure_id if margin_avoid_enabled else ""
        }
    }