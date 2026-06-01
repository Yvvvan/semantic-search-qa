import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text

	

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3")
embeddings = tf.make_ndarray(tf.make_tensor_proto(embed(["können kleine Drachen Kerzen auspusten"]))).tolist()[0]

print(type(embeddings))

print(len(embeddings))

print(embeddings)
