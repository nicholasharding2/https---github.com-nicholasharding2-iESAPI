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
        "OriginalID": "",
        "SecondID": "",
        "NewID": "",
        "ROIType": 0,
        "ReadableCmd": "",
        "Expand": False,
        "ValidIDs": False
    }

