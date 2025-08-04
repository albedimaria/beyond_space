"""
keep the suggested format

# 20 scaling / biasing
python generate.py --model nameModel.ts --mode encode --input_file nameInput.wav --noise 2.2 --scale 1.0 1.2 1.5 1.0 1.2 1.5 1.0 1.2 1.5 1.0 1.2 1.5 1.0 1.2 1.5 1.0 1.3 0.9 1.6 1.1 --bias 0.0 0.1 0.2 0.0 0.1 0.2 0.0 0.1 0.2 0.0 0.1 0.2 0.0 0.1 0.2 0.0 -0.1 0.05 -0.2 0.15 --output_file output.wav
"""

"""
scale = 1 and bias = 0 format

python gen_with_two_inputs.py --model organ.ts --mode encode --input_file1 test1.wav --input_file2 test2.wav --scale 1.0 --bias 0.0
"""