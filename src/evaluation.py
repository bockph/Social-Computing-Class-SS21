# Created by Edoardo Mosca
# For Social Computing/Social Gaming

from sklearn.metrics import f1_score
import keras.backend as K
from tensorflow import convert_to_tensor
import numpy as np

# Extract class with max predicted probability (predicted class)
def take_decisions(predictions):
    return np.argmax(predictions, axis=1)

# Calculates f1 score on test set
def f1_score_overall(y_test, y_pred, label_encoder, label_mapping, only_overall=True):
    
    y_pred = take_decisions(y_pred)
    y_true = label_encoder.inverse_transform(y_test)
    
    # if true we only pass back the overall f1_score and not per class
    if only_overall:
        overall_score = f1_score(y_true, y_pred, labels=[0,1,2], average='weighted')
        return convert_to_tensor(overall_score)
    
    class_scores = f1_score(y_true, y_pred, labels=[0,1,2], average=None)
    overall_score = f1_score(y_true, y_pred, labels=[0,1,2], average='weighted')
    print("F1 Scores:\n {}: {}\n {}: {}\n {}: {}\n Overall: {}"\
          .format(label_mapping[0], class_scores[0], label_mapping[1], class_scores[1], label_mapping[2], class_scores[2], overall_score))