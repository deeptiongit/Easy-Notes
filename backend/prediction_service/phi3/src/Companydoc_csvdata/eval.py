import numpy as np
from datasets import load_metric
from sklearn.metrics import precision_recall_fscore_support

metric = load_metric("accuracy")
preds=[]

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    preds.append(eval_pred)
    # Compute precision, recall, and F1 score
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true=labels, y_pred=predictions, average='weighted')

    # Compute accuracy using the `accuracy` metric from the datasets library
    accuracy = metric.compute(predictions=predictions, references=labels)

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }



from transformers import Trainer

trainer = Trainer(
    model=model, 
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics
    
)