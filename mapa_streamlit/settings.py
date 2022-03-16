DEFAULT_Z_OFFSET = 2
DEFAULT_Z_SCALE = 2.0


class ZOffsetSlider:
    label: str = "z-offset (in millimeter):"
    min_value: int = 0
    max_value: int = 20
    value: int = DEFAULT_Z_OFFSET


class ZScaleSlider:
    label: str = "z-scale (factor to be multiplied to the z-axis):"
    min_value: int = 0.0
    max_value: int = 5.0
    value: int = DEFAULT_Z_SCALE
