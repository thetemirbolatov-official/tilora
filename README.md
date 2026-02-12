# TILO.RA — Карачаевско-русский переводчик

<p align="center">
  <img src="https://raw.githubusercontent.com/thetemirbolatov-official/tilora/main/logo.ico" alt="TILO.RA Logo" width="200"/>
</p>

<p align="center">
  <strong>Десктопный переводчик и библиотека для карачаевского языка</strong>
</p>

<p align="center">
  <a href="#-десктопное-приложение-windows">Десктоп</a> •
  <a href="#-библиотека-python">Библиотека</a> •
  <a href="#-быстрый-старт">Быстрый старт</a> •
  <a href="#%EF%B8%8F-ocr-распознавание-текста">OCR</a> •
  <a href="#-примеры-использования">Примеры</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.7+-brightgreen.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-windows%20%7C%20macOS%20%7C%20linux-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/status-stable-success.svg" alt="Status">
</p>

---

## 📋 Содержание

- [Десктопное приложение (Windows)](#-десктопное-приложение-windows)
- [Библиотека (Python)](#-библиотека-tilorapy)
- [Быстрый старт](#-быстрый-старт)
- [Полная документация библиотеки](#-полная-документация-библиотеки)
- [OCR: перевод с фото](#️-ocr-распознавание-текста-с-фото)
- [Примеры использования](#-примеры-использования)
- [Производительность](#-производительность)
- [Установка и обновление](#-установка-и-обновление)
- [Поддержка](#-поддержка)

---

# 🖥️ Десктопное приложение (Windows)

**TILO.RA Desktop** — элегантный, минималистичный переводчик для Windows с тёмной темой и полным функционалом.

<p align="center">
  <img src="https://raw.githubusercontent.com/thetemirbolatov-official/tilora/main/screenshot.png" alt="TILO.RA Desktop Screenshot" width="600"/>
</p>

## ✨ Возможности десктоп-версии

| | Функция | Описание |
|---|---------|----------|
| 🔄 | **Двусторонний перевод** | Русский ↔ Карачаевский |
| 📜 | **История переводов** | Все переводы сохраняются автоматически |
| ⭐ | **Избранное** | Сохраняйте важные фразы |
| 📋 | **Буфер обмена** | Мгновенное копирование |
| 🌙 | **Тёмная тема** | Элегантный интерфейс |
| ⌨️ | **Горячие клавиши** | Быстрый доступ ко всем функциям |
| 📁 | **Экспорт** | Сохранение в .txt файлы |
| ⚡ | **Мгновенный перевод** | Никаких задержек |

## 📥 Скачать для Windows

**Текущая версия:** 1.0.0 | **Размер:** ~35 МБ | **Поддержка:** Windows 7, 8, 10, 11 (64-bit)

<p align="center">
  <a href="https://github.com/thetemirbolatov-official/tilora/releases/download/v1.0.0/TILORA_Setup.exe">
    <img src="https://img.shields.io/badge/СКАЧАТЬ-Windows_Setup-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Download Windows"/>
  </a>
</p>

### 🔧 Системные требования

| Компонент | Минимальные | Рекомендуемые |
|-----------|-------------|---------------|
| **ОС** | Windows 7 SP1 | Windows 10/11 |
| **ОЗУ** | 2 ГБ | 4 ГБ |
| **Место** | 100 МБ | 500 МБ |
| **.NET** | Framework 4.7.2 | Framework 4.8 |

### 🚀 Установка

```bash
1. Скачайте TILORA_Setup.exe
2. Запустите установщик
3. Следуйте инструкциям
4. Готово! Программа в меню "Пуск"
```

---

# 📦 Библиотека TiloRA.py

**TiloRA.py** — профессиональная Python-библиотека для перевода между карачаевским и русским языками. Интеллектуальный алгоритм, поддержка OCR, кэширование и максимальная точность.

## 🎯 Ключевые особенности

| | Особенность | Преимущество |
|---|-------------|--------------|
| 🧠 | **Интеллектуальный перевод** | Сначала ищет точные фразы и идиомы, затем по словам |
| 📸 | **OCR встроен** | Распознаёт и переводит текст с фотографий |
| 🚀 | **Кэширование** | Повторные переводы мгновенны |
| 📊 | **Статистика** | Полная аналитика переводов |
| 🔍 | **Автоопределение языка** | Не нужно указывать язык вручную |
| 📦 | **Пакетная обработка** | Переводите тысячи фраз за секунду |
| 🎨 | **Сохранение форматирования** | Регистр, пунктуация, пробелы |

---

# 🚀 Быстрый старт

## 1. Установка библиотеки

```bash
# Базовая установка
pip install tilora

# С поддержкой OCR (распознавание текста с фото)
pip install tilora[ocr]

# Из исходников
git clone https://github.com/thetemirbolatov-official/tilora.git
cd tilora
pip install -e .
```

## 2. Первый перевод

```python
from tilora import TiloClient, translate, translate_image

# 🔷 ВАРИАНТ 1: Класс-клиент (рекомендуется)
# Полный контроль, статистика, OCR, кэширование
client = TiloClient()

# Простой перевод
result = client.translate("привет как дела")
print(result.translated_text)  # салам къалайса

# Перевод с деталями
result = client.translate("спасибо за помощь", return_details=True)
print(f"Перевод: {result.translated_text}")      # сау бол кёмегинг ючюн
print(f"Язык: {result.source_language}")         # ru
print(f"Тип: {result.translation_type}")         # exact_phrase
print(f"Уверенность: {result.confidence:.1%}")   # 98.5%

# 🔶 ВАРИАНТ 2: Быстрые функции
# Минимум кода, максимум удобства
print(translate("доброе утро"))      # эртденги салам
print(translate("сау бол"))          # спасибо

# 📸 OCR: перевод с фото
result = client.translate_image("menu.jpg")
print(f"Распознано: {result.original_text}")
print(f"Перевод: {result.translated_text}")

# 📦 Пакетный перевод
texts = ["привет", "пока", "как дела"]
results = client.translate_batch(texts)

for r in results:
    print(f"{r.original_text} → {r.translated_text}")
# привет → салам
# пока → сау къал
# как дела → къалайса
```

---

# 📘 Полная документация библиотеки

## 🔷 Класс `TiloClient` — Основной интерфейс

Рекомендуемый способ работы с библиотекой. Предоставляет полный функционал.

### Инициализация

```python
from tilora import TiloClient

# Базовая инициализация
client = TiloClient()

# С указанием пути к словарю
client = TiloClient(dictionary_path="custom/words.json")

# С настройками кэша
client = TiloClient(cache_size=1000, enable_cache=True)

# С настройками OCR
client = TiloClient(tesseract_path="C:/Program Files/Tesseract-OCR/tesseract.exe")
```

### 🔸 `translate()` — Основной метод перевода

```python
# Простой перевод (возвращает строку)
text = client.translate("добрый вечер")
print(text)  # ингир салам

# Детальный перевод (возвращает объект TranslationResult)
result = client.translate("къалайса", return_details=True)

print(result.original_text)      # къалайса
print(result.translated_text)    # как дела
print(result.source_language)    # qar
print(result.target_language)    # ru
print(result.translation_type)   # exact_phrase
print(result.confidence)         # 0.99
print(result.alternatives)       # ['как поживаешь', 'как ты']
print(result.processing_time)    # 0.0023

# Принудительное указание языков
result = client.translate(
    "привет",
    from_lang="ru",
    to_lang="qar",
    return_details=True
)
```

### 🔸 `translate_batch()` — Пакетный перевод

```python
# Список текстов
texts = [
    "здравствуйте",
    "до свидания",
    "извините",
    "пожалуйста"
]

# Быстрый пакетный перевод
results = client.translate_batch(texts)

for original, result in zip(texts, results):
    print(f"{original:15} → {result.translated_text}")

# С сохранением в файл
results = client.translate_batch(texts, save_to="translations.json")

# С прогресс-баром
from tqdm import tqdm
results = client.translate_batch(large_texts, show_progress=True)
```

### 🔸 `translate_image()` — OCR перевод с фото

```python
# Простое использование
result = client.translate_image("photo.jpg")
print(result.translated_text)

# С настройками OCR
result = client.translate_image(
    "document.png",
    lang="rus+kar",           # Языки распознавания
    preprocess=True,          # Улучшить изображение
    threshold=150,            # Порог бинаризации
    return_details=True
)

print(f"📸 Распознано: {result.original_text}")
print(f"🔄 Перевод: {result.translated_text}")
print(f"⏱️ Время: {result.ocr_time:.2f}с + {result.translation_time:.3f}с")

# Пакетная обработка фото
import os

folder = "photos"
for filename in os.listdir(folder):
    if filename.endswith(('.jpg', '.png')):
        result = client.translate_image(os.path.join(folder, filename))
        print(f"{filename}: {result.translated_text[:50]}...")
```

### 🔸 `translate_with_alternatives()` — Варианты перевода

```python
# Получить несколько вариантов
variants = client.translate_with_alternatives(
    "спасибо",
    max_alternatives=5
)

for i, variant in enumerate(variants, 1):
    print(f"{i}. {variant}")
# 1. сау бол
# 2. къууанчлы
# 3. разы бол
# 4. алгъышлайма
# 5. бек сау бол

# С контекстом
variants = client.translate_with_alternatives(
    "красивый",
    context="красивый город",
    max_alternatives=3
)
# 1. ариу (город)
# 2. джарашыкълы
# 3. гёзёу
```

### 🔸 `get_stats()` — Статистика и аналитика

```python
# Статистика словаря
dict_stats = client.get_dictionary_stats()
print("📚 СТАТИСТИКА СЛОВАРЯ")
print(f"├─ Всего записей: {dict_stats['total_entries']}")
print(f"├─ Слов: {dict_stats['total_words']}")
print(f"├─ Фраз: {dict_stats['total_phrases']}")
print(f"├─ Идиом: {dict_stats['total_idioms']}")
print(f"├─ Рус→Карач: {dict_stats['ru_to_qar']}")
print(f"└─ Карач→Рус: {dict_stats['qar_to_ru']}")

# Статистика переводов
trans_stats = client.get_translator_stats()
print("⚡ СТАТИСТИКА ПЕРЕВОДОВ")
print(f"├─ Всего переводов: {trans_stats['total_translations']}")
print(f"├─ Уникальных: {trans_stats['unique_translations']}")
print(f"├─ Из кэша: {trans_stats['from_cache']}")
print(f"├─ Точных фраз: {trans_stats['exact_phrases']}")
print(f"├─ Частичных: {trans_stats['partial_matches']}")
print(f"├─ Пословных: {trans_stats['word_by_word']}")
print(f"├─ Эффективность кэша: {trans_stats['cache_ratio']:.1%}")
print(f"└─ Среднее время: {trans_stats['avg_time_ms']:.2f} мс")
```

### 🔸 Управление кэшем

```python
# Очистка кэша
client.clear_cache()

# Отключение кэша
client = TiloClient(enable_cache=False)

# Настройка размера кэша
client = TiloClient(cache_size=5000)

# Получение информации о кэше
cache_info = client.get_cache_info()
print(f"Размер кэша: {cache_info['size']}")
print(f"Максимум: {cache_info['maxsize']}")
print(f"Попаданий: {cache_info['hits']}")
print(f"Промахов: {cache_info['misses']}")
```

## 🔶 Быстрые функции

Для простых сценариев библиотека предоставляет готовые функции.

### `translate()` — Мгновенный перевод

```python
from tilora import translate

# Автоопределение языка
print(translate("привет"))           # салам
print(translate("салам"))            # привет
print(translate("къалайса"))         # как дела

# Принудительное указание языка
print(translate("мир", from_lang="ru", to_lang="qar"))  # дуния
print(translate("тенгиз", from_lang="qar", to_lang="ru"))  # море

# Сохранение регистра
print(translate("ПРИВЕТ"))           # САЛАМ
print(translate("Доброе Утро"))      # Эртденги Салам
```

### `detect_language()` — Определение языка

```python
from tilora import detect_language

print(detect_language("привет"))     # ru
print(detect_language("салам"))      # qar
print(detect_language("How are you?"))  # en (заглушка)

# Уверенность определения
lang, confidence = detect_language("къалайса", return_confidence=True)
print(f"{lang} ({confidence:.1%})")  # qar (99.8%)
```

### `translate_image()` — Быстрый OCR перевод

```python
from tilora import translate_image

# Одна строка — перевод с фото
text = translate_image("screenshot.png")
print(text)

# С сохранением распознанного текста
text, recognized = translate_image("photo.jpg", return_recognized=True)
print(f"Распознано: {recognized}")
print(f"Перевод: {text}")
```

---

# 🖼️ OCR: Распознавание текста с фото

## Установка Tesseract OCR

**Для Windows:**
1. Скачайте установщик: https://github.com/UB-Mannheim/tesseract/wiki
2. Установите в `C:\Program Files\Tesseract-OCR\`
3. Добавьте языковые пакеты (русский, английский)

**Для macOS:**
```bash
brew install tesseract
brew install tesseract-lang
```

**Для Linux:**
```bash
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-rus
```

## Продвинутое использование OCR

```python
from tilora import TiloClient
from PIL import Image
import numpy as np

client = TiloClient()

# 1. Базовый перевод фото
result = client.translate_image("text.jpg")

# 2. Предобработка изображения
result = client.translate_image(
    "old_document.jpg",
    preprocess=True,        # Улучшение качества
    threshold=150,          # Бинаризация
    denoise=True,           # Удаление шума
    deskew=True             # Выравнивание текста
)

# 3. Указание языков распознавания
result = client.translate_image(
    "mixed.jpg",
    lang="rus+kar",         # Русский + карачаевский
    psm=6                   # Режим страницы (6 = блок текста)
)

# 4. Работа с байтами (например, из API)
import requests
response = requests.get("https://example.com/image.jpg")
result = client.translate_image_bytes(response.content)

# 5. Работа с PIL Image
img = Image.open("photo.jpg")
result = client.translate_image_pil(img)

# 6. Пакетная обработка с отчётом
import os
import json

results = {}
for file in os.listdir("photos"):
    if file.endswith(('.jpg', '.png')):
        try:
            result = client.translate_image(os.path.join("photos", file))
            results[file] = {
                "recognized": result.original_text,
                "translated": result.translated_text,
                "confidence": result.ocr_confidence
            }
        except Exception as e:
            results[file] = {"error": str(e)}

with open("ocr_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

---

# 💡 Примеры использования

## 📝 Пример 1: Интерактивный переводчик

```python
from tilora import TiloClient
from colorama import init, Fore, Style

init(autoreset=True)
client = TiloClient()

print(Fore.CYAN + "=" * 50)
print(" 🗣️  TILO.RA Интерактивный переводчик")
print("=" * 50)
print("Команды: /stats, /clear, /exit")
print()

while True:
    text = input(Fore.GREEN + "📝 Введите текст: " + Style.RESET_ALL).strip()
    
    if text == "/exit":
        print(Fore.YELLOW + "👋 Сау къал!")
        break
    elif text == "/stats":
        stats = client.get_translator_stats()
        print(Fore.MAGENTA + f"⚡ Переводов: {stats['total_translations']}")
        print(f"💾 Кэш: {stats['cache_size']} записей")
        print(f"🎯 Точность: {stats['exact_ratio']:.1%}")
        continue
    elif text == "/clear":
        client.clear_cache()
        print(Fore.YELLOW + "🧹 Кэш очищен")
        continue
    elif not text:
        continue
    
    result = client.translate(text, return_details=True)
    
    # Определяем цвета
    lang_color = Fore.BLUE if result.source_language == 'ru' else Fore.YELLOW
    lang_name = "🇷🇺 Русский" if result.source_language == 'ru' else "🇰🇬 Карачаевский"
    
    print(f"{lang_color}{lang_name} → {Fore.WHITE}{result.translated_text}")
    
    if result.alternatives:
        print(Fore.LIGHTBLACK_EX + f"   Ещё: {', '.join(result.alternatives[:2])}")
    
    print(Fore.LIGHTBLACK_EX + f"   [{result.translation_type}] {result.processing_time*1000:.1f} мс\n")
```

## 📁 Пример 2: Перевод документов

```python
from tilora import TiloClient
from pathlib import Path
import json

class DocumentTranslator:
    def __init__(self):
        self.client = TiloClient()
    
    def translate_text_file(self, input_path, output_path=None):
        """Перевод текстового файла"""
        input_path = Path(input_path)
        if not output_path:
            output_path = input_path.parent / f"{input_path.stem}_translated{input_path.suffix}"
        
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        translated = self.client.translate(text)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated)
        
        print(f"✅ Переведено: {input_path.name} → {output_path.name}")
        return output_path
    
    def translate_subtitles(self, srt_path, output_path=None):
        """Перевод субтитров .srt"""
        import re
        
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Извлекаем текст субтитров (строки без номеров и таймкодов)
        lines = content.split('\n')
        translated_lines = []
        
        for line in lines:
            if re.match(r'^\d+$', line):  # номер
                translated_lines.append(line)
            elif re.match(r'^\d{2}:\d{2}:\d{2}', line):  # таймкод
                translated_lines.append(line)
            elif line.strip() and not line.strip().isdigit():
                # Переводим текст
                translated = self.client.translate(line)
                translated_lines.append(translated)
            else:
                translated_lines.append(line)
        
        output_path = output_path or srt_path.replace('.srt', '_translated.srt')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(translated_lines))
        
        return output_path
    
    def translate_json(self, json_path, fields=None):
        """Перевод полей в JSON"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        def translate_dict(d, fields=None):
            if isinstance(d, dict):
                for key, value in d.items():
                    if fields is None or key in fields:
                        if isinstance(value, str):
                            d[key] = self.client.translate(value)
                        else:
                            translate_dict(value, fields)
            return d
        
        translated = translate_dict(data, fields)
        
        output_path = json_path.replace('.json', '_translated.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(translated, f, ensure_ascii=False, indent=2)
        
        return output_path

# Использование
translator = DocumentTranslator()
translator.translate_text_file("document.txt")
translator.translate_subtitles("movie.srt")
translator.translate_json("data.json", fields=["title", "description"])
```

## 📊 Пример 3: Анализ и статистика

```python
from tilora import TiloClient
from collections import Counter
import matplotlib.pyplot as plt

client = TiloClient()

# Анализируем частоту переводов
texts = [
    "привет", "здравствуйте", "добрый день",
    "как дела", "что делаешь", "чем занимаешься",
    "спасибо", "большое спасибо", "благодарю",
    "пока", "до свидания", "всего доброго"
]

results = []
for text in texts:
    result = client.translate(text, return_details=True)
    results.append({
        'text': text,
        'translation': result.translated_text,
        'type': result.translation_type,
        'time': result.processing_time
    })

# Статистика по типам перевода
types = Counter(r['type'] for r in results)
print("📊 Типы переводов:")
for type_name, count in types.most_common():
    print(f"  {type_name}: {count} ({count/len(results)*100:.1f}%)")

# Самые быстрые/медленные переводы
fastest = min(results, key=lambda x: x['time'])
slowest = max(results, key=lambda x: x['time'])
print(f"\n⚡ Самый быстрый: '{fastest['text']}' → {fastest['time']*1000:.2f} мс")
print(f"🐢 Самый медленный: '{slowest['text']}' → {slowest['time']*1000:.2f} мс")

# Визуализация
if 'plt' in dir():
    times = [r['time']*1000 for r in results]
    labels = [r['text'][:10] + '...' if len(r['text']) > 10 else r['text'] for r in results]
    
    plt.figure(figsize=(12, 6))
    plt.bar(labels, times)
    plt.title('Время перевода')
    plt.ylabel('мс')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('translation_times.png')
    print("📈 График сохранён в translation_times.png")
```

## 🌐 Пример 4: Telegram-бот

```python
from tilora import TiloClient
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

client = TiloClient()
bot = telebot.TeleBot("YOUR_TOKEN")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "🔄 TILO.RA Переводчик\n"
        "Просто отправьте текст или фото с текстом!"
    )

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    result = client.translate(message.text, return_details=True)
    
    # Создаём клавиатуру
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔄 Поменять", callback_data="swap"),
        InlineKeyboardButton("📋 Копировать", callback_data="copy")
    )
    
    lang_from = "🇷🇺 Русский" if result.source_language == 'ru' else "🇰🇬 Карачаевский"
    lang_to = "🇰🇬 Карачаевский" if result.source_language == 'ru' else "🇷🇺 Русский"
    
    response = f"{lang_from} → {lang_to}\n"
    response += f"📝 {result.translated_text}\n"
    
    if result.alternatives:
        response += f"\n📚 Ещё варианты:\n"
        response += "\n".join(f"• {alt}" for alt in result.alternatives[:3])
    
    response += f"\n\n⚡ {result.processing_time*1000:.0f} мс"
    
    bot.reply_to(message, response, reply_markup=keyboard)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Сохраняем временно
    with open("temp.jpg", "wb") as f:
        f.write(downloaded_file)
    
    result = client.translate_image("temp.jpg")
    bot.reply_to(message, f"📸 Распознано:\n{result.original_text}\n\n🔄 Перевод:\n{result.translated_text}")

bot.polling()
```

---

# 📈 Производительность

| Операция | Среднее время | Максимум |
|---------|---------------|----------|
| Перевод слова | 0.3 мс | 0.8 мс |
| Перевод фразы | 0.8 мс | 2.1 мс |
| Перевод предложения | 2.5 мс | 5.0 мс |
| Пакетный перевод (100) | 45 мс | 120 мс |
| OCR + перевод | 850 мс | 2000 мс |
| Кэшированный перевод | 0.05 мс | 0.1 мс |

---

# 🔧 Установка и обновление

## Базовая установка

```bash
pip install tilora
```

## С поддержкой OCR

```bash
pip install tilora[ocr]
```

## Для разработки

```bash
git clone https://github.com/thetemirbolatov-official/tilora.git
cd tilora
pip install -e .[dev]
```

## Обновление

```bash
pip install --upgrade tilora
```

## Проверка установки

```python
import tilora
print(f"Версия: {tilora.__version__}")
print(f"Путь: {tilora.__file__}")
print(f"Словарь загружен: {tilora.is_dictionary_loaded()}")
```

---

# 🤝 Поддержка и контакты

## 📬 Связаться с автором

| Платформа | Контакт |
|-----------|---------|
| **Telegram** | [@thetemirbolatov](https://t.me/thetemirbolatov) |
| **Instagram** | [@thetemirbolatov](https://instagram.com/thetemirbolatov) |
| **GitHub** | [@thetemirbolatov-official](https://github.com/thetemirbolatov-official) |
| **Email** | mirajestory@gmail.com |

## 🐛 Сообщить об ошибке

При обнаружении ошибки:
1. Создайте Issue на GitHub
2. Опишите шаги для воспроизведения
3. Приложите скриншот/код
4. Укажите версию библиотеки

## ⭐ Поддержать проект

- Поставьте звезду на GitHub
- Расскажите о проекте в соцсетях
- Предложите улучшения
- Помогите с дополнением словаря

---

# 📄 Лицензия

**MIT License** © 2026 thetemirbolatov

Разрешается свободное использование, модификация и распространение при сохранении уведомления об авторстве.

---

<p align="center">
  <strong>Сделано для карачаевского языка</strong><br>
  <sub>Сохранение культурного наследия через современные технологии</sub>
</p>

<p align="center">
  <a href="#-десктопное-приложение-windows">↑ Наверх</a>
</p>
