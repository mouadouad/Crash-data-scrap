import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.keras.layers import Activation, Flatten, Dense, MaxPool2D, BatchNormalization, Conv2D
import os
from PIL import Image


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
'''
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (1,1,1)
            else:
                pixdata[x, y] = (0,0,0)
'''
def standard(img):
    img=np.array(img)
    new_array=[]
    for i in range(80):
        new_array.append([])
        for j in range(260):
            if (img[i][j] == np.array([255,255,255,255])).all() :
                new_array[i].append(1)

            else:
                new_array[i].append(0)
    return new_array


training_list = []
labels_list = []
for file in os.scandir("train"):
    img = Image.open("train/" + file.name)
    labels_list.append(float(file.name[:-4]))
    training_list.append(standard(img))

training_samples = np.array(training_list)
labels_samples = np.array(labels_list)
'''
model = Sequential([
    Conv2D(filters=32, kernel_size=(3,3), padding='same', activation='relu', input_shape=(80,260)),
    MaxPool2D(pool_size=(2,2), strides=2),
    Conv2D(filters=64, kernel_size=(3,3), padding='same', activation='relu'),
    MaxPool2D(pool_size=(2,2), strides=2),
    Flatten(),
    Dense(units=1, activation='relu')
])
'''
model = Sequential([
    Dense(units=100, input_shape=(80,260), activation=None),
    Flatten(),
    Dense(units=1, activation=None)
])

model.compile(optimizer=Adam(learning_rate=0.00001), loss='mse')
model.fit(x=training_samples, y=labels_samples, epochs=3000)
prediction = model.predict(x=np.array([standard(Image.open("test1.png")),standard(Image.open("test2.png")),standard(Image.open("test3.png"))]))
print(prediction)
model.save("model.h5")
