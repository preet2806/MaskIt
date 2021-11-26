
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import os
import pickle
from PIL import Image
import numpy as np

face_cascade= cv2.CascadeClassifier('C:\\Users\\Dinal Aloysius\\Desktop\\FaceMaskProject-SE\\Face-Mask-Detection\\cascades\\data\\haarcascade_frontalface_alt2.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids ={}
x_train= []
y_labels=[]

INIT_LR = 1e-4
EPOCHS = 5
BS = 32

dirc = r"C:\Users\Dinal Aloysius\Desktop\FaceMaskProject-SE\dataset"
ctgry = ["with_mask", "without_mask"]


#created list for storing photos and labelling them whether they are with mask or without mask.
d = []
l = []

for category in ctgry:
    path1 = os.path.join(dirc, category)
    for img in os.listdir(path1):
        if category == "without_mask":
            for root, dirs, files in os.walk(path1):
                for file in files:
                    if file.endswith("png") or file.endswith("jpg"):
                        path=os.path.join(root, file)
                        label =os.path.basename(root).replace(" ","-").lower()
                        if not label in label_ids:
                            label_ids[label]= current_id
                            current_id += 1
                        id_ = label_ids[label]
                        pil_image=Image.open(path).convert("L")
                        size = (550, 550)
                        final_image = pil_image.resize(size, Image.ANTIALIAS)
                        image = np.array(final_image, "uint8")
                        image = preprocess_input(image)
                        #print(image)
                        faces = face_cascade.detectMultiScale(image, scaleFactor=1.5, minNeighbors=5)

                        for (x,y,w,h) in faces:
                            roi = image[y:y+h, x:x+w]
                            d.append(roi)
                            y_labels.append(id_) 
                            l.append(category)   
        else:
    	    img_path = os.path.join(path1, img)
    	    image = load_img(img_path, target_size=(224, 224))
    	    image = img_to_array(image)
    	    image = preprocess_input(image)

    	    d.append(image)
    	    l.append(category)
            


lb = LabelBinarizer()
l = lb.fit_transform(l)
l = to_categorical(l)

d = np.array(d, dtype="float32")
l = np.array(l)

(trainX, testX, trainY, testY) = train_test_split(d, l,
	test_size=0.20, stratify=l, random_state=42)


ag = ImagedGenerator(
	rotation_range=20,
	zoom_range=0.15,
	width_shift_range=0.2,
	height_shift_range=0.2,
	shear_range=0.15,
	horizontal_flip=True,
	fill_mode="nearest")


basicModel = MobileNetV2(weights="imagenet", include_top=False,
	input_tensor=Input(shape=(224, 224, 3)))

headerModel = basicModel.output
headerModel = AveragePooling2D(pool_size=(7, 7))(headerModel)
headerModel = Flatten(name="flatten")(headerModel)
headerModel = Dense(128, activation="relu")(headerModel)
headerModel = Dropout(0.5)(headerModel)
headerModel = Dense(2, activation="softmax")(headerModel)


model = Model(inputs=basicModel.input, outputs=headerModel)


for layer in basicModel.layers:
	layer.trainable = False


#now I am compiling the model

opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])

#now we will train the model


H = model.fit(
	ag.flow(trainX, trainY, batch_size=BS),
	steps_per_epoch=len(trainX) // BS,
	validation_d=(testX, testY),
	validation_steps=len(testX) // BS,
	epochs=EPOCHS)


prediction = model.predict(testX, batch_size=BS)

prediction = np.argmax(prediction, axis=1)


print(classification_report(testY.argmax(axis=1), prediction,
	target_names=lb.classes_))



model.save("mask_detector.model", save_format="h5")

N = EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig("plot.png")