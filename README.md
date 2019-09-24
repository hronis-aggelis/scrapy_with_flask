# scrapy_with_flask

# This app scrapes product details from  https://www.elcorteingles.es/ based on a url and tries to find the corresponding spanish google taxonomy category. It ouputs the result in the browser as json.

# create a virtual enviroment
virtualenv [name]

# activate the virtual enviroment
source [name]/bin/activate

# install packages
pip install -r requirements.txt

# open 2 more terminals and activate the virtual enviroment on both of them.

# go inside the first scraping directory and run the scrapyrt command.
scrapyrt

# go inside the webapp directory and run the flask app with the following command.
FLASK_APP=example.py flask run

# open http://127.0.0.1:5000/ on the browser.
