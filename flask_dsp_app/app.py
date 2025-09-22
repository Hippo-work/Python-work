from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def generate_constellation(bits):
    symbols = 2 * bits - 1 + 0.1 * np.random.randn(len(bits))
    fig, ax = plt.subplots()
    ax.plot(np.real(symbols), np.imag(symbols), 'o')
    ax.set_title("BPSK Constellation")
    ax.grid(True)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    image = None
    if request.method == 'POST':
        bit_count = int(request.form.get('bit_count', 100))
        bits = np.random.randint(0,2, bit_count)
        image = generate_constellation(bits)
    return render_template('index.html', image=image)

if __name__ == '__main__':
    app.run(debug=True)