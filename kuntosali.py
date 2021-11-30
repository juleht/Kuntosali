from codecademySQL import sql_query
import pandas as pd
import numpy as np
from matplotlib  import pyplot as plt
from scipy.stats import chi2_contingency 


# Kuntosaliaineiston tarkastelua tässä projektissa
# hyödynnetään tietokantahakuja, aineistot ovat
# peräisin codeacademysta

print('Tietokannan taulu nimeltä: visits')
vierailut = sql_query('SELECT * FROM visits LIMIT 5')
print(vierailut)
# vierailut sisältävät kuntosalin käyttäjän nimen, sähköpostin, sukupuolen ja vierailupäivämäärän

print('Tietokannan taulu nimeltä: fitness_tests')
kuntotesti = sql_query('SELECT * FROM fitness_tests LIMIT 5')
print(kuntotesti)
# kuntotesti sisältävät kuntosalin käyttäjän nimen, sähköpostin, sukupuolen ja kuntotestin päivämäärän

print('Tietokannan taulu nimeltä: applications')
hakemukset = sql_query('SELECT * FROM applications LIMIT 5')
print(hakemukset)
# hakemukset sisältävät kuntosalin käyttäjän nimen, sähköpostin, sukupuolen ja hakemuksen jättöpäivämäärän

print('Tietokannan taulu nimeltä: purchases')
ostot = sql_query('SELECT * FROM purchases LIMIT 5')
print(ostot)
# ostot sisältävät kuntosalin käyttäjän nimen, sähköpostin, sukupuolen ja jäsenyyden ostamisen päivämäärän

# luodaan yksi iso aineisto kaikista tietokannan tauluista yhdistetään taulut, nimen ja sähköpostiosoitteden perusteella.

df = sql_query('''
SELECT visits.first_name, visits.last_name, visits.gender, visits.email, visits.visit_date, fitness_tests.fitness_test_date, applications.application_date, purchases.purchase_date
FROM visits
LEFT JOIN fitness_tests ON visits.first_name = fitness_tests.first_name AND visits.last_name = fitness_tests.last_name AND visits.email = fitness_tests.email
LEFT JOIN applications ON visits.first_name = applications.first_name AND visits.last_name = applications.last_name AND visits.email = applications.email
LEFT JOIN purchases ON visits.first_name = purchases.first_name AND visits.last_name = purchases.last_name AND visits.email = purchases.email
WHERE visit_date >= '7-1-17'
''')
print('Aineiston viisi ensimmäistä riviä:\n',df.head())
print('Aineston rivi määrä', len(df))

# lisätään aineestoon kolumni ilmaisemaan sitä onko kuntotesti suoritettu vai ei
# A merkitsee, että kuntotesti on suoritettu
# B merkitsee, että kuntotestiä ei ole suoritettu

ft = lambda x : 'A' if x is not None else 'B'
df['AB_testi_ryhma'] = df.fitness_test_date.apply(ft)
ab_counts = df.groupby('AB_testi_ryhma').AB_testi_ryhma.count()
print(f'''
    Kuntosalivierailijat ovat jakautuneet noin puoliksi,
    sen perusteella ovatko tehneet kuntotestin ryhmä 'A'
    tai eivät ole tehneet kuntotestia ryhmä 'B':\n {ab_counts}
''')


arvot = [ab_counts[0],ab_counts[1]]
plt.figure(figsize=(10,10))
plt.subplot(1,1,1)
plt.pie(ab_counts, autopct=lambda x : f'{x:0.2f}%, {x*sum(arvot)/100 : 0.0f} henkilöä', labels=['A','B'])
plt.title('Otoksen jakautuminen')
plt.axis('equal')
plt.legend(['A, Kuntotesti', 'B, Ei kuntotestia'])
plt.show()

# Kuka ottaa hakemuksen kuntosalijäsenyyttä varten?
# Tarkastellaan kuinka moni kuntosalivierailija täyttää hakemuksen jäsenyydestä
at = lambda x : 'On hakemus' if x is not None else 'Ei hakemusta'
df['onko_hakemus'] = df.application_date.apply(at)
hakemus_maarat = df.groupby(['AB_testi_ryhma', 'onko_hakemus']).first_name.count().reset_index()
hakemus_maarat_kaannetty = hakemus_maarat.pivot(
    index = 'AB_testi_ryhma',
    columns='onko_hakemus',
    values='first_name'
).reset_index()
hakemus_maarat_kaannetty['yhteensa'] =  hakemus_maarat_kaannetty['On hakemus'] + hakemus_maarat_kaannetty['Ei hakemusta']
hakemus_maarat_kaannetty['kuinka monella prosentilla on hakemus'] = hakemus_maarat_kaannetty['On hakemus'] / hakemus_maarat_kaannetty['yhteensa']
print(f'''
    Kuinka monet kuntotestin tekijät jättivät hakemuksen kuntosalille:\n {hakemus_maarat_kaannetty}
''')

# Testataan chi2 testillä onko kuntotestin suorittamisella tilastollisesti
# merkitsevää merkitystä jättävätkö kuntosalivierailijat hakemuksen kuntosalijäsenyydestä.

x = pd.concat([hakemus_maarat_kaannetty.iloc[0:1, 1:3], hakemus_maarat_kaannetty.iloc[1:2, 1:3]]).to_numpy()
chi2, pval, dof, expected = chi2_contingency(x)

if pval <0.05:
    print(f'''
    P-arvo {pval} Kuntotestin tarjoaminen vaikutti tilastollisesti merkitsevällä tavalla jäsenyyshakemuksen tekemiseen.
    Ihmiset, joille ei tarjottu kuntotestiä tekivät enemmän hakemuksia kuin he, joille sitä tarjottiin
    ''')
else:
    print(f'''
    P-arvo {pval} Kuntotestin tarjoaminen ei vaikuttanut
    siihen tekevätkö ihmiset kuntosalille jäsenyyshakemuksen.
    ''')


# Tarkastellaan ihmisiä, jotka ovat jättäneet hakemuksen kuntosalille.
im = lambda x : 'Jasen' if x is not None else 'Ei jasen'
df['on_jasen'] = df.purchase_date.apply(im)
ainoastaan_hakekemukset = df[df.onko_hakemus == 'On hakemus']
ainoastaan_hakekemukset_taulu = ainoastaan_hakekemukset.groupby(['AB_testi_ryhma', 'on_jasen']).first_name.count().reset_index()
ainoastaan_hakekemukset_taulu_kaanntetty = ainoastaan_hakekemukset_taulu.pivot(
    index = 'AB_testi_ryhma',
    columns = 'on_jasen',
    values = 'first_name'
).reset_index()

ainoastaan_hakekemukset_taulu_kaanntetty['yhteensa'] = ainoastaan_hakekemukset_taulu_kaanntetty['Jasen'] + ainoastaan_hakekemukset_taulu_kaanntetty['Ei jasen']
ainoastaan_hakekemukset_taulu_kaanntetty['Kuinka moni ostaa jasenyyden?'] = ainoastaan_hakekemukset_taulu_kaanntetty['Jasen'] / ainoastaan_hakekemukset_taulu_kaanntetty['yhteensa']
print(f'''Miten kuntotestin tekeminen vaikuttaa siihen ostavatko
    jäsenyyshakemuksen ottaneet jäsenyyden kuntosalilta:\n {ainoastaan_hakekemukset_taulu_kaanntetty}
    ''')

x_2 = pd.concat([ainoastaan_hakekemukset_taulu_kaanntetty.iloc[0:1, 1:3], ainoastaan_hakekemukset_taulu_kaanntetty.iloc[1:2, 1:3]]).to_numpy()
chi2, pval, dof, expected = chi2_contingency(x_2)

if pval <0.05:
    print(f'''
    P-arvo {pval} Kuntotestin tarjoamisella ja kuntosalijäsenyydellä tilastollisesti merkitsevä ero. Kuntotestin tehneet
    ostivat enemmän kuntosalijäsenyyksiä kuin he, jotka eivät tehneet kuntotestiä.
    ''')
else:
    print(f'''
    P-arvo {pval} Kuntotestin tarjoamisella ja kuntosalijäsenyydellä ei ole tilastollisesti merkitsevää yhteyttä, sekä
    kuntotestin tekijät, että he jotka eivät tehneet kuntotestiä ostivat yhtä paljon jäsenyyksiä.
    ''')


# tarkastellaan koko aineistossa kuntotestin tarjoamisen vaikutusta ostopaatokseen

final_Jasen = df.groupby(['AB_testi_ryhma', 'on_jasen']).first_name.count().reset_index()
final_ainoastaan_hakekemukset_taulu_kaanntetty = final_Jasen.pivot(
    index = 'AB_testi_ryhma',
    columns = 'on_jasen',
    values = 'first_name'
).reset_index()
final_ainoastaan_hakekemukset_taulu_kaanntetty['yhteensa'] = final_ainoastaan_hakekemukset_taulu_kaanntetty['Jasen'] + final_ainoastaan_hakekemukset_taulu_kaanntetty['Ei jasen']
final_ainoastaan_hakekemukset_taulu_kaanntetty['Kuinka moni ostaa jasenyyden?'] = final_ainoastaan_hakekemukset_taulu_kaanntetty['Jasen'] / final_ainoastaan_hakekemukset_taulu_kaanntetty['yhteensa']
print(final_ainoastaan_hakekemukset_taulu_kaanntetty)

x_3 = pd.concat([final_ainoastaan_hakekemukset_taulu_kaanntetty.iloc[0:1, 1:3], final_ainoastaan_hakekemukset_taulu_kaanntetty.iloc[1:2, 1:3]]).to_numpy()
chi2, pval, dof, expected = chi2_contingency(x_3)

if pval < 0.05:
    print(f'''
    P-arvo {pval} Koko aineistossa kuntotestin tarjoamisella ja kuntosalijäsenyyden
    ostamisella on tilastollisesti merkitsevä yhteys. Kuntotestin tehneet ihmiset
    ostivat jäsenyyksiä vähemmän kuin he, jotka eivät tehneet kuntotestiä.
    ''')
else:
    print(f'''
    P-arvo {pval} Ryhmien A (tarjottiin kuntotestiä) ja B (ei kuntotestiä)
    välillä ei ole tilastollisesti merkitsevää eroa, kuntotestin tekeminen ei
    vaikuttanut kuntosalijäsenyyden ostamiseen.
    ''')

plt.figure(figsize=(15,7))
ax = plt.subplot()
xt = ['Osuus vierailijoista, jotka hakevat jäsenyyttä', 'Osuus jäsenyyden hakijoista, jotka ostavat kuntosalikortin', 'Osuus vierailijoista, jotka ostavat kuntosalikortin']
barlegend =['A, Kuntotesti', ' B, Ei Kuntotestia']
Alista = [hakemus_maarat_kaannetty['kuinka monella prosentilla on hakemus'][0], ainoastaan_hakekemukset_taulu_kaanntetty['Kuinka moni ostaa jasenyyden?'][0], final_ainoastaan_hakekemukset_taulu_kaanntetty['Kuinka moni ostaa jasenyyden?'][0]]
Blista = [hakemus_maarat_kaannetty['kuinka monella prosentilla on hakemus'][1], ainoastaan_hakekemukset_taulu_kaanntetty['Kuinka moni ostaa jasenyyden?'][1], final_ainoastaan_hakekemukset_taulu_kaanntetty['Kuinka moni ostaa jasenyyden?'][1]]
x_placement_1 = [2*element + 0.8*1 for element in range(3)]
x_placement_2 = [2*element + 0.8*2 for element in range(3)]
x_placement_ticks = [1.2 + x * 2 for x in range(3)]
plt.bar(x_placement_1, Alista, color = 'blue', label = 'A, Kuntotesti')
plt.bar(x_placement_2, Blista, color = 'orange', label = 'B, Ei kuntotestia')
ax.set_xticks(x_placement_ticks)
ax.set_xticklabels(xt)
ax.set_yticks(np.arange(0,1.1,0.1))
ax.set_yticklabels([str(t) + ' %' for t in range(0, 110, 10)])
plt.title('Kuntotestin vaikutus vierailijoidenkuntosalihakemuksien, -jäsenyyksien määriin')
plt.legend()
plt.show()