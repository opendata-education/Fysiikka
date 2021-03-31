# Lämpötila ja sademäärä

## Tehtävä

Etsi oman kotipaikkakuntasi (tai jonkin muun paikkakunnan) kuukausien keskilämpötilat ja sademäärät ainakin kymmenen viime vuoden ajalta (voit valita myös koko mittaushistorian). Laske vuosien keskilämpötilat ja sademäärät ja piirrä niistä kuvaaja. Mikä vuosi on ollut kaikkein lämpimin? Entä kylmin? Milloin puolestaan on satanut eniten tai vähiten? Voit ottaa mallia esimerkistä.

## Esimerkki

Haetaan [Ilmatieteenlaitoksen hakupalvelusta](https://www.ilmatieteenlaitos.fi/havaintojen-lataus) tiedot Pirkkalan lentoaseman säähavainnoista (kuukauden keskilämpötila ja -sademäärä). Mittaushistoria ulottuu noin 80-luvulle, joten valitaan aikaväliski 1980-2020. Havainnot on ladattu hakupalvelusta ja tallennettu tiedostoon "pirkkala_1980-2020.csv".

Käytetään datan lukemiseen ja käsittelemiseen [pandas](org)-pakettia ja datan visualisoimiseen [matplotlib](https://matplotlib.org/)-pakettia.

# Tuodaan tarvittavat paketit

import pandas as pd
import matplotlib.pyplot as plt

# Luetaan data ja katsotaan ensimmäisten rivien sisältö.
# Data sijaitsee data kansiossa, joka on yhden kansion alempana nykyisestä kansiosta.

data = pd.read_csv('../data/pirkkala_1980-2020.csv')
data.head()

Nähdään, että sademäärät löytyvät sarakkeesta "Kuukauden sadesumma (mm)" ja lämpötilat sarakkeesta "Kuukauden keskilämpötila (degC)". Seuraavaksi meidän tulee ryhmitellä data vuosien perusteella, jotta voimme vertailla dataa vuositasolla. Ryhmittely voidaan tehdä [`groupby()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html)-funktiolla.

# Ryhmitellään data "Vuosi"-sarakkeen perusteella.

data_groups = data.groupby('Vuosi')


Vuositilastojen keskiarvot saadaan [`mean()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.groupby.GroupBy.mean.html)-funktiolla.

# Katsotaan, miltä keskiarvotilastot näyttävät

avg = data_groups.mean()
avg.head()

Tallennetaan keskiarvot omiin muuttujiin. Vuosiluvut saadaan data-ryhmistä [groups](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.groupby.GroupBy.groups.html)-komennolla, josta saamme ryhmät ja niitä vastaavien rivien indeksit. Koska haluamme ainoastaan vuosiluvut (eli ryhmien nimet), käytämme vielä `keys()`-funktiota, joka antaa ainoastaan ryhmien nimet.

# Tallennetaan vuosien keskilämpötilat ja -sademäärät sekä vuosiluvut omiin muuttujiin.

rain = avg['Kuukauden sadesumma (mm)']
temp = avg['Kuukauden keskilämpötila (degC)']
year = data_groups.groups.keys()

Nyt kun data on käsitelty, voimme piirtää kuvaajan. Piirretään sademäärä pylväinä ja lämpötila viivana. Käytetään matplotlib-paketista seuraavia funktioita:

- [`subplots()`](https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.subplots.html) Kuvaajan alustus
- [`plot(x,y)`](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot.html) Piirretään y x:n funktiona
- [`bar(x,y)`](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.bar.html) Pylväsdiagrammi 
- [`twinx()`](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.twinx.html) Luodaan toinen akselisto, jossa on sama x-akseli
- [`set_xlabel('title')`](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_xlabel.html) Asetetaan tiettyyn akselistoon x-akselin otsikko
- [`set_ylabel('title')`](https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.axes.Axes.set_ylabel.html) Asetetaan tiettyyn akselistoon y-akselin otsikko
- [`title('title')`](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.title.html) Otsikko
- [`show()`](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.show.html) Kuvaajan näyttäminen

# Kuvaajan piirtäminen

# Alustetaan kuvaaja subplots-komennolla. Tällöin voimme luoda myöhemmin toisen y-akselin kuvaajaan.
fig, ax = plt.subplots(figsize=(12,8))

# Piirretään lämpötilat
ax.plot(year,temp, 'r', linewidth=3, alpha=0.7)

# Luodaan toinen y-akseli sademääriä varten
ax2 = ax.twinx()

# Piirretään sademäärät pylväinä
ax2.bar(year,rain, alpha=0.7)

# Asetetaan akselien otsikot
ax.set_xlabel('Vuosi')
ax.set_ylabel('Lämpötila (degC)')
ax2.set_ylabel('Sademäärä (mm)')

# Kuvaajan otsikko
plt.title('Vuosien keskilämpötilat ja -sademäärät Pirkkalan lentoasemalla')

# Näytetään kuvaaja
plt.show()

Kuvaajasta huomataan, että sademäärätiedot puuttuvat vuoden 2006 jälkeen. Tarkistetaan vielä [`get_group`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.groupby.GroupBy.get_group.html)-funktion avulla, miltä vuoden 2006 tilastot näyttävät:

data_groups.get_group(2006)

Huomataan, että sademäärien mittaaminen on keskeytetty kesken vuoden 2006. Niimpä meidän täytyy jättää myös vuosi 2006 pois vuositilastoistamme. Korvataan vuoden 2006 arvo NaN (Not a Number) arvolla, joka tarkoittaa, että arvoa ei ole olemassa. Tämä voidaan tehdä [numpy](https://numpy.org/)-paketin [`nan`](https://numpy.org/doc/stable/reference/constants.html#numpy.nan)-arvolla.

# Poistetaan vuosi 2006 rain-taulukosta
# Korvataan arvo numpy-paketin NaN-arvolla, joka tarkoittaa, että arvoa ei ole olemassa.

import numpy as np
rain[2006] = np.nan
rain

# Piirretään kuvaaja uudelleen

fig, ax = plt.subplots(figsize=(12,8))

ax.plot(year,temp, 'r', linewidth=3, alpha=0.7)
ax2 = ax.twinx()
ax2.bar(year,rain, alpha=0.7)

ax.set_xlabel('Vuosi')
ax.set_ylabel('Lämpötila (degC)')
ax2.set_ylabel('Sademäärä (mm)')
plt.title('Vuosien keskilämpötilat ja -sademäärät Pirkkalan lentoasemalla')

plt.show()

Maksimi- ja minimi lämpötilat sekä sademäärät voitaisiin lukea suoraan kuvaajasta.

Ne voidaan kuitenkin saada myös koodaamalla (käytetään [`max()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.max.html)- ja [`min()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.min.html#pandas.Series.min)-funktioita):

max_temp = temp[temp == temp.max()]
max_temp

min_temp = temp[temp == temp.min()]
min_temp

max_rain = rain[rain == rain.max()]
max_rain

min_rain = rain[rain == rain.min()]
min_rain

Kokeile seuraavaksi itse selvittää esimerkiksi oman kotikaupunkisi lämpötilan ja sademäärän vuosittaiset keskiarvot. Voit piirtää myös tietyn vuoden kuukausittaiset keskiarvot!