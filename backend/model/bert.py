# -*- coding: utf-8 -*-
"""BERT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xHEPTsiXqzSaw0z7SC5RiXZi6nLIcDuB
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import torch
from transformers import BertForQuestionAnswering,BertTokenizer, AdamW

from torch.utils.data import DataLoader, TensorDataset

data1 = pd.read_csv('/content/drive/MyDrive/medData/healthFC_annotated.csv')
data2=pd.read_csv('/content/drive/MyDrive/data/promptdata.csv')
context=pd.read_csv('/content/drive/MyDrive/medData/pubmed_landscape_abstracts.csv')

questions = data1['en_text'].tolist() + data2['en_text'].tolist()
answers= data1['en_studies'].tolist() + data2['en_studies'].tolist()
abstract_texts = context['AbstractText'].tolist()

# Initialize BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')

# Tokenize inputs and create input tensors
inputs = tokenizer(context, questions, truncation=True, padding=True, return_tensors="pt")
start_positions = torch.tensor([ans[1] for ans in answers])
end_positions = torch.tensor([ans[2] for ans in answers])
dataset = TensorDataset(inputs['input_ids'], inputs['attention_mask'], start_positions, end_positions)

# Split dataset into train and validation sets
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

# Define DataLoader for batch processing
train_dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=8)

# Setup optimizer and scheduler
optimizer = AdamW(model.parameters(), lr=5e-5)
total_steps = len(train_dataloader) * 3  # Number of batches * number of epochs
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=500, gamma=0.1)

# Training loop
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.train()

for epoch in range(3):  # Adjust num_train_epochs as needed
    for batch in train_dataloader:
        input_ids, attention_mask, start_positions, end_positions = batch
        input_ids, attention_mask = input_ids.to(device), attention_mask.to(device)
        start_positions, end_positions = start_positions.to(device), end_positions.to(device)

        outputs = model(input_ids, attention_mask=attention_mask, start_positions=start_positions, end_positions=end_positions)
        loss = outputs.loss

        # Backward pass
        loss.backward()
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()

# Evaluation loop (compute accuracy metrics like EM and F1 score)
model.eval()
for batch in val_dataloader:
    input_ids, attention_mask, start_positions, end_positions = batch
    input_ids, attention_mask = input_ids.to(device), attention_mask.to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        start_logits, end_logits = outputs.start_logits, outputs.end_logits
        # Compute metrics here (not implemented in this example)