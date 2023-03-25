from flask import Flask, render_template, Response, jsonify, request, send_file
import cv2

app = Flask(__name__, template_folder="website")
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read() #read camera frame: return bool and frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame') #call a function to process

if __name__ == '__main__':
    app.run(debug=True)


