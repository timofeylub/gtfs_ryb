#!/usr/bin/env python3
"""
Скрипт для получения координат остановок из API
Использование: python scripts/fetch-stops-coordinates.py

ВНИМАНИЕ: Этот скрипт только для получения координат.
Не встраивать в итоговый код проекта.
"""

import json
import urllib.request
import os
from pathlib import Path

API_URL = 'https://api.yarobl.dtpax.ru/api/client/v1/stations?left_lng=38.733323&right_lng=39.008915&top_lat=58.088389&bottom_lat=57.99681'

def fetch_stations():
    """Получить список остановок из API"""
    print('Загрузка остановок из API...')
    
    with urllib.request.urlopen(API_URL) as response:
        data = response.read()
        stations = json.loads(data.decode('utf-8'))
    
    return stations

def main():
    try:
        stations = fetch_stations()
        print(f'Получено {len(stations)} остановок')
        
        # Создаем директорию data если её нет
        data_dir = Path(__file__).parent.parent / 'data'
        data_dir.mkdir(exist_ok=True)
        
        # Сохраняем полные данные
        raw_path = data_dir / 'stations-raw.json'
        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump(stations, f, ensure_ascii=False, indent=2)
        print(f'Полные данные сохранены в {raw_path}')
        
        # Создаем упрощенный формат
        simplified = [
            {
                'name': station['name'],
                'lat': station['lat'],
                'lng': station['lng'],
                'address': station['address'],
                'station_id': station['station_id']
            }
            for station in stations
        ]
        
        simplified_path = data_dir / 'stations-simplified.json'
        with open(simplified_path, 'w', encoding='utf-8') as f:
            json.dump(simplified, f, ensure_ascii=False, indent=2)
        print(f'Упрощенные данные сохранены в {simplified_path}')
        
        print('\nПримеры остановок:')
        for station in simplified[:5]:
            print(f'  {station["name"]}: {station["lat"]}, {station["lng"]}')
        
    except Exception as error:
        print(f'Ошибка: {error}')
        exit(1)

if __name__ == '__main__':
    main()

