from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
)
from ragas import evaluate
from datasets import Dataset


import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("data/testset/synthetic_testset.csv")

# Convert the DataFrame to a dictionary format suitable for Dataset.from_dict()
data_samples = {
    'question': df['question'].tolist(),
    'contexts': df['contexts'].apply(eval).tolist(),  # Assuming 'context' column contains string representations of lists
    'ground_truth': df['ground_truth'].tolist(),
    'response': df['ground_truth'].tolist()
}

# Create a Hugging Face Dataset object
dataset = Dataset.from_dict(data_samples)

result = evaluate(
    dataset,
    metrics=[
        context_precision,
        faithfulness,
        answer_relevancy,
        context_recall,
    ],
)



print(result)