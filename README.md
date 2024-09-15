# Cyber Security Project 1: RATE BEER!

LINK: link to the repository https://github.com/ollhaa/cs_project
#
Installation instructions if needed:

1) git clone git@github.com:ollhaa/cs_project.git
2) "python3 manage.py migrate"
3) Admin: admin1234 and passwors admin1234 for permission to add beers in Admin site. You can also create superuser by command "python manage.py createsuperuser" or just registerate by using "Register"

By command "python3 manage.py runserver" you can start the app.

#
Idea of application is that persons with admin rights are able to put different beers (perhaps from alko.fi) for registered users to evaluate.

### FLAW 1: SQL injection: 

exact source link pinpointing flaw: https://github.com/ollhaa/cs_project/blob/692da7820ee407712c4fe968ff68ee1aede31f23/myapp/beers/views.py#L128-L130
#
SQL injection is a security vulnerability that allows an unauthorized user to execute SQL queries against a database.
It can be exploited in any type of application (console, web, desktop, mobile). An application might be vulnerable to SQL injection when allowing the user to enter some data that is later included in a database query. [1]. 

The classic example is that user are able to add "DROP TABLES" to sql-query.
#
Here the problem is twofold. The code is the following: 
c = connection.cursor()
 c.executescript(f"INSERT INTO beers_review (beer_id, reviewer_id, review_text, stars, date_created) VALUES ('{beer}', '{user_id}', '{review}', '{stars}', {now})")
                    
First, command c.executescript allows more than one sql-querys. And secondly, based on [1], ...VALUES('{beer},... is not safe.          
#
how to fix it: https://github.com/ollhaa/cs_project/blob/692da7820ee407712c4fe968ff68ee1aede31f23/myapp/beers/views.py#L132-L134
Comment lines 129-130 of and lines 133-134 on.

new = Review(beer_id=beer, reviewer_id = user_id, stars=stars, date_created=now, review_text=review)
new.save()

We can solve the first one by using c.execute instead of executescript. There are several ways to solve the second one, but using the following: 
new = Review(beer_id=beer, reviewer_id = user_id, stars=stars, date_created=now, review_text=review)
new.save()

We can solve both by using the above. 

### FLAW 2: Cross-site scripting (XSS): 

exact source link pinpointing flaw 2: https://github.com/ollhaa/cs_project/blob/692da7820ee407712c4fe968ff68ee1aede31f23/myapp/beers/templates/beers/review.html#L30-L31
#
Cross-site scripting (XSS) vulnerabilities make it possible for the user to include malicious content to a site that will then be executed on the machine of another user. The malicious content may be permanently stored on the web application (e.g. in a database if the input and output is not sanitized), or it may be included temporarily (e.g. as a part of a query parameter). [2]. 

The good example of XSS is the following: "<script>alert("Hello!")</script>" This is not very bad but it can be something else too. In my app the possible place is when adding new review with comment. 
#
how to fix it: https://github.com/ollhaa/cs_project/blob/692da7820ee407712c4fe968ff68ee1aede31f23/myapp/beers/templates/beers/review.html#L28-L29
Comment lines 30-31 off and lines 28-29 on.

We can just erase |safe because excape is default in Django.

### FLAW 3: Cross-site Request Forgery (CSRF)

exact source link pinpointing flaw 3: 
https://github.com/ollhaa/cs_project/blob/90a34f0c8f6ad57d6600e17184ad9461505cc7b8/myapp/beers/templates/beers/beer.html#L22
https://github.com/ollhaa/cs_project/blob/692da7820ee407712c4fe968ff68ee1aede31f23/myapp/beers/views.py#L115
#
Cross-site Request Forgery (CSRF) makes it possible to create requests from another site (source) to the web application (target). If the user who is accessing the source site is authenticated to the target web application, the browser of the user will send an authentication token (e.g. cookie) with the request to the target application as the user is accessing the source site, making it possible to access data as an authenticated user that should not be accessible. [2]. 
#
how to fix it...
https://github.com/ollhaa/cs_project/blob/692da7820ee407712c4fe968ff68ee1aede31f23/myapp/beers/views.py#L115
Comment line 115 off. This should be enough because @csrf is default.
https://github.com/ollhaa/cs_project/blob/692da7820ee407712c4fe968ff68ee1aede31f23/myapp/beers/templates/beers/beer.html#L22
Comment line 22 on.

We also add @csrf tags to views with post and {% csrf_token %} to html templates. 

### FLAW 4: Identification and Authentication Failures:

exact source link pinpointing flaw 4: https://github.com/ollhaa/cs_project/blob/692da7820ee407712c4fe968ff68ee1aede31f23/myapp/myapp/settings.py#L92-L106
#
Broken Authentication vulnerabilities allow users to impersonate other users. This may happen, for example, through poor session management (session hijacking), through very poor passwords, or through storing the users' passwords in plain-text format (or in an easily decryptable format) and accidentally leaking the data. If the user uses the same password in multiple locations, it is also possible that the data from some other web application is leaked, and a malicious user is able to connect the username and password of another web application to this application. [2].
#
how to fix it... https://github.com/ollhaa/cs_project/blob/692da7820ee407712c4fe968ff68ee1aede31f23/myapp/myapp/settings.py#L92-L106
Comment lines 93-106 on
This is a bit artificial, but Django offers many attributes as a ready-make package. Without comments there are stronger requirements for passwords.

### FLAW 5: Broken access control:

exact source link pinpointing flaw 5: 
https://github.com/ollhaa/cs_project/blob/90a34f0c8f6ad57d6600e17184ad9461505cc7b8/myapp/beers/views.py#L95-L102
and https://github.com/ollhaa/cs_project/blob/90a34f0c8f6ad57d6600e17184ad9461505cc7b8/myapp/beers/views.py#L152-L162
#
Access control enforces policy such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized information disclosure, modification, or destruction of all data or performing a business function outside the user's limits. Common access control vulnerabilities include for example violation of the principle of least privilege or deny by default, where access should only be granted for particular capabilities, roles, or users, but is available to anyone. [3].

In my app i wanted that only registereted users with valid login are able add reviews and are able to see others reviews. 
#
how to fix it... 
https://github.com/ollhaa/cs_project/blob/692da7820ee407712c4fe968ff68ee1aede31f23/myapp/beers/views.py#L160-L173
and 
https://github.com/ollhaa/cs_project/blob/90a34f0c8f6ad57d6600e17184ad9461505cc7b8/myapp/beers/views.py#L103-L114
Comment lines 96-102 off and lines 103-114 on.
Comment lines 150-158 off and lines 164-176 on. 

First of all, there is the registeration and valid login. Without comments unlogged user is able to see reviews. 

### SOURCES: 

1. https://pythonassets.com/posts/reproducing-sql-injection-in-sqlite3-and-pymysql/
2. https://cybersecuritybase.mooc.fi/module-2.3/1-security
3. https://owasp.org/Top10/A01_2021-Broken_Access_Control/
4. https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
