"""
Test per il sistema di audit logging con SHA-3.
"""

import pytest
import hashlib
import os
from pathlib import Path
from luhnalgorithm import hash_card_number, log_validation_to_csv, AUDIT_LOG_FILE


class TestAuditLogging:
    """Test suite per il sistema di audit logging."""
    
    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Pulisce il file di audit prima e dopo i test."""
        if Path(AUDIT_LOG_FILE).exists():
            os.remove(AUDIT_LOG_FILE)
        yield
        if Path(AUDIT_LOG_FILE).exists():
            os.remove(AUDIT_LOG_FILE)
    
    def test_hash_card_sha3_256(self):
        """Test hashing SHA-3 256."""
        card = "4111111111111111"
        hash_result = hash_card_number(card, algorithm='sha3_256')
        
        # Verifica che il risultato sia un hash SHA-3 valido
        assert len(hash_result) == 64  # SHA-3 256 = 64 hex characters
        assert isinstance(hash_result, str)
        assert hash_result.isalnum()
    
    def test_hash_card_sha3_512(self):
        """Test hashing SHA-3 512."""
        card = "4111111111111111"
        hash_result = hash_card_number(card, algorithm='sha3_512')
        
        # Verifica che il risultato sia un hash SHA-3 512 valido
        assert len(hash_result) == 128  # SHA-3 512 = 128 hex characters
        assert isinstance(hash_result, str)
    
    def test_hash_deterministic(self):
        """Test che l'hash dello stesso numero è sempre uguale."""
        card = "4111111111111111"
        
        hash1 = hash_card_number(card)
        hash2 = hash_card_number(card)
        
        assert hash1 == hash2, "L'hash deve essere deterministico"
    
    def test_hash_different_for_different_cards(self):
        """Test che carte diverse producono hash diversi."""
        hash1 = hash_card_number("4111111111111111")
        hash2 = hash_card_number("5555555555554444")
        
        assert hash1 != hash2, "Hash diversi per carte diverse"
    
    def test_hash_not_reversible(self):
        """Test che il numero originale NON può essere recuperato."""
        card = "4111111111111111"
        hash_value = hash_card_number(card)
        
        # Non dovrebbe essere possibile fare reverse hashing
        # (SHA-3 è one-way function)
        assert hash_value != card
        assert not hash_value.startswith("4111")
    
    def test_unsupported_algorithm(self):
        """Test con algoritmo non supportato."""
        with pytest.raises(ValueError, match="Algoritmo non supportato"):
            hash_card_number("4111111111111111", algorithm='md5')
    
    def test_log_validation_creates_file(self):
        """Test che il file di audit viene creato."""
        log_validation_to_csv("4111111111111111", True, "Visa")
        
        assert Path(AUDIT_LOG_FILE).exists(), "File di audit non creato"
    
    def test_log_validation_contains_hash(self):
        """Test che il file di audit contiene hash, non numeri."""
        card = "4111111111111111"
        log_validation_to_csv(card, True, "Visa")
        
        with open(AUDIT_LOG_FILE, 'r') as f:
            content = f.read()
        
        # Verifica che il numero NON sia nel file
        assert card not in content, "⚠️ SICUREZZA: Numero di carta in chiaro nel file!"
        
        # Verifica che l'hash sia nel file
        card_hash = hash_card_number(card)
        assert card_hash in content, "Hash non trovato nel file di audit"
    
    def test_log_csv_format(self):
        """Test che il formato del CSV sia corretto."""
        log_validation_to_csv("4111111111111111", True, "Visa")
        
        with open(AUDIT_LOG_FILE, 'r') as f:
            lines = f.readlines()
        
        # Verifica header
        assert "timestamp" in lines[0]
        assert "card_hash" in lines[0]
        assert "is_valid" in lines[0]
        assert "card_type" in lines[0]
        assert "card_length" in lines[0]
        
        # Verifica numero di colonne
        assert len(lines[1].split(',')) == 5
    
    def test_log_multiple_entries(self):
        """Test logging di più validazioni."""
        log_validation_to_csv("4111111111111111", True, "Visa")
        log_validation_to_csv("5555555555554444", True, "Mastercard")
        log_validation_to_csv("378282246310005", False, "Amex")
        
        with open(AUDIT_LOG_FILE, 'r') as f:
            lines = f.readlines()
        
        # Header + 3 validazioni = 4 righe
        assert len(lines) == 4, f"Atteso 4 righe, trovate {len(lines)}"
        
        # Verifica che i dati siano diversi
        hash1 = lines[1].split(',')[1]
        hash2 = lines[2].split(',')[1]
        hash3 = lines[3].split(',')[1]
        
        assert hash1 != hash2 != hash3, "Gli hash dovrebbero essere diversi"
    
    def test_log_valid_status(self):
        """Test che lo status di validità sia registrato correttamente."""
        log_validation_to_csv("4111111111111111", True, "Visa")
        log_validation_to_csv("4111111111111112", False, "Visa")
        
        with open(AUDIT_LOG_FILE, 'r') as f:
            lines = f.readlines()
        
        # Prima validazione: valida
        assert "Si" in lines[1], "Prima validazione dovrebbe essere 'Si'"
        
        # Seconda validazione: non valida
        assert "No" in lines[2], "Seconda validazione dovrebbe essere 'No'"
    
    def test_log_card_type(self):
        """Test che il tipo di carta sia registrato."""
        log_validation_to_csv("4111111111111111", True, "Visa")
        
        with open(AUDIT_LOG_FILE, 'r') as f:
            content = f.read()
        
        assert "Visa" in content, "Tipo carta non trovato"
    
    def test_log_card_length(self):
        """Test che la lunghezza della carta sia registrata."""
        log_validation_to_csv("4111111111111111", True, "Visa")
        
        with open(AUDIT_LOG_FILE, 'r') as f:
            lines = f.readlines()
        
        # La lunghezza dovrebbe essere 16
        length = lines[1].split(',')[-1].strip()
        assert length == "16", f"Lunghezza attesa 16, trovata {length}"
    
    def test_log_timestamp_format(self):
        """Test che il timestamp sia in formato ISO."""
        log_validation_to_csv("4111111111111111", True, "Visa")
        
        with open(AUDIT_LOG_FILE, 'r') as f:
            lines = f.readlines()
        
        timestamp = lines[1].split(',')[0]
        
        # Verifica formato ISO (2026-02-12T18:23:13...)
        assert "T" in timestamp, "Timestamp non in formato ISO"
        assert "-" in timestamp, "Data non in formato ISO"


class TestHashSecurity:
    """Test di sicurezza per il sistema di hashing."""
    
    def test_sha3_vs_manual(self):
        """Test che SHA-3 sia uguale a hashlib."""
        card = "4111111111111111"
        
        hash_custom = hash_card_number(card)
        hash_manual = hashlib.sha3_256(card.encode()).hexdigest()
        
        assert hash_custom == hash_manual, "Hash non corrisponde"
    
    def test_hash_length_consistency(self):
        """Test che la lunghezza dell'hash sia consistente."""
        for i in range(10):
            card = f"411111111111{str(i).zfill(4)}"
            hash_result = hash_card_number(card)
            
            assert len(hash_result) == 64, f"Hash length non consistente per {card}"
    
    def test_hash_case_sensitivity(self):
        """Test che il numero della carta influenzi l'hash."""
        # Anche se nella pratica i numeri sarebbero gli stessi,
        # verifichiamo che SHA-3 sia sensibile ai dati
        hash1 = hash_card_number("4111111111111111")
        hash2 = hash_card_number("4111111111111112")
        
        assert hash1 != hash2, "Hash dovrebbe essere diverso per numeri diversi"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
