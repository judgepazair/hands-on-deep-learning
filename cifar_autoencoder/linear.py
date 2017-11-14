from keras.models import Model
from keras.layers import Input, Dense
from helpers import NeptuneCallback, load_cifar10, model_summary
from deepsense import neptune

ctx = neptune.Context()
ctx.tags.append('shallow')
encoding_dim = ctx.params['encoding_dim']

input_img = Input(shape=(32 * 32 * 3,))
x = input_img
encoded = Dense(encoding_dim, activation='relu')(x)
x = encoded
decoded = Dense(32 * 32 * 3, activation='sigmoid')(x)

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
model_summary(model)

# loading data
(x_train, y_train), (x_test, y_test) = load_cifar10()
x_train = x_train.reshape(-1, 32 * 32 * 3)
x_test = x_test.reshape(-1, 32 * 32 * 3)

# training
autoencoder.fit(x_train, x_train,
          epochs=50,
          batch_size=256,
          validation_data=(x_test, x_test),
          verbose=2,
          callbacks=[NeptuneCallback(x_test[:5])])
