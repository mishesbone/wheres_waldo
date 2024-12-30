from flask import Flask, render_template, request, jsonify
import random
from PIL import Image, ImageDraw
import io
import time

app = Flask(__name__)

# List of anomalies (cybersecurity threats) for each level
anomalies = ["phishing", "spoofing", "denial_of_service", "insider_threat", "advanced_spoofing", "spear_phishing", "APT"]

# Basic "Waldo-like" figure drawing
def create_waldo(image, anomaly=None, level=1):
    draw = ImageDraw.Draw(image)
    
    # Basic Waldo figure (red-and-white striped shirt, hat, etc.)
    draw.rectangle([350, 250, 450, 350], fill="red")  # body
    draw.ellipse([375, 180, 425, 230], fill="peachpuff")  # face
    draw.line([400, 250, 400, 300], fill="red", width=3)  # legs
    draw.line([375, 250, 375, 300], fill="red", width=3)  # legs
    draw.line([425, 250, 425, 300], fill="red", width=3)  # legs
    
    # Add anomalies (threat actors) to the figure
    if anomaly:
        if anomaly == "phishing":
            draw.ellipse([390, 190, 410, 210], outline="blue", width=5)  # Phishing glasses
        elif anomaly == "spoofing":
            draw.line([375, 180, 425, 180], fill="green", width=5)  # Green hair for spoofing
        elif anomaly == "denial_of_service":
            draw.rectangle([340, 240, 460, 360], fill="purple")  # Overloaded objects for DoS
        elif anomaly == "insider_threat":
            draw.polygon([375, 160, 425, 160, 400, 140], fill="black")  # Hat for insider threat
        elif anomaly == "advanced_spoofing":
            draw.ellipse([370, 170, 430, 230], outline="yellow", width=3)  # Mismatched face for advanced spoofing
        elif anomaly == "spear_phishing":
            draw.line([400, 260, 400, 350], fill="yellow", width=5)  # Yellow rope symbolizing spear phishing
        elif anomaly == "APT":
            draw.rectangle([350, 240, 450, 360], fill="red")  # Anomalous alert for APT
    
    return image

# Main route to serve the game
@app.route('/')
def index():
    return render_template('index.html')

# Route to generate a game image
@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        level = int(request.form['level'])
        img = Image.new('RGB', (800, 600), color='white')
        anomaly = random.choice(anomalies[:level] + [None])  # Add random anomaly based on level
        img = create_waldo(img, anomaly, level)
        
        # Convert the image to a byte array and return it as a response
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue(), 200, {'Content-Type': 'image/png'}

    return 'Invalid request', 400

if __name__ == '__main__':
    app.run(debug=True)
