Pour ce projet nous avons utilier deux modules :
matplotlib et networkx, elles vont nous servir pour creer et afficher des graphes

Toutefois nous avons rencontré des difficulte pour executer le code directement (à savoir que nous étions tous
les 2 sur des PC windows)

Voici les demarches que nous avons effectué pour pallier à ce problème :

dans vsCode ouvrir un powershell et lancer la commande suivante :
  python -m venv nom_env      
  ensuite :
  .\nom_env\Scripts\activate  

  La commande equivalente sous linux est la suivante :
  source <chemin_vers_votre_env>/bin/activate

  En sassurant d'avoir les autorisations nécessaires 

  si vous rencontrez une erreur, faites ceci :
  Ouvrir un cmd en tant qu'administrateur et faire :
  Set-ExecutionPolicy RemoteSigned
  Et dire oui avec O

  Refaire dans le powershelle de vscode :
  .\nom_env\Scripts\activate

  Puis :
  pip install matplotlib et 
  pip install networkx

Cela va installer les modules dans l'environnement virtuel 

Relancer vscode avant execution du programme

Nous avons creer un environnement virtuel d'execution puis on l'a activé et dans cet enironnement on a installer les 2 modules
ainsi nous n'aurons plus de difficulter a executer notre code

Dans le fichier test il y a deja des exemples de systemes pour lesquelles vous pouvez executer les fonctions
