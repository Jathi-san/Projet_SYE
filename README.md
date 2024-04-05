Pour ce projet nous avons utilier deux modules :
matplotlib et networkx, elles vont nous servir pour creer et afficher des graphes

si vous rencontrez des difficulter pour executer le code, faire les demarches suivantes :

dans vsCode ouvrir un powershell et lancer la commande suivante :
  python -m venv nom_env
  ensuite :
  .\nom_env\Scripts\activate

  Si vous etes sous linux :
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
