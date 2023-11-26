from flask import Flask, render_template, jsonify, request
import datetime
app = Flask(__name__)

def createBoard():
    return [[' ' for _ in range(7)] for _ in range(6)]

board = createBoard()

@app.route('/clear', methods=['POST'])
def clear():
    board.clear()
    board.extend(createBoard())

    return jsonify({'result': 'success'})

@app.route('/move', methods=['POST'])
def move():
    id = request.form.get('id')
    # Handle the move here
    parts = id.split('-')
    row = int(parts[0])
    col = int(parts[1])
    board[row][col] = 'X'
    
    return jsonify({'result': 'success'})


@app.route('/data')
def data():
    return jsonify(board)


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
