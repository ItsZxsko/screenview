from flask import Flask, Response, render_template_string, request, redirect, url_for
import pyautogui
import io
from PIL import Image
import uuid

app = Flask(__name__)

def capture_screen():
    screenshot = pyautogui.screenshot()
    img_io = io.BytesIO()
    screenshot.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return img_io

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Screen Viewer</title>
        </head>
        <body>
            <h1>Screen Viewer</h1>
            <form action="/create_room" method="post">
                <input type="submit" value="Create New Room">
            </form>
            <h2>Or enter Room ID</h2>
            <form action="/view" method="get">
                <input type="text" name="room_id" required>
                <input type="submit" value="Enter">
            </form>
        </body>
        </html>
    ''')

@app.route('/create_room', methods=['POST'])
def create_room():
    room_id = str(uuid.uuid4())
    return redirect(url_for('view', room_id=room_id))

@app.route('/view')
def view():
    room_id = request.args.get('room_id')
    if not room_id:
        return redirect(url_for('index'))
    
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Screen Viewer - Room {{ room_id }}</title>
            <style>
                body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                img { width: 90%; height: auto; }
            </style>
        </head>
        <body>
            <h1>Room ID: {{ room_id }}</h1>
            <img id="screenshot" src="/screenshot/{{ room_id }}" alt="Loading..."/>
            <script>
                function refreshImage() {
                    const img = document.getElementById('screenshot');
                    img.src = '/screenshot/{{ room_id }}?' + new Date().getTime();
                }
                setInterval(refreshImage, 1000);
            </script>
        </body>
        </html>
    ''', room_id=room_id)

@app.route('/screenshot/<room_id>')
def screenshot(room_id):
    img_io = capture_screen()
    return Response(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
