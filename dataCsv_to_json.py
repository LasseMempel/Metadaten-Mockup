#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV zu hierarchischem JSON Konverter
Konvertiert eine CSV-Datei mit hierarchischen Beziehungen in verschachtelte JSON-Struktur.
"""

import csv
import json
from typing import Dict, List, Any, Optional


def read_csv_data(csv_file_path: str) -> List[Dict[str, Any]]:
    """
    Liest CSV-Daten ein und bereinigt die Spaltennamen.
    
    Args:
        csv_file_path: Pfad zur CSV-Datei
        
    Returns:
        Liste von Dictionaries mit den CSV-Daten
    """
    data = []
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Bereinige leerse Spaltennamen (z.B. erste Spalte "")
            clean_row = {}
            for key, value in row.items():
                clean_key = key.strip() if key else 'index'
                # Konvertiere leere Strings zu None
                clean_value = value.strip() if value and value.strip() else None
                clean_row[clean_key] = clean_value
            
            data.append(clean_row)
    
    return data


def build_hierarchy(csv_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Baut die hierarchische Struktur aus den CSV-Daten auf.
    
    Args:
        csv_data: Liste der CSV-Zeilen als Dictionaries
        
    Returns:
        Hierarchische JSON-Struktur
    """
    # Erstelle einen Index aller Elemente nach ihrer notation
    elements_by_notation = {}
    
    for item in csv_data:
        notation = item.get('notation')
        if notation:
            # Erstelle das Element mit allen Eigenschaften
            element = {
                'notation': notation,
                'prefLabel': item.get('prefLabel'),
                'definition': item.get('definition'),
                'mandatory': item.get('mandatory'),
                'content': item.get('content'),
                'multi': item.get('multi'),
                'children': []
            }
            
            # Entferne None-Werte für sauberere JSON-Ausgabe
            element = {k: v for k, v in element.items() if v is not None or k == 'children'}
            
            elements_by_notation[notation] = element
    
    # Baue die Hierarchie auf
    root_elements = []
    
    for item in csv_data:
        notation = item.get('notation')
        broader = item.get('broader')
        
        if not notation:
            continue
            
        current_element = elements_by_notation[notation]
        
        if broader == 'top' or broader is None:
            # Top-Level Element
            root_elements.append(current_element)
        elif broader in elements_by_notation:
            # Kind-Element zu einem existierenden Parent hinzufügen
            parent = elements_by_notation[broader]
            parent['children'].append(current_element)
        else:
            # Parent existiert noch nicht - füge zu root hinzu (Fallback)
            print(f"Warnung: Parent '{broader}' für Element '{notation}' nicht gefunden")
            root_elements.append(current_element)
    
    # Entferne leere children-Arrays für sauberere Ausgabe
    def clean_empty_children(element):
        if isinstance(element, dict):
            if 'children' in element and not element['children']:
                del element['children']
            else:
                for child in element.get('children', []):
                    clean_empty_children(child)
    
    for element in root_elements:
        clean_empty_children(element)
    
    return root_elements


def save_json(data: List[Dict[str, Any]], output_file: str, pretty_print: bool = True) -> None:
    """
    Speichert die Daten als JSON-Datei.
    
    Args:
        data: Die zu speichernden Daten
        output_file: Ausgabedatei-Pfad
        pretty_print: Ob das JSON formatiert werden soll
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        if pretty_print:
            json.dump(data, file, ensure_ascii=False, indent=2)
        else:
            json.dump(data, file, ensure_ascii=False)


def main():
    """
    Hauptfunktion - führt die CSV zu JSON Konvertierung durch.
    """
    # Konfiguration
    csv_input_file = 'data.csv'
    json_output_file = 'hierarchy.json'
    
    try:
        print(f"Lese CSV-Datei: {csv_input_file}")
        csv_data = read_csv_data(csv_input_file)
        print(f"✓ {len(csv_data)} Zeilen eingelesen")
        
        print("Baue hierarchische Struktur auf...")
        hierarchy_data = build_hierarchy(csv_data)
        print("✓ Hierarchie erstellt")
        
        print(f"Speichere JSON-Datei: {json_output_file}")
        save_json(hierarchy_data, json_output_file)
        print("✓ JSON-Datei gespeichert")
        
        print(f"\n✅ Konvertierung erfolgreich abgeschlossen!")
        print(f"📁 Ausgabe: {json_output_file}")
        
    except FileNotFoundError:
        print(f"❌ Fehler: CSV-Datei '{csv_input_file}' nicht gefunden")
    except Exception as e:
        print(f"❌ Fehler bei der Konvertierung: {e}")


if __name__ == "__main__":
    main()