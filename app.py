from flask import Flask, render_template, Response, jsonify, request, send_file, stream_with_context, stream_template
import cv2

app = Flask(__name__, template_folder="website")
camera = cv2.VideoCapture(0)
Cascade = cv2.CascadeClassifier('fist.xml')
fistCoords = []
shape = []
xIntervals = []                                                                                         
yIntervals = []

# draws a grid on the camera to guide the user
def drawGrid(shape, frame):
    global xIntervals
    global yIntervals

    y = shape[0]
    x = shape[1]

    # 7x4

    yIntervals = []
    xIntervals = []

    yCounter = 0
    xCounter = 0

    for i in range(0,7):
        yIntervals.append(yCounter)
        yCounter = yCounter + y//4

        xIntervals.append(xCounter)
        xCounter = xCounter + x//7
    
    for i in xIntervals:
        cv2.line(frame, (i, 0), (i, y), (255,0,0), 2)

    for e in yIntervals:
        cv2.line(frame, (0, e), (x, e), (255,0,0), 2)


def getN():
    global xIntervals
    global yIntervals
    oct = "4"
    note = "C"

    if len(fistCoords) > 1:

        value = fistCoords[0]
        value2 = fistCoords[1]

        if (value > xIntervals[0] and value <= xIntervals[1]): oct = "3"
        if (value > xIntervals[1] and value <= xIntervals[2]): oct = "4"
        if (value > xIntervals[2] and value <= xIntervals[3]): oct = "5"
        if (value > xIntervals[3]): oct = "6"

        if (value2 > yIntervals[0] and value2 <= yIntervals[1]): note = "A"
        if (value2 > yIntervals[1] and value2 <= yIntervals[2]): note = "B"
        if (value2 > yIntervals[2] and value2 <= yIntervals[3]): note = "C"
        if (value2 > yIntervals[3] and value2 <= yIntervals[4]): note = "D"
        if (value2 > yIntervals[4] and value2 <= yIntervals[5]): note = "E"
        if (value2 > yIntervals[5] and value2 <= yIntervals[6]): note = "F"
        if (value2 > yIntervals[6]): note = "G"

    val = note + oct

    yield(val)

    return note + oct




def generate_frames():
    global fistCoords
    global shape
    while True:
        success, frame = camera.read() #read camera frame: return bool and frame
        if not success:
            break
        else:

            shape = frame.shape

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            fists = Cascade.detectMultiScale(gray, 1.1, 6) # 1.1,6 for fist

            for (x, y, w, h) in fists:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                fistCoords = [x + w/2, y + h/2] # location of the fist
            
            drawGrid(shape, frame)

            if len(fistCoords) > 1:
                cv2.putText(frame, "x: %s, y: %s" % (fistCoords[0], fistCoords[1]), (30,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(getN(), mimetype="text")


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame') #call a function to process

if __name__ == '__main__':
    app.run(debug=True)


