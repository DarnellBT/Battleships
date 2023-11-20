from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    '''The main function injects elements for main.html. '''
    return "Hello event driven world"

if __name__ == '__main__':
    app.run()
