"""
Validatore Luhn con interfaccia grafica PyQt6.
"""

import sys
import csv
from pathlib import Path
from typing import List, Tuple

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog,
    QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QCheckBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QColor

from luhnalgorithm import validate_luhn, validate_cards_from_csv, AUDIT_LOG_FILE


class LuhnValidatorGUI(QMainWindow):
    """Interfaccia grafica per il validatore Luhn."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inizializza l'interfaccia utente."""
        self.setWindowTitle("Validatore Luhn - Numero Carta di Credito")
        self.setGeometry(100, 100, 700, 600)
        self.setMinimumSize(QSize(700, 500))
        
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale
        main_layout = QVBoxLayout()
        
        # Titolo
        title_label = QLabel("Validatore Luhn")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Tab 1: Validazione singola
        self.create_single_validation_tab()
        
        # Tab 2: Validazione batch (CSV)
        self.create_batch_validation_tab()
        
        central_widget.setLayout(main_layout)
        
        # Stile
        self.set_style()
    
    def create_single_validation_tab(self):
        """Crea il tab per validazione di un singolo numero."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Label e input
        input_label = QLabel("Inserisci numero carta:")
        input_font = QFont()
        input_font.setPointSize(10)
        input_label.setFont(input_font)
        layout.addWidget(input_label)
        
        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("Es: 4111111111111111")
        self.card_input.setMinimumHeight(40)
        self.card_input.returnPressed.connect(self.validate_single_card)
        layout.addWidget(self.card_input)
        
        # Layout per pulsanti e options
        options_layout = QHBoxLayout()
        
        # Checkbox per audit log
        self.audit_checkbox = QCheckBox("📋 Registra in audit log (hashato SHA-3)")
        self.audit_checkbox.setChecked(True)
        options_layout.addWidget(self.audit_checkbox)
        
        options_layout.addStretch()
        layout.addLayout(options_layout)
        
        # Pulsante validazione
        validate_button = QPushButton("Valida")
        validate_button.setMinimumHeight(40)
        validate_button.clicked.connect(self.validate_single_card)
        validate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        layout.addWidget(validate_button)
        
        # Area risultati
        result_label = QLabel("Risultato:")
        result_label.setFont(input_font)
        layout.addWidget(result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(100)
        self.result_text.setFont(QFont("Courier", 11))
        layout.addWidget(self.result_text)
        
        # Pulsante visualizza audit log
        view_audit_button = QPushButton("📊 Visualizza Audit Log")
        view_audit_button.clicked.connect(self.view_audit_log)
        view_audit_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        layout.addWidget(view_audit_button)
        
        # Info
        info_label = QLabel(
            "ℹ️ Lunghezza accettata: 13-19 cifre\n"
            "ℹ️ I numeri vengono salvati NON in chiaro (SHA-3 hash)\n"
            "ℹ️ Premi INVIO o clicca 'Valida' per validare"
        )
        info_label.setStyleSheet("color: #666; font-size: 9pt;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        self.tabs.addTab(widget, "Singolo Numero")
    
    def create_batch_validation_tab(self):
        """Crea il tab per validazione batch da CSV."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Descrizione
        desc_label = QLabel("Carica un file CSV con colonna 'card_number'")
        layout.addWidget(desc_label)
        
        # Pulsante carica file
        load_button = QPushButton("📁 Carica CSV")
        load_button.setMinimumHeight(40)
        load_button.clicked.connect(self.load_csv_file)
        load_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        layout.addWidget(load_button)
        
        # Tabella risultati
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Numero Carta", "Validità", "Messaggio"])
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.results_table)
        
        # Info
        info_label = QLabel(
            "ℹ️ Formato CSV:\n"
            "card_number\n"
            "4532015112830366\n"
            "5555555555554444"
        )
        info_label.setStyleSheet("color: #666; font-size: 9pt; background-color: #f5f5f5; padding: 10px;")
        layout.addWidget(info_label)
        
        widget.setLayout(layout)
        self.tabs.addTab(widget, "Validazione Batch (CSV)")
    
    def validate_single_card(self):
        """Valida un singolo numero di carta."""
        card_number = self.card_input.text().strip()
        
        if not card_number:
            self.show_result("Errore: Inserisci un numero di carta!", error=True)
            return
        
        try:
            # Valida e opzionalmente fa l'audit log
            enable_audit = self.audit_checkbox.isChecked()
            is_valid = validate_luhn(card_number, log_audit=enable_audit)
            
            if is_valid:
                result_text = f"✓ VALIDAZIONE RIUSCITA!\n\nNumero: {card_number}\nStato: VALIDO"
                if enable_audit:
                    result_text += f"\n\n📋 Registrato in: {AUDIT_LOG_FILE}"
                self.show_result(result_text, success=True)
            else:
                result_text = f"✗ VALIDAZIONE FALLITA!\n\nNumero: {card_number}\nStato: NON VALIDO"
                if enable_audit:
                    result_text += f"\n\n📋 Registrato in: {AUDIT_LOG_FILE}"
                self.show_result(result_text, error=True)
        
        except ValueError as e:
            self.show_result(f"✗ ERRORE\n\n{str(e)}", error=True)
    
    def show_result(self, message: str, success: bool = False, error: bool = False):
        """Mostra il risultato nella text area."""
        self.result_text.setText(message)
        
        if success:
            self.result_text.setStyleSheet(
                "QTextEdit { background-color: #e8f5e9; color: #2e7d32; border: 2px solid #4caf50; }"
            )
        elif error:
            self.result_text.setStyleSheet(
                "QTextEdit { background-color: #ffebee; color: #c62828; border: 2px solid #f44336; }"
            )
        else:
            self.result_text.setStyleSheet(
                "QTextEdit { background-color: #fff3e0; color: #f57c00; border: 2px solid #ff9800; }"
            )
    
    def load_csv_file(self):
        """Carica e valida un file CSV."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleziona file CSV", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            results = validate_cards_from_csv(file_path)
            self.populate_results_table(results)
            QMessageBox.information(self, "Successo", f"Caricate {len(results)} carte dal file!")
        
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Errore", f"File non trovato: {e}")
        except ValueError as e:
            QMessageBox.critical(self, "Errore", f"Errore CSV: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore imprevisto: {e}")
    
    def populate_results_table(self, results: List[Tuple[str, bool, str]]):
        """Popola la tabella dei risultati."""
        self.results_table.setRowCount(0)
        
        for row_num, (card, is_valid, error) in enumerate(results):
            self.results_table.insertRow(row_num)
            
            # Numero carta
            card_item = QTableWidgetItem(card)
            self.results_table.setItem(row_num, 0, card_item)
            
            # Validità
            status_item = QTableWidgetItem()
            if error:
                status_item.setText("❌ ERRORE")
                status_item.setBackground(QColor("#ffebee"))
            elif is_valid:
                status_item.setText("✓ VALIDO")
                status_item.setBackground(QColor("#e8f5e9"))
            else:
                status_item.setText("✗ INVALID")
                status_item.setBackground(QColor("#fff3e0"))
            self.results_table.setItem(row_num, 1, status_item)
            
            # Messaggio errore
            msg_item = QTableWidgetItem(error)
            self.results_table.setItem(row_num, 2, msg_item)
    
    def view_audit_log(self):
        """Visualizza il file di audit log."""
        try:
            if not Path(AUDIT_LOG_FILE).exists():
                QMessageBox.information(self, "Audit Log", "Nessun audit log trovato.\nEsegui almeno una validazione con 'Registra in audit log' abilitato.")
                return
            
            with open(AUDIT_LOG_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Crea una finestra di dialogo per mostrare il contenuto
            dialog = QMessageBox(self)
            dialog.setWindowTitle("📋 Audit Log (SHA-3 Hashed)")
            dialog.setText("Validazioni registrate (numeri in hash SHA-3, NON in chiaro)")
            dialog.setDetailedText(content)
            dialog.setStyleSheet("QMessageBox { min-width: 600px; }")
            dialog.exec()
        
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nella lettura dell'audit log: {e}")
    
    def set_style(self):
        """Applica uno stile moderno all'applicazione."""
        style = """
            QMainWindow {
                background-color: #fafafa;
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 8px;
                font-size: 12pt;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
            QTextEdit {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 20px;
                border: 1px solid #ccc;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
            }
            QTableWidget {
                border: 1px solid #ddd;
                gridline-color: #eee;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: none;
            }
        """
        self.setStyleSheet(style)


def main():
    """Punto di ingresso dell'applicazione."""
    app = QApplication(sys.argv)
    window = LuhnValidatorGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
