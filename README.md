# Tchai
## Description du projet
L'objectif de l'application Tchai est de concevoir un système de transactions électroniques avec une intégrité garantie, accessible
par le protocole HTTP.

## Structure de l'API
L'API est conçue avec le microframework Flask.  
Chaque route HTTP correspond à un cas d'utilisation, un service fourni par l'API.
On utilise les Pluggables Views de Flask pour avoir une approche basée sur des classes. Ce paradigme facilite la réutilisation du code en organisant la logique des routes HTTP en classes.  
Chaque classe héritant de ```ViewTchai``` (```tchaivX/views```) correspond à une route HTTP. Elles sont chacune associées à un fichier HTML qui lui sert de template (```tchaivX/templates```) pour retourner le résultat de chaque fonctionnalité.
Chaque View possède un lien vers le service de base de données pour persister ou récupérer des données (```tchaivX/stockage```) dans une base de données SQLite. Elles communiquent avec ce service par un modèle composé de deux classes ```Utilisateur``` et ```Transaction``` (```tchaivX/modele```).
Toutes les erreurs fonctionnelles ou techniques sont catchées puis encapsulées dans une classe héritant de ```ExceptionSerializable``` (```tchaivX/exceptions```). Un template d'erreur gère la conversion de l'exception en une page HTML.

## Auteurs
-	__Pierre-Nicolas CHASSAGNE__ : Pierre-Nicolas_Chassagne@etu.u-bourgogne.fr,
-	__Nicolas FORGERON__ : Nicolas_Forgeron@etu.u-bourgogne.fr.


## Tchai v1
Pour exécuter tchai v1, on exécute le fichier ```tchaiv1/main.py```.
### Exercice 3
-	__Ajouter un utilisateur__ :  
Une transaction est une somme d'argent transférer entre deux personnes à une date donnée.
Avant d'enregistrer une transaction, on doit créer au moins deux utilisateurs.
Pour ajouter un utilisateur, on utilise l'URI :  
```/ajouterUtilisateur```  
avec un body json comportant par exemple les informations :
```json
{
    "nomUtilisateur" : "test2",
    "montantInitialUtilisateur" : 20
}
```
La réponse envoyée est :
```html
<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta charset="utf-8" />
	<title></title>
</head>

<body>
	L'utilisateur test1 a été ajouté avec un montant initial de 20.0.
</body>

</html>
```
-	__Enregistrer une transaction__ :  
Pour enregistrer une transaction, on utilise l'URI :  
```/enregistrerTransaction```  
avec un body json comportant par exemple les informations :
```json
{
    "nomUtilisateur1" : "test1",
    "nomUtilisateur2" : "test2",
    "montantTransaction" : 20,
}
```
La réponse envoyée est :
```html
<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta charset="utf-8" />
	<title></title>
</head>

<body>
	La transaction a été enregistrée :
	test1 a donné 20.0 à test2 le 2021-12-17 09:15:29.538309.
</body>

</html>
```
Le montant de la transaction doit être positif sinon une exception sera levé.
```html
<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta charset="utf-8" />
	<title></title>
</head>

<body>
	<h4>
		Exception montant transaction
	</h4>
	<h4>
		Une erreur est survenue :
		<br />
        Une exception lors de la récupération du montant de la transaction : le montant de la transaction doit être positif ou nul.
    </h4>
		<br />
		<h4>Détails :</h4>
		<div>
			Status :
			500
		</div>
		<div>
			Stack Trace :
			<pre></pre>
		</div>
</body>

</html>
```

-	__Afficher les transactions__ :  
Pour afficher toutes les transactions dans l'ordre chronologique, on utilise l'URI :  
```/afficherTransactions```  
La réponse envoyée est :
```html
<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta charset="utf-8" />
	<title></title>
</head>

<body>
	La liste des transactions dans l'ordre chronologiques est :

	<div>test1 a donné 20.0 à test2 le 2021-12-17 09:15:29</div>

</body>

</html>
```
-	__Afficher les transactions d'un utilisateur__ :  
Pour afficher toutes les transactions dans l'ordre chronologique lié à un utilisateur, on utilise l'URI :  
```/afficherTransactionsAvecUtilisateur```  
avec un body json comportant par exemple les informations :
```json
{
    "nomUtilisateur" : "test1"
}
```
La réponse envoyée est :
```html
<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta charset="utf-8" />
	<title></title>
</head>

<body>
	La liste des transactions dans l'ordre chronologiques de l'utilisateur est :

	<div>test1 a donné 20.0 à test2 le 2021-12-17 09:15:29</div>

</body>

</html>
```
-	__Afficher le solde d'un compte utilisateur__ :  
Pour afficher le solde d'un compte utilisateur, on utilise l'URI :  
```/afficherSoldeCompte```  
avec un body json comportant par exemple les informations :
```json
{
    "nomUtilisateur" : "test1"
}
```
La réponse envoyée est :
```html
<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta charset="utf-8" />
	<title></title>
</head>

<body>
	Le solde du compte de l'utilisateur test1 est : 0.0.
</body>

</html>
```
### Exercice 4
__Attaque 1__  
Pour exécuter l'attaque 1, on exécute le fichier ```tchaiv1/tests/mainAttaque1.py```.
Celui-ci crée deux utilisateurs, une transaction et modifie le montant de cette transaction.  
Après l'attaque, il est impossible de savoir si le montant d'une transaction a été modifié.
On doit donc dans la version 2 calculer le hash de la transaction en cours pour tester si elle a été modifiée.


## Tchai v2
Pour exécuter tchai v2, on exécute le fichier ```tchaiv2/main.py```.
### Exercice 5
Avant d'enregistrer une transaction, on calcule son hash en concaténant les noms d'utilisateur, le montant et la date de transaction.
Par exemple le hash de la transaction ```test1test220.02021-12-17 11:10:02``` est :
```7789c71739fa3f40e639798b9d18e47e```  
La fonction de hachage est MD5.  
L'API HTTP pour enregistrer une transaction reste la même.

### Exercice 6
On ajoute l'action suivante :
-	__Vérifier l'intégrité des transactions__ :  
Pour vérifier l’intégrité des transactions en recalculant les hashs à partir des données et en les comparant avec les hashs stockés précédemment, on utilise l'URI :  
```/verifierIntegriteTransactions```  
La réponse envoyée est :
```html
<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta charset="utf-8" />
	<title></title>
</head>

<body>
	La liste des transactions non vérifiées dont le hash est incorrect sont :

</body>

</html>

```
### Exercice 7
__Attaque 1__
Pour exécuter l'attaque 1, on exécute le fichier ```tchaiv2/tests/mainAttaque1.py```.
Celui-ci crée deux utilisateurs, une transaction et modifie le montant de cette transaction.  
Après l'attaque, on détecte les transactions qui ont été modfifiées grâce au hash de chaque transaction.

### Exercice 8
__Attaque 2__
Pour exécuter l'attaque 2, on exécute le fichier ```tchaiv2/tests/mainAttaque2.py```.
Celui-ci crée deux utilisateurs, trois transactions de test1 vers test 2.
On supprime la première transaction de test1 vers test2.  
Après l'attaque, on ne peut pas détecter la transaction qui a été supprimée grâce au hash de chaque transaction car la vérification se base sur le hash de chaque transaction de manière unitaire.
On doit donc dans la version 3 calculer le hash avec la transaction en cours et les valeurs de la transaction précédente.


## Tchai v3
Pour exécuter tchai v2, on exécute le fichier ```tchaiv3/main.py```.
### Exercice 9
Avant d'enregistrer une transaction, on calcule son hash en concatenant les noms d'utilisateur, le montant, la date de transaction et le hash de la transaction précédente.
Pour le hash de la première transaction, on considère que le hash de la transaction précédente est une chaine de caractère vide.
Par exemple le hash de la transaction ```test1test220.02021-12-17 11:13:07``` avec comme hash de la transaction précédente ```e850ddabfc8a59ca361aab0b2b8828e8``` est :
```c6990f8374bdcb30e598076242aaaa75```
La fonction de hachage est MD5.  
L'API HTTP pour enregistrer une transaction reste la même.

### Exercice 10
__Attaque 1__  
Pour exécuter l'attaque 1, on exécute le fichier ```tchaiv3/tests/mainAttaque1.py```.
Celui-ci crée deux utilisateurs, une transaction et modifie le montant de cette transaction.  
Après l'attaque, on détecte les transactions qui ont été modfifié grâce au hash de chaque transaction.

__Attaque 2__  
Pour exécuter l'attaque 2, on exécute le fichier ```tchaiv3/tests/mainAttaque2.py```.
Celui-ci crée deux utilisateurs, trois transactions de test1 vers test 2.
On supprimela première transaction de test1 vers test2.  
Après l'attaque, on détecte la transaction suivant la transaction qui a été supprimée.
Le hash de la transaction détecté est recalculé et ne correspond pas au hash stocké car il est calculé avec la transaction précédente et celle-ci a été supprimée.
On détecte donc l'attaque.