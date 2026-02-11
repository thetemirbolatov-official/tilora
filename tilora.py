"""
tilora.py - Полная библиотека переводчика карачаевского языка
ТОЛЬКО ВНЕШНИЙ СЛОВАРЬ - никаких встроенных переводов!
Версия 4.0.0 (Стабильная)

Автор: Tilora Team
Лицензия: MIT

Использование ТОЛЬКО из файла words.json
Без встроенных словарей!
"""

import json
import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass, field
from collections import defaultdict
import base64
import tempfile
from io import BytesIO

# ========== ПРОВЕРКА И НАСТРОЙКА TESSERACT OCR ==========

TESSERACT_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    os.path.join(os.path.dirname(__file__), 'data', 'tesseract.exe'),
    os.path.join(os.path.dirname(__file__), 'data', 'Tesseract-OCR', 'tesseract.exe'),
    'tesseract'
]

TESSERACT_CMD = None
OCR_AVAILABLE = False

# Ищем Tesseract
for tess_path in TESSERACT_PATHS:
    if os.path.exists(tess_path):
        TESSERACT_CMD = tess_path
        OCR_AVAILABLE = True
        break

if not OCR_AVAILABLE:
    try:
        import shutil
        tess_in_path = shutil.which('tesseract')
        if tess_in_path:
            TESSERACT_CMD = tess_in_path
            OCR_AVAILABLE = True
    except:
        pass

# Пытаемся импортировать pytesseract
try:
    import pytesseract
    from PIL import Image, ImageEnhance
    
    if TESSERACT_CMD:
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
    
    try:
        version = pytesseract.get_tesseract_version()
        OCR_AVAILABLE = True
    except:
        OCR_AVAILABLE = False
except ImportError:
    OCR_AVAILABLE = False

# ========== КОНСТАНТЫ ==========

# Только для определения языка - НЕ СЛОВАРЬ!
KARACHAY_CHARS = {'ң', 'ғ', 'ә', 'ө', 'ү', 'һ', 'қ', 'ў', 'ѕ', 'ј', 'ѓ', 'ќ', 'џ'}
KARACHAY_COMBINATIONS = {'къ', 'нг', 'дж', 'гъ', 'гь', 'кь', 'нъ', 'пъ', 'тъ', 'бг'}
KARACHAY_ENDINGS = {'са', 'се', 'гъа', 'ге', 'ны', 'ни', 'ла', 'ле', 'дан', 'ден', 
                   'ма', 'ме', 'ды', 'ди', 'ду', 'дю', 'ту', 'тю', 'гъы', 'ги'}


@dataclass
class TranslationResult:
    """Результат перевода с дополнительной информацией"""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float
    translation_type: str  # 'exact_phrase', 'partial_phrase', 'word_by_word', 'not_found'
    alternatives: List[str] = field(default_factory=list)
    
    def __str__(self):
        return self.translated_text
    
    def to_dict(self) -> Dict:
        return {
            'original': self.original_text,
            'translated': self.translated_text,
            'from': self.source_language,
            'to': self.target_language,
            'confidence': self.confidence,
            'type': self.translation_type,
            'alternatives': self.alternatives
        }


class KarachayDictionary:
    """Загрузка словарей ТОЛЬКО из JSON файла"""
    
    def __init__(self, dictionary_path: Optional[str] = None):
        """Инициализация словаря - ТОЛЬКО ИЗ ФАЙЛА!"""
        self.dictionary_path = self._find_dictionary(dictionary_path)
        
        # Основные словари - будут заполнены из JSON
        self.ru_to_qar = {}      # Русский -> Карачаевский
        self.qar_to_ru = {}      # Карачаевский -> Русский
        self.ru_to_qar_multi = {}  # Русский -> [варианты]
        self.qar_to_ru_multi = {}  # Карачаевский -> [варианты]
        
        # Фразы и идиомы
        self.phrases_ru_to_qar = {}
        self.phrases_qar_to_ru = {}
        
        # Сортированные фразы
        self.sorted_phrases_ru = []
        self.sorted_phrases_qar = []
        
        # Статистика
        self.stats = {
            'total_words': 0, 
            'total_phrases': 0, 
            'total_variants': 0,
            'ru_entries': 0,
            'qar_entries': 0
        }
        
        # ЗАГРУЖАЕМ ТОЛЬКО ИЗ ФАЙЛА!
        self._load_dictionaries()
        
        # Если словарь пустой - критическая ошибка
        if len(self.ru_to_qar) == 0 and len(self.qar_to_ru) == 0:
            raise RuntimeError("❌ КРИТИЧЕСКАЯ ОШИБКА: Словарь не загружен! Файл words.json не найден или пуст!")
        
        self._build_indexes()
    
    def _find_dictionary(self, dictionary_path: Optional[str]) -> str:
        """Поиск файла словаря - ТОЛЬКО JSON!"""
        if dictionary_path and os.path.exists(dictionary_path):
            print(f"✅ Словарь загружен: {dictionary_path}")
            return dictionary_path
        
        # Проверяем возможные пути
        paths_to_try = [
            'data/words.json',
            'words.json',
            os.path.join(os.path.dirname(__file__), 'data', 'words.json'),
            os.path.join(os.path.dirname(__file__), 'words.json'),
            '../data/words.json',
            './data/words.json'
        ]
        
        for path in paths_to_try:
            if os.path.exists(path):
                print(f"✅ Словарь загружен: {os.path.abspath(path)}")
                return os.path.abspath(path)
        
        # Если словарь не найден - выбрасываем исключение
        raise FileNotFoundError(
            "❌ ФАЙЛ СЛОВАРЯ НЕ НАЙДЕН!\n"
            "Поместите файл words.json в папку 'data' или в текущую директорию.\n"
            "Использование встроенных словарей ОТКЛЮЧЕНО!"
        )
    
    def _load_dictionaries(self):
        """Загрузка словарей ТОЛЬКО из JSON файла"""
        try:
            with open(self.dictionary_path, 'r', encoding='utf-8') as f:
                raw_dict = json.load(f)
            
            if not raw_dict:
                raise ValueError("Файл словаря пуст!")
            
            ru_count = 0
            qar_count = 0
            
            for key, value in raw_dict.items():
                if not value:
                    continue
                
                # Определяем направление
                is_russian = self._is_russian_text(key)
                
                # Разбиваем переводы на варианты
                translations = self._split_translations(value)
                
                if not translations:
                    continue
                
                if is_russian:
                    # Русский -> Карачаевский
                    self.ru_to_qar_multi[key.lower()] = translations
                    self.ru_to_qar[key.lower()] = translations[0]
                    ru_count += 1
                    
                    if ' ' in key:
                        self.phrases_ru_to_qar[key.lower()] = translations[0]
                    
                    # Добавляем в обратный словарь
                    for trans in translations[:10]:
                        clean_trans = self._clean_word(trans)
                        if clean_trans:
                            if clean_trans not in self.qar_to_ru_multi:
                                self.qar_to_ru_multi[clean_trans] = [key]
                                self.qar_to_ru[clean_trans] = key
                                qar_count += 1
                            elif key not in self.qar_to_ru_multi[clean_trans]:
                                self.qar_to_ru_multi[clean_trans].append(key)
                else:
                    # Карачаевский -> Русский
                    self.qar_to_ru_multi[key.lower()] = translations
                    self.qar_to_ru[key.lower()] = translations[0]
                    qar_count += 1
                    
                    if ' ' in key:
                        self.phrases_qar_to_ru[key.lower()] = translations[0]
                    
                    # Добавляем в обратный словарь
                    for trans in translations[:10]:
                        clean_trans = self._clean_word(trans)
                        if clean_trans:
                            if clean_trans not in self.ru_to_qar_multi:
                                self.ru_to_qar_multi[clean_trans] = [key]
                                self.ru_to_qar[clean_trans] = key
                                ru_count += 1
                            elif key not in self.ru_to_qar_multi[clean_trans]:
                                self.ru_to_qar_multi[clean_trans].append(key)
            
            self.stats['total_words'] = ru_count + qar_count
            self.stats['total_phrases'] = len(self.phrases_ru_to_qar) + len(self.phrases_qar_to_ru)
            self.stats['total_variants'] = sum(len(v) for v in self.ru_to_qar_multi.values()) + \
                                          sum(len(v) for v in self.qar_to_ru_multi.values())
            self.stats['ru_entries'] = ru_count
            self.stats['qar_entries'] = qar_count
            
            print(f"📚 Загружено: {self.stats['total_words']} слов, {self.stats['total_phrases']} фраз")
            
        except Exception as e:
            raise RuntimeError(f"❌ Ошибка загрузки словаря: {e}")
    
    def _build_indexes(self):
        """Построение индексов для быстрого поиска"""
        # Сортируем фразы по длине
        self.sorted_phrases_ru = sorted(self.phrases_ru_to_qar.keys(), 
                                       key=lambda x: len(x), reverse=True)
        self.sorted_phrases_qar = sorted(self.phrases_qar_to_ru.keys(), 
                                        key=lambda x: len(x), reverse=True)
    
    @staticmethod
    def _split_translations(text: str) -> List[str]:
        """Разделение переводов на варианты"""
        if not text:
            return []
        
        text = str(text)
        for sep in [';', ' и ', ' или ', '/', '\\', '|', '  ', '   ']:
            text = text.replace(sep, ',')
        
        variants = [v.strip() for v in text.split(',') if v.strip()]
        
        seen = set()
        unique = []
        for v in variants:
            clean = re.sub(r'\s+', ' ', v)
            if clean and clean not in seen:
                seen.add(clean)
                unique.append(clean)
        
        return unique
    
    @staticmethod
    def _clean_word(word: str) -> str:
        """Очистка слова от знаков препинания"""
        if not word:
            return ""
        return re.sub(r'[^\w\s-]', '', word).strip().lower()
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Нормализация текста для поиска"""
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @staticmethod
    def _is_russian_text(text: str) -> bool:
        """Определение, содержит ли текст русские буквы"""
        if not text:
            return False
        rus_pattern = re.compile(r'[а-яА-ЯёЁ]')
        kar_pattern = re.compile(r'[ңғәөүһқўѕјѓќџ]')
        
        has_russian = bool(rus_pattern.search(text))
        has_karachay = bool(kar_pattern.search(text))
        
        return has_russian and not has_karachay
    
    def get_translation(self, word: str, from_lang: str, return_all: bool = False):
        """Получение перевода слова ТОЛЬКО ИЗ СЛОВАРЯ"""
        if not word:
            return [] if return_all else None
        
        clean_word = self._clean_word(word)
        
        if from_lang == 'ru':
            if return_all:
                return self.ru_to_qar_multi.get(clean_word, [])
            return self.ru_to_qar.get(clean_word)
        else:
            if return_all:
                return self.qar_to_ru_multi.get(clean_word, [])
            return self.qar_to_ru.get(clean_word)
    
    def find_phrases(self, text: str, from_lang: str) -> List[Tuple[str, str, int, int]]:
        """Поиск фраз в тексте"""
        found = []
        if not text:
            return found
        
        norm_text = self.normalize_text(text)
        phrases_dict = self.phrases_ru_to_qar if from_lang == 'ru' else self.phrases_qar_to_ru
        sorted_phrases = self.sorted_phrases_ru if from_lang == 'ru' else self.sorted_phrases_qar
        
        for phrase in sorted_phrases:
            if not phrase:
                continue
            
            norm_phrase = self.normalize_text(phrase)
            
            if len(norm_phrase) <= 2:
                continue
            
            if norm_phrase in norm_text:
                pos = norm_text.find(norm_phrase)
                if pos != -1:
                    found.append((
                        phrase,
                        phrases_dict[phrase],
                        pos,
                        pos + len(phrase)
                    ))
        
        # Сортируем по длине
        found.sort(key=lambda x: len(x[0]), reverse=True)
        return found


class LanguageDetector:
    """Определитель языка (только для определения, НЕ СЛОВАРЬ)"""
    
    def __init__(self, dictionary: KarachayDictionary):
        self.dict = dictionary
    
    def detect(self, text: str) -> str:
        """Определение языка текста"""
        if not text or not isinstance(text, str):
            return 'ru'
        
        text_lower = text.lower().strip()
        
        if not text_lower:
            return 'ru'
        
        # 1. Проверка специфических символов
        if any(c in text_lower for c in KARACHAY_CHARS):
            return 'qar'
        
        # 2. Проверка характерных комбинаций
        if any(c in text_lower for c in KARACHAY_COMBINATIONS):
            return 'qar'
        
        # 3. Анализ слов по словарю
        words = re.findall(r'\b[а-яёңғәөүһқўѕјѓќџ]+\b', text_lower)
        
        if not words:
            return 'ru'
        
        ru_score = 0
        qar_score = 0
        
        for word in words[:20]:
            if word in self.dict.ru_to_qar:
                ru_score += 1
            if word in self.dict.qar_to_ru:
                qar_score += 1
        
        if qar_score > ru_score:
            return 'qar'
        
        return 'ru'
    
    def detect_with_confidence(self, text: str) -> Tuple[str, float]:
        """Определение языка с оценкой уверенности"""
        if not text:
            return 'ru', 0.0
        
        words = re.findall(r'\b\w+\b', text.lower())
        if not words:
            return 'ru', 0.5
        
        ru_matches = sum(1 for w in words if w in self.dict.ru_to_qar)
        qar_matches = sum(1 for w in words if w in self.dict.qar_to_ru)
        
        total = ru_matches + qar_matches
        
        if total == 0:
            return 'ru', 0.5
        
        if ru_matches > qar_matches:
            return 'ru', ru_matches / total
        elif qar_matches > ru_matches:
            return 'qar', qar_matches / total
        else:
            return 'ru', 0.5


class TextProcessor:
    """Обработка текста"""
    
    @staticmethod
    def preserve_case(original: str, translated: str) -> str:
        """Сохранение регистра"""
        if not original or not translated:
            return translated or ""
        
        if original[0].isupper():
            if len(translated) > 0:
                return translated[0].upper() + translated[1:]
        return translated
    
    @staticmethod
    def preserve_punctuation(original: str, translated: str) -> str:
        """Сохранение пунктуации"""
        if not original or not translated:
            return translated or ""
        
        original = original.strip()
        translated = translated.strip()
        
        if not original or not translated:
            return translated
        
        orig_last = original[-1]
        trans_last = translated[-1]
        
        if orig_last in '.!?;:,' and trans_last not in '.!?;:,':
            translated += orig_last
        
        return translated


class KarachayTranslator:
    """
    Основной класс переводчика - ТОЛЬКО ВНЕШНИЙ СЛОВАРЬ!
    """
    
    def __init__(self, dictionary_path: Optional[str] = None):
        """Инициализация переводчика"""
        self.dictionary = KarachayDictionary(dictionary_path)
        self.detector = LanguageDetector(self.dictionary)
        self.text_processor = TextProcessor()
        self.cache = {}
        
        self.stats = {
            'translations': 0,
            'cache_hits': 0,
            'ocr_translations': 0
        }
    
    def translate(self, 
                 text: str, 
                 source_lang: Optional[str] = None,
                 target_lang: Optional[str] = None,
                 return_details: bool = False) -> Union[str, TranslationResult]:
        """
        Перевод текста ТОЛЬКО по словарю!
        """
        if not text or not isinstance(text, str):
            return "" if not return_details else TranslationResult("", "", "ru", "ru", 0.0, "empty", [])
        
        text = text.strip()
        if not text:
            return "" if not return_details else TranslationResult("", "", "ru", "ru", 0.0, "empty", [])
        
        # Определяем языки
        if source_lang is None:
            source_lang, confidence = self.detector.detect_with_confidence(text)
        else:
            confidence = 0.9
        
        if target_lang is None:
            target_lang = 'qar' if source_lang == 'ru' else 'ru'
        
        # Проверка кэша
        cache_key = f"{source_lang}:{target_lang}:{text.lower()}"
        if cache_key in self.cache:
            self.stats['cache_hits'] += 1
            cached = self.cache[cache_key]
            if return_details:
                return TranslationResult(text, cached, source_lang, target_lang, 1.0, "cached", [])
            return cached
        
        self.stats['translations'] += 1
        
        # ВЫПОЛНЯЕМ ПЕРЕВОД ТОЛЬКО ИЗ СЛОВАРЯ
        if source_lang == 'ru' and target_lang == 'qar':
            translated, trans_type, alternatives = self._translate_ru_to_qar(text)
        elif source_lang == 'qar' and target_lang == 'ru':
            translated, trans_type, alternatives = self._translate_qar_to_ru(text)
        else:
            translated, trans_type, alternatives = text, "unsupported", []
        
        # Сохраняем в кэш
        self.cache[cache_key] = translated
        
        if return_details:
            return TranslationResult(
                text, translated, source_lang, target_lang,
                confidence, trans_type, alternatives[:3]
            )
        
        return translated
    
    def _translate_ru_to_qar(self, text: str) -> Tuple[str, str, List[str]]:
        """Перевод с русского на карачаевский ТОЛЬКО ИЗ СЛОВАРЯ"""
        alternatives = []
        text_lower = text.lower()
        
        # 1. Точное совпадение всей фразы
        if text_lower in self.dictionary.phrases_ru_to_qar:
            translation = self.dictionary.phrases_ru_to_qar[text_lower]
            translation = self.text_processor.preserve_case(text, translation)
            translation = self.text_processor.preserve_punctuation(text, translation)
            return translation, 'exact_phrase', alternatives
        
        # 2. Ищем фразы внутри текста
        phrases = self.dictionary.find_phrases(text_lower, 'ru')
        if phrases:
            result = text
            for phrase, translation, start, end in phrases:
                # Находим позицию в оригинальном тексте с учетом регистра
                orig_phrase = text[start:end]
                translated_part = self.text_processor.preserve_case(orig_phrase, translation)
                result = result[:start] + translated_part + result[end:]
            return result, 'partial_phrase', alternatives
        
        # 3. Дословный перевод
        words = re.findall(r'\b\w+\b|[^\w\s]+|\s+', text)
        translated_words = []
        
        for word in words:
            if re.match(r'\b\w+\b', word):
                translation = self.dictionary.get_translation(word, 'ru')
                if translation:
                    translated_word = self.text_processor.preserve_case(word, translation)
                    translated_words.append(translated_word)
                    
                    # Собираем альтернативы для первого слова
                    if not alternatives:
                        alts = self.dictionary.get_translation(word, 'ru', return_all=True)
                        if len(alts) > 1:
                            alternatives = [self.text_processor.preserve_case(word, a) for a in alts[1:4]]
                else:
                    # Слово не найдено - оставляем как есть
                    translated_words.append(word)
            else:
                translated_words.append(word)
        
        result = ''.join(translated_words)
        result = self.text_processor.preserve_punctuation(text, result)
        
        if not result or result == text:
            return text, 'not_found', alternatives
        
        return result, 'word_by_word', alternatives
    
    def _translate_qar_to_ru(self, text: str) -> Tuple[str, str, List[str]]:
        """Перевод с карачаевского на русский ТОЛЬКО ИЗ СЛОВАРЯ"""
        alternatives = []
        text_lower = text.lower()
        
        # 1. Точное совпадение всей фразы
        if text_lower in self.dictionary.phrases_qar_to_ru:
            translation = self.dictionary.phrases_qar_to_ru[text_lower]
            translation = self.text_processor.preserve_case(text, translation)
            translation = self.text_processor.preserve_punctuation(text, translation)
            return translation, 'exact_phrase', alternatives
        
        # 2. Ищем фразы внутри текста
        phrases = self.dictionary.find_phrases(text_lower, 'qar')
        if phrases:
            result = text
            for phrase, translation, start, end in phrases:
                orig_phrase = text[start:end]
                translated_part = self.text_processor.preserve_case(orig_phrase, translation)
                result = result[:start] + translated_part + result[end:]
            return result, 'partial_phrase', alternatives
        
        # 3. Дословный перевод
        words = re.findall(r'\b\w+\b|[^\w\s]+|\s+', text)
        translated_words = []
        
        for word in words:
            if re.match(r'\b\w+\b', word):
                translation = self.dictionary.get_translation(word, 'qar')
                if translation:
                    translated_word = self.text_processor.preserve_case(word, translation)
                    translated_words.append(translated_word)
                    
                    if not alternatives:
                        alts = self.dictionary.get_translation(word, 'qar', return_all=True)
                        if len(alts) > 1:
                            alternatives = [self.text_processor.preserve_case(word, a) for a in alts[1:4]]
                else:
                    translated_words.append(word)
            else:
                translated_words.append(word)
        
        result = ''.join(translated_words)
        result = self.text_processor.preserve_punctuation(text, result)
        
        if not result or result == text:
            return text, 'not_found', alternatives
        
        return result, 'word_by_word', alternatives
    
    def translate_from_image(self, image_input: Union[str, bytes]) -> Optional[TranslationResult]:
        """
        Перевод текста с изображения
        ИСПРАВЛЕНО: правильная обработка фото и текста
        """
        if not OCR_AVAILABLE:
            print("⚠️ Tesseract OCR не найден!")
            return None
        
        try:
            import pytesseract
            from PIL import Image, ImageEnhance
            
            # Получаем изображение
            image = None
            
            if isinstance(image_input, str):
                if not os.path.exists(image_input):
                    print(f"❌ Файл не найден: {image_input}")
                    return None
                
                try:
                    image = Image.open(image_input)
                except Exception as e:
                    print(f"❌ Ошибка открытия: {e}")
                    return None
            elif isinstance(image_input, bytes):
                try:
                    image = Image.open(BytesIO(image_input))
                except Exception as e:
                    print(f"❌ Ошибка декодирования: {e}")
                    return None
            else:
                return None
            
            if image is None:
                return None
            
            # Конвертируем в RGB
            if image.mode in ('RGBA', 'LA', 'P'):
                bg = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA':
                    bg.paste(image, mask=image.split()[3])
                elif image.mode == 'P':
                    image = image.convert('RGBA')
                    bg.paste(image, mask=image.split()[3])
                else:
                    bg.paste(image, mask=image.convert('RGBA').split()[3])
                image = bg
            
            # Улучшаем для OCR
            image = image.convert('L')
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Распознаем текст - ТОЛЬКО РУССКИЙ И АНГЛИЙСКИЙ!
            custom_config = r'--oem 3 --psm 6 -l rus'
            try:
                extracted_text = pytesseract.image_to_string(image, config=custom_config)
            except:
                custom_config = r'--oem 3 --psm 6 -l eng'
                extracted_text = pytesseract.image_to_string(image, config=custom_config)
            
            extracted_text = extracted_text.strip()
            
            if not extracted_text:
                print("⚠️ Текст на изображении не найден")
                return None
            
            # ОЧИЩАЕМ ТЕКСТ ОТ МУСОРА!
            # Убираем лишние пробелы, переносы строк, специальные символы
            extracted_text = re.sub(r'\s+', ' ', extracted_text)
            extracted_text = re.sub(r'[^\w\s.,!?;:а-яА-ЯёЁңғәөүһқўѕјѓќџ-]', '', extracted_text)
            extracted_text = extracted_text.strip()
            
            if len(extracted_text) < 2:
                return None
            
            print(f"📝 Распознанный текст: {extracted_text[:100]}")
            
            # Переводим текст
            result = self.translate(extracted_text, return_details=True)
            result.translation_type = f"ocr_{result.translation_type}"
            
            self.stats['ocr_translations'] += 1
            
            return result
            
        except Exception as e:
            print(f"❌ Ошибка OCR: {e}")
            return None
    
    def get_dictionary_stats(self) -> Dict[str, Any]:
        """Статистика словаря"""
        return {
            'total_words': self.dictionary.stats['total_words'],
            'total_phrases': self.dictionary.stats['total_phrases'],
            'ru_entries': self.dictionary.stats['ru_entries'],
            'qar_entries': self.dictionary.stats['qar_entries']
        }


# ========== ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР ==========

_GLOBAL_TRANSLATOR = None

def get_translator(dictionary_path: Optional[str] = None) -> KarachayTranslator:
    """Получение глобального экземпляра переводчика"""
    global _GLOBAL_TRANSLATOR
    if _GLOBAL_TRANSLATOR is None:
        _GLOBAL_TRANSLATOR = KarachayTranslator(dictionary_path)
    return _GLOBAL_TRANSLATOR


def translate(text: str, from_lang: Optional[str] = None, to_lang: Optional[str] = None) -> str:
    """Быстрый перевод текста"""
    translator = get_translator()
    return translator.translate(text, from_lang, to_lang)


def detect_language(text: str) -> str:
    """Быстрое определение языка"""
    translator = get_translator()
    return translator.detector.detect(text)


def translate_image(image_path: str) -> str:
    """
    Перевод текста с изображения
    ИСПРАВЛЕНО: возвращает ТОЛЬКО переведенный текст без мусора
    """
    translator = get_translator()
    result = translator.translate_from_image(image_path)
    
    if result:
        # Очищаем результат от возможного мусора
        clean_text = re.sub(r'\s+', ' ', result.translated_text)
        clean_text = re.sub(r'[^\w\s.,!?;:а-яА-ЯёЁңғәөүһқўѕјѓќџ-]', '', clean_text)
        return clean_text.strip()
    return ""


# ========== ТЕСТИРОВАНИЕ ==========

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 TILORA - ТОЛЬКО ВНЕШНИЙ СЛОВАРЬ")
    print("=" * 60)
    
    try:
        translator = get_translator()
        
        # Тестовые переводы
        test_texts = [
            "привет",
            "доброе утро",
            "как дела",
            "я иду домой",
            "до свидания"
        ]
        
        for text in test_texts:
            result = translator.translate(text, return_details=True)
            lang_name = "Русский" if result.source_language == 'ru' else "Карачаевский"
            confidence = int(result.confidence * 100)
            
            print(f"\n📝 {lang_name}: {text}")
            print(f"   ➡️  {result.translated_text} ({confidence}%)")
            print(f"   📌 Тип: {result.translation_type}")
        
        print("\n" + "=" * 60)
        stats = translator.get_dictionary_stats()
        print(f"📚 Статистика словаря:")
        print(f"   • Всего записей: {stats['total_words']}")
        print(f"   • Фраз: {stats['total_phrases']}")
        print(f"   • Русско-карачаевских: {stats['ru_entries']}")
        print(f"   • Карачаевско-русских: {stats['qar_entries']}")
        print(f"🔍 OCR: {'Доступен' if OCR_AVAILABLE else 'Не доступен'}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ {e}")
        print("\n📌 Решение:")
        print("   1. Создайте папку 'data' в текущей директории")
        print("   2. Поместите файл words.json в папку 'data'")
        print("   3. Или поместите words.json в текущую директорию")
        print("=" * 60)