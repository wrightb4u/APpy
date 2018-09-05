from flask import render_template
import connexion

# create the application instance
app = connexion.App(__name__, specification_dir='./')

# Add the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

# Create a URL route to this resource
@app.route('/')

def home():
    """
    This function just responds to the browser URL localhost:8080/
    :return:    the rendered template 'home.html'
    """
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True,port=8080)

