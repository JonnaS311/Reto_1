import pandas as pd
import matplotlib.pyplot as plt


def candidatos(dataframe, partido):
    sel_partido = dataframe[dataframe['partido'] == partido]
    respuesta = pd.DataFrame(sel_partido.groupby('candidato').sum()['votos'].reset_index())
    mas_votados = respuesta[respuesta['votos'] == respuesta['votos'].max()]
    return respuesta, mas_votados['candidato']


def busqueda(dataframe, nom_candidato):
    sel_candidato = dataframe[dataframe["candidato"].squeeze().str.contains(nom_candidato, case=False)==True]
    return sel_candidato


def comparar(dataframe, p1, p2):
    data = dataframe.groupby(['partido'])["votos"].sum()
    new = pd.DataFrame((data[p1], data[p2]), index=['A', 'B'], columns=['votos'])
    new.plot.bar(color='#86efac', figsize=(5, 5))
    plt.savefig('app/static/resources/ima1.png')
    c1 = candidatos(dataframe, p1)[1]
    c2 = candidatos(dataframe, p2)[1]

    return c1.squeeze(), c2.squeeze()


def registro_mayor(dataframe, partido):
    respuesta = dataframe[dataframe['votos'] == dataframe['votos'][dataframe['partido'] == partido].max()]
    return respuesta[respuesta['partido'] == partido]

