"""
Validatore numero carta di credito usando l'algoritmo di Luhn.

⚠️ AVVISO SICUREZZA:
- NON usare con numeri di carta reali in produzione
- Usa SOLO numeri di test autorizzati per testing
- Implementa tokenization/crittografia per dati reali
- Conforme GDPR e PCI DSS per ambiente di test
"""

import logging
import csv
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Costanti
MIN_CARD_LENGTH = 13
MAX_CARD_LENGTH = 19
AUDIT_LOG_FILE = "validation_audit.csv"


def hash_card_number(card_number: str, algorithm: str = 'sha3_256') -> str:
    """
    Genera un hash del numero di carta usando SHA-3.
    
    Args:
        card_number: Numero di carta in chiaro
        algorithm: Algoritmo di hashing (default: sha3_256)
        
    Returns:
        Hash SHA-3 del numero di carta
        
    Note:
        Il numero originale NON può essere recuperato dall'hash (one-way function)
        Conforme PCI DSS e GDPR - Non salva dati in chiaro
    """
    if algorithm == 'sha3_256':
        return hashlib.sha3_256(card_number.encode()).hexdigest()
    elif algorithm == 'sha3_512':
        return hashlib.sha3_512(card_number.encode()).hexdigest()
    else:
        raise ValueError(f"Algoritmo non supportato: {algorithm}")


def log_validation_to_csv(
    card_number: str, 
    is_valid: bool, 
    card_type: str = "Unknown",
    filename: str = AUDIT_LOG_FILE
) -> None:
    """
    Registra la validazione in un file CSV con hash SHA-3.
    
    Args:
        card_number: Numero di carta (verrà hashato)
        is_valid: Risultato della validazione
        card_type: Tipo di carta (Visa, Mastercard, ecc.)
        filename: Path del file CSV per l'audit log
        
    Note:
        - Il numero di carta viene hashato prima di salvare
        - Timestamp automatico
        - Conforme GDPR - No dati personali in chiaro
        - Conforme PCI DSS - Hashing crittografico
    """
    try:
        card_hash = hash_card_number(card_number)
        timestamp = datetime.now().isoformat()
        
        # Crea il file se non esiste
        file_exists = Path(filename).exists()
        
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'card_hash', 'is_valid', 'card_type', 'card_length'])
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'timestamp': timestamp,
                'card_hash': card_hash,
                'is_valid': 'Si' if is_valid else 'No',
                'card_type': card_type,
                'card_length': len(card_number)
            })
        
        logger.info(f"Audit log salvato: {card_hash[:8]}... - Valido: {is_valid}")
    
    except Exception as e:
        logger.error(f"Errore nel logging audit: {e}")


def detect_card_type(card_number: str) -> str:
    """
    Rileva il tipo di carta dal numero.
    
    Args:
        card_number: Numero di carta
        
    Returns:
        Tipo di carta (Visa, Mastercard, Amex, Discovery, Other)
    """
    if not card_number:
        return "Unknown"
    
    first_digit = card_number[0]
    first_two = card_number[:2]
    first_four = card_number[:4]
    
    if first_digit == '4':
        return 'Visa'
    elif first_two in ['51', '52', '53', '54', '55']:
        return 'Mastercard'
    elif first_four in ['3400', '3782']:
        return 'American Express'
    elif first_digit == '6':
        return 'Discovery'
    elif first_two in ['36', '38']:
        return 'Diners Club'
    else:
        return 'Other'


def validate_luhn(card_number: str, log_audit: bool = False) -> bool:
    """
    Valida un numero di carta usando l'algoritmo di Luhn.
    
    Args:
        card_number: Stringa contenente il numero della carta
        log_audit: Se True, registra la validazione nel file di audit (hashata)
        
    Returns:
        True se il numero è valido, False altrimenti
        
    Raises:
        ValueError: Se l'input non contiene solo cifre o è vuoto
        
    Example:
        >>> validate_luhn("4111111111111111")  # Visa test (ufficiale)
        True
        >>> validate_luhn("4111111111111112", log_audit=True)  # Registra in audit
        False
        
    Note:
        Usa SOLO numeri di test autorizzati (Visa, Mastercard, Amex forniscono liste pubbliche)
        NON usare numeri di carta reali per testing!
        Se log_audit=True, il numero viene hashato con SHA-3 prima di essere salvato
    """
    if not card_number:
        raise ValueError("Il numero non può essere vuoto")
    
    if not card_number.isdigit():
        raise ValueError("Il numero deve contenere solo cifre")
    
    if len(card_number) < MIN_CARD_LENGTH or len(card_number) > MAX_CARD_LENGTH:
        raise ValueError(f"Il numero deve avere {MIN_CARD_LENGTH}-{MAX_CARD_LENGTH} cifre")
    
    digits = [int(d) for d in card_number]
    checksum = 0
    
    # Processa tutte le cifre tranne l'ultima
    for i, digit in enumerate(digits[:-1]):
        # Raddoppia ogni seconda cifra (da destra)
        if (len(digits) - i) % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    
    # Verifica se il check digit è corretto
    check_digit = (10 - (checksum % 10)) % 10
    is_valid = check_digit == digits[-1]
    
    # Log audit opzionale (numero hashato, non in chiaro)
    if log_audit:
        card_type = detect_card_type(card_number)
        log_validation_to_csv(card_number, is_valid, card_type)
    
    return is_valid


def validate_cards_from_csv(csv_file: str, enable_audit: bool = True) -> List[Tuple[str, bool, str]]:
    """
    Valida carte di credito lette da un file CSV.
    
    Args:
        csv_file: Percorso al file CSV (colonna 'card_number')
        enable_audit: Se True, registra i risultati nel file di audit
        
    Returns:
        Lista di tuple (numero_carta, è_valido, messaggio_errore)
        
    Note:
        Se enable_audit=True, ogni validazione viene registrata in 'validation_audit.csv'
        con il numero di carta HASHATO (SHA-3), non in chiaro
        Conforme GDPR e PCI DSS
    """
    try:
        import csv as csv_module
    except ImportError:
        raise ImportError("Il modulo csv non è disponibile")
    
    results = []
    
    if not Path(csv_file).exists():
        raise FileNotFoundError(f"File non trovato: {csv_file}")
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv_module.DictReader(f)
            if reader.fieldnames is None or 'card_number' not in reader.fieldnames:
                raise ValueError("Il CSV deve avere una colonna 'card_number'")
            
            for row_num, row in enumerate(reader, start=2):
                card = row.get('card_number', '').strip()
                try:
                    is_valid = validate_luhn(card, log_audit=enable_audit)
                    results.append((card, is_valid, ""))
                    status = 'Valido' if is_valid else 'Non valido'
                    logger.info(f"Riga {row_num}: {card[-4:]}... - {status}")
                except ValueError as e:
                    results.append((card, False, str(e)))
                    logger.warning(f"Riga {row_num}: {card} - Errore: {e}")
    
    except Exception as e:
        logger.error(f"Errore lettura CSV: {e}")
        raise
    
    return results




def get_card_input() -> str:
    """Chiede all'utente di inserire un numero di carta."""
    while True:
        try:
            card = input("Inserire il numero della carta (solo cifre): ").strip()
            if not card.isdigit():
                print("Errore: Inserire solo cifre")
                continue
            if len(card) < MIN_CARD_LENGTH or len(card) > MAX_CARD_LENGTH:
                print(f"Errore: Il numero deve avere {MIN_CARD_LENGTH}-{MAX_CARD_LENGTH} cifre")
                continue
            return card
        except KeyboardInterrupt:
            print("\nOperazione annullata")
            raise


def main():
    """Funzione principale."""
    while True:
        try:
            card_number = get_card_input()
            
            if validate_luhn(card_number):
                print("✓ Numero corretto!")
            else:
                print("✗ Numero non valido, riprovare")
                
            if input("\nVuoi verificare un altro numero? (s/n): ").lower() != 's':
                break
                
        except ValueError as e:
            print(f"Errore: {e}")
        except KeyboardInterrupt:
            print("\nProgram terminato")
            break


if __name__ == "__main__":
    main()