# Tchai
## Description du projet
L'objectif de l'application Tchai est de concevoir un système de transactions électroniques avec une intégrité garantie, accessible
par le protocole HTTP.

## Structure de l'API
L'API est conçue avec le microframework Flask.  
Chaque route HTTP correspond à un cas d'utilisation, un service fourni par l'API.
On utilise les Pluggables Views de Flask pour avoir une approche basée sur des classes. Ce paradigme facilite la réutilisation du code en organisant la logique des routes HTTP en classes.  
Chaque classe héritant de ```ViewTchai``` (```Tchai/tchaiX/views```) correspond à une route HTTP. Elles sont chacune associées à un fichier HTML qui lui sert de template (```Tchai/tchaiX/templates```) pour retourner le résultat de chaque fonctionnalité.
Chaque View possède un lien vers le service de base de données pour persister ou récupérer des données (```Tchai/tchaiX/stockage```) dans une base de données SQLite. Elles communiquent avec ce service par un modèle composé de deux classes ```Utilisateur``` et ```Transaction``` (```Tchai/tchaiX/modele```).
Toutes les erreurs fonctionnelles ou techniques sont catchées puis encapsulées dans une classe héritant de ```ExceptionSerializable``` (```Tchai/tchaiX/exceptions```). Un template d'erreur gère la conversion de l'exception en une page HTML.

## Installation
-	Cloner le projet,
-	Installer les dépendances contenues dans le requirements.txt :
```pip install -r requirements.txt```

## Auteurs
-	__Pierre-Nicolas CHASSAGNE__ : Pierre-Nicolas_Chassagne@etu.u-bourgogne.fr,
-	__Nicolas FORGERON__ : Nicolas_Forgeron@etu.u-bourgogne.fr.


## Tchai v1
Pour exécuter tchai v1, on exécute le fichier ```Tchai/tchai1/main.py```.
### Exercice 3
-	__Ajouter un utilisateur__ :  
Une transaction est une somme d'argent transférer entre deux personnes à une date donnée.
Avant d'enregistrer une transaction, on doit créer au moins deux utilisateurs.
Pour ajouter un utilisateur, on utilise l'URI :  
```/ajouterUtilisateur```  
avec un body json comportant par exemple les informations :
```json
{
    "nomUtilisateur" : "test1",
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
Pour exécuter l'attaque 1, on exécute le fichier ```Tchai/tchai1/tests/mainAttaque1.py```.
Celui-ci crée deux utilisateurs, une transaction et modifie le montant de cette transaction.  
Après l'attaque, il est impossible de savoir si le montant d'une transaction a été modifié.
On doit donc dans la version 2 calculer le hash de la transaction en cours pour tester si elle a été modifiée.


## Tchai v2
Pour exécuter tchai v2, on exécute le fichier ```Tchai/tchai2/main.py```.
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
Pour exécuter l'attaque 1, on exécute le fichier ```Tchai/tchai2/tests/mainAttaque1.py```.
Celui-ci crée deux utilisateurs, une transaction et modifie le montant de cette transaction.  
Après l'attaque, on détecte les transactions qui ont été modfifiées grâce au hash de chaque transaction.

### Exercice 8
__Attaque 2__
Pour exécuter l'attaque 2, on exécute le fichier ```Tchai/tchai2/tests/mainAttaque2.py```.
Celui-ci crée deux utilisateurs, trois transactions de test1 vers test 2.
On supprime la première transaction de test1 vers test2.  
Après l'attaque, on ne peut pas détecter la transaction qui a été supprimée grâce au hash de chaque transaction car la vérification se base sur le hash de chaque transaction de manière unitaire.
On doit donc dans la version 3 calculer le hash avec la transaction en cours et les valeurs de la transaction précédente.


## Tchai v3
Pour exécuter tchai v3, on exécute le fichier ```Tchai/tchai3/main.py```.
### Exercice 9
Avant d'enregistrer une transaction, on calcule son hash en concatenant les noms d'utilisateur, le montant, la date de transaction et le hash de la transaction précédente.
Pour le hash de la première transaction, on considère que le hash de la transaction précédente est une chaine de caractère vide.
Par exemple le hash de la transaction ```test1test220.02021-12-17 11:13:07``` avec comme hash de la transaction précédente ```e850ddabfc8a59ca361aab0b2b8828e8``` est :
```c6990f8374bdcb30e598076242aaaa75```
La fonction de hachage est MD5.  
L'API HTTP pour enregistrer une transaction reste la même.

### Exercice 10
__Attaque 1__  
Pour exécuter l'attaque 1, on exécute le fichier ```Tchai/tchai3/tests/mainAttaque1.py```.
Celui-ci crée deux utilisateurs, une transaction et modifie le montant de cette transaction.  
Après l'attaque, on détecte les transactions qui ont été modfifié grâce au hash de chaque transaction.

__Attaque 2__  
Pour exécuter l'attaque 2, on exécute le fichier ```Tchai/tchai3/tests/mainAttaque2.py```.
Celui-ci crée deux utilisateurs, trois transactions de test1 vers test 2.
On supprime la première transaction de test1 vers test2.  
Après l'attaque, on détecte la transaction suivant la transaction qui a été supprimée.
Le hash de la transaction détecté est recalculé et ne correspond pas au hash stocké car il est calculé avec la transaction précédente et celle-ci a été supprimée.
On détecte donc l'attaque.

### Exercice 11
__Attaque 3__  
Pour exécuter l'attaque 3, on exécute le fichier ```Tchai/tchai3/tests/mainAttaque3.py```.
Celui-ci crée deux utilisateurs. On suppose que l'attaquant connait la méthode de calcul de hash et peut enregistrer des transactions.
On insère une transaction de test1 vers test2.  
Ici, l'utilisateur test2 utilise l'utilisateur test1 pour faire une transaction.  
Après l'attaque, on ne peut pas détecter les transactions qui ont été supprimé
L'attaque consite à ce que test2 falsifie l'identité de test1.  
On doit donc dans la version 4 prouver que ce sont bien les utilisateurs qui effectue des transaction avec la cryptographie assymétrique.


## Tchai v4
Pour exécuter tchai v4, on exécute le fichier ```Tchai/tchai4/main.py```.
### Exercice 13
Pour qu'une transaction soit valide, il faut fournir en plus des deux noms d'utilisateurs et du montant une signature.  
On génère une paire de clés RSA par utilisateur.  
La signature est obtenue en signant la transaction hachée avec la clé privée.
La clé publique permet de vérifier la signature de la transaction avant de l'enregistrer.  
On s'assure ainsi de l'authenticité de l'expéditeur.

On ajoute et on modifie les actions suivantes :
-	__Ajouter un utilisateur__ :  
Pour ajouter un utilisateur, on utilise l'URI :  
```/ajouterUtilisateur```  
avec un body json comportant par exemple les informations :
```json
{
    "nomUtilisateur" : "test2",
    "montantInitialUtilisateur" : 20
}
```
On génère une paire de clés RSA.  
La clé publique est stockée dans une nouvelle colonne de la table utilisateur de la base de données.  
La clé privée est encodée en abse64 et transmise dans la réponse HTTP.  
Elle est également sauvegardée dans le fichier ```<nomUtilisateur>.pem```.  
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
	Sa clé publique est :
	-----BEGIN PUBLIC KEY-----
	MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuCPD1CndYauV9da7MmEO
	hpuOtcoGjV5xCcUKBLcgVJZ7LZS3/7v3QDcL+NrkJwA4GLrLW38W+DhwkBATusQm
	yuybyvnefJL4ywuuhIMH4sHvmprKB1BF56dW2jh6s6yiB0MYPHaosK3tWkDqnhAh
	ZNNmfjM4o6AgUIe4+DgdXwx+NqjrcSr3tS4/qNC37ASQyRZywNvEwG5TjQIK7Urc
	Ok6YgCJOYTrZHK6R2hmUx2HNw8taMWuUULXsPvmG4+ntO52nc4DbM9dtCmUxUdBc
	uoWc2tWOfQxT5GoqtCkkPfMdaRp0MOErbvrfRtw9PSUILQt7PJzY684V/uZu2vn3
	4QIDAQAB
	-----END PUBLIC KEY-----.
	Sa clé privée est dans le fichier test1.pem :
	LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcFFJQkFBS0NBUUVBdUNQRDFDbmRZYXVWOWRhN01tRU9ocHVPdGNvR2pWNXhDY1VLQkxjZ1ZKWjdMWlMzCi83djNRRGNMK05ya0p3QTRHTHJMVzM4VytEaHdrQkFUdXNRbXl1eWJ5dm5lZkpMNHl3dXVoSU1INHNIdm1wcksKQjFCRjU2ZFcyamg2czZ5aUIwTVlQSGFvc0szdFdrRHFuaEFoWk5ObWZqTTRvNkFnVUllNCtEZ2RYd3grTnFqcgpjU3IzdFM0L3FOQzM3QVNReVJaeXdOdkV3RzVUalFJSzdVcmNPazZZZ0NKT1lUclpISzZSMmhtVXgySE53OHRhCk1XdVVVTFhzUHZtRzQrbnRPNTJuYzREYk05ZHRDbVV4VWRCY3VvV2MydFdPZlF4VDVHb3F0Q2trUGZNZGFScDAKTU9FcmJ2cmZSdHc5UFNVSUxRdDdQSnpZNjg0Vi91WnUydm4zNFFJREFRQUJBb0lCQUFRMzlncmltMmE3SHc0MAorV0NPNkkyNUN6N0RFazI3Y3RxazRlMFFHcmlUWXI2dFpqNkFzbm85Tkp3U3ZEakFSSmk4OFU4ZklSSW1YVjVRCmp2b250NldOSUlmWXZBSVZ2aWROTlFZbVNCaEg1Z2JRU21YNjN1SWU4MktBR2lBTENjS0J0UkRBRFc3d1NpUjMKNGFRbHhaVVZNb2M4UWswOTNEV3FHVmpPOU0zT1RoRTJ0Z2xNelFHTW02KzNjV3J1MmFrYS9YbkJEckpjMENBSApMWTJsWkdrZEZtRWdKRHFqSndOd0JzWDkrR0JUKzJTUnJpZWVoRDVmWkxCMFVXbmF2aTJqbTJQOHNUbTFyRUJDCjlVbHdoMmorMW94VUhPUkttMjhlRmVPTDFvdlZLWWs0MTdoWCtDekJmUitadXJHV1QweFZLVFM0aG1MdHNzamgKVC9qaFRJRUNnWUVBem9LemRVTEVEYzdhdEdHemZHa0wwdCt6RjdMS1ZZa3Nab0NwZ2ZNcXZkYWhWSUMwUG5OdQpFSzR1SERsUmZiSDI5bGFaV0plWnk0dWxCeHBZL3VqUEZQdnhOVk5LczFwbWE0dXFyZU44U3ppU0tjaE5oQVNkCmpEeHVZd2JrOWlMTG1jWWZlbDlEcHVpVUV2Y2RGemFxY1QyczVQSjN5bGFtMGlSUkFjb2xhOEVDZ1lFQTVFU2cKUTJhL3gyaTF2QzJjejFreC9tRlB1K2JiZlR0cGNUUm5zaXhGKzJuMExNTXFBM290SWx0VnJqTXp6b2E2ODNjegpMdFE5ckJuOE9MOWp0MHhQOWlrREVTc0RndzJxTEh2VGlZTU4vRFk4dDBHRkxldGlVNklPSVJySllYT2tXRkVLCjBqcjBPZUY1eHNseWVuelpwTFg3Rk1mVWlqSGRCeDYzRlQ2OEZDRUNnWUVBbjh2VFFiRmdNNjhVM08rZEMyL2QKamxjN0plTmJYY1MvYnJHd2VMWEpKUXluMmRPZHBaVjhYYnZxUWp5NEtpTkRqbXFFVG1GQXlKaE9JcWpvcEpkUgpabE50Mm0yUktDZVRpVFNSNWV4WmlYdEUzci8zKzJmMjRVVUJ4ZTdYelA0dnZkWHBGYkFSa1YzMjlwWHhGTDFnCk5qQWJVUzJ1TkF2SkdtS3ZyRXJYbWdFQ2dZRUFnZGMvU2RlQ01zMHV3cEUzWndJWFc5akNYK0ZhN0FzRldTMHoKNXJja1AzUHZQaDd0SVBrMy94and6WnUyVmoxd3pkZjV0eU5teVNRbXdhaXI4YkZvc2w1MXJpaEhZUjQrcy9yagpRbzdYUDZVaU9DTCt2RFh0d2lDbDVOSzF4Y2JmcnBTNmtRYVRzUEMrTWdLWUtYQW01SGZYRCtUeTBvQzJkcnhUCjY3TzVpOEVDZ1lFQXNqSlgwU3NaRmU1WkhXSFdXTnA1bkxCR3JMQ01hVjltbVg3bTBERmo3UHhTNW1DSmNqK2sKRHZyK0pMN1BySk54bFpGUnNYVHdaUVVLd0MvbWNTRThCbGFuMENKWWRDaDFKL2JFMGJ4NmlLNlFLMXNWdG85ZQpNU2dTVnZiNzZEL0xyT3V0RitZeFEwQU5LT2hLYmtaNld1S2M0TjhPeG5Jb2Y1SC9yOVpNNWVJPQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQ==.
</body>

</html>
```

-	__Signer une transaction__ :  
Pour vérifier l’intégrité des transactions en recalculant les hashs à partir des données et en les comparant avec les hashs stockés précédemment, on utilise l'URI :  
```/signerTransaction```    
avec un body json comportant par exemple les informations :
```json
{
    "nomUtilisateur1" : "test1",
    "nomUtilisateur2" : "test2",
    "montantTransaction" : 20,
    "clePriveeUtilisateur1": "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcFFJQkFBS0NBUUVBdUNQRDFDbmRZYXVWOWRhN01tRU9ocHVPdGNvR2pWNXhDY1VLQkxjZ1ZKWjdMWlMzCi83djNRRGNMK05ya0p3QTRHTHJMVzM4VytEaHdrQkFUdXNRbXl1eWJ5dm5lZkpMNHl3dXVoSU1INHNIdm1wcksKQjFCRjU2ZFcyamg2czZ5aUIwTVlQSGFvc0szdFdrRHFuaEFoWk5ObWZqTTRvNkFnVUllNCtEZ2RYd3grTnFqcgpjU3IzdFM0L3FOQzM3QVNReVJaeXdOdkV3RzVUalFJSzdVcmNPazZZZ0NKT1lUclpISzZSMmhtVXgySE53OHRhCk1XdVVVTFhzUHZtRzQrbnRPNTJuYzREYk05ZHRDbVV4VWRCY3VvV2MydFdPZlF4VDVHb3F0Q2trUGZNZGFScDAKTU9FcmJ2cmZSdHc5UFNVSUxRdDdQSnpZNjg0Vi91WnUydm4zNFFJREFRQUJBb0lCQUFRMzlncmltMmE3SHc0MAorV0NPNkkyNUN6N0RFazI3Y3RxazRlMFFHcmlUWXI2dFpqNkFzbm85Tkp3U3ZEakFSSmk4OFU4ZklSSW1YVjVRCmp2b250NldOSUlmWXZBSVZ2aWROTlFZbVNCaEg1Z2JRU21YNjN1SWU4MktBR2lBTENjS0J0UkRBRFc3d1NpUjMKNGFRbHhaVVZNb2M4UWswOTNEV3FHVmpPOU0zT1RoRTJ0Z2xNelFHTW02KzNjV3J1MmFrYS9YbkJEckpjMENBSApMWTJsWkdrZEZtRWdKRHFqSndOd0JzWDkrR0JUKzJTUnJpZWVoRDVmWkxCMFVXbmF2aTJqbTJQOHNUbTFyRUJDCjlVbHdoMmorMW94VUhPUkttMjhlRmVPTDFvdlZLWWs0MTdoWCtDekJmUitadXJHV1QweFZLVFM0aG1MdHNzamgKVC9qaFRJRUNnWUVBem9LemRVTEVEYzdhdEdHemZHa0wwdCt6RjdMS1ZZa3Nab0NwZ2ZNcXZkYWhWSUMwUG5OdQpFSzR1SERsUmZiSDI5bGFaV0plWnk0dWxCeHBZL3VqUEZQdnhOVk5LczFwbWE0dXFyZU44U3ppU0tjaE5oQVNkCmpEeHVZd2JrOWlMTG1jWWZlbDlEcHVpVUV2Y2RGemFxY1QyczVQSjN5bGFtMGlSUkFjb2xhOEVDZ1lFQTVFU2cKUTJhL3gyaTF2QzJjejFreC9tRlB1K2JiZlR0cGNUUm5zaXhGKzJuMExNTXFBM290SWx0VnJqTXp6b2E2ODNjegpMdFE5ckJuOE9MOWp0MHhQOWlrREVTc0RndzJxTEh2VGlZTU4vRFk4dDBHRkxldGlVNklPSVJySllYT2tXRkVLCjBqcjBPZUY1eHNseWVuelpwTFg3Rk1mVWlqSGRCeDYzRlQ2OEZDRUNnWUVBbjh2VFFiRmdNNjhVM08rZEMyL2QKamxjN0plTmJYY1MvYnJHd2VMWEpKUXluMmRPZHBaVjhYYnZxUWp5NEtpTkRqbXFFVG1GQXlKaE9JcWpvcEpkUgpabE50Mm0yUktDZVRpVFNSNWV4WmlYdEUzci8zKzJmMjRVVUJ4ZTdYelA0dnZkWHBGYkFSa1YzMjlwWHhGTDFnCk5qQWJVUzJ1TkF2SkdtS3ZyRXJYbWdFQ2dZRUFnZGMvU2RlQ01zMHV3cEUzWndJWFc5akNYK0ZhN0FzRldTMHoKNXJja1AzUHZQaDd0SVBrMy94and6WnUyVmoxd3pkZjV0eU5teVNRbXdhaXI4YkZvc2w1MXJpaEhZUjQrcy9yagpRbzdYUDZVaU9DTCt2RFh0d2lDbDVOSzF4Y2JmcnBTNmtRYVRzUEMrTWdLWUtYQW01SGZYRCtUeTBvQzJkcnhUCjY3TzVpOEVDZ1lFQXNqSlgwU3NaRmU1WkhXSFdXTnA1bkxCR3JMQ01hVjltbVg3bTBERmo3UHhTNW1DSmNqK2sKRHZyK0pMN1BySk54bFpGUnNYVHdaUVVLd0MvbWNTRThCbGFuMENKWWRDaDFKL2JFMGJ4NmlLNlFLMXNWdG85ZQpNU2dTVnZiNzZEL0xyT3V0RitZeFEwQU5LT2hLYmtaNld1S2M0TjhPeG5Jb2Y1SC9yOVpNNWVJPQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQ=="
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
	La signature de la transaction -> test1 a donné 20.0 à test2 le 2021-12-17 12:27:46.345967 est :
	4924c0bd08fdd926105b5a8fd06b6198c937eb85d44c31f707c2ed97c782bd651a5fa73e4c6ee01dbf4e7f59433cf52cdf0b108ce7d61c89c25997357a085438e3535f5ea796b622de888508062d4d9ed1533bdc207c7fe1989b3ae72ac193a5c9a4ac848d755f82778a80289da459fada828330175e00347c99dceb239b94887d09c0da4a32022570d2b9d4625220d0201eb42c558a5fd85667bf936175c7486ce17ed5e6f2082270d0be5518f4ae853258755174f41aad870150a8a5a645903ac08764658f2c1aad226c730e95944e751c0200330f44e826a17ef32c8b0fe76b2e87e3c23eede1b543469759c1996609088a26f0f49406b717a9a61c0da138
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
    "signature": "4924c0bd08fdd926105b5a8fd06b6198c937eb85d44c31f707c2ed97c782bd651a5fa73e4c6ee01dbf4e7f59433cf52cdf0b108ce7d61c89c25997357a085438e3535f5ea796b622de888508062d4d9ed1533bdc207c7fe1989b3ae72ac193a5c9a4ac848d755f82778a80289da459fada828330175e00347c99dceb239b94887d09c0da4a32022570d2b9d4625220d0201eb42c558a5fd85667bf936175c7486ce17ed5e6f2082270d0be5518f4ae853258755174f41aad870150a8a5a645903ac08764658f2c1aad226c730e95944e751c0200330f44e826a17ef32c8b0fe76b2e87e3c23eede1b543469759c1996609088a26f0f49406b717a9a61c0da138"
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
	test1 a donné 20.0 à test2 le 2021-12-17 12:28:25.758480 -> hash : e7c08c38d0b6a04a7c2a3e2d0d89ec03.
</body>

</html>
```
La signature doit être celle obtenue en signant la même transaction sinon une exception sera levée.
```html
<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta charset="utf-8" />
	<title></title>
</head>

<body>
	<h4>
		Exception validité de la signature
	</h4>
	<h4>
		Une erreur est survenue :
		<br />
        Une erreur s&#39;est produite lors du controle de la signature.
    </h4>
		<br />
		<h4>Détails :</h4>
		<div>
			Status :
			500
		</div>
		<div>
			Stack Trace :
			<pre>Traceback (most recent call last):
  File &#34;C:\Users\Jean-Claude\Desktop\ESIREM\S9\SYSTEMES INFORMATIONS AVANCES SK\TP\TP01_FF_Version4\TP01\TP01\tchai4\views\EnregistrerTransactionView.py&#34;, line 38, in getParametresTemplate
    pkcs1_15.new(clePublique).verify(messageHash, binascii.unhexlify(signature.encode(&#34;utf-8&#34;)));
  File &#34;C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\lib\site-packages\Crypto\Signature\pkcs1_15.py&#34;, line 137, in verify
    raise ValueError(&#34;Invalid signature&#34;)
ValueError: Invalid signature
</pre>
		</div>
</body>

</html>
```