# WATERLAND
## _Django project, Tecnologie web_
### _(Fabiano Faccini, matricola 130056)_

[![N|Solid](https://images.g2crowd.com/uploads/product/image/social_landscape/social_landscape_505df21738edbe9baababa9d60be291d/github.png)](https://github.com/faby95/waterland_tecnologie_web_project)

## Requisiti:
#### (Pre-requisiti da avere installato)
* __Python__ (Ho utilizzato la versione 3.10, quindi dalla 3.10 o superiori sicuramente vanno bene, nel Pipfile ho inserito la versione '*' per facilitarne il processo di installazione (andrà ad utilizzare la versione di python corrente che trova), assicuratevi di avere sul pc una versione python >= 3.10 (Nota aggiornata: ho testato il sito anche con le versioni python 3.7 e 3.8 e funziona correttamente))
* __Pipenv__ (Nel progetto è presente un Pipfile che permetterà l'installazione automatica delle dipendenze una volta installato l'ambiente virtuale, verrà creato automaticamente il Pipfile.lock)
#### (Framework utilizzato)
* __Django__ (Verrà installato automaticamente all'installazione dell'ambiente virtuale, è tutto contenuto nel Pipfile)
#### (Dipendenze utilizzate)  
### pip install ... 
##### (Operazione automatizzata dal Pipfile, installazione automatica con pipenv)
* __django-crispy-forms__
* __django-admin-interface__
* __pillow__
* __django-cleanup__
#### (Ulteriori dipendenze)
* __bootstrap__ (cdn importate nella base.html) [![N|Solid](https://www.geekandjob.com/uploads/wiki/40d4cef4ffedd6c9d9ac006932092638.png)](https://getbootstrap.com/docs/4.3/getting-started/introduction/)
* __sweet allert__ (utilizzato per i messaggi di avviso interni al sito, presente in static/js)

[![N|Solid](https://raw.githubusercontent.com/t4t5/sweetalert/e3c2085473a0eb5a6b022e43eb22e746380bb955/assets/logotype.png)](https://sweetalert.js.org/guides/)
* __chart.js__ (utilizzato per il grafico, presente in static/js)

[![N|Solid](https://camo.githubusercontent.com/9be0208aa516b4d1976412d27e9f73d851ea253f8ee005a0b600939f841bba8b/68747470733a2f2f7777772e63686172746a732e6f72672f6d656469612f6c6f676f2d7469746c652e737667)](https://www.chartjs.org/)
* __jsPDF__ (utilizzato per generare il pdf dell'acquisto del customer, presente in static/js)

[![N|Solid](https://www.bypeople.com/wp-content/uploads/2019/03/jspdf-featured-2.png)](https://parall.ax/products/jspdf?utm_source=cdnjs&utm_medium=cdnjs_link&utm_campaign=cdnjs_library)

#### (Installazione) 
> Creare una cartella (in questo caso l'ho chiamata progetto), successivamente entriamo nella cartella
```sh
mkdir progetto
cd ./progetto
```
> Ora che siamo all'interno della cartella progetto, andiamo a scaricare il progetto al suo interno
```sh
git clone https://github.com/faby95/waterland_tecnologie_web_project.git
```
> Ora all'interno della cartella progetto troveremo una cartella chiamata "waterland_tecnologie_web_project", entriamo nella cartella
```sh
cd ./waterland_tecnologie_web_project
```
> Installiamo l'ambiente virtuale con pipenv (le dipendenze saranno scaricate automaticamente)
```sh
pipenv install
```
> Terminata la procedura di installazione dell'ambiente virtuale, entriamo in quest'ultimo attraverso il seguente comando
```sh
pipenv shell
```
> (Opzionale) Per ulteriore verifica (una volta all'interno dell'ambiente virtuale), se vogliamo accertarci che tutte le dipendenze di interesse siano state installate digitare il seguente comando. Se l'installazione automatica non va a buon fine, una volta all'interno dell'ambiente virtuale installare le dipendenze a mano (elencate nella sezione pip install ... di questo file)
```sh
pip freeze
```
> Ora possiamo avviare il server web (in ascolto alla porta 8000 in questo caso)
```sh
python manage.py runserver 8000
```
> Ora è possibile avviare un browser web e accedere al sito al seguente indirizzo
```sh
http://127.0.0.1:8000
```
> oppure
```sh
http://localhost:8000
```
#### (Utilizzo)
Il sito contiene una pagina informativa generale, ulteriori link alla sezione Faq, Feedbadk e About us (che contiene i contatti anche), queste pagine sono visibili a tutti.
Viene mostrata una sezione di sign-in e log-in, la sign-in divide due tipologie di utenti, staff e customer.
I customer possono acquistare biglietti giornalieri e season pass, possono lasciare feedback solo se almeno un acquisto è stato effettuato, possono lasciare Faq, ed inoltre hanno una loro sezione che raggruppa le loro richieste (Faq) in ordine decrescente di creazione, in modo da avere in vista eventuali risposte a domande recenti lasciate, sicuramente l'interesse è spostato maggiormente su quelle.
Il customer ha due sezioni dove vengono raggruppati in ordine di validità tutti i daily ticket o season pass, anche qui il raggruppamento è dovuto al fatto che l'interesse è spostato verso l'acquisto valido, quindi sul periodo di validità in ordine decrescente, un utente volendo può scorrere però i suoi vecchi acquisti.

Lo staff per registrarsi ha bisogno di un istanza valida nella StaffAuthTable, una tabella nel database che viene ipoteticamente popolata da chi assume con un secondo software (utilizzare l'interfaccia di admin in questa demo per simulare il software di assunzione che crea l'istanza, la creiamo noi dalla tabella), se la combinazione di chiave e codice staff fanno match, l'utente viene creato, altrimenti sarà impossibile creare un utente staff, una volta utilizzata l'istanza valida, questa diverrà invalida per sempre e il code staff è univoco, perciò non sarà mai più utilizzabile la stessa combinazione. Uno staff licenziato deve cancellare il suo utente staff nella sezione profilo, dopo di che non avrà più modo di registrarsi come tale affinchè non venga creata nuovamente un istanza valida di registrazione e che quest'ultimo ne entri a conoscenza.

Gli staff possono cancellare i Feedback (se eventualmente contengono "parole forti"), possono cancellare eventuali Faq, possono rispondere alle Faq (senza firmarsi), possono cercare la lista degli acquisti di un utente per verificare se davvero ha acquistato un ticket o season pass valido (se un utente ad esempio si dimentica di portare il ticket, gli basta comunicare il suo username per verificare gli acquisti), possibilità di verificare i guadagni ed i season pass venduti nell'arco di un preciso anno, possibilità di verificare i guadagni ed i daily ticket venduti nell'arco di un giorno, nell'arco di un anno oppure nell'arco di un periodo custom (range personalizzato), più visualizzazione grafica (grafico con chart.js) per vedere i periodi di picco degli acquisti.

