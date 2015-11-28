# API Super Lachaise

Une base de données touristique avec API pour le cimetière du Père-Lachaise à Paris, enrichie en continu par les contributeurs d'[OpenStreetMap](https://www.openstreetmap.org/) et Wikimedia ([Wikipédia](https://fr.wikipedia.org/), [Wikidata](https://www.wikidata.org/), [Wikimedia Commons](https://commons.wikimedia.org/)).

L'application récupère les tombes et mémoriaux référencés au Père-Lachaise par OpenStreetMap, puis établit un lien vers les entrées correspondantes dans la base Wikidata, qu'il s'agisse des personnes ou des lieux. Les pages Wikipédia en plusieurs langues ainsi que les photographies issues de Wikimedia Commons sont aussi référencées.

Vous souhaitez réutiliser l'API ou y contribuer ? Retrouvez le projet sur [Github](https://github.com/MaximeLM/superlachaise_api).

Super Lachaise, c'est aussi une [application mobile](http://www.superlachaise.fr) qui vous accompagne dans votre visite du Père-Lachaise.

## Exemples d'utilisation

Afficher la liste des rubriques de l'API :  
[https://api.superlachaise.fr/perelachaise/api/](https://api.superlachaise.fr/perelachaise/api/)

Lister les entrées correspondant à Oscar Wilde dans les différentes rubriques :

 * OpenStreetMap : [https://api.superlachaise.fr/perelachaise/api/openstreetmap\_elements/?search=Oscar+Wilde](https://api.superlachaise.fr/perelachaise/api/openstreetmap_elements/?search=Oscar+Wilde)
 * Wikidata et Wikipédia : [https://api.superlachaise.fr/perelachaise/api/wikidata\_entries/?search=Oscar+Wilde](https://api.superlachaise.fr/perelachaise/api/wikidata_entries/?search=Oscar+Wilde)
 * Wikimedia Commons : [https://api.superlachaise.fr/perelachaise/api/wikimedia\_commons\_categories/?search=Oscar+Wilde](https://api.superlachaise.fr/perelachaise/api/wikimedia_commons_categories/?search=Oscar+Wilde)

Afficher les données agrégées pour Oscar Wilde :  
[https://api.superlachaise.fr/perelachaise/api/superlachaise\_pois/?search=Oscar+Wilde](https://api.superlachaise.fr/perelachaise/api/superlachaise_pois/?search=Oscar+Wilde)

### Recherche avancée

#### Par division

Lister les tombes et mémoriaux des divisions 76 et 97 du cimetière :  
[https://api.superlachaise.fr/perelachaise/api/superlachaise\_pois/?sector=76+97](https://api.superlachaise.fr/perelachaise/api/superlachaise_pois/?sector=76+97)

#### Par catégorie : profession, hommes ou femmes, tombes ou mémoriaux

Lister les tombes de personnalités liées au cinéma :  
[https://api.superlachaise.fr/perelachaise/api/superlachaise\_pois/?category=cinema](https://api.superlachaise.fr/perelachaise/api/superlachaise_pois/?category=cinema)

Lister les tombes de femmes liées au cinéma ou au théâtre :  
[https://api.superlachaise.fr/perelachaise/api/superlachaise\_pois/?category=women&category=cinema+theatre](https://api.superlachaise.fr/perelachaise/api/superlachaise_pois/?category=women&category=cinema+theatre)

Lister les mémoriaux :  
[https://api.superlachaise.fr/perelachaise/api/superlachaise\_pois/?category=memorial](https://api.superlachaise.fr/perelachaise/api/superlachaise_pois/?category=memorial)

#### Par dates de naissance ou de décès

Lister les tombes de personnalités ayant vécu au XIX<sup>e</sup> siècle :  
[https://api.superlachaise.fr/perelachaise/api/superlachaise\_pois/?born\_after=1800&died\_before=1900](https://api.superlachaise.fr/perelachaise/api/superlachaise_pois/?born_after=1800&died_before=1900)

#### Par date de dernière modification

Lister les entrées modifiées après une certaine date :  
[https://api.superlachaise.fr/perelachaise/api/superlachaise\_pois/?modified\_since=2015-06-12](https://api.superlachaise.fr/perelachaise/api/superlachaise_pois/?modified_since=2015-06-12)
