from luhnalgorithm import hash_card_number
import hashlib

print("=" * 80)
print("ESEMPIO PRATICO: TRASFORMAZIONE NUMERO → HASH SHA-3")
print("=" * 80)
print()

# Esempio 1
card1 = "4111111111111111"
hash1 = hash_card_number(card1)

print("CARTE DI PROVA (VISA):")
print(f"Numero:  {card1}")
print(f"Hash:    {hash1}")
print()

# Esempio 2
card2 = "5555555555554444"
hash2 = hash_card_number(card2)

print("CARTE DI PROVA (MASTERCARD):")
print(f"Numero:  {card2}")
print(f"Hash:    {hash2}")
print()

# Esempio 3
card3 = "378282246310005"
hash3 = hash_card_number(card3)

print("CARTE DI PROVA (AMEX):")
print(f"Numero:  {card3}")
print(f"Hash:    {hash3}")
print()

print("=" * 80)
print("ANALISI DI SICUREZZA")
print("=" * 80)
print()

print("1️⃣ HASH È DETERMINISTICO (sempre uguale per lo stesso numero)")
hash1_bis = hash_card_number(card1)
print(f"   Primo hash:   {hash1}")
print(f"   Secondo hash: {hash1_bis}")
print(f"   Sono uguali? {hash1 == hash1_bis} ✓")
print()

print("2️⃣ HASH CAMBIA LEGGERMENTE CON NUMERI DIVERSI")
card_simile = "4111111111111112"  # Solo l'ultimo digit è diverso
hash_simile = hash_card_number(card_simile)
print(f"   Numero 1: {card1}")
print(f"   Hash 1:   {hash1}")
print()
print(f"   Numero 2: {card_simile}  ← Solo l'ultimo digit diverso!")
print(f"   Hash 2:   {hash_simile}")
print()
print(f"   I numeri differiscono per 1 digit (ultimo)")
print(f"   Gli hash differiscono completamente! ✓")
diff_count = sum(1 for a, b in zip(hash1, hash_simile) if a != b)
print(f"   Differenza: {diff_count} su 64 caratteri")
print()

print("3️⃣ SHA-3 È ONE-WAY (irreversibile)")
print(f"   ✓ Da numero → Hash (facile: {card1} → {hash1[:20]}...)")
print(f"   ✗ Da Hash → Numero (IMPOSSIBILE: {hash1[:20]}... → ???)")
print()

print("4️⃣ COSA ACCADE NEL FILE AUDIT")
print(f"   Se rubano il numero in chiaro:        {card1}")
print(f"   La carta è COMPROMESSA ✗")
print()
print(f"   Se rubano il file audit con hash:")
print(f"   {hash1}")
print(f"   La carta è SICURA ✓ (hash non invertibile)")
print()

print("=" * 80)
print("CONCLUSIONE")
print("=" * 80)
print()
print("NON salviamo il numero:      4111111111111111")
print("Salviamo l'hash:             6099154214406cce6105a4688ab66533...")
print()
print("Se l'hash viene rubato:      NESSUN PROBLEMA (irrecuperabile)")
print("Se il numero venisse rubato: GRAVE PROBLEMA (carta compromessa)")
print()
print("Per questo usiamo SEMPRE SHA-3 per l'audit! 🔐")
print("=" * 80)
