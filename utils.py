import base64
from PIL import Image
from io import BytesIO

def array_image2base64(arr):
    pil_img = Image.fromarray(arr)
    buff = BytesIO()
    pil_img.save(buff, format="PNG")
    # Yes, its png. No jpeg is not better.
    return base64.b64encode(buff.getvalue())

def figure2base64(fig):
    buff = BytesIO()
    fig.savefig(buff, format="PNG")
    return base64.b64encode(buff.getvalue())
