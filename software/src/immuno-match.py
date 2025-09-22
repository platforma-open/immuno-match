import argparse
from transformers import (
        RoFormerTokenizer,
        RoFormerForSequenceClassification,
        Trainer,TrainingArguments
    )

import pandas as pd

import torch
from datasets import load_dataset

from functools import partial

import warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore')

import os

# Define local model paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_MODEL_MAP = {
    "immunomatch-kappa": None,  # Will be set via command line args
    "immunomatch-lambda": None  # Will be set via command line args
}

# Functions for the calculation of the pairing score for batches of VH-VL

def preprocess_seq(example,hseqcol="input_Hseq",lseqcol="input_Lseq"):
    return {"input_Hseq":" ".join(list(example[hseqcol])), "input_Lseq":" ".join(list(example[lseqcol]))}

def tokenize_function(examples, tokenizer, hseqcol="input_Hseq",lseqcol="input_Lseq",max_length=256,return_tensors="pt"):
    return tokenizer(examples[hseqcol], examples[lseqcol], padding="max_length", truncation=True, max_length=max_length, return_tensors=return_tensors)

def tokenize_the_datasets(df_dir,hseq_col,lseq_col,tokenizer):
    """
    Tokenize the datasets
    args:input:
    df_dir: str, the directory of the dataset
    hseq_col: str, the column name of the heavy chain sequence
    lseq_col: str, the column name of the light chain sequence
    """
    df=pd.read_csv(df_dir)
    datasets=load_dataset("csv", data_files={"test":df_dir})
    tokenized_datasets=datasets.map(partial(preprocess_seq,hseqcol=hseq_col,lseqcol=lseq_col))
    tokenized_datasets=tokenized_datasets.map(partial(tokenize_function,tokenizer=tokenizer),batched=True)
    return df, tokenized_datasets

def pairing_scores_batches (df_dir,hseq_col,lseq_col,model_checkpoint):
  """
  Load the model and make the pairing prediction on batches of sequences
  args:input:
  df_dir: the directory of the csv files holding the sequences of pairs of VH and VL sequences
  hseq_col: the column name of the column of VH sequences
  lseq_col: the column name of the column of VL sequences
  model_checkpoint: the check point of the version of ImmunoMatch of your interest
  """

  tokenizer = RoFormerTokenizer.from_pretrained(model_checkpoint, local_files_only=True)
  model=RoFormerForSequenceClassification.from_pretrained(model_checkpoint, local_files_only=True)

  df,tokenized_datasets = tokenize_the_datasets (df_dir, hseq_col, lseq_col, tokenizer)

  batch_size=48
  args = TrainingArguments(
    f"tmp",
    evaluation_strategy = "no",
    save_strategy = "epoch",
    #learning_rate=2e-5,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    #num_train_epochs=5,
    #weight_decay=0.01,
    report_to="none"
    #load_best_model_at_end=True,
    #metric_for_best_model="accuracy",
    #push_to_hub=True,
  )

  trainer = Trainer(
            model,
            args,
            tokenizer=tokenizer,
            )
  pred_result=trainer.predict(tokenized_datasets["test"])

  pairing_scores=torch.nn.functional.softmax(torch.tensor(pred_result.predictions),dim=1)[:,1].tolist()
  df["pairing_scores"]=pairing_scores

  return df

def main():
    parser = argparse.ArgumentParser(description='Run ImmunoMatch predictions on antibody sequences')
    
    # Model directory arguments
    parser.add_argument('--kappa_dir', type=str,
                      required=True,
                      help='Directory path for the kappa model (mandatory)')
    parser.add_argument('--lambda_dir', type=str,
                      required=True,
                      help='Directory path for the lambda model (mandatory)')
    
    # Arguments for batch mode
    parser.add_argument('--input', type=str,
                      required=True,
                      help='Input CSV file containing antibody sequences')
    parser.add_argument('--hseq_col', type=str, default='VH',
                      help='Column name for heavy chain sequences (default: VH)')
    parser.add_argument('--lseq_col', type=str, default='VL',
                      help='Column name for light chain sequences (default: VL)')
    parser.add_argument('--ltype_col', type=str, default='locus',
                      help='Column name for light chain type (default: locus)')
    parser.add_argument('--output', type=str,
                      required=True,
                      help='Output CSV file for predictions')
    
    args = parser.parse_args()
    
    # Set model paths based on command line arguments
    LOCAL_MODEL_MAP["immunomatch-kappa"] = args.kappa_dir
    LOCAL_MODEL_MAP["immunomatch-lambda"] = args.lambda_dir
    
    # Verify model directories exist
    if not os.path.exists(LOCAL_MODEL_MAP["immunomatch-kappa"]) or not os.path.exists(LOCAL_MODEL_MAP["immunomatch-lambda"]):
        raise ValueError(f"Both kappa and lambda models must exist at their specified paths: {LOCAL_MODEL_MAP['immunomatch-kappa']} and {LOCAL_MODEL_MAP['immunomatch-lambda']}")
    
    data = pd.read_csv(args.input)
    results = []
    
    # Process kappa chains
    kappa_data = data.loc[data[args.ltype_col].apply(lambda x: "IGK" in x)]
    if len(kappa_data) > 0:
        k_data_dir = "kappa_data.csv"
        kappa_data.to_csv(k_data_dir, index=False)
        k_results = pairing_scores_batches(
            k_data_dir,
            args.hseq_col,
            args.lseq_col,
            LOCAL_MODEL_MAP["immunomatch-kappa"]
        )
        results.append(k_results)
        os.remove(k_data_dir)
    
    # Process lambda chains
    lambda_data = data.loc[data[args.ltype_col].apply(lambda x: "IGL" in x)]
    if len(lambda_data) > 0:
        l_data_dir = "lambda_data.csv"
        lambda_data.to_csv(l_data_dir, index=False)
        l_results = pairing_scores_batches(
            l_data_dir,
            args.hseq_col,
            args.lseq_col,
            LOCAL_MODEL_MAP["immunomatch-lambda"]
        )
        results.append(l_results)
        os.remove(l_data_dir)
    
    # Combine or use results as appropriate
    if not results:
        raise ValueError("No valid sequences found in input data. Ensure the locus column contains 'IGK' or 'IGL' values.")
    elif len(results) > 1:
        results_df = pd.concat(results).sort_index()
    else:
        results_df = results[0]
    
    # Save results
    results_df.to_csv(args.output, index=False)
    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()