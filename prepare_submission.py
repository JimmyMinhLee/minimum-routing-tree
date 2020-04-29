import sys
import os
import json
from parse import validate_file

# Usage: python3 prepare_submission.py outputs/ submission.json
if __name__ == '__main__':
    outputs_dir = sys.argv[1]
    # print(outputs_dir)
    submission_name = sys.argv[2]
    # print(submission_name)
    submission = {}
    for input_path in os.listdir("inputs"):
        graph_name = input_path.split('.')[0]
        # print(graph_name)
        output_file = f'{outputs_dir}/{graph_name}.out'
        # print(output_file)
        if os.path.exists(output_file) and validate_file(output_file):
            output = open(f'{outputs_dir}/{graph_name}.out').read()
            submission[input_path] = output
    with open(submission_name, 'w') as f:
        f.write(json.dumps(submission))
