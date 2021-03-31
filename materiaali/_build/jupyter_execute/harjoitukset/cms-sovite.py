# Funktion sovittaminen histogrammiin

Tutustutaan tässä harjoituksessa siihen, miten histogrammiin voidaan tehdä sovite. Sovite on erinomainen työkalu, kun halutaan selvittää esimerkiksi jakauman odotusarvo ja hajonta. Hiukkasfysiikan tapauksessa tämä tulee kyseeseen, kun pyritään selvittämään histogrammissa olevan piikin paikkaa ja leveyttä.

Tutkitaan hiukkasfysiikan dataa sellaisista törmäyksistä, joissa on havaittu kaksi myonia. Data on haettu CERN:n avoin data portaalista ja se löytyy tämän notebookin kanssa samasta hakemistosta nimellä "Dimuon_DoubleMu.csv".

## Datan hakeminen ja piirtäminen

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('../data/Dimuon_DoubleMu.csv')
data.head()

plt.hist(data['M'], bins=300)
plt.show()

Rajataan tarkastelumme invariantin massan välille 80 GeV - 100 GeV ja piirretään data tällä välillä. Huom. Tällä kertaa `plt.hist()`-funktion paluuarvot on otettu talteen. Funktiolla on kolme paluuarvoa, joista meitä kiinnostaa kaksi ensimmäistä: histogrammin pylväiden arvot sekä pylväiden reunat.

alaraja = 80
yläraja = 100
pylväitä = 100

plt.figure()
arvot, reunat, _ = plt.hist(data['M'], bins=pylväitä, range=(alaraja, yläraja))
plt.xlabel('Invariantti massa (GeV)')
plt.ylabel('Tapahtumien lukumäärä')
plt.show()

## Sovitefunktion määritteleminen

Tavoitteenamme on tehdä sovite yllä olevaan jakaumaan. Hiukkasfysiikassa yleisesti käytettävä jakaumafunktio on [Breit-Wigner -jakauma](https://en.wikipedia.org/wiki/Relativistic_Breit%E2%80%93Wigner_distribution), mutta käytetään tässä Gaussin jakaumaa, joka ottaa taustatapahtumat myös huomioon.

Tällainen Gaussin funktio on muotoa:

$f(x) = a\frac{e^{-(x-\mu)^2}}{2\sigma^2} + bx + c$,

missä $a$ on kerroin, $\mu$ odotusarvo, $\sigma^2$ varianssi ja $b$ ja $c$ taustatapahtumiin liittyviä kertoimia.

Määritellään funktio:

import numpy as np

def gauss(x, *p):
    a, mu, sigma, b, c = p
    return a*np.exp(-(x-mu)**2/(2.*sigma**2)) + b*x + c

## Sovitteen tekeminen

Tehdään seuraavaksi sovite scipy-paketin curve_fit -funktiolla. Meidän tulee kuitenkin ensin määrittää pylväiden keskikohdat, jotta sovite osuu oikealle kohdalle.

from scipy.optimize import curve_fit

# Pylväiden keskikohdat saadaan ottamalla kahden vierekkäisen reunan keskiarvo
keskikohdat = (reunat[:-1] + reunat[1:])/2

# Sovitetta varten tarvitaan sopivat alkuarvaukset. Jos sovite epäonnistuu, kokeile jotain muita alkuarvoja
# Alkuarvot ovat järjestyksessä a, mu, sigma, b, c
p0 = [100, 90, 1, 1, 1]

# Lasketaan optimaaliset kertoimet
kertoimet, _ = curve_fit(gauss, keskikohdat, arvot, p0=p0)

# Lasketaan sovite kertoimien avulla
sovite = gauss(keskikohdat, *kertoimet)

# Piirretään alkuperäinen histogrammi sekä sovitefunktio
plt.hist(data['M'], bins=pylväitä, range=(alaraja, yläraja))
plt.plot(keskikohdat, sovite, label='Sovite')
plt.xlabel('Invariantti massa (GeV)')
plt.ylabel('Tapahtumien lukumäärä')

# Tulostetaan odotusarvo ja piikin leveys (FWHM)
print('Odotusarvo = ', kertoimet[1])
print('Piikin leveys = ', 2*np.sqrt(2*np.log(2))*kertoimet[2])

plt.show()

Tämän tuloksen perusteella saamme Z-bosonin massaksi noin 90,86 GeV. Kokeile, saatko sovitettua [Breit-Wigner -jakauman](https://en.wikipedia.org/wiki/Relativistic_Breit%E2%80%93Wigner_distribution) histogrammiin. Onko sovite parempi kuin Gaussin jakauma? Kokeile myös, miten pylväiden lukumäärän muuttaminen vaikuttaa tulokseen.