from flask import Flask, render_template, Response, jsonify, request, send_file
import cv2

app = Flask(__name__, template_folder="website")
camera = cv2.VideoCapture(0)
Cascade = cv2.CascadeClassifier('fist.xml')
fistCoords = []

def generate_frames():
    global fistCoords
    while True:
        success, frame = camera.read() #read camera frame: return bool and frame
        if not success:
            break
        else:

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            fists = Cascade.detectMultiScale(gray, 1.1, 6) # 1.1,6 for fist

            for (x, y, w, h) in fists:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                fistCoords = [x + w/2, y + h/2] # location of the fist
            
            cv2.putText(frame, "x: %s, y: %s" % (fistCoords[0], fistCoords[1]))

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


