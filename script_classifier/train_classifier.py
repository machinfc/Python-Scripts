## Last update: 23/08/2023
# This script works with the "data_train_classifier_2" folder for all Fluized and Compacted experiments. 
import random
from pathlib import Path

import numpy as np
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

from craterslab.classification import (
    NUM_CLASSES,
    get_trained_model,
    get_untrained_model,
    normalize,
    save_trained_model,
)
from craterslab.sensors import DepthMap


DATA_PATH = Path("data/data_train_classifier_2")

NUM_EPOCHS = 4
BATCH_SIZE = 2
LEARNING_RATE = 0.0001

SIMPLE_INDICIES = [1, 2, 3, 4, 5, 6, 7, 8, 26, 27, 29, 31, 35, 42, 43, 48, 49, 51]

# Define the categories and their corresponding file names and ids
categories = {
    "empty": {
        "files": [f'plane_{i}.npz' for i in range(1, 17)],
        "id": 0,
    },
    "simple_craters": {
        "files": [f'fluized_{i}.npz' for i in SIMPLE_INDICIES],
        "id": 1,
    },
    "complex_craters": {
        "files": [f'fluized_{i}.npz' for i in range(1, 52) if not i in SIMPLE_INDICIES]
        + [f'compacted_{i}.npz' for i in range(25, 50)],
        "id": 2,
    },
    "sand_mounds": {
        "files": [f'compacted_{i}.npz' for i in range(1, 25)],
        "id": 3,
    },
}


def regularize(dm: DepthMap) -> DepthMap:
    cropping_coin = random.random()
    if cropping_coin < 0.25:
        dm.crop_borders(ratio=cropping_coin)
    elif cropping_coin < 0.90:
        dm.auto_crop()
    if random.random() > 0.5:
        dm.map = dm.map.T
    return dm


# Preprocess images and labels
images = []
labels = []
for category, details in categories.items():
    for file in details["files"]:
        path = DATA_PATH / file
        dm = DepthMap.load(path)
        if details["id"]:
            dm = regularize(dm)
        img = normalize(dm.map, expand=False)
        images.append(img)
        labels.append(details["id"])

# Convert images and labels to numpy arrays
images = np.expand_dims(np.array(images), axis=-1)
labels = to_categorical(np.array(labels), num_classes=NUM_CLASSES)


# Split the data into train and test sets
train_images, test_images, train_labels, test_labels = train_test_split(
    images, labels, test_size=0.1
)

# Train and save the model
model = get_untrained_model(lr=LEARNING_RATE)
model.fit(train_images, train_labels, epochs=NUM_EPOCHS, batch_size=BATCH_SIZE)
save_trained_model(model)

# Load the model from the file
model = get_trained_model()

# Test the model on the test set
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f"Test set accuracy: {test_acc}")
