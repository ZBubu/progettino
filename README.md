Per far funzionare il programma è necessario scaricare tesseract
utente di prova: admin@example.com adminpassword
## .env
- SQLALCHEMY_DATABASE_URI: indirizzo del database
- SECRET_KEY: Secret Key usata per flask login
- TESSERACT: Path della cartella contenente il file tesseract.exe
- TESSDATA_PREFIX: Path della cartella tessdata
 
## API 

Rotte pubbliche (API JSON)

- GET /api/users
	- Descrizione: Restituisce la lista di tutti gli utenti in formato JSON.
	- Risposta: 200 con array di utenti oppure 404 con {"message":"No users found"} se nessun utente.

- GET /api/users/<id>
	- Descrizione: Restituisce i dati dell'utente con l'id numerico specificato.
	- Parametri: `id` (int)
	- Risposta: 200 con oggetto utente oppure 404 se non trovato.

- GET /api/users/<email>
	- Descrizione: Restituisce l'utente corrispondente all'email passata come stringa.
	- Parametri: `email` (stringa nel path)
	- Risposta: 200 con oggetto utente oppure 404 se non trovato.

- GET /api/results
	- Descrizione: Restituisce la lista di tutti i risultati salvati.
	- Risposta: 200 con array di risultati oppure 404 con {"message":"No results found"}.

- GET /api/results/greater/<val>
	- Descrizione: (Sperimentale) Restituisce i risultati con campo `result` maggiore del valore passato.
	- Parametri: `val` (int)

- GET /api/results/lastHour
	- Descrizione: Restituisce i risultati salvati nell'ultima ora.


