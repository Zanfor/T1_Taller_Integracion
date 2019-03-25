from flask import Flask, request
from flask import render_template
import requests
import json
import forms

def parse(peli):
	return [peli["title"], peli["release_date"][:4], peli["director"], peli["producer"], peli["episode_id"], peli["url"].split("/")[-2]]

def superparse(peli):
	personajes = list()
	planetas = list()
	naves = list()
	char = peli["characters"]
	pla = peli["planets"]
	nav = peli["starships"]
	for c in char:
		personaje = requests.get(c).json()["name"]
		personajes.append([personaje, c.split("/")[-2]])
	for p in pla:
		planeta = requests.get(p).json()["name"]
		planetas.append([planeta, p.split("/")[-2]])
	for n in nav:
		nave = requests.get(n).json()["name"]
		naves.append([nave, n.split("/")[-2]])
	return [peli["title"], peli["release_date"], peli["director"], peli["producer"], peli["episode_id"], personajes, planetas, naves]

def perparse(per):
	naves = list()
	peliculas = list()
	nav = per["starships"]
	pel = per["films"]
	pla = per["homeworld"]
	for n in nav:
		nave = requests.get(n).json()["name"]
		naves.append([nave, n.split("/")[-2]])
	for p in pel:
		pelicula = requests.get(p).json()["title"]
		peliculas.append([pelicula, p.split("/")[-2]])
	planeta = [requests.get(pla).json()["name"], pla.split("/")[-2]]
	seelf = [per["name"], per["url"].split("/")[-2]]

	return [per["name"], per["height"], per["mass"], per["hair_color"], per ["skin_color"], per ["eye_color"], per["birth_year"], per["gender"], planeta, peliculas, naves, seelf]

def planparse(plan):
	peliculas = list()
	pel = plan["films"]
	personajes = list()
	char = plan["residents"]
	for c in char:
		personaje = requests.get(c).json()["name"]
		personajes.append([personaje, c.split("/")[-2]])
	for p in pel:
		pelicula = requests.get(p).json()["title"]
		peliculas.append([pelicula, p.split("/")[-2]])
	seelf = [plan["name"], plan["url"].split("/")[-2]]
	return [plan["name"], plan["rotation_period"], plan["orbital_period"], plan["diameter"], plan["climate"], plan["gravity"], plan["terrain"], plan["surface_water"], plan["population"], personajes, peliculas, seelf]

def navparse(nav):
	peliculas = list()
	pel = nav["films"]
	for p in pel:
		pelicula = requests.get(p).json()["title"]
		peliculas.append([pelicula, p.split("/")[-2]])
	personajes = list()
	char = nav["pilots"]
	for c in char:
		personaje = requests.get(c).json()["name"]
		personajes.append([personaje, c.split("/")[-2]])
	seelf = [nav["name"], nav["url"].split("/")[-2]]
	return [nav["name"], nav["model"], nav["manufacturer"], nav["cost_in_credits"], nav["length"], nav["max_atmosphering_speed"], nav["crew"], nav["passengers"], nav["cargo_capacity"], nav["consumables"], nav["hyperdrive_rating"], nav["MGLT"], nav["starship_class"], personajes, peliculas, seelf]

app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def hello():
	search_form = forms.SearchForm(request.form)
	if request.method == "POST":
		peliculas = requests.get("https://swapi.co/api/films/?search={}".format(search_form.criteria.data))
		json_pelis = peliculas.json()
		peliculas = json_pelis["results"]
		peliculas_2 = list()
		for peli in peliculas:
			peliculas_2.append(parse(peli))
		personajes = requests.get("https://swapi.co/api/people/?search={}".format(search_form.criteria.data))
		json_pers = personajes.json()
		personajes = json_pers["results"]
		personajes_2 = list()
		for per in personajes:
			personajes_2.append(perparse(per))
		naves = requests.get("https://swapi.co/api/starships/?search={}".format(search_form.criteria.data))
		json_naves = naves.json()
		naves = json_naves["results"]
		naves_2 = list()
		for na in naves:
			naves_2.append(navparse(na))
		planetas = requests.get("https://swapi.co/api/planets/?search={}".format(search_form.criteria.data))
		json_plans = planetas.json()
		planetas = json_plans["results"]
		planetas_2 = list()
		for pl in planetas:
			planetas_2.append(planparse(pl))
		return render_template("search.html", peliculas = peliculas_2, personajes = personajes_2 , naves= naves_2, planetas= planetas_2, form = search_form)

	peliculas = requests.get("https://swapi.co/api/films")
	json_pelis = peliculas.json()
	peliculas = json_pelis["results"]
	peliculas_2 = list()
	for peli in peliculas:
		peliculas_2.append(parse(peli))

	return render_template("index.html", peliculas= peliculas_2, form = search_form)


@app.route("/pelis/<int:num>", methods = ["GET","POST"])
def render_peli(num):
	search_form = forms.SearchForm(request.form)
	if request.method == "POST":
		peliculas = requests.get("https://swapi.co/api/films/?search={}".format(search_form.criteria.data))
		json_pelis = peliculas.json()
		peliculas = json_pelis["results"]
		peliculas_2 = list()
		for peli in peliculas:
			peliculas_2.append(parse(peli))
		personajes = requests.get("https://swapi.co/api/people/?search={}".format(search_form.criteria.data))
		json_pers = personajes.json()
		personajes = json_pers["results"]
		personajes_2 = list()
		for per in personajes:
			personajes_2.append(perparse(per))
		naves = requests.get("https://swapi.co/api/starships/?search={}".format(search_form.criteria.data))
		json_naves = naves.json()
		naves = json_naves["results"]
		naves_2 = list()
		for na in naves:
			naves_2.append(navparse(na))
		planetas = requests.get("https://swapi.co/api/planets/?search={}".format(search_form.criteria.data))
		json_plans = planetas.json()
		planetas = json_plans["results"]
		planetas_2 = list()
		for pl in planetas:
			planetas_2.append(planparse(pl))
		return render_template("search.html", peliculas = peliculas_2, personajes = personajes_2 , naves= naves_2, planetas= planetas_2, form = search_form)

	pelicula = requests.get("https://swapi.co/api/films/{}".format(num))
	json_peli = superparse(pelicula.json())
	return render_template("movie.html", p=json_peli, crawl=pelicula.json()["opening_crawl"], form = search_form)

@app.route("/chars/<int:num>", methods = ["GET","POST"])
def render_char(num):
	search_form = forms.SearchForm(request.form)
	if request.method == "POST":
		peliculas = requests.get("https://swapi.co/api/films/?search={}".format(search_form.criteria.data))
		json_pelis = peliculas.json()
		peliculas = json_pelis["results"]
		peliculas_2 = list()
		for peli in peliculas:
			peliculas_2.append(parse(peli))
		personajes = requests.get("https://swapi.co/api/people/?search={}".format(search_form.criteria.data))
		json_pers = personajes.json()
		personajes = json_pers["results"]
		personajes_2 = list()
		for per in personajes:
			personajes_2.append(perparse(per))
		naves = requests.get("https://swapi.co/api/starships/?search={}".format(search_form.criteria.data))
		json_naves = naves.json()
		naves = json_naves["results"]
		naves_2 = list()
		for na in naves:
			naves_2.append(navparse(na))
		planetas = requests.get("https://swapi.co/api/planets/?search={}".format(search_form.criteria.data))
		json_plans = planetas.json()
		planetas = json_plans["results"]
		planetas_2 = list()
		for pl in planetas:
			planetas_2.append(planparse(pl))
		return render_template("search.html", peliculas = peliculas_2, personajes = personajes_2 , naves= naves_2, planetas= planetas_2, form = search_form)

	personaje = requests.get("https://swapi.co/api/people/{}".format(num))
	json_per = perparse(personaje.json())
	return render_template("character.html", p=json_per, form = search_form)

@app.route("/plan/<int:num>", methods = ["GET","POST"])
def render_plan(num):
	search_form = forms.SearchForm(request.form)
	if request.method == "POST":
		peliculas = requests.get("https://swapi.co/api/films/?search={}".format(search_form.criteria.data))
		json_pelis = peliculas.json()
		peliculas = json_pelis["results"]
		peliculas_2 = list()
		for peli in peliculas:
			peliculas_2.append(parse(peli))
		personajes = requests.get("https://swapi.co/api/people/?search={}".format(search_form.criteria.data))
		json_pers = personajes.json()
		personajes = json_pers["results"]
		personajes_2 = list()
		for per in personajes:
			personajes_2.append(perparse(per))
		naves = requests.get("https://swapi.co/api/starships/?search={}".format(search_form.criteria.data))
		json_naves = naves.json()
		naves = json_naves["results"]
		naves_2 = list()
		for na in naves:
			naves_2.append(navparse(na))
		planetas = requests.get("https://swapi.co/api/planets/?search={}".format(search_form.criteria.data))
		json_plans = planetas.json()
		planetas = json_plans["results"]
		planetas_2 = list()
		for pl in planetas:
			planetas_2.append(planparse(pl))
		return render_template("search.html", peliculas = peliculas_2, personajes = personajes_2 , naves= naves_2, planetas= planetas_2, form = search_form)

	planeta = requests.get("https://swapi.co/api/planets/{}".format(num))
	json_pla = planparse(planeta.json())
	return render_template("planet.html", p=json_pla, form = search_form)

@app.route("/naves/<int:num>", methods = ["GET","POST"])
def render_nave(num):
	search_form = forms.SearchForm(request.form)
	if request.method == "POST":
		peliculas = requests.get("https://swapi.co/api/films/?search={}".format(search_form.criteria.data))
		json_pelis = peliculas.json()
		peliculas = json_pelis["results"]
		peliculas_2 = list()
		for peli in peliculas:
			peliculas_2.append(parse(peli))
		personajes = requests.get("https://swapi.co/api/people/?search={}".format(search_form.criteria.data))
		json_pers = personajes.json()
		personajes = json_pers["results"]
		personajes_2 = list()
		for per in personajes:
			personajes_2.append(perparse(per))
		naves = requests.get("https://swapi.co/api/starships/?search={}".format(search_form.criteria.data))
		json_naves = naves.json()
		naves = json_naves["results"]
		naves_2 = list()
		for na in naves:
			naves_2.append(navparse(na))
		planetas = requests.get("https://swapi.co/api/planets/?search={}".format(search_form.criteria.data))
		json_plans = planetas.json()
		planetas = json_plans["results"]
		planetas_2 = list()
		for pl in planetas:
			planetas_2.append(planparse(pl))
		return render_template("search.html", peliculas = peliculas_2, personajes = personajes_2 , naves= naves_2, planetas= planetas_2, form = search_form)

	nave = requests.get("https://swapi.co/api/starships/{}".format(num))
	json_nav = navparse(nave.json())
	return render_template("ships.html", n=json_nav, form = search_form)


if __name__ == "__main__":
    app.run(debug = False, port=3000)
