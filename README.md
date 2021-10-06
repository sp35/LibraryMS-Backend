# LibraryMS-Backend

<h1>Setup (for Ubuntu and Mac):</h1>
<h3>Clone the repository</h3>
<pre>git clone https://github.com/sp35/LibraryMS-Backend.git</pre>
<h3>Make a new Virtual Environment</h3>
<pre>virtualenv -p python3 venv</pre>
<h3>Activating the Virtual Environment</h3>
<pre>source venv/bin/activate</pre>
<h3>Shifitng to the project repository</h3>
<pre>cd LibraryMS-Backend</pre>
<h3>Install the required modules</h3>
<pre>pip install -r utils/requirements.txt</pre>
<h3>Run the migrations and Synchronize the Database using</h3>
<pre>python manage.py migrate</pre>
<h3>Create a superuser</h3>
<pre>python manage.py createsuperuser</pre>
<h3>Run the server</h3>
<pre>python manage.py runserver</pre>
<h3>Now open up your browser at http://localhost:8000/ and the API is
hosted on your local setup.</h3>
