"""
Will store all the functions corresponding to shapes which will be masked as
shapes in lottie
"""

import sys
import settings
import re
from helpers.transform import gen_helpers_transform
from helpers.blendMode import get_blend
from helpers.mask import gen_mask
from common.misc import get_color_hex, is_animated
from common.Count import Count
from effects.fill import gen_effects_fill
from synfig.group import get_additional_width, get_additional_height
sys.path.append("..")


def gen_layer_shape_solid(lottie, layer, idx):
    """
    Generates the dictionary corresponding to layers/shapes.json

    Args:
        lottie (dict)       : Lottie generated solid layer stored here
        layer  (common.Layer.Layer) : Synfig format solid layer
        idx    (int)        : Stores the index(number of) of solid layer

    Returns:
        (None)
    """
    layer.add_offset()

    # Setting the solid layer which will be masked
    index = Count()
    lottie["ddd"] = settings.DEFAULT_3D
    lottie["ind"] = idx
    lottie["ty"] = settings.LAYER_SOLID_TYPE
    lottie["nm"] = layer.get_description()
    lottie["sr"] = settings.LAYER_DEFAULT_STRETCH
    lottie["ks"] = {}   # Transform properties to be filled
    lottie["ef"] = []   # Stores the effects

    pos = [settings.lottie_format["w"]/2 + get_additional_width()/2,
           settings.lottie_format["h"]/2 + get_additional_height()/2]
    anchor = pos
    gen_helpers_transform(lottie["ks"], pos, anchor)

    lottie["ef"].append({})
    gen_effects_fill(lottie["ef"][-1], layer, index.inc())

    lottie["ao"] = settings.LAYER_DEFAULT_AUTO_ORIENT
    lottie["sw"] = settings.lottie_format["w"] + get_additional_width() # Solid Width
    lottie["sh"] = settings.lottie_format["h"] + get_additional_height() # Solid Height

    lottie["sc"] = get_color_hex(layer.get_param("color").get()[0])

    invert = False
    Inv = layer.get_param("invert").get()
    flag = False
    #So far only 'not' convert method seems to be supported for invert param in circle, will add more subsequently.
    if Inv is not None:
        if "bool" not in str(Inv[0]) and "animated" not in str(Inv[0]):
            is_animate = is_animated(Inv[0][0][0])
            flag = True
        else:
            is_animate = is_animated(Inv[0])
        if is_animate == settings.NOT_ANIMATED:
            if flag:
                val = "false"
                if Inv[0][0][0].attrib["value"] == "false":
                    val = "true"
            else:
                val = Inv[0].attrib["value"]
        elif is_animate == settings.SINGLE_WAYPOINT:
            if flag:
                val = "false"
                if Inv[0][0][0][0][0].attrib["value"] == "false":
                    val = "true"
            else:
                val = Inv[0][0][0].attrib["value"]
        else:
            # If animated, always set invert to false
            val = "false"
        if val == "true":
            invert = True

    # hackvars to change layer properties using layer names.
    # For example: a layer with the name: left_arm_-_ip_30 will init the at the 30th frame.
    if '_-_' in layer.get_description():
        hackvars = re.split('_',re.split('_-_',layer.get_description())[1])
        lottie["ip"] = 1 + int(hackvars[1]) #The +1 is needed to stop flashing.
    else:
        lottie["ip"] = settings.lottie_format["ip"]
    lottie["op"] = settings.lottie_format["op"]
    lottie["st"] = 0            # Don't know yet
    get_blend(lottie, layer)

    hasMask = True

    lottie["hasMask"] = hasMask
    lottie["masksProperties"] = []
    lottie["masksProperties"].append({})

    if layer.get_type() in {"star", "circle", "rectangle", "filled_rectangle"}:
        bline_point = layer
    else:
        bline_point = layer.get_param("bline", "vector_list")

    gen_mask(lottie["masksProperties"][0], invert, bline_point, index.inc())
