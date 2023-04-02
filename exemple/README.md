# Exemple 

```sh-sesion
$ issurge ./exemple.issurge --debug --dry-run

Running with options: {'--': False,
 '--debug': True,
 '--dry-run': True,
 '--help': False,
 '<file>': 'issues',
 '<submitter-args>': []}
@me ~by:lubin                                            Making children from  ~by:lubin @me
~area:search                                                     Making children from  ~by:lubin ~area:search @me
mettre un bouton "rechercher" à la place de "voir                        Made mettre un bouton "rechercher"  (...) ~by:lubin ~area:search @me
~responsive quand on rentre les informations, fair                       Made quand on rentre les informatio (...) ~responsive ~by:lubin ~area:search @me
~notsure enlever la mise à jour automatique de la                        Made enlever la mise à jour automat (...) ~by:lubin ~area:search ~notsure @me
photo cliquable comme le reste du bloc                                   Made photo cliquable comme le reste (...) ~by:lubin ~area:search @me
~styling bouton "voir sur la carte" et "retour à l                       Made bouton "voir sur la carte" et  (...) ~by:lubin ~area:search ~styling @me
~styling bouton "déposer une annonce" en bleu et a                       Made bouton "déposer une annonce" e (...) ~by:lubin ~area:search ~styling @me
~styling bouton "connexion" de la même taille de "                       Made bouton "connexion" de la même  (...) ~by:lubin ~area:search ~styling @me
~notsure choisir si le tri est croissant ou décroi                       Made choisir si le tri est croissan (...) ~by:lubin ~area:search ~notsure @me
~area:navigation                                                 Making children from  ~by:lubin ~area:navigation @me
~responsive                                                              Making children from  ~responsive ~by:lubin ~area:navigation @me
bouton "déposer une annonce" en bleu                                             Made bouton "déposer une annonce" e (...) ~responsive ~by:lubin ~area:navigation @me
mettre des majuscules à "recherche", "administrati                               Made mettre des majuscules à "reche (...) ~responsive ~by:lubin ~area:navigation @me
sur ordi, ajouter le bouton "déposer une annonce"                        Made sur ordi, ajouter le bouton "d (...) ~by:lubin ~area:navigation @me
~notsure ~bug le bouton mes annonces n'apparait pa                       Made le bouton mes annonces n'appar (...) ~bug ~by:lubin ~area:navigation ~notsure @me
~feature création d'annonces par les admins:                             création d'annonces par les ad (...) ~feature expects a description
~feature création d'annonces par les admins:                             Made création d'annonces par les ad (...) ~feature ~by:lubin ~area:navigation @me [...]
~notsure bouton aide qui renvoie sur le mail loca7                       Made bouton aide qui renvoie sur le (...) ~by:lubin ~area:navigation ~notsure @me
~area:accounts                                                   Making children from  ~area:accounts ~by:lubin @me
/login: ajouter un espace entre "Mot de passe perd                       Made /login: ajouter un espace entr (...) ~area:accounts ~by:lubin @me
/login: expliquer quand il y a redirection:                              /login: expliquer quand il y a (...) expects a description
/login: expliquer quand il y a redirection:                              Made /login: expliquer quand il y a (...) ~area:accounts ~by:lubin @me [...]
~notsure /register: mettre nom et prénom séparemen                       /register: mettre nom et préno (...) ~notsure expects a description
~notsure /register: mettre nom et prénom séparemen                       Made /register: mettre nom et préno (...) ~area:accounts ~by:lubin ~notsure @me [...]
/register: obligatoire : que le nom et mail                              Made /register: obligatoire : que l (...) ~area:accounts ~by:lubin @me
/register: remplacer "optionnel" par "conseillé"                         Made /register: remplacer "optionne (...) ~area:accounts ~by:lubin @me
/register: le picto information par rapport au tem                       Made /register: le picto informatio (...) ~area:accounts ~by:lubin @me
~area:add                                                        Making children from  ~by:lubin ~area:add @me
plus d'espace entre "Nouvelle annonce", "Votre ann                       Made plus d'espace entre "Nouvelle  (...) ~by:lubin ~area:add @me
mettre explication validation par admin plus en va                       mettre explication validation  (...) expects a description
mettre explication validation par admin plus en va                       Made mettre explication validation  (...) ~by:lubin ~area:add @me [...]
~bug barre noire très bizarre pour le choix du typ                       Made barre noire très bizarre pour  (...) ~bug ~by:lubin ~area:add @me
mettre des * pour les champs obligatoires                                Made mettre des * pour les champs o (...) ~by:lubin ~area:add @me
ne pas mettre charges et caution obigatoire:                             ne pas mettre charges et cauti (...) expects a description
ne pas mettre charges et caution obigatoire:                             Made ne pas mettre charges et cauti (...) ~by:lubin ~area:add @me [...]
mettre la date du jour par défaut                                        Made mettre la date du jour par déf (...) ~by:lubin ~area:add @me
~notsure interdire une date inférieure à celle du                        interdire une date inférieure  (...) ~notsure expects a description
~notsure interdire une date inférieure à celle du                        Made interdire une date inférieure  (...) ~by:lubin ~notsure ~area:add @me [...]
Ajouter plus d'aspects:                                                  Ajouter plus d'aspects expects a description
Ajouter plus d'aspects:                                                  Made Ajouter plus d'aspects ~by:lubin ~area:add @me [...]
~bug <InputRichText> liste et lien ne fonctionne p                       Made <InputRichText> liste et lien  (...) ~bug ~by:lubin ~area:add @me
<InputRichText> laisser le bouton gras/italique "e                       Made <InputRichText> laisser le bou (...) ~by:lubin ~area:add @me
<InputImages> mettre "cliquez dans cette zone" ava                       Made <InputImages> mettre "cliquez  (...) ~by:lubin ~area:add @me
~area:manage                                                     Making children from  ~by:lubin ~area:manage @me
bouton "nouvelle annonce" en bleu et plus gros                           Made bouton "nouvelle annonce" en b (...) ~by:lubin ~area:manage @me
préciser le nombre d'annonce à côté de "mes annonc                       Made préciser le nombre d'annonce à (...) ~by:lubin ~area:manage @me
préciser quelles annonces sont en attente de valid                       Made préciser quelles annonces sont (...) ~by:lubin ~area:manage @me
changer les boutons dans les blocs, mettre : "Modi                       Made changer les boutons dans les b (...) ~by:lubin ~area:manage @me
~bug la suppression d'annonce ne fonctionne pas                          Made la suppression d'annonce ne fo (...) ~bug ~by:lubin ~area:manage @me
~area:admin                                                      Making children from  ~by:lubin ~area:admin @me
sur PC, possibilité de cliquer sur la photo, le n°                       Made sur PC, possibilité de cliquer (...) ~by:lubin ~area:admin @me
~responsive ~bug arrière plan des boutons d'action                       Made arrière plan des boutons d'act (...) ~responsive ~by:lubin ~area:admin ~bug @me
~responsive faire descendre le clavier quand on fa                       Made faire descendre le clavier qua (...) ~responsive ~by:lubin ~area:admin @me
~feature catégorie "tout":                                               catégorie "tout" ~feature expects a description
~feature catégorie "tout":                                               Made catégorie "tout" ~feature ~by:lubin ~area:admin @me [...]
~notsure ~feature catégorie "signalées"                                  Made catégorie "signalées" ~feature ~by:lubin ~area:admin ~notsure @me
~bug appartements pas triés par date de dernière m                       Made appartements pas triés par dat (...) ~bug ~by:lubin ~area:admin @me
~feature pastille orange pour le nombre d'annonce                        Made pastille orange pour le nombre (...) ~feature ~by:lubin ~area:admin @me
~bug ~important quand on appuie sur valider ou pub                       quand on appuie sur valider ou (...) ~important ~bug expects a description
~bug ~important quand on appuie sur valider ou pub                       Made quand on appuie sur valider ou (...) ~important ~bug ~by:lubin ~area:admin @me [...]
~feature boutons pour la catégorie "en ligne" :                          boutons pour la catégorie "en  (...) ~feature expects a description
~feature boutons pour la catégorie "en ligne" :                          Made boutons pour la catégorie "en  (...) ~feature ~by:lubin ~area:admin @me [...]
~bug ~important "suppr." ne fonctionne pas depuis                        Made "suppr." ne fonctionne pas dep (...) ~important ~bug ~by:lubin ~area:admin @me
~typo mettre "archivées"                                                 Made mettre "archivées" ~by:lubin ~typo ~area:admin @me
changer boutons pour la catégorie "archivées"                            Made changer boutons pour la catégo (...) ~by:lubin ~area:admin @me
~area:view                                                       Making children from  ~area:view ~by:lubin @me
enlever calendrier et contact, envoyer un mail et                        Made enlever calendrier et contact, (...) ~area:view ~by:lubin @me
~responsive plus d'espace entre téléphone et les b                       Made plus d'espace entre téléphone  (...) ~responsive ~area:view ~by:lubin @me
~bug ~important la photo de mon annonce test n'app                       Made la photo de mon annonce test n (...) ~important ~bug ~area:view ~by:lubin @me
~feature ajouter un bouton accueil en bleu en haut                       Made ajouter un bouton accueil en b (...) ~area:view ~by:lubin ~feature @me
ajouter de l'espace entre "Description" et le text                       Made ajouter de l'espace entre "Des (...) ~area:view ~by:lubin @me
~notsure mettre la police du texte de description                        Made mettre la police du texte de d (...) ~area:view ~by:lubin ~notsure @me
~feature ~awaiting mettre les noms de famille des                        Made mettre les noms de famille des (...) ~area:view ~by:lubin ~awaiting ~feature @me
plus d'espace entre le bloc de gauche avec les inf                       Made plus d'espace entre le bloc de (...) ~area:view ~by:lubin @me
~bug ~important le signalement de fonction pas:                          le signalement de fonction pas ~important ~bug expects a description
~bug ~important le signalement de fonction pas:                          Made le signalement de fonction pas ~important ~bug ~area:view ~by:lubin @me [...]
~notsure fond photo blanc plutôt que noir                                Made fond photo blanc plutôt que no (...) ~area:view ~by:lubin ~notsure @me
~nosture ~possibilité de les afficher en plus gran                       Made de les afficher en plus grand ~area:view ~by:lubin ~nosture ~possibilité @me
~nosture animation de défilement des photos                              Made animation de défilement des ph (...) ~area:view ~by:lubin ~nosture @me
~area:edit                                                       Making children from  ~area:edit ~by:lubin @me
bandeau modifications en attente : en rouge avec l                       Made bandeau modifications en atten (...) ~area:edit ~by:lubin @me
~notsure quand il n'y a aucune modification, ne pa                       Made quand il n'y a aucune modifica (...) ~area:edit ~by:lubin ~notsure @me
~notsure [PC] attention : quand on modifie le prix                       Made [PC] attention : quand on modi (...) ~area:edit ~by:lubin ~notsure @me
~area:account                                                    Making children from  ~area:account ~by:lubin @me
profil: préciser "Ces informations apparaitront su                       Made profil: préciser "Ces informat (...) ~area:account ~by:lubin @me
~feature                                                         Making children from  ~feature ~by:lubin @me
tutos interactifs :                                                      tutos interactifs expects a description
tutos interactifs :                                                      Made tutos interactifs ~feature ~by:lubin @me [...]
faire un arbre des admins avec nom prénom années A                       Made faire un arbre des admins avec (...) ~feature ~by:lubin @me
Submitting issues...
Would run glab issue new -t "mettre un bouton \"rechercher\" à la place de \"voir sur la carte\" (c'est plus clair surtout sur mobile)" -d "" -a @me -l by:lubin -l area:search
Would run glab issue new -t "quand on rentre les informations, faire descendre le clavier quand on fait ok" -d "" -a @me -l responsive -l by:lubin -l area:search
Would run glab issue new -t "enlever la mise à jour automatique de la recherche" -d "" -a @me -l by:lubin -l area:search -l notsure
Would run glab issue new -t "photo cliquable comme le reste du bloc" -d "" -a @me -l by:lubin -l area:search
Would run glab issue new -t "bouton \"voir sur la carte\" et \"retour à la liste\" en bleu" -d "" -a @me -l by:lubin -l area:search -l styling
Would run glab issue new -t "bouton \"déposer une annonce\" en bleu et aussi gros que le bouton \"voir sur la carte\"" -d "" -a @me -l by:lubin -l area:search -l styling
Would run glab issue new -t "bouton \"connexion\" de la même taille de \"déposer une annonce\"" -d "" -a @me -l by:lubin -l area:search -l styling
Would run glab issue new -t "choisir si le tri est croissant ou décroissant" -d "" -a @me -l by:lubin -l area:search -l notsure
Would run glab issue new -t "bouton \"déposer une annonce\" en bleu" -d "" -a @me -l responsive -l by:lubin -l area:navigation
Would run glab issue new -t "mettre des majuscules à \"recherche\", \"administration\" et \"mon compte\"" -d "" -a @me -l responsive -l by:lubin -l area:navigation
Would run glab issue new -t "sur ordi, ajouter le bouton \"déposer une annonce\" en bleu" -d "" -a @me -l by:lubin -l area:navigation
Would run glab issue new -t "le bouton mes annonces n'apparait pas quand je suis connecté en admin, j'arrive à y accéder que en faisant \"déposer une annonce\" quand je ne suis pas connecté" -d "" -a @me -l bug -l by:lubin -l area:navigation -l 
notsure
Would run glab issue new -t "création d'annonces par les admins" -d "il arrive souvent qu'on en ajoute nous même : dans ce cas, créer un type d'annonce spécial où on rentre les coordonnées du proprio mais l'annonce appartient à l'admin et apparait 
dans mes annonces. Normalement ça arrivera plus beaucoup mais vaut mieux prévoir le coup pour la première année et pour les habitués
" -a @me -l feature -l by:lubin -l area:navigation
Would run glab issue new -t "bouton aide qui renvoie sur le mail loca7. Mettre ce bouton un peu partout." -d "" -a @me -l by:lubin -l area:navigation -l notsure
Would run glab issue new -t "/login: ajouter un espace entre \"Mot de passe perdu ?\" et le bouton \"Réinitialisez-le\"" -d "" -a @me -l area:accounts -l by:lubin
Would run glab issue new -t "/login: expliquer quand il y a redirection" -d "- [ ] depuis /appartements/ajouter: \"Vous devez vous connecter pour déposer et gérer vos annonces. Si vous n'avez pas de compte, créez-en un !\"
" -a @me -l area:accounts -l by:lubin
Would run glab issue new -t "/register: mettre nom et prénom séparement" -d "\"nom complet\" pas assez clair (faut penser aux petits vieux)
" -a @me -l area:accounts -l by:lubin -l notsure
Would run glab issue new -t "/register: obligatoire : que le nom et mail" -d "" -a @me -l area:accounts -l by:lubin
Would run glab issue new -t "/register: remplacer \"optionnel\" par \"conseillé\"" -d "" -a @me -l area:accounts -l by:lubin
Would run glab issue new -t "/register: le picto information par rapport au temps de hack du mdp ne renvoie vers rien" -d "" -a @me -l area:accounts -l by:lubin
Would run glab issue new -t "plus d'espace entre \"Nouvelle annonce\", \"Votre annonce sera validée .....\" et \"type de logement\"" -d "" -a @me -l by:lubin -l area:add
Would run glab issue new -t "mettre explication validation par admin plus en valeur" -d "- [ ]
- [ ] La remettre au-dessus du bouton \"Poster\"
" -a @me -l by:lubin -l area:add
Would run glab issue new -t "barre noire très bizarre pour le choix du type de logement -> l'enlever ou la mettre en blanc" -d "" -a @me -l bug -l by:lubin -l area:add
Would run glab issue new -t "mettre des * pour les champs obligatoires" -d "" -a @me -l by:lubin -l area:add
Would run glab issue new -t "ne pas mettre charges et caution obigatoire" -d "- [ ] prendre exemple sur l'ancien loca7 pour le petit texte à ajouter
" -a @me -l by:lubin -l area:add
Would run glab issue new -t "mettre la date du jour par défaut" -d "" -a @me -l by:lubin -l area:add
Would run glab issue new -t "interdire une date inférieure à celle du jour" -d "j'ai essayé et ça me renvoie sur une page qui fait \"oops, impossible de poster l'annonce\"
" -a @me -l by:lubin -l notsure -l area:add
Would run glab issue new -t "Ajouter plus d'aspects" -d "- [ ] Ascenseur
- [ ] Fibre
- [ ] ...
Plus il y en a, mieux c'est
" -a @me -l by:lubin -l area:add
Would run glab issue new -t "<InputRichText> liste et lien ne fonctionne pas" -d "" -a @me -l bug -l by:lubin -l area:add
Would run glab issue new -t "<InputRichText> laisser le bouton gras/italique \"enfoncé\" quand on est sur un texte gras/italique" -d "" -a @me -l by:lubin -l area:add
Would run glab issue new -t "<InputImages> mettre \"cliquez dans cette zone\" avant \"glissez-déposer vos fichiers ici\"" -d "" -a @me -l by:lubin -l area:add
Would run glab issue new -t "bouton \"nouvelle annonce\" en bleu et plus gros" -d "" -a @me -l by:lubin -l area:manage
Would run glab issue new -t "préciser le nombre d'annonce à côté de \"mes annonces\"" -d "" -a @me -l by:lubin -l area:manage
Would run glab issue new -t "préciser quelles annonces sont en attente de validation, de modification et archivées, ou alors faire un système de filtrage comme dans le panneau administration" -d "" -a @me -l by:lubin -l area:manage
Would run glab issue new -t "changer les boutons dans les blocs, mettre : \"Modifier\" \"Archiver\" \"Supprimer\" pour les annonces en ligne et \"Modifier\" \"Mettre en ligne\" \"Supprimer\" pour les annonces archivées" -d "" -a @me -l by:lubin -l 
area:manage
Would run glab issue new -t "la suppression d'annonce ne fonctionne pas" -d "" -a @me -l bug -l by:lubin -l area:manage
Would run glab issue new -t "sur PC, possibilité de cliquer sur la photo, le n°, prix, adresse, nom, signalement et date, le tout renvoyant vers l'annonce" -d "" -a @me -l by:lubin -l area:admin
Would run glab issue new -t "arrière plan des boutons d'action transparent" -d "" -a @me -l responsive -l by:lubin -l area:admin -l bug
Would run glab issue new -t "faire descendre le clavier quand on fait OK sur la barre de recherche" -d "" -a @me -l responsive -l by:lubin -l area:admin
Would run glab issue new -t "catégorie \"tout\"" -d "mettre une couleur sur le numéro de l'annonce : vert pour en attente, orange pour archivées
" -a @me -l feature -l by:lubin -l area:admin
Would run glab issue new -t "catégorie \"signalées\"" -d "" -a @me -l feature -l by:lubin -l area:admin -l notsure
Would run glab issue new -t "appartements pas triés par date de dernière modification" -d "" -a @me -l bug -l by:lubin -l area:admin
Would run glab issue new -t "pastille orange pour le nombre d'annonce en attente" -d "" -a @me -l feature -l by:lubin -l area:admin
Would run glab issue new -t "quand on appuie sur valider ou publier, le bouton reste enfoncé jusqu'à ce qu'on clique ailleurs" -d "et l'annonce ne bouge pas de la catégorie \"en attente\". Quand on refresh, on tombe sur une page \"Oops! erreur 
interne\", mais quand on revient sur administration, l'annonce a bien été validée et est mainteneant dans la catégorie \"en ligne\".
" -a @me -l important -l bug -l by:lubin -l area:admin
Would run glab issue new -t "boutons pour la catégorie \"en ligne\"" -d "\"Archiver\" \"Modifier\" \"Suppr.\", avec supprimer qui supprime définitivement
" -a @me -l feature -l by:lubin -l area:admin
Would run glab issue new -t "\"suppr.\" ne fonctionne pas depuis \"en ligne\"" -d "" -a @me -l important -l bug -l by:lubin -l area:admin
Would run glab issue new -t "mettre \"archivées\"" -d "" -a @me -l by:lubin -l typo -l area:admin
Would run glab issue new -t "changer boutons pour la catégorie \"archivées\"" -d "" -a @me -l by:lubin -l area:admin
Would run glab issue new -t "enlever calendrier et contact, envoyer un mail et appeler suffit" -d "" -a @me -l area:view -l by:lubin
Would run glab issue new -t "plus d'espace entre téléphone et les boutons modifier-supprimer-archiver" -d "" -a @me -l responsive -l area:view -l by:lubin
Would run glab issue new -t "la photo de mon annonce test n'apparaît pas" -d "" -a @me -l important -l bug -l area:view -l by:lubin
Would run glab issue new -t "ajouter un bouton accueil en bleu en haut au milieu qui revient à la page d'accueil" -d "" -a @me -l area:view -l by:lubin -l feature
Would run glab issue new -t "ajouter de l'espace entre \"Description\" et le texte de description" -d "" -a @me -l area:view -l by:lubin
Would run glab issue new -t "mettre la police du texte de description en moins gras, en normal ou light" -d "" -a @me -l area:view -l by:lubin -l notsure
Would run glab issue new -t "mettre les noms de famille des proprio en majuscule" -d "" -a @me -l area:view -l by:lubin -l awaiting -l feature
Would run glab issue new -t "plus d'espace entre le bloc de gauche avec les infos et le bloc de description" -d "" -a @me -l area:view -l by:lubin
Would run glab issue new -t "le signalement de fonction pas" -d "\"oops! erreur interne\"
" -a @me -l important -l bug -l area:view -l by:lubin
Would run glab issue new -t "fond photo blanc plutôt que noir" -d "" -a @me -l area:view -l by:lubin -l notsure
Would run glab issue new -t "de les afficher en plus grand" -d "" -a @me -l area:view -l by:lubin -l nosture -l possibilité
Would run glab issue new -t "animation de défilement des photos" -d "" -a @me -l area:view -l by:lubin -l nosture
Would run glab issue new -t "bandeau modifications en attente : en rouge avec le texte centré" -d "" -a @me -l area:edit -l by:lubin
Would run glab issue new -t "quand il n'y a aucune modification, ne pas faire apparaitre en tant que modification" -d "" -a @me -l area:edit -l by:lubin -l notsure
Would run glab issue new -t "[PC] attention : quand on modifie le prix par exemple, quand on fait entrée ça enregistre l'ensemble des modifications et on revient sur l'annonce : faut enlever ça pcq les gens vont le faire à chaque fois et il y a aura
10 000 modifications" -d "" -a @me -l area:edit -l by:lubin -l notsure
Would run glab issue new -t "profil: préciser \"Ces informations apparaitront sur toutes vos annonces\"" -d "" -a @me -l area:account -l by:lubin
Would run glab issue new -t "tutos interactifs" -d "lancer le tuto -> un cercle apparaît sur les boutons sur lesquels cliquer et il est impossible de cliquer ailleurs
tutos pour : créer un compte, poster une annonce, modifier une annonce, archiver une annonce, remettre une annonce en ligne
" -a @me -l feature -l by:lubin
Would run glab issue new -t "faire un arbre des admins avec nom prénom années AE" -d "" -a @me -l feature -l by:lubin
```
