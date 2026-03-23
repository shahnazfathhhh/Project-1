from flask import Flask, render_template, Response
import cv2
import numpy as np
import tensorflow as tf
import datetime
import webbrowser

app = Flask(__name__)

# Load model CNN
model = tf.keras.models.load_model("finger_count_model.h5")
classes = ['0','1','2','3','4','5']

# Kamera
cap = cv2.VideoCapture(0)

# Preprocess frame
def preprocess_frame(frame):
    img = cv2.resize(frame, (128,128))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Fungsi aksi sesuai README
def perform_action(result):
    if result == '1':
        now = datetime.datetime.now()
        return f"Halo! {now.strftime('%H:%M:%S')}"
    
    elif result == '2':
        webbrowser.open("https://chat.openai.com")
        return "Membuka ChatGPT"
    
    elif result == '3':
        webbrowser.open("https://youtube.com")
        return "Membuka YouTube"
    
    elif result == '4':
        webbrowser.open("https://instagram.com")
        return "Membuka Instagram"
    
    else:
        return f"Jumlah jari: {result}"

# Streaming kamera
def generate_frames():
    last_action = ""
    last_time = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        # Prediksi
        img = preprocess_frame(frame)
        pred = model.predict(img, verbose=0)
        result = classes[np.argmax(pred)]

        # Hindari spam buka browser
        current_time = cv2.getTickCount() / cv2.getTickFrequency()
        if current_time - last_time > 3:  # delay 3 detik
            last_action = perform_action(result)
            last_time = current_time

        # Tampilkan teks
        cv2.putText(frame, f"Gesture: {result}",
                    (10,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2)

        cv2.putText(frame, last_action,
                    (10,80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255,0,0),
                    2)

        # Encode frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route utama
@app.route('/')
def index():
    return render_template('index.html')

# Route video stream
@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
