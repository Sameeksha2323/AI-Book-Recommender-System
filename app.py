from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    new_website_url = "https://ai-book-recommendation-project.onrender.com/"  # <--- REPLACE WITH YOUR ACTUAL NEW URL

    return render_template('index.html', new_website_url=new_website_url)

if __name__ == '__main__':
    app.run(debug=True)
