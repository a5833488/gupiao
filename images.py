import tensorflow as tf
import os
import numpy as np
import re
from PIL import Image
import matplotlib.pyplot as plt

lines = tf.gfile.GFile('pbs/output_labels.txt').readlines()
uid_to_human = {}
ss = []
for uid,line in enumerate(lines):
    line = line.strip('\n')
    uid_to_human[uid] = line

def id_to_string(node_id):
    if node_id not  in uid_to_human:
        return ''
    return uid_to_human[node_id]

def text_save(content,filename,mode='a'):
    # Try to save a list variable in txt file.
    file = open(filename,mode)
    for i in range(len(content)):
        file.write(str(content[i])+'\n')
    file.close()

with tf.gfile.FastGFile('pbs/output_graph.pb','rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def,name='')

with tf.Session() as sess:
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    for root,dirs,files in os.walk('images/'):
        for file in files:
            image_data = tf.gfile.FastGFile(os.path.join(root,file),'rb').read()
            predic = sess.run(softmax_tensor,{'DecodeJpeg/contents:0':image_data})
            predic = np.squeeze(predic)
            top_k = predic.argsort()[::-1]

            image_path = os.path.join(root,file)
            print(image_path)
            img = Image.open(image_path)

            plt.imshow(img)
            plt.axis('off')
            # plt.show()
            top_k = predic.argsort()[::-1]
            for node_id in top_k:
                humann_string = id_to_string(node_id)
                score = predic[node_id]
                submit = os.path.split(file)[-1] + "\t" + humann_string.upper()
                ss.append(submit)
                # print(submit)
                print('%s(score=%0.5f)' % (humann_string, score))
            plt.show()


                # break
            # print('%s(score=%0.5f)'%(humann_string,score))

# text_save(ss,'ssud.txt')