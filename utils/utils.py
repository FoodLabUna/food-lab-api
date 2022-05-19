import tflite_runtime.interpreter as tflite
from tflite.keras.models import Sequential
from tflite.keras.layers import Conv2D
from tflite.keras.layers import MaxPooling2D
from tflite.keras.layers import Flatten
from tflite.keras.layers import Dense
import numpy as np
#import tensorflow as tf
import config as conf


def validaImagem(nameImage):
    classifier = Sequential()
    # Passo 1 - Primeira Camada de Convolução
    classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))
    # Passo 2 - Pooling
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    # Adicionando a Segunda Camada de Convolução
    classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    # Passo 3 - Flattening
    classifier.add(Flatten())
    # Passo 4 - Full connection
    classifier.add(Dense(units = 128, activation = 'relu'))
    classifier.add(Dense(units = 1, activation = 'sigmoid'))
    # Compilando a rede
    classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy']) 
    # Criando os objetos train_datagen e validation_datagen com as regras de pré-processamento das imagens
    from keras.preprocessing.image import ImageDataGenerator
    train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

    validation_datagen = ImageDataGenerator(rescale = 1./255)

    # Pré-processamento das imagens de treino e validação
    training_set = train_datagen.flow_from_directory(conf.appDir+'/utils/data_set_fish/train',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

    validation_set = validation_datagen.flow_from_directory(conf.appDir+'/utils/data_set_fish/validation',
                                                        target_size = (64, 64),
                                                        batch_size = 32,
                                                        class_mode = 'binary')

    # Executando o treinamento (esse processo pode levar bastante tempo, dependendo do seu computador)
    history = classifier.fit(training_set,
                         steps_per_epoch = len(training_set),
                         epochs = 10,
                         validation_steps = len(validation_set))
    print (history)

  
   
    test_image = tflite.keras.preprocessing.image.load_img(nameImage, target_size = (64, 64))
    test_image = tflite.keras.preprocessing.image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = classifier.predict(test_image)
    training_set.class_indices
    
    prediction = ''
    
    if result[0][0] == 1:
        prediction = 'TILÁPIA'
    else:
        prediction = 'MERLUZA'


    return prediction,history.history['accuracy']