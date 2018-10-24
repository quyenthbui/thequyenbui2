from flask import *
from models.service import User, Song, Book, Video, Place, Contribution
import mlab
from standardize import ChuanHoa, ChuanHoa1
from random import*

app = Flask(__name__)
app.secret_key = "moody"
mlab.connect()

admin = User.objects(username="admin").first()
admin_id = str(admin["id"])

check_login = 0
check_delete = 0
check_contribute = 0
contributed = 0
happy_user = 1
count = 0

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html",
                            error_code = 404,
                            error_message = "Oops, page not found."), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("error.html",
                            error_code = 500,
                            error_message = "Oops, internal server error."), 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    return render_template("error.html",
                            error_code = 500,
                            error_message = "Oops, something went wrong."), 500

@app.route('/')
def index():
    global check_login
    check_login = 1
    global check_contribute
    check_contribute = 1
    global contributed
    user = None
    global count

    if contributed == 0:
        count += 1
    else:
        count = -6

    if "user_id" in session:
        user = User.objects.with_id(session["user_id"])
        return render_template('index.html', user = user, count = count)
    else:
        return render_template('index.html',user = user, count = count)

@app.route('/login', methods=['GET','POST'])
def login():
    if 'user_id' in session:
        flash("You have already logged in.")
        return render_template("404.html"), 404
    else:
        global check_login
        global happy_user
        error = None

        if request.method == "GET":
            return render_template('login.html')
        elif request.method == "POST":
            form = request.form
            username = form["username"]
            password = form["password"]

            acc = User.objects(username=username, password=password).first()
            if acc is None:
                error = 'Login failed. Try logging in again.'
                return render_template('login.html', error = error)
            else:
                session["user_id"] = str(acc["id"])
                if username == "admin":
                    flash("Hello Boss. Have a good day.")
                    return redirect(url_for('admin'))
                else:
                    flash('You were successfully logged in.')
                    if check_login == 1:
                        return redirect(url_for('index'))
                    elif check_login == 2:
                        return redirect(url_for('recommend',happy=happy_user))
                    if check_login == 3:
                        return redirect(url_for('contribute'))
                    else:
                        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if 'user_id' in session:
        del session['user_id']
        flash('Logged out!')
        return redirect(url_for('index'))
    else:
        flash('You have not logged in!')
        return render_template("404.html"), 404

@app.route('/signup', methods=['GET','POST'])
def signup():
    if 'user_id' in session:
        flash("You have already logged in. Try logging out before creating new account.")
        return render_template("404.html"), 404
    else:
        error = None
        if request.method == "GET":
            return render_template('signup.html')
        elif request.method == "POST":
            form = request.form
            f_user = User.objects(username = form['username'])
            f_user2 = User.objects(email = form['email'])

            if (form["fullname"] == "") or (form["username"] == "") or (form["password"] == "") or (form["email"] == ""):
                error = "Sign up failed. Try signing up again."
            elif f_user:
                error = "Username existed. Try another one."
            elif f_user2:
                error = "Email existed. Try another one."
            else:
                new_user = User(fullname=form["fullname"],
                                username=form["username"],
                                password=form["password"],
                                email=form["email"],
                                contributed = 0
                                )
                new_user.save()
                flash('You were successfully signed up.')
                return redirect(url_for('login'))
            return render_template('signup.html', error = error)

@app.route('/recommend/<int:happy>')
def recommend(happy):
    global admin_id
    global count
    global happy_user
    global check_login
    global check_contribute
    global contributed
    check_contribute = 2
    check_login = 2
    happy_user = happy
    user = None

    if contributed == 0:
        count += 1
    else:
        count = -6
    if "user_id" in session:
        user = User.objects.with_id(session["user_id"])

    all_song_admin = Song.objects(happy=happy, user_id=admin_id)
    song_admin = sample(set(all_song_admin),6)

    all_book_admin = Book.objects(happy=happy, user_id=admin_id)
    book_admin = sample(set(all_book_admin),2)

    all_video_admin = Video.objects(happy=happy, user_id=admin_id)
    video_admin = sample(set(all_video_admin),4)

    all_place_admin = Place.objects(happy=happy, user_id=admin_id)
    place_admin = choice(all_place_admin)
    name_place_admin = ChuanHoa1(place_admin["name"])

    if "user_id" in session:
        all_contribution = Contribution.objects(approved = True, happy = happy, user_id__ne=session["user_id"])
    else:
        all_contribution = Contribution.objects(approved = True, happy = happy)

    user_place = None
    user_contribution = None

    if (len(all_contribution) > 0):
        user_contribution = choice(all_contribution)
        user_place = ChuanHoa1(user_contribution.place["name"])

    return render_template('recommend.html', song_admin=song_admin,
                                             book_admin=book_admin,
                                             video_admin=video_admin,
                                             place_admin=place_admin,
                                             name_place_admin=name_place_admin,
                                             user=user,
                                             happy = happy,
                                             count = count,
                                             user_contribution = user_contribution,
                                             user_place = user_place)

@app.route('/contribute', methods=["GET", "POST"])
def contribute():
    global check_login
    global contributed
    check_login = 3
    error = None

    if  request.method == "GET":
        if "user_id" in session:
            user = User.objects.with_id(session["user_id"])
            return render_template("contribute.html", user=user)
        else:
            return redirect(url_for('login'))
    elif request.method == "POST":
        form = request.form
        f_img_song = form['link_img_song']
        f_img_book = form['link_img_book']
        f_img_video = form['link_img_video']

        if form['link_img_song'] == "":
            f_img_song = "https://sv1.uphinhnhanh.com/images/2018/05/10/music-player.png"
        if form['link_img_book'] == "":
            f_img_book = "https://sv1.uphinhnhanh.com/images/2018/05/10/notebook.png"
        if form['link_img_video'] == "":
            f_img_video = "https://sv1.uphinhnhanh.com/images/2018/05/10/default-video-image.png"
        new_song = Song(happy = form["happy_level"],
                        name = ChuanHoa(form["name_song"]),
                        author = ChuanHoa(form["author_song"]),
                        link = form["link_song"],
                        link_img = f_img_song,
                        user_id = session["user_id"])
        new_song.save()
        new_book = Book(happy = form["happy_level"],
                        name = ChuanHoa(form["name_book"]),
                        author = ChuanHoa(form["author_book"]),
                        link = form["link_book"],
                        link_img = f_img_book,
                        user_id = session["user_id"])
        new_book.save()
        new_video = Video(happy = form["happy_level"],
                        name = ChuanHoa(form["name_video"]),
                        author = ChuanHoa(form["author_video"]),
                        link = form["link_video"],
                        link_img = f_img_video,
                        user_id = session["user_id"])
        new_video.save()
        new_place = Place(happy = form["happy_level"],
                          name = ChuanHoa(form["name_place"]),
                          describe = form["cat_place"],
                          link = form["add_place"],
                          user_id = session["user_id"])
        new_place.save()
        new_contribution = Contribution(happy = form["happy_level"],
                                        song = new_song,
                                        video = new_video,
                                        book = new_book,
                                        place = new_place,
                                        user_id = session["user_id"],
                                        approved = False)
        new_contribution.save()
        contributed = 1

        # flash('Thanks for your contribution. Yours will be reviewed as soon as possible.')
        flash(Markup('Thanks for your contribution. Yours will be reviewed as \
        soon as possible. More? <a href="/contribute">Click here</a>'))

        if check_contribute == 1:
            return redirect(url_for('index'))
        elif check_contribute == 4:
            return redirect(url_for('personal'))
        elif check_contribute == 2:
            return redirect(url_for('recommend',happy=happy_user))
        else:
            return redirect(url_for('index'))

@app.route('/personal')
def personal():
    global check_delete
    global contributed
    global check_contribute
    global count
    check_delete = 1

    if contributed == 0:
        count += 1
    else:
        count = -6

    check_contribute = 4
    if "user_id" not in session:
        flash('Not found.')
        return render_template("404.html"), 404
    else:
        user = User.objects.with_id(session["user_id"])
        all_contribution = Contribution.objects(user_id = session["user_id"])
        return render_template("personal.html", user = user,
                                                all_contribution = all_contribution,
                                                length = len(all_contribution),
                                                count = count)

@app.route('/delete_contribution/<contribution_id>')
def delete_contribution(contribution_id):
    contribution = Contribution.objects.with_id(contribution_id)

    if contribution is None:
        flash("Something was wrong")
        return render_template("404.html"), 404
    else:
        contribution.delete()
        contribution.book.delete()
        contribution.song.delete()
        contribution.video.delete()
        contribution.place.delete()
        flash("Successfully deleted.")

        if check_delete == 1:
            return redirect(url_for('personal'))
        elif check_delete == 2:
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('index'))

@app.route('/admin')
def admin():
    global check_delete
    check_delete = 2

    if ("user_id" in session):
        user = User.objects.with_id(session["user_id"])
        if user.username == "admin":
            all_user = User.objects()
            length_user = len(all_user)
            length_contributed_user = len(User.objects(contributed__gt=0))
            length_user_contribution = len(Contribution.objects(approved = True))
            length_base = len(Book.objects()) + len(Video.objects()) + len(Song.objects()) + len(Place.objects())
            not_approved_contribution = Contribution.objects(approved = False)
            length = len(not_approved_contribution)

            return render_template("admin.html", user = user,
                                                all_user = all_user,
                                                not_approved_contribution = not_approved_contribution,
                                                length = length,
                                                length_user = length_user - 1,
                                                length_user_contribution = length_user_contribution,
                                                length_base = length_base,
                                                length_contributed_user = length_contributed_user)
        else:
            flash("You don't have permission to visit here. Get out!")
            return render_template("404.html"), 404
    else:
        return redirect(url_for('login'))

@app.route('/approve_contribution/<contribution_id>')
def approve_contribution(contribution_id):
    contribution = Contribution.objects.with_id(contribution_id)

    if contribution is None:
        flash("Something was wrong")
        return render_template("404.html"), 404
    else:
        contribution.update(set__approved=True)
        new_contributed = contribution.user_id.contributed + 1
        contribution.user_id.update(set__contributed = new_contributed)
        flash("Successfully approved.")
        return redirect(url_for('admin'))

@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    user = User.objects.with_id(user_id)
    all_contribution = Contribution.objects(user_id = user_id)
    if user is None:
        flash("Something was wrong")
        return render_template("404.html"), 404
    else:
        user.delete()
        if all_contribution:
            for contribution in all_contribution:
                contribution.delete()
                contribution.book.delete()
                contribution.song.delete()
                contribution.video.delete()
                contribution.place.delete()

        flash("Successfully deleted.")
        if check_delete == 1:
            return redirect(url_for('personal'))
        elif check_delete == 2:
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(debug=True)
