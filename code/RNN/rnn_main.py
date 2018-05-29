""" Recurrent Neural Network.
A Recurrent Neural Network (LSTM) implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits (http://yann.lecun.com/exdb/mnist/)
Links:
    [Long Short Term Memory](http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf)
    [MNIST Dataset](http://yann.lecun.com/exdb/mnist/).
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
"""

from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import os


# import data
def get_data():

    addrs = 404
    ids = 100
    days = 371
    addr_day = np.fromfile("addr_day.bin", dtype=np.float64)
    addr_day.shape = addrs, days
    addr_id = np.fromfile("addr_id.bin", dtype=np.float64)
    addr_id.shape = addrs, ids
    return addr_day, addr_id


def gen_data(x_data, y_data):

    permutation = np.random.permutation(y_data.shape[0])
    shuffled_dataset = x_data[permutation, :]
    shuffled_labels = y_data[permutation, :]
    return shuffled_dataset, shuffled_labels


def divide_data(x_data, y_data):

    train_data = x_data[:360, :]
    train_label = y_data[:360, :]
    test_data = x_data[360:, :]
    test_label = y_data[360:, :]
    return train_data, train_label, test_data, test_label


'''
To classify images using a recurrent neural network, we consider every image
row as a sequence of pixels. Because MNIST image shape is 28*28px, we will then
handle 28 sequences of 28 steps for every sample.
'''


# Training Parameters
learning_rate = 0.001
training_steps = 20000
batch_size = 40
display_step = 200

# Network Parameters
# num_input = 28 # MNIST data input (img shape: 28*28)
# timesteps = 28 # timesteps
# num_hidden = 128 # hidden layer num of features
# num_classes = 10 # MNIST total classes (0-9 digits)
num_input = 53 # BTN data input (shape: 365*1)
timesteps = 7 # timesteps, days of one year
num_hidden = 128 # hidden layer num of features
num_classes = 100 # BTN total classes (0-99 walletID)

# tf Graph input
X = tf.placeholder("float", [None, timesteps, num_input])
Y = tf.placeholder("float", [None, num_classes])

# Define weights
weights = {
    'out': tf.Variable(tf.random_normal([num_hidden, num_classes]))
}
biases = {
    'out': tf.Variable(tf.random_normal([num_classes]))
}


def RNN(x, weights, biases):

    # Prepare data shape to match `rnn` function requirements
    # Current data input shape: (batch_size, timesteps, n_input)
    # Required shape: 'timesteps' tensors list of shape (batch_size, n_input)

    # Unstack to get a list of 'timesteps' tensors of shape (batch_size, n_input)
    x = tf.unstack(x, timesteps, 1)

    # Define a lstm cell with tensorflow
    lstm_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)

    # Get lstm cell output
    outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

    # Linear activation, using rnn inner loop last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']


logits = RNN(X, weights, biases)
prediction = tf.nn.softmax(logits)

# Define loss and optimizer
loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=logits, labels=Y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

# Evaluate model (with test logits, for dropout to be disabled)
correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

x_data_ori, y_data_ori = get_data()
xx, yy = gen_data(x_data_ori, y_data_ori)
train_data, train_label, test_data, test_label \
    = divide_data(xx, yy)

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()

config = tf.ConfigProto()
config.gpu_options.allow_growth = True

saver = tf.train.Saver()
checkpoint_dir = "./model"

# Start training

with tf.Session(config=config) as sess:

    # Run the initializer
    sess.run(init)

    for step in range(1, training_steps+1):
        for i in range(9):
            batch_x = train_data[i*batch_size:(i+1)*batch_size, :]
            batch_y = train_label[i*batch_size:(i+1)*batch_size, :]
            # batch_x, batch_y = mnist.train.next_batch(batch_size)
            # Reshape data to get 28 seq of 28 elements
            batch_x = batch_x.reshape((batch_size, timesteps, num_input))
            # Run optimization op (backprop)
            sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})

        if step % display_step == 0 or step == 1:
            # Calculate batch loss and accuracy
            loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x,
                                                                 Y: batch_y})
            print("Step " + str(step) + ", Minibatch Loss= " + \
                  "{:.4f}".format(loss) + ", Training Accuracy= " + \
                  "{:.3f}".format(acc))

    print("Optimization Finished!")

    # Calculate accuracy for 128 mnist test images
    test_len = 44
    test_data = test_data.reshape((-1, timesteps, num_input))
    print("Testing Accuracy:", \
        sess.run(accuracy, feed_dict={X: test_data, Y: test_label}))
    checkpoint_path = os.path.join(checkpoint_dir, 'RNN_model.ckpt')
    saver.save(sess, checkpoint_path)