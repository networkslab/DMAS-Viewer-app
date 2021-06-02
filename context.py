from collections import namedtuple

Context = namedtuple("Context", ["image_width",
                                 "image_height",
                                 "dmas_image",
                                 "colored",
                                 "colored_context"])

ColoredContext = namedtuple("ColoredContext", ["offset",
                                               "bounds_x",
                                               "bounds_y"])