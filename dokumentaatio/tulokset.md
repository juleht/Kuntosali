## Tulokset

Projektissa muodostetaan ensin neljästä eri taulusta yksi isompi aineisto, jossa on 5004 riviä ja mukana vain 17.7.2017 jälkeen tehdyt vierailut. Tietokantataulut kuvaavat vierailuajankohtaa (visits), kuntotestin suoritusajankohtaa (fitness_tests), jäsenyyshakemuksen jättämisen ajankohtaa (applications) ja jäsenyyden ostamisen ajankohtaa (purchases). Kuntosalivierailijat jaetaan kahteen osaan sen perusteella tarjottiinko heille kuntotestiä vai ei. Alla piirakkakaavio vierailijoiden jakautumisesta.

![piirakka](/kuvat/AB_testi_ympyrakaavio.png)

![AB](/kuvat/AB.png)

Tehdään vielä X2-testi, jolla selvitetään vaikuttiko kuntotestin tarjoaminen tilastollisesti merkitsevällä tavalla kuntosalihakemuksen tekemiseen. Testin p-arvo 0.0009. Kuntotestin tarjoaminen vaikutti jäsenyyshakemuksen tekemiseen. Vierailijat, joille kuntotestiä ei tarjottu tekivät enemmän hakemuksia jäsenyyttä varten. 

![hakemukset](/kuvat/hakemus.png)

Tarkastellaan vielä lähemmin osajoukkoa vierailijoista, jotka jättivät hakemuksen kuntosalijäsenyydestä. Tehdään X2-testi, jolla selvitetään vaikuttaako hakemuksen täyttäminen tilastollisesti merkitsevällä tavalla varsinaisen salijäsenyyden ostamiseen. X2-testin p-arvo 0.432 hakemuksen täyttäminen ei vaikuttanut kummassakaan ryhmässä varsinaiseen ostopäätökseen.

![ostot](/kuvat/ostot.png)

Tarkastellaan edelleen chi2-testillä vaikuttaako kuntotesti tarjoaminen kuntosalijäsenyyden ostamiseen koko joukossa. Tässä ryhmässä testi oli merkitsevä p-arvo 0.014, kuntotestin tarjoaminen vierailijalle vaikutti siihen ostaako vierailija jäsenyyden vai ei. Joukko ihmisiä keille kuntotestiä tarjottiin ostivat vähemmän jäsenyyksiä kuin he joille sitä ei tarjottu. Alla histogrammi, joka kuvaa eri ryhmien prosentuaalisia eroja.

![histogrammi](/kuvat/pylvaskaavio.png)
