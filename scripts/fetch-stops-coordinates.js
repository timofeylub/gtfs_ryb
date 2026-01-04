/**
 * Скрипт для получения координат остановок из API
 * Использование: node scripts/fetch-stops-coordinates.js
 * 
 * ВНИМАНИЕ: Этот скрипт только для получения координат.
 * Не встраивать в итоговый код проекта.
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const API_URL = 'https://api.yarobl.dtpax.ru/api/client/v1/stations?left_lng=38.733323&right_lng=39.008915&top_lat=58.088389&bottom_lat=57.99681';

function fetchStations() {
  return new Promise((resolve, reject) => {
    https.get(API_URL, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const stations = JSON.parse(data);
          resolve(stations);
        } catch (error) {
          reject(error);
        }
      });
    }).on('error', (error) => {
      reject(error);
    });
  });
}

async function main() {
  try {
    console.log('Загрузка остановок из API...');
    const stations = await fetchStations();
    
    console.log(`Получено ${stations.length} остановок`);
    
    // Сохраняем в файл для дальнейшего использования
    const outputPath = path.join(__dirname, '..', 'data', 'stations-raw.json');
    const outputDir = path.dirname(outputPath);
    
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    fs.writeFileSync(outputPath, JSON.stringify(stations, null, 2), 'utf8');
    console.log(`Данные сохранены в ${outputPath}`);
    
    // Создаем упрощенный формат для использования
    const simplified = stations.map(station => ({
      name: station.name,
      lat: station.lat,
      lng: station.lng,
      address: station.address,
      station_id: station.station_id
    }));
    
    const simplifiedPath = path.join(__dirname, '..', 'data', 'stations-simplified.json');
    fs.writeFileSync(simplifiedPath, JSON.stringify(simplified, null, 2), 'utf8');
    console.log(`Упрощенные данные сохранены в ${simplifiedPath}`);
    
    console.log('\nПримеры остановок:');
    simplified.slice(0, 5).forEach(station => {
      console.log(`  ${station.name}: ${station.lat}, ${station.lng}`);
    });
    
  } catch (error) {
    console.error('Ошибка:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { fetchStations };

