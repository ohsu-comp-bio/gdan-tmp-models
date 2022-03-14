#!/usr/bin/env python

import os
import sys
import pickle
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--data", help='data to make subtype predictions')
parser.add_argument("--out", help="file to save predictions to")
parser.add_argument("--trained", nargs = '+',help="trained model pickle file")
args = parser.parse_args()

# data = sys.argv[1]
# out = sys.argv[2]
# models = sys.argv[3:]

feat=pd.read_csv(args.data, sep="\t", index_col=0)

out = {}
for model in args.trained:
    model_name = os.path.basename(model)
    obj = pickle.load(open(model, "rb"))
    X = feat[obj.feature_names_in_]

    labels = pd.Series(obj.predict(X), index=X.index, name="Labels")

    if hasattr(obj, "predict_proba"):
        for c, p in zip(obj.classes_, obj.predict_proba(X).T):
            out[model_name] = labels
            out["%s:%s" % (model_name, c)] = p
    else:
        out[model_name] = labels

df = pd.DataFrame(out)
if args.out == "-":
    df.to_csv(sys.stdout, sep="\t")
else:
    df.to_csv(args.out, sep="\t")
