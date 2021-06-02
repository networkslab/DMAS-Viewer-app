# DMAS Viewer app

This is DMAS algorithm output visualizator for [Breats Cancer Detection Project](http://networks.ece.mcgill.ca/node/250).
DMAS implementation used in project is basically outputting three dimensional numpy arrays of floats in .npy format.

**Note:** for testing purposes real DMAS image can be replaced by any three dimensional numpy array.


## How to run

```python
python3 viewer_app.py --image <path_to_dmas_image>
```
This will run a server on [127.0.0.1:5000](http://127.0.0.1:5000/)

To customize a look of the viewer, you can specify a config:
```python
python3 viewer_app.py --image <path_to_dmas_image> --config <path_to_config>
```

## Requrements
* numpy
* matplotlib
* flask
