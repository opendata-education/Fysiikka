# Interaktiiviset kartat

Edellisessä esimerkissä piirsimme kartan, joka antoi nopeasti hyvän kokonaiskuvan maailman hiilidioksidipäästöistä. Kartalla valtiot oli väritetty siten, että mitä tummempi väri, sitä suuremmat päästöt valtiolla oli. Mitä, jos haluaisimmekin tietää tarkalleen tietyn valtion päästöt?

Tässä harjoituksessa tarkoituksena on tehdä samantyylinen kartta, mutta lisätään siihen interaktiivisia ominaisuuksia. Tehdään sellainen kartta, jossa näytölle ilmestyy alueen tietoja, kun hiirellä liikutaan alueen päälle. Käytetään vaihtelun vuoksi eri esimerkkidataa kuin viime kerralla. Piirretään tällä kertaa Suomen kunnat ja niissä asuvien eläkeläisten osuus väestöstä.

Suomen karttaa varten tarvittavat kuntarajat saadaan ladattua [Maanmittauslaitoksen tiedostopalvelusta](https://tiedostopalvelu.maanmittauslaitos.fi/tp/kartta). Tiedosto löytyy datakansiosta nimellä "SuomenKuntajako_2020_250k.mid".

Eläkeläisten osuus kuntien väestöstä on myös avointa dataa ja saatavilla [Tilastokeskuksen palvelusta](https://pxnet2.stat.fi/PXWeb/pxweb/fi/Kuntien_avainluvut/). Tämäkin tiedosto on valmiiksi ladattu ja hieman siistitty paremmin tätä esimerkkiä sopivaksi. Se löytyy datakansiosta nimellä "elakelaisten_osuus_2018_kuntajako_2020.csv". Nimi viittaa siihen, että kyseessä on eläkeläisten osuus väestöstä vuodelta 2018, mutta vuoden 2020 kuntajaolla.

## Datan lukeminen

Aloitetaan harjoitus samoin, kuten aiemmin, eli lataamalla datatiedostot ja yhdistämällä ne yhdeksi datasetiksi. Käytämme jälleen [pandas](https://pandas.pydata.org/) ja [geopandas](https://geopandas.org/) -kirjastoja tähän.

import pandas as pd
import geopandas as gpd

# Luetaan kuntarajat sisältävä tiedosto geopandasin read_file()-funktiolla
# encoding='latin1' varmistaa, että ääkköset tulevat oikein
cities = gpd.read_file('../data/SuomenKuntajako_2020_250k.mid', encoding='latin1')

# Katsotaan, mitä tiedosto sisältää
cities.head()

# Luetaan kuntien eläkeläistiedot sisältävä tiedosto pandasin read_csv()-funktiolla
pensioners = pd.read_csv('../data/elakelaisten_osuus_2018_kuntajako_2020.csv')

# Katsotaan, mitä tiedosto sisältää
pensioners.head()

# Yhdistetään tiedot kaupunkien nimien perusteella
data = cities.merge(pensioners, left_on='namefin', right_on='alue')

# Katsotaan tulos
data.head()

## Kartan piirtäminen Bokeh-kirjaston avulla

Hienoa, datan lukeminen onnistui! Piirretään seuraavaksi tiedot näytölle [Bokeh](https://bokeh.org/)-kirjaston avulla. Kuvan piirtämiseksi tarvitsemme seuraavia funktioita tai luokkia:

- [`figure()`](https://docs.bokeh.org/en/latest/docs/reference/plotting.html#bokeh.plotting.figure): Alustetaan kuva. Voidaan antaa esim. kuvan otsikko tässä vaiheessa "title"-parametrilla.
- [`GeoJSONDataSource`](https://docs.bokeh.org/en/latest/docs/reference/models/sources.html#bokeh.models.sources.GeoJSONDataSource): Muutetaan datamme GeoJSONDataSource-muotoiseksi, jotta sen piirtäminen bokeh:lla onnistuu helposti.
- [`LinearColorMapper`](https://docs.bokeh.org/en/latest/docs/reference/models/mappers.html#bokeh.models.mappers.LinearColorMapper): Lisätään värit karttaan.
- [`Greens`](https://docs.bokeh.org/en/latest/docs/reference/palettes.html#brewer-palettes): Käytetään vihreää värikarttaa.
- [`output_notebook()`](https://docs.bokeh.org/en/latest/docs/reference/io.html#bokeh.io.output.output_notebook): Tämän funktion avulla ḱuva piirtyy koodisolun alapuolelle (jos show-funktiota on myös käytetty). Muussa tapauksessa kuva avautuisi uuteen välilehteen.
- [`show()`](https://docs.bokeh.org/en/latest/docs/reference/io.html#bokeh.io.show): Tällä käskyllä näytetään kuva.

# Tuodaan tarvittavat funktiot. Huom. ne pitää tuoda oikeista kirjastoista.
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper
from bokeh.palettes import Greens
from bokeh.io import output_notebook, show

# Alustetaan kuva ja asetetaan otsikko. Tallennetaan kuva muuttujaan "fig".
fig = figure(title="Eläkeläisten osuus väestöstä vuonna 2018 vuoden 2020 kuntajaolla (%). ")

# Muutetaan datamme ensin json-tyyppiseksi ja sen jälkeen GeoJSONDataSource:ksi
data_json = data.to_json()
geosource = GeoJSONDataSource(geojson = data_json)

# Valitaan 6 eri väriä Greens-värikartasta. Lopussa oleva [::-1] kääntää värikartan toisinpäin, toisin sanoen tummemmat
# ilmaisevat silloin suurempaa lukuarvoa.
palette = Greens[6][::-1]

# Valitaan värien minimiarvoksi datamme pienin arvo ja maksimiarvoksi datamme suurin arvo.
color_mapper = LinearColorMapper(palette = palette,
                                 low = data['elakelaisten_osuus'].min(),
                                 high = data['elakelaisten_osuus'].max())

# Piirretään kuntarajat kartalle. GeoJSONDataSourcessa datamme 'geometry'-sarake on muuttunut 'xs'- ja 'ys'-sarakkeiksi.
# Piirretään siis ne käyttäen lähteenä määrittämäämme "geosource"-muuttujaa.
# Lisätään vielä värit kartalle määrittelemällä "fill_color", jolle pitää kertoa sekä datasarakkeen nimi sekä
# käyttämämme värikartta.
fig.patches('xs','ys',
            source = geosource,
            fill_color={'field':'elakelaisten_osuus','transform': color_mapper})

# Asetetaan tulos näkymään solun alapuolella.
output_notebook()

# Näytetään kartta
show(fig)

Noniin, nyt saimme piirrettyä kartan käyttämällä bokeh-kirjastoa! Huomataan, että Itä-Suomessa on paljon tummanvihreitä alueita, joissa eläkeläisten osuus väestöstä on suuri verrattuna esimerkiksi pääkaupunkiseutuun. (Huom. rannikolla olevien kuntien rajat näyttävät oudoilta, koska myös merialueet on huomioitu kartassa)

Kartassa on valmiiksi hyödyllisiä työkaluja, joiden  avulla voimme zoomata ja liikutella karttaa tai halutessamme vaikkapa tallentaa sen. Tässä on jo hieman interaktiivisuutta, mutta tavoitteenamme oli tehdä sellainen kartta, jossa näytölle ilmestyy alueen tietoja, kun hiirellä liikutaan alueen päälle. Tätä varten tarvitsemme vielä [`HoverTool`](https://docs.bokeh.org/en/latest/docs/reference/models/tools.html#bokeh.models.tools.HoverTool)-työkalun bokeh-kirjastosta.

from bokeh.models import HoverTool

# Tehdään uusi HoverTool-olio ja tallennetaan se muuttujaan "hover".
hover = HoverTool()

# Lisätään hover-oliolle "tooltips"-tietoja, eli nämä tiedot näkyvät, kun hiiri liikutetaan alueen päälle.
# @-merkin jälkeen tuleva sana kertoo, mistä datan sarakkeesta tiedot haetaan.
hover.tooltips = [('Kaupunki', '@alue'),('Eläkeläisten osuus (%)','@elakelaisten_osuus')]

# Lisätään hover kuvan työkaluihin
fig.add_tools(hover)

# Näytetään kuva.
output_notebook()
show(fig)

Loistavaa! Voimme nyt poimia kartastamme kuntia hiirellä ja nähdä, mikä on eläkeläisten osuus väestöstä kyseisissä kunnissa! Eikä siihen mennyt montaakaan koodiriviä.

Kokeile itse hakea jokin muu kuntakohtainen data, piirtää se kartalle ja lisätä vielä interaktiivinen "hover"-työkalu. Voit myös yrittää etsiä jotain muuta, kuten valtiokohtaista dataa tai jotakin muuta, kunhan löydät sopivan tiedoston, joka sisältää alueiden rajat.