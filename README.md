# scrapy_with_flask

# Usage
This app scrapes product details from  https://www.elcorteingles.es/ based on a url and tries to find the corresponding spanish google taxonomy category. It ouputs the result in the browser as json.

# Create and activate a virtual enviroment
virtualenv [name]
source [name]/bin/activate

# Install packages
pip install -r requirements.txt

# Steps to run the app
1) open 2 more terminals and activate the virtual enviroment on both of them.
2) from the first scraping directory run "scrapyrt"
3) from the the webapp directory run "FLASK_APP=example.py flask run"

# Run the app
open http://127.0.0.1:5000/ on the browser.
