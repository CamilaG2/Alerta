import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
import os

# Esta función entrena un modelo para clasificar imágenes en 4 categorías
def entrenar_clasificador(data_dir="data/clasificador", modelo_salida="modelo_clasificador.h5", epochs=10):
    img_size = 224
    batch_size = 16

    # Generador de imágenes con aumento de datos y separación en entrenamiento/validación
    datagen = ImageDataGenerator(
        rescale=1./255,       # Normaliza los píxeles a valores entre 0 y 1
        validation_split=0.2  # 20% de las imágenes se usan para validación
    )

    # Carga las imágenes de entrenamiento desde carpetas
    train_gen = datagen.flow_from_directory(
        data_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    # Carga las imágenes de validación
    val_gen = datagen.flow_from_directory(
        data_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )

    # Usamos MobileNetV2 como base (modelo preentrenado con ImageNet)
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(img_size, img_size, 3))
    base_model.trainable = False  # No se entrena la base (solo las capas nuevas)

    # Añadimos las capas finales para nuestra clasificación personalizada
    x = base_model.output
    x = GlobalAveragePooling2D()(x)  # Reduce el tamaño de salida sin perder información
    predictions = Dense(len(train_gen.class_indices), activation='softmax')(x)  # Capa final con tantas clases como tengamos

    # Definimos el modelo completo
    model = Model(inputs=base_model.input, outputs=predictions)

    # Compilamos el modelo con optimizador Adam y función de pérdida para clasificación múltiple
    model.compile(optimizer=Adam(learning_rate=1e-4), loss='categorical_crossentropy', metrics=['accuracy'])

    # Entrenamos el modelo con los datos de entrenamiento y validación
    print("Entrenando modelo...")
    model.fit(train_gen, validation_data=val_gen, epochs=epochs)

    # Guardamos el modelo entrenado
    print(f"Guardando modelo en: {modelo_salida}")
    model.save(modelo_salida)

    return model
