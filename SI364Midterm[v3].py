###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
import os
import json
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, ValidationError # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required # Here, too
from flask_sqlalchemy import SQLAlchemy
import requests
import re

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = 'somecomplicatedstring'

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/364Midterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################


def get_or_create_TopHeadlines(db_session):
    name = "headline"
    h = db_session.query(TopHeadlines).filter_by(name = name).first()
    print ("HACKER VOICE: WE'RE IN THE TOP HEADLINES EXCEPT STATEMENT")
    baseURL = 'https://newsapi.org/v2/top-headlines?apiKey=06493a2b1faa481eb7ec3ecd48c85eda&country=us'
    response = requests.get(baseURL).json()['articles']
    # print (response.keys())
    # print (response["status"])
    # print (response["totalResults"])
    # print ("length: ",len(response))
    # print ("IS IT WORKING??")
    # print("YO, OVER HERE, OVER HERE MAN. This is where the NewsAPI info is supposed to be!")
    counter = 0
    for a in response:
        headline = a["title"]
        author = a["author"]
        pubdate = a["publishedAt"][0:10]
        description = a["description"]
        URL = a["url"]
        source = a["source"]["name"]
        print ("printing data...\n", "Headline:\n",headline, "\nAuthor:\n",author, "\nDate:\n",pubdate, "\nDescription:\n",description, "\nURL:\n",URL, "\nSource:\n",source)
        h = TopHeadlines(name= name, headline=headline, author=author, pubdate=pubdate, description=description, URL=URL, source=source)
        db.session.add(h)
        db.session.commit()
        counter += 1
        print ("has looped", counter, "\n---------------\n")

    # flash("Successfully added top headlines!")
    return redirect(url_for('top_headlines'))



def get_or_create_Article(db_session, keyword):
    h = db.session.query(Article).filter_by(name = keyword).first()
    baseURL = 'https://newsapi.org/v2/everything?apiKey=06493a2b1faa481eb7ec3ecd48c85eda&sortyBy=popularity&q={}'.format(keyword)
    response = requests.get(baseURL).json()['articles'][0]
    print ("get my search response now please", response)

    if h:
        # flash("Article already exists")
        return redirect(url_for('searched_articles'))
       
    else:
        headline = response["title"]
        author = response["author"]
        pubdate = response["publishedAt"][0:10]
        description = response["description"]
        URL = response["url"]
        source = response["source"]["name"]
        h = Article(name= keyword, headline=headline, author=author, pubdate=pubdate, description=description, URL=URL, source=source)
        db.session.add(h)
        db.session.commit()

        # flash('Successfully added article!')
        return redirect(url_for('searched_articles'))


# Error Handlers

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


##################
##### MODELS #####
##################


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer,primary_key=True)
    print ("This is now running the Article(db.Model) thing")
    name = db.Column(db.String(30), unique=True)
    author = db.Column(db.String(100))
    headline = db.Column(db.String(300))
    pubdate = db.Column(db.String(25))
    description = db.Column(db.String(500))
    URL = db.Column(db.String(500))
    source = db.Column(db.String(100)) #, db.ForeignKey("sources.id")) # take source from here

    def __repr__(self):
        return "Keyword: {} -- Headline: {} -- Source: {} -- Author: {} -- Published on {} -- Blurb: {} -- URL: {} -- (ID: {})".format(self.name, self.headline, self.source, self.author, self.pubdate, self.description, self.URL, self.id)


class TopHeadlines(db.Model):
    __tablename__ = "topH" # 2. table is not populating because get_or_create_TopHeadlines isn't being called
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    author = db.Column(db.String(100))
    headline = db.Column(db.String(300)) #, db.ForeignKey("sources.id")) # take headline from here, then match them in Source
    pubdate = db.Column(db.String(25))
    description = db.Column(db.String(500))
    URL = db.Column(db.String(350))
    source = db.Column(db.String(100))

    def __repr__(self):
        return "Headline: {} -- Source: {} -- Author: {} -- Published on {} -- Blurb: {} -- URL: {} -- (ID: {})".format(self.headline, self.source, self.author, self.pubdate, self.description, self.URL, self.id)

# class Source(db.Model): # combining the sources you searched with headlines from top headlines if the source exists there
#     __tablename__ = "sources"
#     id = db.Column(db.Integer, primary_key=True)
#     source = db.relationship('Article', backref='Source')
#     headline = db.relationship('TopHeadlines',backref='Source')


# class Movie(db.Model):
#     __tablename__ = "movies"
#     id = db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.String(64))
#     director_id = db.Column(db.Integer,db.ForeignKey("directors.id"))

# class Director(db.Model):
#     __tablename__ = "directors"
#     id = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(255))
#     movies = db.relationship('Movie',backref='Director') # building the relationship -- one director, many movies

    



###################
###### FORMS ######
###################

class ArticleSearchForm(FlaskForm):
    print ("this is the article search form")
    keyword = StringField("Enter keyword(s) longer than 1 character to search for an article: \n",validators=[Required("A keyword is required.")]) 

    def validate_keyword(self, field):
        if len(str(field.data)) <= 1:
            raise ValidationError('Enter a keyword longer than 1 character!')

    submit = SubmitField()



class TopHeadlinesForm(FlaskForm):
    print ("this is the TH form")
    submit = SubmitField()

class Icebreaker(FlaskForm):
    intro = StringField("Let's get to know each other a little bit before I start giving you articles willy nilly, I'm not that kinda gal you know. What's your name?", validators=[Required()])

    # def validate_intro(self, field):
    #     result = re.findall('[^a-zA-Z\s-]', field.data) # ^!@#$%&()+=1234567890/?<>~`\*
    #     print(field.data)
    #     print (result)
    #     if len(result) != 0:
    #         raise ValidationError('Names cannot have any numbers or special characters in them!')

    submit = SubmitField()



#######################
###### VIEW FXNS ######
#######################

@app.route('/', methods=['GET', 'POST'])
def search():
    form = ArticleSearchForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    form2 = Icebreaker()
    form3 = TopHeadlinesForm()
    print ("testing before if statement in search route")
    print ("Article Search Form: ", form)
    print ("Icebreaker: ", form2)
    if form2.validate_on_submit() and method == "POST":
        return redirect(url_for('search'))
    if form.validate_on_submit():
        name = form.keyword.data
        print("Len of name:  ", len(name))
        print("Type of name: ", type(name))
        print ("Name: ", name)
        print ("calling get_or_create_TopHeadlines")
        get_or_create_Article(db.session, name)
        return redirect(url_for('searched_articles'))

    else:
        flash("Enter a keyword longer than 1 character!")

    # if form3.validate_on_submit():
    #     get_or_create_TopHeadlines(db.session)
    #     return redirect(url_for('top_headlines'))
    # else:
    #     print ("Top headlines isn't grabbing anything")
    #     return redirect(url_for('search'))
    return render_template('index.html',form=form, form2=form2, form3=form3)

@app.route('/getTH', methods=['GET', 'POST'])
def getTop():
    form3 = TopHeadlinesForm()
    print ("TopHeadlinesForm: ", form3)
    if form3.validate(): # 3. is the form not validating on submit?
        get_or_create_TopHeadlines(db.session)
        return redirect(url_for('top_headlines'))
    else:
        print ("Top headlines isn't grabbing anything")
        return redirect(url_for('top_headlines'))
    return render_template('top_headlines.html', form3=form3)


@app.route('/keywords')
def all_keywords():
    lst = []
    names = Article.query.all()
    for n in names:
        lst.append((n.name, n.id))
    return render_template('keywords.html',names=lst)

@app.route('/headlines')
def top_headlines():
    headlines = TopHeadlines.query.all()
    print ("Headlines: ", headlines) # 1. this is empty because its trying to find info in the table
    return render_template('top_headlines.html', headlines=headlines)

@app.route('/articles')
def searched_articles():
    articles = Article.query.all()
    return render_template('searched_articles.html', articles=articles)


## Code to run the application...
if __name__ == "__main__":
    db.create_all()
    app.run(use_reloader=True,debug=True)

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
