from flask import Flask, render_template, request
from sodapy import Socrata
import pandas as pd
from funciones import candidatos, busqueda, comparar, registro_mayor

app = Flask(__name__)
client = Socrata("www.datos.gov.co", None)
result = client.get('75f2-fe2s', limit=5000, offset=1000000)
data = pd.DataFrame.from_records(result)
data['votos'] = pd.to_numeric(data['votos'])
html = data.to_html()
partidos = data.loc[:, ['partido']].dropna().squeeze().unique()


@app.route('/')
def index():

    var = data.groupby(['partido'])["votos"].sum().reset_index()
    votos_partidos = pd.DataFrame(var).to_html()
    return render_template('datos.html', data=html, votos=votos_partidos)


@app.route('/funcion1', methods=['GET', 'POST'])
def funcion1():
    res = candidatos(data, 'PARTIDO LIBERAL COLOMBIANO')

    if request.method == 'POST':
        valor = request.form['partidos']
        post = candidatos(data, valor)
        return render_template('funcion1.html', candidatos=post[0].to_html(), votados=post[1], partidos=partidos)

    return render_template('funcion1.html', candidatos=res[0].to_html(), votados=res[1], partidos=partidos)


@app.route('/funcion2', methods=['GET', 'POST'])
def funcion2():
    if request.method == 'POST':
        nombre = request.form['nombre']
        return render_template('funcion2.html', candidato=busqueda(data, nombre).to_html())
    return render_template('funcion2.html', candidato=busqueda(data, "Alvaro uribe velez").to_html())


@app.route('/funcion3', methods=['GET', 'POST'])
def funcion3():
    c = comparar(data, 'PARTIDO CENTRO DEMOCRÁTICO', 'PARTIDO ALIANZA VERDE')
    registro_p1 = registro_mayor(data, 'PARTIDO CENTRO DEMOCRÁTICO').to_html()
    registro_p2 = registro_mayor(data, 'PARTIDO ALIANZA VERDE').to_html()
    if request.method == 'POST':
        p1 = request.form['partido_1']
        p2 = request.form['partido_2']
        c = comparar(data, p1, p2)
        registro_p1 = registro_mayor(data, p1).to_html()
        registro_p2 = registro_mayor(data, p2).to_html()
        return render_template('funcion3.html', partidos=partidos, p1=p1, p2=p2, c1=c[0], c2=c[1], r1=registro_p1, r2=registro_p2)
    return render_template('funcion3.html', partidos=partidos, p1='PARTIDO CENTRO DEMOCRÁTICO', p2='PARTIDO ALIANZA VERDE', c1=c[0], c2=c[1], r1=registro_p1, r2=registro_p2)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
    pass
