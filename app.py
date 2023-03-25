from flask import Flask, render_template, Response, jsonify, request, send_file
import cv2

app = Flask(__name__, template_folder="website")
camera = cv2.VideoCapture(0)
Cascade = cv2.CascadeClassifier('fist.xml')
fistCoords = []
shape = []

# draws a grid on the camera to guide the user
def drawGrid(shape, frame):
    x = shape[0]
    y = shape[1]

    # 7x4

    yIntervals = []
    xIntervals = []

    yCounter = 0
    xCounter = 0

    for i in range(0,7):
        yIntervals.append(yCounter)
        yCounter = yCounter + y/7

        xIntervals.append(xCounter)
        xCounter = xCounter + x/4
    
    cv2.line(frame, (yIntervals[0],0), (yIntervals[0], y))
    cv2.line(frame, (yIntervals[1],0), (yIntervals[1], y))

    for i in yIntervals:
        cv2.line(frame, (i, 0), (i, y), (255,0,0), 2)

    for e in xIntervals:
        cv2.line(frame, (0, e), (x, e), (255,0,0), 2)



def generate_frames():
    global fistCoords
    global shape
    while True:
        success, frame = camera.read() #read camera frame: return bool and frame
        if not success:
            break
        else:

            shape = frame.shape()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            fists = Cascade.detectMultiScale(gray, 1.1, 6) # 1.1,6 for fist

            for (x, y, w, h) in fists:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                fistCoords = [x + w/2, y + h/2] # location of the fist
<<<<<<< Updated upstream
            
            cv2.putText(frame, str(fistCoords), (30,30))

            drawGrid(shape, frame)

=======
            if len(fistCoords) > 1:
                cv2.putText(frame, "x: %s, y: %s" % (fistCoords[0], fistCoords[1]), (30,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
>>>>>>> Stashed changes
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


