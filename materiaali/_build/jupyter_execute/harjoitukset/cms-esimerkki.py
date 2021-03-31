# CMS ja avoin data

CERN:n CMS-kokeessa törmäytetään protoneita toisiinsa ja tutkitaan, mitä hiukkasia törmäyksessä syntyy. Törmäystapahtumista kertyy valtava määrä dataa, jota on julkaistu myös avoimesti saataville [CERN:n avoin data portaalissa](https://opendata.cern.ch/). Tässä harjoituksessa tutustutaan siihen, mitä nämä datasetit sisältävät ja mitä niiden avulla voitaisiin selvittää. Tämä tarjoaa oppilaille mainion tilaisuuden kokeilla oikean tieteen metodeja autenttisilla mittaustuloksilla.

## 1. Datan hakeminen

Aloitetaan hakemalla data. Data on ladattu CERN:n avoin data portaalista ja tallennettu samaan hakemistoon tämän notebookin kanssa. Tarkastellaan datatiedostoa **Dimuon_DoubleMu.csv**, joka sisältää dataa törmäystapahtumista, joissa on havaittu kaksi myonia.

# Aloitetaan hakemalla tarvittavat python-paketit import-komennolla
# Voit suorittaa koodisolut Run-painikkeella tai paina CTRL+ENTER.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Luetaan datatiedoston sisältö ja tallennetaan tiedot muuttujaan "kaksi_myonia"

kaksi_myonia = pd.read_csv('Dimuon_DoubleMu.csv')

# Tarkastellaan miltä data näyttää

kaksi_myonia.head()

Datatiedostotta näyttäisi olevan paljon tietoa. Jokainen rivi vastaa yhtä törmäystapahtumaa, jossa on havaittu kaksi myonia. Rivillä on aina mittausdataa molemmista havaitusta myonista. Esimerkiksi *E* tarkoittaa myonin energiaa ja *p* liikemäärää. Viimeinen sarake *M* viittaa myoneiden *invarianttiin massaan*, jota tarkastellaan pian enemmän.

# Katsotaan vielä, kuinka monta riviä dataa tiedostossa on

len(kaksi_myonia)

## 2. Invariantti massa & histogrammi

Aiemmasta tutkimuksesta tiedetään, että monet eri hiukkaset voivat hajota kahdeksi myoniksi ja että alkuperäinen hiukkanen voidaan tunnistaa laskemalla myoneiden niin sanottu **invariantti massa**. CMS-detektorilla voidaan mitata mm. myoneiden energia ja liikemäärä. Kun nämä suureet tiedetään, myoneiden invariantti massa on

$M = \sqrt{(E_1 + E_2)^2 - \|\textbf{p}_1 + \textbf{p}_2 \| ^2}$.

Mikäli myonit olivat peräisin yhden hiukkasen hajoamisesta, myoneiden invariantti massa vastaa tämän hiukkasen massaa. Jos taas myonit eivät olleet peräisin samasta hiukkasesta, invariantin massan arvo ei merkitse mitään.

Kun protonit törmäävät hiukkaskiihdyttimessä, vapautuu valtava määrä energiaa, joka muuttuu uusiksi hiukkasiksi. Törmäyksessä voisi syntyä esimerkiksi Z-bosoni, joka on kuitenkin niin lyhytikäinen, että se hajoaa nopeasti toisiksi hiukkasiksi, esimerkiksi kahdeksi myoniksi. Nämä myonit havaitaan hiukkasilmaisimessa ja myoneille lasketun invariantin massan avulla pääsemme käsiksi "emohiukkasen" eli tässä tapauksessa Z-bosonin massaan.

Histogrammi on erinomainen työkalu hiukkasfysiikan tutkimuksessa. Tekemällä histogrammin invarianttien massojen arvosta, voimme erottaa merkityksettömistä taustatapahtumista ne tapahtumat, jotka ovat kiinnostavia. Eikun tutkimaan!

# Invariantti massa voitaisiin laskea ylläolevan kaavan avulla.
# Se löytyy kuitenkin valmiiksi laskettuna jo datasetin viimeisestä sarakkeesta "M", joten käytetään sitä.
# Tallennetaan invarianttien massojen sarake omaan muuttujaan
invariantti_massa = kaksi_myonia['M']

# Piirretään histogrammi kahden myonin invarianteista massoista 300 pylväällä
fig = plt.figure(figsize=(15, 10))
plt.hist(invariantti_massa , bins=300)

# Näillä riveillä määritellään otsikko sekä akseleiden tekstit.
plt.xlabel('Invariantti massa [GeV/c²]', fontsize=15)
plt.ylabel('Tapahtumien lukumäärä', fontsize=15)
plt.title('Kahden myonin invariantti massa', fontsize=15)

# Näytetään kuvaaja
plt.show()

Huomataan, että muutamilla invariantin massan arvoilla histogrammiin syntyy piikki. Nämä piikit vastaavat emohiukkasten massaa, joista kaksi myonia ovat peräisin. Tutkitaan tarkemmin histogrammin väliä 80 GeV - 100 GeV.

# Piirretään histogrammi kahden myonin invarianteista massoista 100 pylväällä välillä 80 GeV - 100 GeV
fig = plt.figure(figsize=(15, 10))
plt.hist(invariantti_massa , bins=100, range=(80,100))

# Näillä riveillä määritellään otsikko sekä akseleiden tekstit.
plt.xlabel('Invariantti massa [GeV/c²]', fontsize=15)
plt.ylabel('Tapahtumien lukumäärä', fontsize=15)
plt.title('Kahden myonin invariantti massa', fontsize=15)

# Näytetään kuvaaja
plt.show()

Huomataan, että datasta erottuu selkeä piikki noin 91 GeV kohdalla. Tämä johtuu siitä, taustatapahtumissa syntyvien kahden myonin lisäksi syntyy paljon sellaisia tapahtumia, joissa myonien invariantti massa on lähellä 91 GeV:iä. Tämä tarkoittaa sitä, että myonit ovat peräisin johtain hiukkasesta, jonka massa on 91 GeV. Tämä hiukkanen tunnetaan nimellä Z-bosoni.

Kokeile itse etsiä alkuperäisestä datasta toinen piikki, ja katso löydätkö jonkin toisen hiukkasen! Mikä hiukkanen voisi olla kyseessä?