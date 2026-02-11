# 🗣️ Tilora — Карачаевско-русский и русско-карачаевский переводчик

**Версия:** 1.0.0  
**Автор:** Temirbolatov (@thetemirbolatov)  
**Лицензия:** MIT  
**Статус:** Стабильный релиз 🚀

---

## 🌟 О проекте

**Tilora** — это мощная, профессиональная библиотека для двустороннего перевода между карачаевским и русским языками. 

Разработана с любовью к карачаевскому языку и культуре. Библиотека использует обширную базу данных слов, фраз и идиом, обеспечивая максимально точный перевод с сохранением контекста, регистра и пунктуации.

---

## ✨ Возможности

| Функция | Описание |
|---------|----------|
| 🔄 **Двусторонний перевод** | Русский ↔ Карачаевский |
| 🎯 **Приоритет фраз** | Сначала ищет точные фразы и идиомы |
| 📖 **Дословный перевод** | Если фраза не найдена — переводит по словам |
| 🖼️ **OCR с фото** | Извлекает текст с изображений и переводит |
| 📦 **Пакетная обработка** | Перевод нескольких текстов за раз |
| ⚡ **Кэширование** | Высокая скорость повторных переводов |
| 🎨 **Сохранение форматирования** | Регистр, пунктуация, пробелы |
| 📊 **Статистика** | Детальная информация о переводах |
| 🔍 **Автоопределение языка** | Автоматически определяет исходный язык |

---

## 📦 Установка

### Базовая установка

```bash
pip install tilora
С поддержкой OCR (распознавание текста с фото)
bash
pip install tilora[ocr]
Установка из исходников
bash
git clone https://github.com/thetemirbolatov-official/tilora.git
cd tilora
pip install -e .
🔧 Требования к системе
Минимальные требования
Python 3.7+

100 МБ свободного места

2 ГБ ОЗУ (рекомендуется)

Для работы OCR (Windows)
ВАЖНО! Tesseract OCR не входит в комплект библиотеки. Для работы с изображениями необходимо:

Скачать Tesseract OCR:
https://github.com/UB-Mannheim/tesseract/wiki

Установить в любую папку (рекомендуется: C:\Program Files\Tesseract-OCR\)

Или поместить tesseract.exe в папку data вашего проекта

Библиотека автоматически найдёт Tesseract в системе или в папке data.

🚀 Быстрый старт
Минимальный пример
python
from tilora import translate

# Простой перевод
print(translate("привет"))          # салам
print(translate("салам"))           # привет
print(translate("доброе утро"))     # эртденги салам
Расширенное использование
python
from tilora import KarachayTranslator, detect_language

# Создаём экземпляр переводчика
translator = KarachayTranslator()

# Перевод с деталями
result = translator.translate("как дела", return_details=True)

print(f"Оригинал: {result.original_text}")
print(f"Перевод: {result.translated_text}")
print(f"Язык: {result.source_language}")
print(f"Уверенность: {result.confidence:.1%}")
print(f"Тип: {result.translation_type}")
📖 Полная документация
1. Базовые функции
translate(text, from_lang=None, to_lang=None)
Быстрый перевод текста.

python
from tilora import translate

# Автоопределение языка
print(translate("привет"))           # салам
print(translate("салам"))            # привет

# Принудительное указание языка
print(translate("привет", from_lang='ru'))     # салам
print(translate("салам", from_lang='qar'))     # привет
detect_language(text)
Определение языка текста.

python
from tilora import detect_language

print(detect_language("привет"))     # ru
print(detect_language("салам"))      # qar
print(detect_language("къалайса"))   # qar
translate_batch(texts)
Пакетный перевод нескольких текстов.

python
from tilora import translate_batch

texts = ["привет", "как дела", "до свидания"]
results = translate_batch(texts)

for original, translated in zip(texts, results):
    print(f"{original} → {translated}")
2. Класс KarachayTranslator
Полный контроль над процессом перевода.

python
from tilora import KarachayTranslator

# Инициализация
translator = KarachayTranslator()

# Указание пути к словарю
translator = KarachayTranslator("data/words.json")

# Перевод с детальной информацией
result = translator.translate("доброе утро", return_details=True)

print(f"Перевод: {result.translated_text}")
print(f"Тип: {result.translation_type}")  # exact_phrase, partial_phrase, word_by_word
print(f"Альтернативы: {result.alternatives}")
Методы класса:
Метод	Описание
translate(text, ...)	Основной метод перевода
translate_batch(texts, ...)	Пакетный перевод
translate_from_image(image_path)	Перевод с изображения
translate_with_alternatives(text, max_alternatives=3)	Варианты перевода
get_dictionary_stats()	Статистика словаря
get_translator_stats()	Статистика переводов
clear_cache()	Очистка кэша
3. OCR — Распознавание текста с фото
python
from tilora import translate_image, KarachayTranslator

# Быстрый способ
text = translate_image("photo.jpg")
print(f"Перевод с фото: {text}")

# Расширенный способ
translator = KarachayTranslator()
result = translator.translate_from_image("photo.jpg")

if result:
    print(f"Распознано: {result.original_text}")
    print(f"Перевод: {result.translated_text}")
Поддерживаемые форматы: JPG, JPEG, PNG, BMP, TIFF, WEBP

4. Альтернативные переводы
python
from tilora import KarachayTranslator

translator = KarachayTranslator()

# Получить несколько вариантов перевода
variants = translator.translate_with_alternatives("спасибо", max_alternatives=3)

for i, variant in enumerate(variants, 1):
    print(f"{i}. {variant}")
5. Статистика и информация
python
from tilora import KarachayTranslator

translator = KarachayTranslator()

# Статистика словаря
dict_stats = translator.get_dictionary_stats()
print(f"📚 Слов в словаре: {dict_stats['total_words']}")
print(f"📝 Фраз: {dict_stats['total_phrases']}")
print(f"🇷🇺 Русско-карачаевских: {dict_stats['ru_entries']}")
print(f"🇰🇬 Карачаевско-русских: {dict_stats['qar_entries']}")

# Статистика переводов
trans_stats = translator.get_translator_stats()
print(f"⚡ Выполнено переводов: {trans_stats['total_translations']}")
print(f"💾 Кэш: {trans_stats['cache_size']} записей")
print(f"🎯 Эффективность кэша: {trans_stats['cache_ratio']:.1%}")
🎯 Примеры использования
Пример 1: Интерактивный переводчик
python
from tilora import translate, detect_language

print("🔄 Tilora Переводчик (выход: 'q')")
print("-" * 40)

while True:
    text = input("\n📝 Введите текст: ").strip()
    
    if text.lower() == 'q':
        break
    
    if not text:
        continue
    
    lang = detect_language(text)
    lang_name = "🇷🇺 Русский" if lang == 'ru' else "🇰🇬 Карачаевский"
    
    result = translate(text)
    
    print(f"{lang_name} → {result}")
Пример 2: Перевод файла
python
from tilora import KarachayTranslator

def translate_file(input_path, output_path):
    translator = KarachayTranslator()
    
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    translated = translator.translate(text)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(translated)
    
    print(f"✅ Перевод сохранён в {output_path}")

translate_file("input.txt", "output.txt")
Пример 3: Пакетная обработка фото
python
import os
from tilora import translate_image

folder = "photos"
results = {}

for filename in os.listdir(folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(folder, filename)
        translation = translate_image(path)
        results[filename] = translation
        print(f"{filename} → {translation[:50]}...")

# Сохраняем результаты
with open("translations.txt", "w", encoding="utf-8") as f:
    for filename, translation in results.items():
        f.write(f"{filename}: {translation}\n")
📊 Производительность
Операция	Скорость
Перевод слова	< 0.001 сек
Перевод фразы (5-10 слов)	< 0.005 сек
Перевод предложения (20+ слов)	< 0.02 сек
OCR + перевод фото	0.5-2 сек
Кэшированный перевод	< 0.0001 сек
🔄 Обновление
bash
# Обновление библиотеки
pip install --upgrade tilora

# Проверка версии
python -c "import tilora; print(tilora.__version__)"
❗ Часто задаваемые вопросы
❓ Не работает OCR. Что делать?
Установите Tesseract OCR:
https://github.com/UB-Mannheim/tesseract/wiki

Или поместите tesseract.exe в папку data вашего проекта

Проверьте установку:

python
from tilora import KarachayTranslator
tr = KarachayTranslator()
print(tr.translate_from_image("test.jpg"))
❓ Где скачать словарь?
Словарь words.json автоматически загружается при установке библиотеки и находится в папке data пакета.

❓ Поддерживаются ли другие языки?
В текущей версии поддерживаются только русский и карачаевский языки.

❓ Можно ли использовать в коммерческих проектах?
Да, библиотека распространяется под лицензией MIT, что позволяет использовать её в любых проектах, включая коммерческие.

🤝 Содействие проекту
Мы приветствуем любой вклад в развитие проекта!

Как помочь:
⭐ Поставьте звезду на GitHub

🐛 Сообщайте об ошибках в Issues

💡 Предлагайте улучшения

📖 Дополняйте словарь новыми словами и фразами

🌐 Рассказывайте о проекте в соцсетях

👨‍💻 Автор
Temirbolatov (@thetemirbolatov)

Разработчик, энтузиаст карачаевского языка и культуры.

📱 Социальные сети:
Платформа	Никнейм
ВКонтакте	@thetemirbolatov
Instagram	@thetemirbolatov
Telegram	@thetemirbolatov
GitHub	@thetemirbolatov-official
📧 Контакт:
По всем вопросам: thetemirbolatov@gmail.com

📄 Лицензия
MIT License

Copyright (c) 2024 Temirbolatov

Разрешается свободное использование, копирование, модификация и распространение при условии сохранения уведомления об авторстве.

🌟 Благодарности
Спасибо всем, кто помогает сохранять и развивать карачаевский язык!

Особая благодарность:

Карачаевскому научно-исследовательскому институту

Всем носителям языка, участвовавшим в составлении словаря

Сообществу разработчиков open-source

Сделано для карачаевского языка