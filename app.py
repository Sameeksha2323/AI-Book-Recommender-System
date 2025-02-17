from flask import Flask,render_template,request
import pickle
import numpy as np

books = pickle.load(open('Books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
popular_df = pickle.load(open('popular.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

def recommend_books(book_name):
    try:
        index_pos = np.where(pt.index == book_name)[0][0] # Directly get index, will error if not found
        similar_items = sorted(list(enumerate(similarity_scores[index_pos])), key=lambda x: x[1], reverse=True)[1:5]
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)
        return data
    except IndexError: # Catch IndexError if book is not in pt.index
        return "Book not available in the top rating database."

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    # user_input = request.form.get('user_input')
    # index = np.where(pt.index == user_input)[0][0]
    # similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    # data = []
    # for i in similar_items:
    #     item = []
    #     temp_df = books[books['Book-Title'] == pt.index[i[0]]]
    #     item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
    #     item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
    #     item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

    #     data.append(item)

    # print(data)

    # return render_template('recommend.html',data=data)
    user_input_book = request.form.get('user_input')
    recommendations_or_message = recommend_books(user_input_book) # Get either recommendations or message

    if isinstance(recommendations_or_message, str): # Check if it's the "not available" message
        return render_template('recommend.html', book_name=user_input_book, not_found_message=recommendations_or_message) # Pass message, empty top_books
    else:
        return render_template('recommend.html', book_name=user_input_book, recommendations=recommendations_or_message, not_found_message="")

if __name__ == '__main__':
    app.run(debug=True)