# Validatore Luhn - Numero Carta di Credito

Un validatore Python robusto e completamente testato per verificare la validità dei numeri di carta di credito usando l'algoritmo di Luhn.

⚠️ **AVVISO IMPORTANTE - PRIVACY E SICUREZZA**

**NON UTILIZZARE NUMERI DI CARTA REALI!**

Questo progetto usa SOLO numeri di test artificiali autorizzati per testing:
- ✓ Conforme a standard PCI DSS
- ✓ Compliant GDPR - No dati reali
- ✓ Usa numeri di test ufficiali pubblici
- ✓ Nessuna sincronizzazione dati sensibili

## Caratteristiche

✅ **Algoritmo di Luhn** - Implementazione corretta dello standard internazionale  
✅ **Validazione completa** - Controlla lunghezza, formato e checksum  
✅ **Supporto CSV** - Valida batch di carte da file CSV  
✅ **Logging integrato** - Traccia tutte le operazioni  
✅ **17 test unitari** - Copertura completa dei casi d'uso e edge cases  
✅ **Type hints** - Annotazioni di tipo per maggiore sicurezza  
✅ **Docstrings dettagliate** - Documentazione completa di ogni funzione  

## Installazione

```bash
pip install pytest
```

## Utilizzo

### Validazione di un singolo numero

```python
from luhnalgorithm import validate_luhn

# Numero valido (Visa)
if validate_luhn("4532015112830366"):
    print("✓ Carta valida!")
else:
    print("✗ Carta non valida!")
```

### Interfaccia interattiva

```bash
python luhnalgorithm.py
```

### Validazione bulk da CSV

```python
from luhnalgorithm import validate_cards_from_csv

results = validate_cards_from_csv("carte.csv")
for card, is_valid, error in results:
    if error:
        print(f"{card}: ERRORE - {error}")
    else:
        print(f"{card}: {'✓ Valida' if is_valid else '✗ Non valida'}")
```

## Format CSV

Il file CSV deve contenere una colonna `card_number`:

```csv
card_number
4532015112830366
5555555555554444
374245455400126
```

## Esecuzione test

```bash
# Esegui tutti i test con output dettagliato
pytest test_luhnalgorithm.py -v

# Esegui con copertura
pytest test_luhnalgorithm.py --cov=luhnalgorithm

# Esegui un test specifico
pytest test_luhnalgorithm.py::TestValidateLuhn::test_valid_visa_card -v
```

## Specifiche

| Parametro | Valore |
|-----------|--------|
| Lunghezza minima | 13 cifre |
| Lunghezza massima | 19 cifre |
| Formato accettato | Solo cifre (0-9) |
| Algoritmo | Luhn (ISO/IEC 7812) |

## Miglioramenti implementati

### Rispetto alla versione originale:

1. **Logging** - Ogni operazione è registrata e tracciabile
2. **Supporto CSV** - Validazione batch di file
3. **Costanti** - Magic number rimossi e centralizzati
4. **Test suite** - 17 test automatici che coprono:
   - Numeri di carta validi (Visa, Mastercard, Amex)
   - Numeri non validi
   - Input vuoti/non validi
   - Input troppo corti/lunghi
   - Whitespace e caratteri speciali
   - Edge cases

5. **Documentazione** - Docstrings completi con esempi
6. **Type hints** - Annotazioni di tipo per ogni funzione
7. **Error handling** - Gestione eccezioni più robusta
8. **Separazione responsabilità** - Ogni funzione ha un compito specifico

## Esempi di test

```bash
# Esegui un singolo test
pytest test_luhnalgorithm.py::TestValidateLuhn::test_valid_visa_card -v

# Output:
# test_luhnalgorithm.py::TestValidateLuhn::test_valid_visa_card PASSED [100%]
```

## Carte di test valide

Questi numeri di test sono **AUTORIZZATI UFFICIALMENTE** da Visa, Mastercard, Amex e Discovery per testing:

| Tipo | Numero | Stato |
|------|--------|-------|
| Visa | 4111111111111111 | ✓ Valido |
| Mastercard | 5555555555554444 | ✓ Valido |
| American Express | 378282246310005 | ✓ Valido |
| Discovery | 6011111111111117 | ✓ Valido |
| Test Non Valido | 4111111111111112 | ✗ Checksum errato |

Fonte: Numeri ufficiali per testing da Visa, Mastercard, Amex (pubblici e autorizzati)

**Conformità:**
- 🔒 **GDPR Compliant** - Non usa dati personali reali
- 🔐 **PCI DSS** - Segue standard internazionali di sicurezza
- ✅ **Privacy** - File locale, non sincronizzato
- 📋 **Trasparenza** - Chiaramente documentati come test

## Sicurezza e Privacy

### ⚠️ Cosa NON fare (VIETATO):

```python
# ❌ SBAGLIATO - Non fare mai questo!
with open('carte.csv', 'w') as f:
    f.write('4532,1234,5678,9012')  # NUMERO REALE!

# ❌ Non committare in git
git add carte_reali.csv

# ❌ Non salvare su cloud
shutil.copy('carte.csv', 'OneDrive/')
```

### ✅ Cosa fare (CORRETTO):

```python
# ✓ CORRETTO - Usa numeri di test autorizzati
with open('carte_test.csv', 'w') as f:
    f.write('4111111111111111')  # Numero di test Visa

# ✓ Documenta che è test
# carte_test.csv - SOLO PER TESTING, numeri artificiali

# ✓ Non sincronizzare se contiene dati sensibili
# .gitignore: carte_reali.csv
```

### Conformità GDPR:

- ℹ️ Non archiviare numeri di carta reali senza cifratura
- ℹ️ Non sincronizzare su cloud senza TLS/SSL
- ℹ️ Documentare chiaramente uso solo test
- ℹ️ Implementare access control e audit log
- ℹ️ Data retention: cancellare dopo test

### Conformità PCI DSS:

- ℹ️ Usa tokenization per carte reali
- ℹ️ Non salvare CVV/CVC
- ℹ️ Crittografia end-to-end
- ℹ️ Accesso ristretto a dati sensibili
- ℹ️ Monitoraggio e logging

### Per sviluppo con dati reali:

1. **Ambiente di test separato** - Isolato da produzione
2. **Dati fittizi** - Mock/stub per simulare risposte
3. **Tokenization** - Servizi di pagamento certificati
4. **Crittografia** - AES-256 minimum
5. **Audit trail** - Logging di tutti gli accessi

## Note di sicurezza

⚠️ **Questo strumento è solo per validazione sintattica!**  
Non verifica se la carta è stata compromessa o se l'intestatario è autorizzato.

Usa solo per:
- Testing di applicazioni in ambiente controllato
- Validazione formato durante lo sviluppo
- Analisi forensica (con dati autorizzati)

Con dati reali, implementa:
- Tokenization PCI-compliant
- Crittografia forte
- Conformità normative (GDPR, PCI DSS)
- Audit logging completo

## Licenza

MIT - Uso libero per scopi educativi e di ricerca
