#!/usr/bin/env python3
"""
Скрипт для обновления координат остановок в api/stops.json
на основе данных из API
"""

import json
import re
from pathlib import Path

def normalize_name(name):
    """Нормализация названия для сравнения"""
    # Убираем лишние пробелы, приводим к нижнему регистру
    name = name.lower().strip()
    # Убираем "(Рыбинск)" и подобные
    name = re.sub(r'\([^)]*\)', '', name)
    # Убираем лишние пробелы
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def find_matching_station(stop_name, stations):
    """Найти соответствующую остановку в данных API"""
    normalized_stop = normalize_name(stop_name)
    
    # Прямое совпадение
    for station in stations:
        if normalize_name(station['name']) == normalized_stop:
            return station
    
    # Частичное совпадение
    for station in stations:
        station_name = normalize_name(station['name'])
        if normalized_stop in station_name or station_name in normalized_stop:
            return station
    
    return None

def main():
    # Читаем текущие остановки
    stops_path = Path(__file__).parent.parent / 'api' / 'stops.json'
    with open(stops_path, 'r', encoding='utf-8') as f:
        stops_data = json.load(f)
    
    # Читаем данные из API
    stations_path = Path(__file__).parent.parent / 'data' / 'stations-simplified.json'
    with open(stations_path, 'r', encoding='utf-8') as f:
        stations = json.load(f)
    
    # Обновляем координаты
    updated_count = 0
    for stop in stops_data['stops']:
        station = find_matching_station(stop['name'], stations)
        if station:
            stop['latitude'] = station['lat']
            stop['longitude'] = station['lng']
            stop['address'] = station.get('address', '')
            stop['station_id'] = station.get('station_id', '')
            updated_count += 1
            print(f"[OK] Обновлено: {stop['name']} -> {station['lat']}, {station['lng']}")
        else:
            print(f"[--] Не найдено: {stop['name']}")
    
    # Сохраняем обновленные данные
    stops_data['last_updated'] = "2025-01-27T00:00:00Z"
    stops_data['note'] = "Координаты обновлены из API yarobl.dtpax.ru"
    
    with open(stops_path, 'w', encoding='utf-8') as f:
        json.dump(stops_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nОбновлено {updated_count} из {len(stops_data['stops'])} остановок")

if __name__ == '__main__':
    main()

