def empty_legacy_base(sequence: int) -> dict:
    """
    Base legacy command with all required fields present.
    """
    return {
        "CommandSequence": sequence,
        "Directive": 0,
        "UniformMargin": 0.0,
        "X1": 0.0,
        "X2": 0.0,
        "Y1": 0.0,
        "Y2": 0.0,
        "Z1": 0.0,
        "Z2": 0.0,
        "OriginalID": None,
        "SecondID": None,
        "NewID": None,
        "ROIType": 0,
        "ReadableCmd": "",
        "Expand": False,
        "ValidIDs": False
    }

def legacy_margin(cmd: dict, sequence: int) ->dict:
    base = empty_legacy_base(sequence)

    p = cmd["parameters"]
    margins = p["margins_cm"]

    # assess if outer or inner
    o_or_i = cmd["outer_or_inner"]
    expand = True if "outer" in o_or_i else False

    # Need to convert into mm for legacy

    # assess if symmetric
    symmetric = cmd["symmetric"]
    if symmetric:
        base.update({
            "UniformMargin" : margins[0] * 10
        })
    else:
        base.update({
            "X1" : margins["lat_left"] * 10,
            "X2" : margins["lat_right"] * 10,
            "Y1" : margins["vert_up"] * 10,
            "Y2" : margins["vert_down"] * 10,
            "Z1" : margins["long_sup"] * 10,
            "Z2" : margins["long_inf"] * 10,
        })

    base.update({
        "Directive":6,
        "OriginalID":cmd["input_structure"],
        "NewID": cmd["output_structure"],
        "ReadableCmd": cmd["readable_command"],
        "Expand": expand
    })