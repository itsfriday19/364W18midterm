# 364W18midterm

I used the News API for my project. My code allows the user to do two main things:
1. Click a button to get at most 20 articles/posts from live top and breaking news at the time of the search.
2. Enter a keyword, and have the app return a relevant article/post. Input that is less than 1 character will not validate.
All articles display the headline, the author, the publication date, a short description, the url, and the source publisher of the article/post.

The user is also prompted to enter their name on the main page to say hi to the app. Users can also see, in different views, which keywords they've already searched, previous articles they found with searching, and the top headlines. All pages can be navigated to from the navigation section at the top of every page.

routes:
http://localhost:5000/ --> index.html
http://localhost:5000/getTH --> top_headlines.html
http://localhost:5000/keywords --> keywords.html
http://localhost:5000/headlines --> top_headlines.html
http://localhost:5000/articles --> searched_articles.html


Requirements:

  **At least one errorhandler for a 404 error and a corresponding template.**    
  
  **Ensure that the SI364midterm.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up)**    
  
  **Add navigation in base.html with links (using a href tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, like this )**    
  
  **Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.**    
  
  **Include at least 2 additional template .html files we did not provide.** **At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.
        These could be in the same template, and could be 1 of the 2 additional template files.**
        
   **At least one errorhandler for a 404 error and a corresponding template.**
    
   **At least one request to a REST API that is based on data submitted in a WTForm.**    
   
   **At least one additional (not provided) WTForm that sends data with a GET request to a new page.**    
   
   **At least one additional (not provided) WTForm that sends data with a POST request to the same page.**    
   
   **At least one custom validator for a field in a WTForm.**    
   
   **At least 2 additional model classes.**        
   
   Have a one:many relationship that works properly built between 2 of your models.
   
   **Successfully save data to each table.**    
   
   **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).**    
   
   **Query data using an .all() method in at least one view function and send the results of that query to a template.**    
   
   **Include at least one use of redirect. (HINT: This should probably happen in the view function where data is posted...)**    
   
   **Include at least one use of url_for. (HINT: This could happen where you render a form...)**    
   
   **Have at least 3 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of base.html.)**

   **Project description in README**
  
Additional Requirements for an additional 200 points (to reach 100%) -- an app with extra functionality!    

(100 points) Include an additional model class (to make at least 4 total in the application) with at least 3 columns. Save data to it AND query data from it; use the data you query in a view-function, and as a result of querying that data, something should show up in a view. (The data itself should show up, OR the result of a request made with the data should show up.)

  **(100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will not save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3).**
