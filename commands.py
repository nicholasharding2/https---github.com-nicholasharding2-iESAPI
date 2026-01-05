import uuid
def build_copy_command(
    original_structure_id: str,
    output_structure_id: str,
    dicom_roi_type: str
)-> dict:
    """
    Build a schema entry for a Copy command.
    
    :param original_structure_id: Description
    :type original_structure_id: str
    :param output_structure_id: Description
    :type output_structure_id: str
    :param dicom_roi_type: Description
    :type dicom_roi_type: str
    :return: Description
    :rtype: dict
    """
    readable = f"Copy {original_structure_id} into {output_structure_id} with a ROI type of {dicom_roi_type}."
    return{
        "id": str(uuid.uuid4()),
        "command": "Copy",
        "input_structure": original_structure_id,
        "output_structure": output_structure_id,
        "dicom_roi_type": dicom_roi_type,
        "readable_command": readable
    }

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
            f"Grow a symmetric {outer_or_inner} margin of "
            f"{lat_l:.1f} cm from {original_structure_id} into {output_structure_id}"
        )
    else:
        readable = (
            f"Grow asymmetric {outer_or_inner} margins of "
            f"Lat L {lat_l:.1f}, Lat R {lat_r:.1f} "
            f"Vert U {vert_u:.1f}, Vert I {vert_d:.1f} "
            f"Long S {long_s:.1f}, Long I {long_i:.1f} (cm) "
            f"from {original_structure_id} into {output_structure_id}"
        )

    
    if margin_avoid_enabled:
        readable += f" avoiding {avoid_structure_id}."
    else:
        readable += "."
    
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

def build_extract_wall_command(
    original_structure_id: str,
    output_structure_id: str,
    margins: list[float],
)-> dict:
    """
    Build a schema entry for an Extract Wall command.

    Parameters
    ----------
    original_structure_id : str
        Source structure ID
    output_structure_id : str
        Resulting structure ID
    margins : list of 2 floats
        [outer_wall, inner_wall]
    """
    # validation
    if len(margins)!=2:
        raise ValueError("margins must have two floats")
    
    outer_margin, inner_margin = margins
    readable = (
        f"Extract a wall with outer margin {outer_margin:.1f} cm and "
        f"inner margin {inner_margin:.1f} cm from {original_structure_id} into {output_structure_id}."
    )

    return {
        "id": str(uuid.uuid4()),
        "command": "Extract Wall",
        "input_structure": original_structure_id,
        "output_structure": output_structure_id,
        "readable_command":readable,
        "parameters":{
            "margins_cm":{
                "outer_margin":outer_margin,
                "inner_margin":inner_margin
            }
        }
    }

def build_crop_command(
        original_structure_id: str,
        output_structure_id: str,
        outside_or_inside: str,
        crop_structure_id: str,
        additional_margin_enabled: bool=False,
        additional_margin: float=0.0
)->dict:
    """
    Build a schema entry for a Crop command
    
    Parameters
    ----------
    :param original_structure_id: Source structure ID
    :type original_structure_id: str
    :param output_structure_id: Output structure ID
    :type output_structure_id: str
    :param outside_or_inside: Crop part extending outside or inside crop structure
    :type outside_or_inside: str
    :param crop_structure_id: Structure to crop from
    :type crop_structure_id: str
    :param additional_margin: Additional margin to crop away from crop structure (cm)
    :type additional_margin: float
    :return: Description
    :rtype: dict
    """
    # add validation?
    
    if additional_margin_enabled:
        readable = (
            f"Crop structure {original_structure_id} "
            f"extending {outside_or_inside} {crop_structure_id} "
            f"with an additional margin of {additional_margin:.1f} cm "
            f"into {output_structure_id}."
        )
    else:
        readable = (
            f"Crop structure {original_structure_id} "
            f"extending {outside_or_inside} {crop_structure_id} "
            f"into {output_structure_id}."
        ) 
    
    return {
        "id": str(uuid.uuid4()),
        "command" : "Crop",
        "input_structure" : original_structure_id,
        "output_structure": output_structure_id,
        "crop_structure" : crop_structure_id,
        "outside_or_inside" : outside_or_inside,
        "additional margin_cm" : additional_margin,
        "readable_command" : readable

    }

def build_bool_command(
        original_structure_id : str,
        output_structure_id : str,
        second_structure_id : str,
        operator : str
)-> dict:
    """
    Build a schema entry for Boolean command

    Parameters
    ---------
    
    :param original_structure_id: First structure in operator
    :type original_structure_id: str
    :param output_structure_id: Target structure for operation
    :type output_structure_id: str
    :param second_structure_id: Second structure in operato
    :type second_structure_id: str
    :param operator: The boolean operator
    :type operator: str
    :return: Description
    :rtype: dict
    """
    # Validation
    # operator should be either OR, AND, SUB or XOR
    allowed_booleans = ["OR","AND","SUB","XOR"]

    if operator not in allowed_booleans:
        raise ValueError("The boolean operator must be OR, AND, SUB or XOR.")

    # make the readable
    if operator == "OR":
        readable = f"Create a union of {original_structure_id} and {second_structure_id} and put into {output_structure_id}."
    elif operator == "AND":
        readable = f"Keep the overlapping parts of {original_structure_id} and {second_structure_id} and put into {output_structure_id}."
    elif operator == "SUB":
        readable = f"Subtract {second_structure_id} from {original_structure_id} and put into {output_structure_id}"
    elif operator == "XOR":
        readable = f"Keep the non-overlapping parts of {original_structure_id} and {second_structure_id} and put into {output_structure_id}"

    return {
        "id" : str(uuid.uuid4()),
        "command" : "Crop",
        "first_input_structure" : original_structure_id,
        "second_input_structure" : second_structure_id,
        "output_structure" : output_structure_id,
        "boolean_operator" : operator,
        "readable_command" : readable
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