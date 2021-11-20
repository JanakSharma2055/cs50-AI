# CS50 Introduction to Artificial intelligence with Python

## Traffic
In this project we are supposed to write an AI to identify which traffic sign appears in a photograph.

We have used TensorFlow to build a neural network to classify road signs based on an image of those signs. For the dataset we are using the [German Traffic Sign Recognition Benchmark (GTSRB)](https://benchmark.ini.rub.de/?section=gtsrb&subsection=news) dataset, which contains thousands of images of 43 different kinds of road signs.

## Experimentation

### Model 1
Initially I applied **one** convolution layer with 28 filters and a kernel of size 3x3 , **one** max pooling layer of size 2x2, **one** hidden  dense layer of size 128 with 0.4 dropout.

   
```sh
Epoch 1/10
500/500 [==============================] - 5s 9ms/step - loss: 4.3437 - accuracy: 0.0672   
Epoch 2/10
500/500 [==============================] - 4s 9ms/step - loss: 3.5112 - accuracy: 0.0785
Epoch 3/10
500/500 [==============================] - 4s 9ms/step - loss: 3.4437 - accuracy: 0.0840
Epoch 4/10
500/500 [==============================] - 4s 9ms/step - loss: 3.1743 - accuracy: 0.1703
Epoch 5/10
500/500 [==============================] - 4s 9ms/step - loss: 2.6453 - accuracy: 0.2968
Epoch 6/10
500/500 [==============================] - 4s 8ms/step - loss: 2.0865 - accuracy: 0.4042
Epoch 7/10
500/500 [==============================] - 4s 9ms/step - loss: 1.7989 - accuracy: 0.4691
Epoch 8/10
500/500 [==============================] - 4s 8ms/step - loss: 1.6016 - accuracy: 0.5136
Epoch 9/10
500/500 [==============================] - 4s 8ms/step - loss: 1.4483 - accuracy: 0.5571
Epoch 10/10
500/500 [==============================] - 4s 8ms/step - loss: 1.3175 - accuracy: 0.6010
333/333 - 1s - loss: 0.8410 - accuracy: 0.7668
```
Clearly from the results we can make a conclusion that there is a very low accuracy and the accuracy on test set is greater than that of training set which might have happened because of underfitting.
### Model 2
I added one another convolution layer and a max pooling layer of same dimension as in model 1. Dropout percentage was set to 0.5 this time.
```sh
Epoch 1/10
500/500 [==============================] - 5s 10ms/step - loss: 3.0448 - accuracy: 0.3021
Epoch 2/10
500/500 [==============================] - 5s 9ms/step - loss: 1.3585 - accuracy: 0.5953
Epoch 3/10
500/500 [==============================] - 5s 9ms/step - loss: 0.8053 - accuracy: 0.7535
Epoch 4/10
500/500 [==============================] - 5s 9ms/step - loss: 0.5614 - accuracy: 0.8273
Epoch 5/10
500/500 [==============================] - 5s 9ms/step - loss: 0.4180 - accuracy: 0.8734
Epoch 6/10
500/500 [==============================] - 5s 9ms/step - loss: 0.3525 - accuracy: 0.8923
Epoch 7/10
500/500 [==============================] - 5s 9ms/step - loss: 0.2865 - accuracy: 0.9117
Epoch 8/10
500/500 [==============================] - 5s 9ms/step - loss: 0.2655 - accuracy: 0.9202
Epoch 9/10
500/500 [==============================] - 5s 9ms/step - loss: 0.2315 - accuracy: 0.9323
Epoch 10/10
500/500 [==============================] - 5s 9ms/step - loss: 0.2254 - accuracy: 0.9339
333/333 - 1s - loss: 0.1106 - accuracy: 0.9729
```
Clearly the accuracy has increased but still we can see some underfitting.

### Model 3
I added additional dense layer for this case with 68 units and a dropout of 0.4 
```sh
Epoch 1/10
500/500 [==============================] - 5s 10ms/step - loss: 3.5334 - accuracy: 0.2068
Epoch 2/10
500/500 [==============================] - 5s 9ms/step - loss: 1.9934 - accuracy: 0.4249
Epoch 3/10
500/500 [==============================] - 5s 10ms/step - loss: 1.5047 - accuracy: 0.5373
Epoch 4/10
500/500 [==============================] - 5s 10ms/step - loss: 1.2090 - accuracy: 0.6172
Epoch 5/10
500/500 [==============================] - 5s 9ms/step - loss: 1.0197 - accuracy: 0.6775
Epoch 6/10
500/500 [==============================] - 5s 9ms/step - loss: 0.8774 - accuracy: 0.7205
Epoch 7/10
500/500 [==============================] - 5s 10ms/step - loss: 0.7662 - accuracy: 0.7580
Epoch 8/10
500/500 [==============================] - 5s 10ms/step - loss: 0.6675 - accuracy: 0.7920
Epoch 9/10
500/500 [==============================] - 5s 10ms/step - loss: 0.6005 - accuracy: 0.8169
Epoch 10/10
500/500 [==============================] - 5s 10ms/step - loss: 0.5345 - accuracy: 0.8367
333/333 - 1s - loss: 0.2822 - accuracy: 0.9292
```
This has reduced our accuracy than that in model 2.

### Model 4
I removed the second dropout layer from model 3. Accuracy has increased doing so as shown below
```sh
Epoch 1/10
500/500 [==============================] - 5s 10ms/step - loss: 3.3400 - accuracy: 0.2340  
Epoch 2/10
500/500 [==============================] - 5s 9ms/step - loss: 1.5981 - accuracy: 0.5336
Epoch 3/10
500/500 [==============================] - 5s 9ms/step - loss: 1.0464 - accuracy: 0.6812
Epoch 4/10
500/500 [==============================] - 5s 9ms/step - loss: 0.7716 - accuracy: 0.7676
Epoch 5/10
500/500 [==============================] - 5s 9ms/step - loss: 0.6416 - accuracy: 0.8032
Epoch 6/10
500/500 [==============================] - 5s 9ms/step - loss: 0.5384 - accuracy: 0.8417
Epoch 7/10
500/500 [==============================] - 5s 10ms/step - loss: 0.4856 - accuracy: 0.8567
Epoch 8/10
500/500 [==============================] - 5s 10ms/step - loss: 0.3923 - accuracy: 0.8818
Epoch 9/10
500/500 [==============================] - 5s 10ms/step - loss: 0.3623 - accuracy: 0.8934
Epoch 10/10
500/500 [==============================] - 5s 10ms/step - loss: 0.3423 - accuracy: 0.9010
333/333 - 1s - loss: 0.1787 - accuracy: 0.9538
```
### Model 5
Removing second dense layer and the dropout , I increased the no of units in first dense layer.There was an increase in accuracy with increase in number of units.
```sh
Summary of model
------------------------
Model: "sequential"_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d (Conv2D)              (None, 28, 28, 28)        784       
_________________________________________________________________
max_pooling2d (MaxPooling2D) (None, 14, 14, 28)        0
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 12, 12, 28)        7084
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 6, 6, 28)          0
_________________________________________________________________
flatten (Flatten)            (None, 1008)              0
_________________________________________________________________
dense (Dense)                (None, 600)               605400
_________________________________________________________________
dropout (Dropout)            (None, 600)               0
_________________________________________________________________
dense_1 (Dense)              (None, 43)                25843
=================================================================
Total params: 639,111
Trainable params: 639,111
Non-trainable params: 0
```
The result is shown below
```sh
Epoch 1/10
500/500 [==============================] - 7s 13ms/step - loss: 2.9532 - accuracy: 0.4426  
Epoch 2/10
500/500 [==============================] - 6s 13ms/step - loss: 0.7581 - accuracy: 0.7851
Epoch 3/10
500/500 [==============================] - 6s 12ms/step - loss: 0.4793 - accuracy: 0.8650
Epoch 4/10
500/500 [==============================] - 6s 12ms/step - loss: 0.3730 - accuracy: 0.8957
Epoch 5/10
500/500 [==============================] - 6s 12ms/step - loss: 0.3176 - accuracy: 0.9108
Epoch 6/10
500/500 [==============================] - 6s 12ms/step - loss: 0.2794 - accuracy: 0.9194
Epoch 7/10
500/500 [==============================] - 6s 12ms/step - loss: 0.2676 - accuracy: 0.9241
Epoch 8/10
500/500 [==============================] - 6s 12ms/step - loss: 0.2338 - accuracy: 0.9362
Epoch 9/10
500/500 [==============================] - 6s 12ms/step - loss: 0.1938 - accuracy: 0.9470
Epoch 10/10
500/500 [==============================] - 6s 12ms/step - loss: 0.2142 - accuracy: 0.9426
333/333 - 1s - loss: 0.2162 - accuracy: 0.9462
```