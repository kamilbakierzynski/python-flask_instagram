import random, time, datetime, os
import scripts.functions as functions
import scripts.file_management as file_management
from flask import Flask, render_template, request, url_for, flash, redirect, session

app = Flask(__name__)
app.secret_key = '49ee3b663dfa476d9e492011bc6bc03c'

@app.route("/")
def index():
    if 'username' in session:
        session.pop('username', None)
    data = ['How are you today?', 'Hope you have a great day!', 'Smile :)', 'Hi, I\'ve been waiting for you.', 'Oh. What a beautifull day!', 'Share your secrets with me ;)', 'Hey! Nice to see you!',
    'If you want to join the fun, you have to know a password!', 'Hola!', 'Do I know you from somewhere?', 'Yup, he forgot abot this field :/']
    random.shuffle(data)
    return render_template('login.html', label=data[0])


@app.route("/menu")
def menu():
    return render_template('menu.html')

@app.route("/login", methods=['GET', 'POST'])
def login_instagram_gui():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        functions.selenium_browser.init()
        succes = functions.instagram_login(username, password)
        if succes:
            return render_template('menu.html')
    return render_template('login.html')

@app.route("/follow_page")
def follow_page():
    return render_template('follow.html')

@app.route("/follow_acc", methods=['GET', 'POST'])
def follow_accounts():
    if 'people_to_unfollow_list' in session:
        session.pop('people_to_unfollow_list', None)
    if 'skip_above' in session:
        session.pop('skip_above', None)
    if 'people_to_keep' in session:
        session.pop('people_to_keep', None)
    if request.method == 'POST':
        hashtag = request.form['hashtag']

        if hashtag[0] == "#":
            hashtag = hashtag[1:]
            
        num_follows = request.form['num_follows']
        likes_also = False
        try:
            likes_also = request.form['likes_also']
            if likes_also == 'on':
                likes_also = True
        except:
            pass
        if hashtag == '':
            hashtag = 'f4f'
        followed_list = functions.follow_or_like_on_hashtag(hashtag, int(num_follows), likes_also)
        return render_template('success.html', acc_list=followed_list, title="Here is a list of accounts you've followed.")
    return render_template('follow.html')

@app.route("/unfollow_page")
def unfollow_page():
    return render_template('unfollow.html')

@app.route("/unfollow_acc", methods=['GET', 'POST'])
def unfollow_accounts():
    username = session.get('username', None)
    if request.method == 'POST':
        option = request.form['dropdown']
        if option == "1":
            people_to_unfollow = file_management.read_last_run()
            people_skipped = functions.unfollow_list(people_to_unfollow, '', 1000000000)
            return render_template('success.html', acc_list=people_skipped)
        skip_above = request.form['skip_above']
        follow_list, following_list = functions.scrape_for_followers_and_following(username)
        people_to_unfollow = functions.compare_for_unfollow(follow_list, following_list)
        people_to_keep = file_management.read_keep_following_list()
        people_not_in_list = functions.compare_with_keep_following(people_to_unfollow, people_to_keep)
        session['people_to_unfollow_list'] = people_not_in_list
        session['skip_above'] = skip_above
        session['people_to_keep'] = people_to_keep
        return redirect(url_for('unfollow_accounts_alert'))
    return render_template('unfollow.html')    

@app.route("/unfollow_acc_alert")
def unfollow_accounts_alert():
    if 'people_to_unfollow_list' in session:
        people_to_unfollow = session.get('people_to_unfollow_list', None)
    if len(people_to_unfollow) == 0:
        return render_template('success.html', acc_list=people_to_unfollow, title="Your account is clean.")
    return render_template('success_decision.html', acc_list=people_to_unfollow, title="Here is a list of accounts to unfollow")

@app.route('/unfollow_acc_list')
def unfollow_accounts_list():
    if 'people_to_unfollow_list' in session:
        people_to_unfollow = session.get('people_to_unfollow_list', None)
    if 'skip_above' in session:
        skip_above = session.get('skip_above', None)
    if 'people_to_keep' in session:
        people_to_keep = session.get('people_to_keep', None)
    people_skipped = functions.unfollow_list(people_to_unfollow, people_to_keep, int(skip_above)*1000)
    if len(people_skipped) == 0:
        return render_template('success.html', acc_list=people_skipped, title="No one was skipped.")
    return render_template('success.html', acc_list=people_skipped, title="You've skipped this accounts.")

@app.route('/save_list_unfollow')
def save_list_unfollow():
    if 'people_to_unfollow_list' in session:
        people_to_unfollow = session.get('people_to_unfollow_list', None)
    file_management.append_to_keep_following(people_to_unfollow)
    if 'people_to_unfollow_list' in session:
        session.pop('people_to_unfollow_list', None)
    if 'skip_above' in session:
        session.pop('skip_above', None)
    return redirect(url_for('menu'))

@app.route("/settings")
def settings_page():
    keep_following_list = file_management.read_keep_following_list()
    return render_template('settings.html', acc_list=keep_following_list)

@app.route("/save_list", methods=['GET', 'POST'])
def save_list():
    if request.method == 'POST':
        new_list = request.form['keep_following_list']
        formated_list = []
        output = ''
        for char in new_list:
            if char not in [' ', '\r', '\n']:
                output += char
            elif (char == ' ' or char == '\n') and output != '':
                formated_list.append(output)
                output = ''
        file_management.overwrite_keep_following(formated_list)
        flash('Saved')
        return redirect(url_for('settings_page'))

@app.route("/stats")
def stats_page():
    labels, values_followers, values_follows = file_management.display_stats()
    if len(labels) > 50:
        labels = labels[-50:]
        values_followers = values_followers[-50:]
        values_follows = values_follows[-50:]
    for index, value in enumerate(values_followers):
        if index == len(values_followers)-1:
            value = f"{value}"
        else:
            value = f"{value},"
    for index, value in enumerate(values_follows):
        if index == len(values_follows)-1:
            value = f"{value}"
        else:
            value = f"{value},"
    for index, label in enumerate(labels):
        label = datetime.datetime.fromtimestamp(int(label))
        label = str(label).split(' ')[0].split('-')
        label = f"{label[2]}.{label[1]}"
        if index == len(labels)-1:
            label = f"{label}"
        else:
            label = f"{label},"
    
    return render_template('stats.html', labels=labels, data_followers=values_followers, data_follows=values_follows)

@app.route('/get_likes')
def get_likes():
    username = session.get('username', None)
    _, pics, graph_data = functions.get_likes_from_photos(username)
 
    return render_template('stats_likes.html', labels=graph_data[0], values=graph_data[1], photo_count=len(pics))

@app.route('/like', methods=['GET', 'POST'])
def like_page():
    if request.method == 'POST':
        hashtag = request.form['hashtag']
        if hashtag[0] == "#":
            hashtag = hashtag[1:]
        num_likes = request.form['num_likes']
        if hashtag == '':
            hashtag = 'l4l'
        followed_list = functions.follow_or_like_on_hashtag(hashtag, int(num_likes), with_likes=True, with_follow=False)
        return render_template('success.html', acc_list=followed_list, title="Here is a list of accounts which photos you've liked.")
    return render_template('like.html')

@app.route('/photos')
def photos_page():
    username = session.get('username', None)
    pics, like_list = functions.get_likes_from_photos(username, details=False)
    preety_label = []
    for i in range(len(pics)):
        preety_label.append(f'Photo {i+1}')
    max_likes = -1
    index_max = 0
    for x in range(len(like_list)):
        if like_list[x] >= max_likes:
            max_likes = like_list[x]
            index_max = x
    functions.display_photo(username, index_max)
    return render_template('stats_photos.html', labels=preety_label, values=like_list)

@app.route('/about')
def about_page():
    return render_template('about.html')
  
@app.errorhandler(Exception)
def handle_exception(e):
    return render_template("error.html", e=e), 500

if __name__ == '__main__':
    app.run(debug=True)
    