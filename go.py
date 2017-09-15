#!/usr/bin/python -u

import csv
import datetime
import logging
import sys

from pkg_resources import resource_filename
from nupic.frameworks.opf.model_factory import ModelFactory

import model_params

_ANOMALY_THRESHOLD = 0.8


def createModel():
    return ModelFactory.create(model_params.MODEL_PARAMS)


def findAnomaly(input_filename):
    model = createModel()
    model.enableInference({'predictedField': 'flowout'})

    with open (input_filename) as fin:
        reader = csv.reader(fin)
        output_filename = input_filename + '.res'
        csvWriter = csv.writer(open(output_filename, "wb"))
        csvWriter.writerow(["timestamp", "flowout", "anomaly_score"])
        headers = reader.next()
        reader.next()
        reader.next()
        for i, record in enumerate(reader, start = 1):
            modelInput = dict(zip(headers, record))
            try:
                modelInput["flowout"] = float(modelInput["flowout"].strip())
                modelInput["timestamp"] = datetime.datetime.strptime(modelInput["timestamp"].strip(), "%Y/%m/%d %H:%M")
            except:
                continue
            result = model.run(modelInput)
            anomalyScore = result.inferences['anomalyScore']
            #anomalyLabel = result.inferences['anomalyLabel']
            csvWriter.writerow([modelInput["timestamp"], modelInput["flowout"], anomalyScore])

            if anomalyScore > _ANOMALY_THRESHOLD:
                print modelInput["timestamp"], anomalyScore



if __name__ == "__main__":
    for fname in sys.argv[1:]:
        findAnomaly(fname)

