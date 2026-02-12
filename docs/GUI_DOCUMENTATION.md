# Validatore Luhn GUI - PyQt6

Applicazione con interfaccia grafica per la validazione di numeri di carta di credito usando l'algoritmo di Luhn.

⚠️ **AVVISO IMPORTANTE DI SICURITÀ E PRIVACY**

**NON utilizzare NUNCA numeri di carta reali o dati sensibili in file CSV o test!**

Questo progetto usa SOLO numeri di test artificiali per scopi didattici:
- I numeri di test sono pubblici e autorizzati
- Sono generati artificialmente per testing
- Non rappresentano carte reali
- Rispettano standard PCI DSS per ambiente di test

**Conformità:**
- ✓ GDPR - No dati reali conservati
- ✓ PCI DSS - Solo numeri di test ufficiali
- ✓ Privacy - File locale, non sincronizzato

## Caratteristiche

✨ **Interfaccia moderna** - Applicazione desktop professionale  
📊 **Due modalità**:
  - Validazione singola numero
  - Validazione batch da CSV  
🎨 **Design intuitivo** - Colori e feedback visivi  
⚡ **Reattiva** - Risposta immediata agli input  
📁 **Supporto file** - Carica facilmente file CSV  

## Installazione

```bash
pip install PyQt6
```

## Esecuzione

```bash
python luhn_gui.py
```

## Funzionalità

### Tab 1: Singolo Numero

![Schermata validazione singola]

**Come usare:**
1. Inserisci il numero di carta nel campo
2. Premi INVIO oppure clicca "Valida"
3. Visualizza il risultato con codice colore

**Feedback:**
- 🟢 **Verde**: Carta valida
- 🔴 **Rosso**: Errore o carta non valida
- 🟠 **Arancione**: Avviso

**Numeri di test AUTORIZZATI (Standard Visa/Mastercard per testing):**

✓ **Numeri VALIDI** (Passano validazione Luhn):
- Visa: `4111111111111111` (numero di test ufficiale Visa)
- Mastercard: `5555555555554444` (numero di test ufficiale Mastercard)
- Amex: `378282246310005` (numero di test ufficiale Amex)
- Discovery: `6011111111111117` (numero di test ufficiale Discovery)

✗ **Numeri NON VALIDI** (Per testare rifiuto):
- Checksum sbagliato: `4111111111111112`
- Formato errato: `1234567890`

💡 Questi numeri sono pubblici documenti ufficiali per testing

### Tab 2: Validazione Batch (CSV)

**Formato CSV richiesto:**
```csv
card_number
4532015112830366
5555555555554444
374245455400126
```

**Come usare:**
1. Clicca "📁 Carica CSV"
2. Seleziona il file CSV dal tuo computer
3. Visualizza i risultati in tabella

**Risultati:**
- ✓ VALIDO: Carta valida
- ✗ INVALID: Carta non ha superato validazione
- ❌ ERRORE: Problema con il formato/lunghezza

**Colonne:**
| Colonna | Descrizione |
|---------|-------------|
| Numero Carta | Il numero di carta dal CSV |
| Validità | Stato della validazione |
| Messaggio | Dettagli di errore (se presente) |

## File CSV di Test

È incluso il file `carte_test.csv` con numeri di test UFFICIALI e AUTORIZZATI:

```csv
card_number
4111111111111111
5555555555554444
378282246310005
6011111111111117
4111111111111112
1234567890
```

**Note sulla privacy:**
- ✓ Usa SOLO numeri di test pubblici
- ✓ Non salva dati sensibili reali
- ✓ File locale non sincronizzato
- ✓ Conforme a standard PCI DSS

Usalo liberamente per testare la validazione batch senza preoccupazioni di sicurezza!

## Interfaccia

```
┌─────────────────────────────────────────┐
│  Validatore Luhn                        │
├─ Singolo Numero ─ Validazione Batch ──┤
│                                         │
│ Inserisci numero carta:                 │
│ [                                    ]  │
│ [       Valida       ]                  │
│                                         │
│ Risultato:                              │
│ ┌─────────────────────────────────────┐ │
│ │                                     │ │
│ │  ✓ VALIDAZIONE RIUSCITA!           │ │
│ │  Numero: 4532015112830366          │ │
│ │  Stato: VALIDO                      │ │
│ │                                     │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ℹ️ Lunghezza accettata: 13-19 cifre   │
│ ℹ️ Premi INVIO o clicca 'Valida'      │
└─────────────────────────────────────────┘
```

## Scorciatoie Tastiera

| Tasto | Azione |
|-------|--------|
| INVIO | Valida il numero (nel tab Singolo) |
| CTRL+O | Apri file CSV (nel tab Batch) |
| ALT+TAB | Cambia tab |

## Colori e Feedback

**Validazione Riuscita:**
- Sfondo: Verde chiaro (#e8f5e9)
- Testo: Verde scuro (#2e7d32)
- Bordo: Verde (#4caf50)

**Errore:**
- Sfondo: Rosso chiaro (#ffebee)
- Testo: Rosso scuro (#c62828)
- Bordo: Rosso (#f44336)

**Avviso:**
- Sfondo: Arancione chiaro (#fff3e0)
- Testo: Arancione scuro (#f57c00)
- Bordo: Arancione (#ff9800)

## Pulsanti

**Valida** (Verde)
- Valida il numero di carta inserito
- Cambiano colore al hover
- Click fornisce feedback tattile

**Carica CSV** (Blu)
- Apre il file browser
- Permette selezione file CSV
- Carica e processa automaticamente

## Gestione Errori

L'applicazione gestisce correttamente:
- ✓ File non trovato
- ✓ formato CSV errato
- ✓ Colonna mancante
- ✓ Input non numerico
- ✓ Lunghezza non valida
- ✓ Errori di parsing

## Requisiti

- Python 3.8+
- PyQt6
- luhnalgorithm.py (modulo locale)

## Licenza

MIT - Uso libero per scopi educativi

## Riferimenti Sicurezza

- [PCI Security Standards Council](https://www.pcisecuritystandards.org/) - Standard PCI DSS
- [OWASP Testing Guide](https://owasp.org/) - Best practices sicurezza
- [Visa Testing Numbers](https://developer.visa.com/apis/docs) - Numeri di test ufficiali Visa
- [Mastercard Testing](https://developer.mastercard.com/) - Numeri di test Mastercard
- [Regolamento GDPR](https://gdpr.eu/) - Protezione dati personali

## Supporto

Per problemi:
1. Verifica che PyQt6 sia installato
2. Assicurati che luhnalgorithm.py sia nella stessa directory
3. Controlla il formato del file CSV
4. Verifica di usare SOLO numeri di test nel CSV
