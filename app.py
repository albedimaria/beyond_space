from flask import Flask, render_template, request, send_from_directory
import torch
import os
import time
from generate import get_rave_output, get_model_ratio_and_dim
import shutil

app = Flask(__name__)

model = None
model_path = ''
downsampling_ratio = None
latent_dim = 0

STATIC_FOLDER = os.path.join(os.getcwd(), 'static')
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

MODEL_FOLDER = os.path.join(os.getcwd(), 'models/')
if not os.path.exists(MODEL_FOLDER):
    os.makedirs(MODEL_FOLDER)
@app.route('/', methods=['GET'])
def index():
    return render_template(
        'index.html',
        message="Rave Latent Space Explorer",
        current_model=os.path.basename(model_path),
        latent_dim=latent_dim,
        mode='prior',
        scale=[1.0] * latent_dim if latent_dim > 0 else [],
        bias=[0.0] * latent_dim if latent_dim > 0 else []
    )

@app.route('/load_model', methods=['GET', 'POST'])
def load_model():
    global model, model_path, downsampling_ratio, latent_dim
    message = "Rave Latent Space Explorer"

    if request.method == 'POST':
        if 'model_file' in request.files:
            model_file = request.files['model_file']
            if model_file.filename != '':
                new_model_path = os.path.join(MODEL_FOLDER, model_file.filename)
                model_file.save(new_model_path)
                print(f"New model uploaded: {new_model_path}")

                try:
                    model = torch.jit.load(new_model_path)
                    downsampling_ratio, latent_dim = get_model_ratio_and_dim(model)
                    print(f"Downsampling ratio: {downsampling_ratio}, Latent dim: {latent_dim}")

                    model_path = new_model_path
                except Exception as e:
                    message = f"Error loading model: {str(e)}"

    return render_template(
        'index.html',
        message=message,
        current_model=os.path.basename(model_path),
        latent_dim=latent_dim,
        mode='encode',
        scale=[1.0] * latent_dim if latent_dim > 0 else [],
        bias=[0.0] * latent_dim if latent_dim > 0 else []
    )
@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    global model, downsampling_ratio, latent_dim
    mode = ''
    duration = None
    temperature = None
    input_file = ''
    output_file = 'output.wav'
    timestamp = int(time.time())  # Generate a unique timestamp
    scale = [1.0] * latent_dim if latent_dim > 0 else []
    bias = [0.0] * latent_dim if latent_dim > 0 else []
    noise_amount = float(request.form.get('noise_amount', 0.0))

    if model is None:
        return render_template(
            'index.html',
            message="No model loaded. Please load a model first.",
            current_model=os.path.basename(model_path),
            latent_dim=latent_dim,
            mode='prior',
            scale=scale,
            bias=bias,
            noise_amount=noise_amount
        )

    mode = request.form['mode']
    duration = float(request.form['duration']) if request.form['duration'] else None
    temperature = float(request.form['temperature']) if request.form['temperature'] else None
    input_file = request.form['input_file']
    output_file = request.form['output_file'] if request.form['output_file'] else 'output.wav'

    if latent_dim > 0:
        scale = [float(request.form.get(f'scale_{i}', 1.0)) for i in range(latent_dim)]
        bias = [float(request.form.get(f'bias_{i}', 0.0)) for i in range(latent_dim)]

    print(f"Mode: {mode}, Duration: {duration}, Temperature: {temperature}, Input: {input_file}, Output: {output_file}")
    print(f"Scale: {scale}")
    print(f"Bias: {bias}")
    print(f"Noise Amount: {noise_amount}")

    # Generate the output file
    get_rave_output(model, mode, duration, temperature, input_file, output_file, downsampling_ratio, scale, bias, noise_amount)

    # Move the output file to the static directory
    static_audio_path = os.path.join(STATIC_FOLDER, output_file)
    os.rename(output_file, static_audio_path)

    # Copy the input file to the static directory while preserving the directory structure
    if input_file and os.path.exists(input_file):
        # Get the relative path of the input file (relative to the working directory)
        relative_input_path = os.path.relpath(input_file, start=os.getcwd())
        
        # Construct the destination path in the static directory
        static_input_path = os.path.join(STATIC_FOLDER, relative_input_path)
        
        # Create the directory structure in the static folder if it doesn't exist
        os.makedirs(os.path.dirname(static_input_path), exist_ok=True)
        
        # Copy the file
        shutil.copy(input_file, static_input_path)
        
        # Update input_file to point to the static directory
        input_file = relative_input_path

    return render_template(
        'index.html',
        message='Rave Latent Space Explorer',
        audio_file=output_file,
        mode=mode,
        duration=duration,
        temperature=temperature,
        input_file=input_file,  # This now points to the file in the static directory
        output_file=output_file,
        timestamp=timestamp,
        current_model=os.path.basename(model_path),
        latent_dim=latent_dim,
        scale=scale,
        bias=bias,
        noise_amount=noise_amount
    )

@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory(STATIC_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
