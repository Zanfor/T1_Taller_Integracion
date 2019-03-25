from wtforms import Form, StringField

class SearchForm(Form):
	criteria = StringField("Texto a buscar")
	
