# Backdoor (Python Project)




# Modèle Client / Serveur 


Dans le cas de notre Backdoor, le modèle Client/Serveur est un peu à redéfinir :

- Le rôle de la machine A va être d'établir la connection avec le Backdoor, elle est donc considérée comme étant le SERVEUR.

- Le rôle de la machine B ( Backdoor )  va être de fournir ses services ( par définition elle est aussi a considérée comme 
"serveur" ) mais sera appelée machine CLIENT.

On a donc ici un modèle de type "hybride".

Avantages : 

Le fait d’avoir désigné la machine A comme étant le serveur et donc celle qui établi la connection nous permet de n’avoir qu’à définir notre propre IP avant de déployer le backdoor dans un réseau.

# Fonctions présentes
- Reverse Shell
- Keylogger
- Scan réseau ( Scapy )
- Gestion des logs ( client, serveur, keylogger )
- Upload & Download


# Connection + Encryption

Nous avons opté pour l'utilisation du protocole TCP qui facilite ainsi la gestion du flux sur le réseau, garantit la non perte des paquets et facilite l'écriture du code ainsi que la gestion des sockets.

En revanche, le nombre de paquets sur le réseau est un peu plus conséquent.


En ce qui concerne l'encryption, le module SSL fait plus que correctement le travail, il s'occupe de gérer le chiffrement des données grâce à un certificat et offre une authentification des deux partis. 

python 3 ssl →  https://docs.python.org/3/library/ssl.html

Gen the private Key & Certificate : 

	openssl genrsa -out priv.pem 2048
	openssl rsa -in priv.pem -pubout -out pub.pem
	openssl req -new -key priv.pem -out cert.csr
	openssl x509 -req -days 365 -in cert.csr -signkey priv.pem -out cert.crt

Seul le certificat est utilisé sur la machine infectée.

# Heritage & Thread

Le Reverse Shell ainsi que le Keylogger implémentés ont été défini en tant que "Threads" pour pouvoir s’effectuer en parallèle au programme principale. Ils héritent aussi de la classe SecureCommunication qui leur permet de communiquer sur un socket différent de celui par défaut. 


# Shell

Le Reverse Shell ( et ses communications ) mit en place est complètement sécurisé grâce au module SSL et travail en parallèle au programme principale en ouvrant un ( ou plusieurs ) terminal à part, ce qui permet de profiter de ses fonctionnalitées en live.



# Keylogger

Nous sommes partis du module Pynput qui offre un keylogger simple à implémenter et nous avons adapté son code pour faciliter la relecture et réduire le nombre de paquets envoyés.


Pynput → https://theembeddedlab.com/tutorials/keylogger-python/

# Scapy

Utilisation du module Scapy qui propose des outils réseaux ( conception de paquets, ... ) qui nous permet de faire un scan global du réseau ou d'une machine spécifique, grâce à l’envoi de requêtes ARP.


# Logging 

Utilisation du module logging pour une gestion des logs efficace selon différent niveau de verbosité.
Trois fichiers de log sont présents, un pour le client, un pour le serveur et le dernier pour le
keylogger.
Une fonction clear_log permet de supprimer les logs existants.

# Arguments

En ce qui concerne la gestion des arguments proposant; du côté serveur une aide, un mode verbose ainsi que la possibilité de définir un path personnel pour sauvegarder les logs …
et du côté client la possibilité de définir l’adresse ip du serveur.

