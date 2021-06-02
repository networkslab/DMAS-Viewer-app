import numpy as np
import argparse
import os
import json
import matplotlib.pyplot as pyplot
import context
from utils import array_image2base64, figure2base64
from flask import Flask, render_template, jsonify
from flask import request

import matplotlib
matplotlib.use("Agg")

app = Flask(__name__)


CONTEXT = None


@app.route("/get_image", methods=["GET"])
def get_image():
    value = request.args.get("slider_", 0, type=int)

    image = CONTEXT.dmas_image[:,:,value].copy()
    vmin = image.min()
    vmax = image.max()

    if CONTEXT.colored:
        dx = CONTEXT.colored_context.offset
        bounds_x = CONTEXT.colored_context.bounds_x
        bounds_y = CONTEXT.colored_context.bounds_y
        extent = [(bounds_y[0]+dx)* 100, (bounds_y[1] - dx)* 100, (bounds_x[1] - dx)* 100, (bounds_x[0] + dx)* 100]

        fig = pyplot.figure()
        pyplot.imshow(image, vmin=vmin, vmax=vmax, extent=extent, interpolation='none')
        pyplot.xticks([])
        pyplot.yticks([])
        # fig.tight_layout()
        pyplot.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        new_image_string = figure2base64(fig)
        pyplot.close(fig)
    else:
        image = image / vmax * 255
        image[image==vmin] = 255
        # for plain image array
        new_image_string = array_image2base64(image.astype(np.uint8))

    new_image_string = new_image_string.decode("utf-8")

    return jsonify(img=new_image_string)

@app.route("/", methods=["GET"])
def index():
    render_args = {
        "max_slider" : CONTEXT.dmas_image.shape[-1],
        "image_src": "/get_image",
        "image_width" : CONTEXT.image_width, #in persents of page size
        "image_height": CONTEXT.image_height, #in persents of page size,
    }
    return render_template("index.html",**render_args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DMAS Viewer.")
    parser.add_argument("--image", metavar="image", required=True, type=str,
                        help="path to DMAS image")
    parser.add_argument("--config", metavar="config", required=False, type=str,
                        default="./config.json", help="viewer JSON config")
    args = parser.parse_args()

    if not str.endswith(args.config,".json"):
        raise RuntimeError(f"Wrong config extension, *.json expected but *{os.path.splitext(args.config)[1]} given")
    if not os.path.isfile(args.config):
        raise RuntimeError("Config does not exist")

    with open(args.config,"r") as f:
        config = json.load(f)

    ## reading of array here
    if not str.endswith(args.image,".npy"):
        raise RuntimeError(f"Wrong DMAS image extension, *.npy expected but *{os.path.splitext(args.config)[1]} given")

    if not os.path.isfile(args.image):
        raise RuntimeError("DMAS voxel image does not exist.")

    image = np.load(args.image)

    if len(image.shape) != 3:
        raise RuntimeError("DMAS image should be three dimensional")


    CONTEXT = context.Context(image_width=config["image_width"],
                      image_height=config["image_height"],
                      dmas_image=image,
                      colored=config["colored"],
                      colored_context=context.ColoredContext(
                            offset=config["colored_details"]["offset"],
                            bounds_x=config["colored_details"]["bounds_x"],
                            bounds_y=config["colored_details"]["bounds_y"]
                      ))

    app.run()
