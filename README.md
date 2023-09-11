# Craterslab Depth Maps and Data Analysis

This repository contains scripts for fetching depth maps of laboratory experiments from Kinect sensors for craterslab observables analysis.

## Scripts Overview

### Surface Type Correction
- **`surfaceTypeFixer.py`**: Corrects the SurfaceType for misclassifications caused by the "train_classifier.py" script and inaccurate ellipse fitting for individual files. It allows changing the number of points used for the ellipse fit and crop methods. It exports corrected observables for these two errors. It also corrects the surfaces in case of correct classification by the train_classifier.

### Data Analysis
- **`dataAnalyzer.py`**: Calculates observables from .npz files of laboratory experiments using craterslab. It can report incorrect crater Surface Type classifications or bad fitted ellipses. For this reason, it allows 2D and 3D visualization of the data to find poorly fitted ellipses that may report incorrect observables or identify potential incorrect Surface Type classifications. To correct these errors, please use `ellipseFixer.py` and `surfaceTypeFixer.py`.

- **`lrocAnalyzer.py`**: Calculates observables from .xyz files for lroc data using craterslab. It can report incorrect crater classifications or bad fitted ellipses. For this reason, it allows 2D and 3D visualization of the data to find poorly fitted ellipses that may report incorrect observables or identify potential incorrect surface classifications. To correct these errors, please use `lrocFixer.py`.

### Data Visualization
- **`visualization.py`**: Load a point cloud from an .xyz file containing data from lroc. Then, analyze the crater using craterslab functionalities. It can perform visualizations, profiles, fix bad ellipse fitting, correct wrongly Surface Type classification, print its observables, and export the crater's profile.

- **`profileExtractor.py`**: This script manually extracts a new profile, exports its distance and height values, and displays its slopes for a single file. If you need to calculate height and depth values for profiles automatically associated with slopes, please refer to lines 51-61 and 73-78.

- **`slopeCalculator.py`**: Calculates slopes automatically computed by craterslab. It enables 2D visualization and provides numerical values of slopes for visual error correction. For manual corrections of inaccurately computed slopes and profiles, obtained automatically, use `profileFixer.py`.

### Surface Type Correction for Multiple Files
- **`multiSurfaceTypeFixer.py`**: Corrects the SurfaceType for misclassifications by the "train_classifier.py" script for multiple files and exports their observables. Note that it does not correct bad fitted ellipses.

### Depth Map Visualization
- **`depthMapVisualizer.py`**: Load depth maps from files, compute an elliptical model, and plot the depth map together with the water model and its max profile. This script was used for exporting .eps graphs. It is important to note that water model visualization doesn't work for Sand Mounds.

- **`singleDepthMapVisualizer.py`**: This script is similar to the file `visualization.py`, but it only loads a single depth map from a file and plots it. It is important to note that water model visualization doesn't work for Sand Mounds.

## Usage

You can clone this repository and run the scripts mentioned above to analyze and correct depth maps obtained from Kinect sensors using craterslab.

For detailed usage instructions, please refer to the individual script files in the repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
