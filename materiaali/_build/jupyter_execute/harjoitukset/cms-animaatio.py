# CMS animaatio

Tässä notebookissa tehdään animaatio, joka näyttää, miten piikki histogrammissa muodostuu datamäärän kertyessä suuremmaksi. Suorita kaikki koodisolut. Viimeisen solun suorittamisen jälkeen animaatio ilmestyy näytölle (tässä voi mennä muutama minuutti).

# Tuodaan paketit
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation

# Luetaan data ja valitaan tapahtumat, joissa invariantti massa on välillä 80 GeV - 100 GeV.
# Data koostuu törmäystapahtumista, joissa on havaittu kaksi myonia.
muons = pd.read_csv('Dimuon_DoubleMu.csv')
data = muons[(muons['M'] > 80) & (muons['M'] < 100)]['M']

# Määritetään funktio, joka päivittää histogrammin
# num-parametri kertoo, monesko "frame" on menossa
def updt_hist(num, data):
    plt.cla() # pyyhitään vanha histogrammi pois
    plt.ylim(0,40) # kiinnitetään y-akselin rajat
    plt.xlim(80,100) # kiinnitetään x-akselin rajat
    plt.title(f'Events: {num*5}', fontsize=15) # otsikko
    plt.xlabel('Invariant mass of two muons (GeV)', fontsize=15)
    plt.ylabel('Events per bin', fontsize=15)
    # lisätään histogrammiin aina 5 datapistettä joka "framella".
    plt.hist(data[:num*5], bins = 80)

%%capture
# tämä ns. magic-funktio estää ylimääräisiä frameja ponnahtamasta esiin kesken animaation.

# Alustetaan kuvaaja
fig = plt.figure(figsize=(15,10))

# Luodaan animaatio, jossa 150 kuvaa.
anim = matplotlib.animation.FuncAnimation(fig, updt_hist, frames = 150, fargs = (data,))

# Tehdään animaatiosta HTML representaatio
from IPython.display import HTML
HTML(anim.to_jshtml())

HTML(anim.to_jshtml())