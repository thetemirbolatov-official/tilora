"""
tilora.py - Официальная библиотека API tilora.ru
ТОЛЬКО API, без локальных словарей!
Версия 1.0.0

Автор: thetemirbolatov
Лицензия: MIT

Поддерживаемые методы:
- Перевод текста (русский ↔ карачаевский)
- Пакетный перевод
- Определение языка
- OCR и перевод с изображений
- Статистика и статус API

Документация: https://tilora.ru/api.html
"""

import json
import base64
from io import BytesIO
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from pathlib import Path

import requests
from PIL import Image

__version__ = "1.0.0"
__author__ = "thetemirbolatov"


class TiloApiError(Exception):
    """Базовое исключение для ошибок API"""
    pass


class TiloConnectionError(TiloApiError):
    """Ошибка подключения к API"""
    pass


class TiloRateLimitError(TiloApiError):
    """Превышение лимита запросов"""
    pass


class TiloClient:
    """
    Клиент для работы с API tilora.ru
    
    Пример использования:
        >>> client = TiloClient()
        >>> result = client.translate("привет как дела")
        >>> print(result.translated_text)
        салам къалайса
    
    Args:
        api_key: API ключ (по умолчанию публичный ключ)
        timeout: Таймаут запросов в секундах
        max_retries: Количество повторных попыток при ошибках
    """
    
    BASE_URL = "https://tilora.ru"
    PUBLIC_API_KEY = "KARACHAY-OPEN-KEY"
    
    def __init__(
        self,
        api_key: str = PUBLIC_API_KEY,
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
            "User-Agent": f"tilora-python-client/{__version__}"
        })
        
        # Статистика клиента
        self._stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "cached_responses": 0,
            "total_chars_translated": 0,
            "total_images_processed": 0
        }
        
        # Простой кэш
        self._cache = {}
        self._enable_cache = True
        
        # Проверка подключения при инициализации
        self._check_connection()
    
    def _check_connection(self) -> bool:
        """Проверка доступности API"""
        try:
            health = self.get_health()
            if health.get("status") == "operational":
                return True
            raise TiloConnectionError("API недоступен")
        except requests.exceptions.RequestException as e:
            raise TiloConnectionError(f"Ошибка подключения: {e}")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        cache_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Внутренний метод для выполнения запросов к API
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        # Проверка кэша для GET запросов
        if method == "GET" and cache_key and self._enable_cache:
            if cache_key in self._cache:
                self._stats["cached_responses"] += 1
                return self._cache[cache_key]
        
        self._stats["total_requests"] += 1
        
        for attempt in range(self.max_retries):
            try:
                if method == "GET":
                    response = self.session.get(
                        url,
                        timeout=self.timeout
                    )
                else:  # POST
                    response = self.session.post(
                        url,
                        json=data,
                        timeout=self.timeout
                    )
                
                # Проверка статуса ответа
                if response.status_code == 429:
                    raise TiloRateLimitError(
                        "Превышен лимит запросов (100/час)"
                    )
                
                response.raise_for_status()
                result = response.json()
                
                # Сохраняем в кэш для GET запросов
                if method == "GET" and cache_key and self._enable_cache:
                    self._cache[cache_key] = result
                
                self._stats["successful_requests"] += 1
                return result
                
            except requests.exceptions.Timeout:
                if attempt == self.max_retries - 1:
                    self._stats["failed_requests"] += 1
                    raise TiloConnectionError(
                        f"Таймаут запроса после {self.max_retries} попыток"
                    )
            except requests.exceptions.ConnectionError:
                if attempt == self.max_retries - 1:
                    self._stats["failed_requests"] += 1
                    raise TiloConnectionError(
                        "Ошибка подключения к серверу"
                    )
            except requests.exceptions.HTTPError as e:
                if response.status_code == 401:
                    raise TiloApiError("Неверный API ключ")
                elif response.status_code == 413:
                    raise TiloApiError("Превышен максимальный размер данных")
                elif response.status_code == 400:
                    error_data = response.json()
                    raise TiloApiError(
                        error_data.get("error", "Некорректный запрос")
                    )
                else:
                    raise TiloApiError(f"HTTP ошибка: {e}")
        
        return {"success": False, "error": "Максимальное количество попыток исчерпано"}
    
    def _encode_image(self, image_input: Union[str, bytes, Path, Image.Image]) -> str:
        """
        Кодирование изображения в base64
        """
        try:
            if isinstance(image_input, (str, Path)):
                with open(str(image_input), "rb") as f:
                    image_bytes = f.read()
            elif isinstance(image_input, bytes):
                image_bytes = image_input
            elif isinstance(image_input, Image.Image):
                buffered = BytesIO()
                # Конвертируем в RGB если нужно
                if image_input.mode in ('RGBA', 'LA', 'P'):
                    rgb_image = Image.new('RGB', image_input.size, (255, 255, 255))
                    if image_input.mode == 'RGBA':
                        rgb_image.paste(image_input, mask=image_input.split()[3])
                    else:
                        rgb_image.paste(image_input)
                    image_input = rgb_image
                image_input.save(buffered, format="PNG")
                image_bytes = buffered.getvalue()
            else:
                raise ValueError(f"Неподдерживаемый тип: {type(image_input)}")
            
            # Проверка размера (макс 16MB)
            if len(image_bytes) > 16 * 1024 * 1024:
                raise TiloApiError("Размер изображения превышает 16MB")
            
            return base64.b64encode(image_bytes).decode("utf-8")
            
        except Exception as e:
            raise TiloApiError(f"Ошибка обработки изображения: {e}")
    
    def _parse_confidence(self, confidence_value: Any) -> float:
        """
        Преобразование confidence в число
        """
        if confidence_value is None:
            return 0.9
        if isinstance(confidence_value, (int, float)):
            return float(confidence_value)
        if isinstance(confidence_value, str):
            confidence_value = confidence_value.lower()
            if confidence_value == "high":
                return 0.95
            elif confidence_value == "medium":
                return 0.80
            elif confidence_value == "low":
                return 0.60
            else:
                try:
                    return float(confidence_value)
                except (ValueError, TypeError):
                    return 0.90
        return 0.90
    
    def translate(
        self,
        text: str,
        source_lang: Optional[str] = None,
        target_lang: Optional[str] = None
    ) -> "TranslationResult":
        """
        Перевод текста через API tilora.ru
        
        Args:
            text: Текст для перевода
            source_lang: Язык оригинала (ru/qar), если не указан - определяется автоматически
            target_lang: Целевой язык (ru/qar), если не указан - определяется автоматически
        
        Returns:
            TranslationResult: Результат перевода
        """
        if not text or not isinstance(text, str):
            return TranslationResult(
                original_text=str(text) if text else "",
                translated_text="",
                source_language="ru",
                target_language="qar",
                success=False,
                error="Пустой текст"
            )
        
        text = text.strip()
        if not text:
            return TranslationResult(
                original_text="",
                translated_text="",
                source_language="ru",
                target_language="qar",
                success=False,
                error="Пустой текст"
            )
        
        # Подготовка параметров
        payload = {"text": text}
        if source_lang:
            payload["source_lang"] = source_lang
        if target_lang:
            payload["target_lang"] = target_lang
        
        # Выполнение запроса
        result = self._make_request("POST", "/api/v2/translate", payload)
        
        # Обновляем статистику
        if result.get("success"):
            self._stats["total_chars_translated"] += len(text)
        
        return TranslationResult.from_api_response(result, text, self._parse_confidence)
    
    def translate_batch(
        self,
        texts: List[str],
        source_lang: Optional[str] = None,
        target_lang: Optional[str] = None
    ) -> List["TranslationResult"]:
        """
        Пакетный перевод нескольких текстов
        
        Args:
            texts: Список текстов для перевода (макс. 50)
            source_lang: Язык оригинала
            target_lang: Целевой язык
        
        Returns:
            List[TranslationResult]: Список результатов перевода
        """
        if not texts:
            return []
        
        if len(texts) > 50:
            raise TiloApiError("Максимум 50 текстов за один запрос")
        
        # Подготовка параметров
        payload = {"texts": texts}
        if source_lang:
            payload["source_lang"] = source_lang
        if target_lang:
            payload["target_lang"] = target_lang
        
        # Выполнение запроса
        result = self._make_request("POST", "/api/v2/translate/batch", payload)
        
        results = []
        if result.get("success"):
            for i, item in enumerate(result.get("results", [])):
                results.append(
                    TranslationResult.from_api_response(item, texts[i], self._parse_confidence)
                )
                
                if item.get("success"):
                    self._stats["total_chars_translated"] += len(texts[i])
        else:
            # Если пакетный перевод не удался, переводим по одному
            for text in texts:
                results.append(self.translate(text, source_lang, target_lang))
        
        return results
    
    def detect_language(self, text: str) -> "DetectionResult":
        """
        Определение языка текста
        
        Args:
            text: Текст для анализа
        
        Returns:
            DetectionResult: Результат определения языка
        """
        if not text or not isinstance(text, str):
            return DetectionResult(
                text=str(text) if text else "",
                language_code="ru",
                language_name="Русский",
                confidence=0.5,
                success=False,
                error="Пустой текст"
            )
        
        text = text.strip()
        if not text:
            return DetectionResult(
                text="",
                language_code="ru",
                language_name="Русский",
                confidence=0.5,
                success=False,
                error="Пустой текст"
            )
        
        result = self._make_request(
            "POST",
            "/api/v2/detect",
            {"text": text},
            cache_key=f"detect:{text}"
        )
        
        return DetectionResult.from_api_response(result, text, self._parse_confidence)
    
    def translate_image(
        self,
        image_input: Union[str, bytes, Path, Image.Image],
        source_lang: Optional[str] = None,
        target_lang: Optional[str] = None
    ) -> "ImageTranslationResult":
        """
        Перевод текста с изображения
        
        Args:
            image_input: Изображение (путь к файлу, bytes, PIL Image)
            source_lang: Язык оригинала
            target_lang: Целевой язык
        
        Returns:
            ImageTranslationResult: Результат OCR и перевода
        """
        # Кодирование изображения
        image_data = self._encode_image(image_input)
        
        # Подготовка параметров
        payload = {"image_data": image_data}
        if source_lang:
            payload["source_lang"] = source_lang
        if target_lang:
            payload["target_lang"] = target_lang
        
        # Выполнение запроса
        result = self._make_request("POST", "/api/v2/translate/image", payload)
        
        # Обновляем статистику
        self._stats["total_images_processed"] += 1
        if result.get("success"):
            self._stats["total_chars_translated"] += len(
                result.get("extracted_text", "")
            )
        
        return ImageTranslationResult.from_api_response(result, self._parse_confidence)
    
    def ocr(
        self,
        image_input: Union[str, bytes, Path, Image.Image]
    ) -> "OCRResult":
        """
        Извлечение текста с изображения без перевода
        
        Args:
            image_input: Изображение (путь к файлу, bytes, PIL Image)
        
        Returns:
            OCRResult: Результат распознавания текста
        """
        # Кодирование изображения
        image_data = self._encode_image(image_input)
        
        # Выполнение запроса
        result = self._make_request(
            "POST",
            "/api/v2/ocr",
            {"image_data": image_data}
        )
        
        self._stats["total_images_processed"] += 1
        
        return OCRResult.from_api_response(result, self._parse_confidence)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Получение статистики API
        
        Returns:
            Dict: Статистика словаря и использования API
        """
        result = self._make_request(
            "GET",
            "/api/v2/stats",
            cache_key="stats"
        )
        return result.get("stats", {}) if result.get("success") else {}
    
    def get_health(self) -> Dict[str, Any]:
        """
        Проверка состояния API
        
        Returns:
            Dict: Информация о состоянии сервиса
        """
        return self._make_request(
            "GET",
            "/api/v2/health",
            cache_key="health"
        )
    
    def get_supported_languages(self) -> List[Dict[str, Any]]:
        """
        Получение списка поддерживаемых языков
        
        Returns:
            List[Dict]: Информация о языках
        """
        result = self._make_request(
            "GET",
            "/api/v2/languages",
            cache_key="languages"
        )
        return result.get("languages", []) if result.get("success") else []
    
    def clear_cache(self):
        """Очистка кэша клиента"""
        self._cache.clear()
        self._stats["cached_responses"] = 0
    
    def get_client_stats(self) -> Dict[str, Any]:
        """
        Получение статистики использования клиента
        
        Returns:
            Dict: Статистика клиента
        """
        return {
            **self._stats,
            "cache_size": len(self._cache),
            "version": __version__
        }
    
    @property
    def is_available(self) -> bool:
        """Проверка доступности API"""
        try:
            health = self.get_health()
            return health.get("status") == "operational"
        except:
            return False


# ============= ВСПОМОГАТЕЛЬНЫЕ КЛАССЫ =============

class TranslationResult:
    """Результат перевода текста"""
    
    def __init__(
        self,
        original_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
        success: bool = True,
        confidence: float = 1.0,
        error: Optional[str] = None,
        characters: int = 0,
        alternatives: List[str] = None,
        raw_response: Optional[Dict] = None
    ):
        self.original_text = original_text
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language
        self.success = success
        self.confidence = confidence
        self.error = error
        self.characters = characters or len(original_text)
        self.alternatives = alternatives or []
        self.raw_response = raw_response
        self.timestamp = datetime.now()
    
    @classmethod
    def from_api_response(cls, response: Dict, original_text: str, parse_confidence_func=None):
        """Создание объекта из ответа API"""
        if response.get("success"):
            confidence = response.get("confidence", 1.0)
            if parse_confidence_func:
                confidence = parse_confidence_func(confidence)
            
            return cls(
                original_text=original_text,
                translated_text=response.get("translated_text", ""),
                source_language=response.get("from", "ru"),
                target_language=response.get("to", "qar"),
                success=True,
                confidence=confidence,
                characters=response.get("characters", len(original_text)),
                alternatives=response.get("alternatives", []),
                raw_response=response
            )
        else:
            return cls(
                original_text=original_text,
                translated_text=original_text,
                source_language="ru",
                target_language="qar",
                success=False,
                error=response.get("error", "Неизвестная ошибка"),
                raw_response=response
            )
    
    def __str__(self):
        return self.translated_text
    
    def __repr__(self):
        return f"TranslationResult({self.original_text[:20]} → {self.translated_text[:20]})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            "original": self.original_text,
            "translated": self.translated_text,
            "from": self.source_language,
            "to": self.target_language,
            "success": self.success,
            "confidence": self.confidence,
            "error": self.error,
            "characters": self.characters,
            "alternatives": self.alternatives,
            "timestamp": self.timestamp.isoformat()
        }


class DetectionResult:
    """Результат определения языка"""
    
    def __init__(
        self,
        text: str,
        language_code: str,
        language_name: str,
        confidence: float,
        success: bool = True,
        error: Optional[str] = None,
        characters: int = 0,
        raw_response: Optional[Dict] = None
    ):
        self.text = text
        self.language_code = language_code
        self.language_name = language_name
        self.confidence = confidence
        self.success = success
        self.error = error
        self.characters = characters or len(text)
        self.raw_response = raw_response
        self.timestamp = datetime.now()
    
    @classmethod
    def from_api_response(cls, response: Dict, original_text: str, parse_confidence_func=None):
        """Создание объекта из ответа API"""
        if response.get("success"):
            confidence = response.get("confidence", 0.9)
            if parse_confidence_func:
                confidence = parse_confidence_func(confidence)
            
            return cls(
                text=original_text,
                language_code=response.get("language_code", "ru"),
                language_name=response.get("language_name", "Русский"),
                confidence=confidence,
                success=True,
                characters=response.get("characters", len(original_text)),
                raw_response=response
            )
        else:
            return cls(
                text=original_text,
                language_code="ru",
                language_name="Русский",
                confidence=0.5,
                success=False,
                error=response.get("error", "Неизвестная ошибка"),
                raw_response=response
            )
    
    def __str__(self):
        return f"{self.language_name} ({int(self.confidence * 100)}%)"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "language_code": self.language_code,
            "language_name": self.language_name,
            "confidence": self.confidence,
            "success": self.success,
            "error": self.error,
            "characters": self.characters,
            "timestamp": self.timestamp.isoformat()
        }


class OCRResult:
    """Результат распознавания текста"""
    
    def __init__(
        self,
        extracted_text: str,
        language_code: str,
        language_name: str,
        success: bool = True,
        confidence: float = 0.8,
        error: Optional[str] = None,
        characters: int = 0,
        lines: int = 0,
        raw_response: Optional[Dict] = None
    ):
        self.extracted_text = extracted_text
        self.language_code = language_code
        self.language_name = language_name
        self.success = success
        self.confidence = confidence
        self.error = error
        self.characters = characters or len(extracted_text)
        self.lines = lines or extracted_text.count('\n') + 1
        self.raw_response = raw_response
        self.timestamp = datetime.now()
    
    @classmethod
    def from_api_response(cls, response: Dict, parse_confidence_func=None):
        """Создание объекта из ответа API"""
        if response.get("success"):
            extracted = response.get("extracted_text", "")
            confidence = response.get("confidence", 0.8)
            if parse_confidence_func:
                confidence = parse_confidence_func(confidence)
            
            return cls(
                extracted_text=extracted,
                language_code=response.get("language_code", "ru"),
                language_name=response.get("language_name", "Русский"),
                success=True,
                confidence=confidence,
                characters=response.get("characters", len(extracted)),
                lines=response.get("lines", extracted.count('\n') + 1),
                raw_response=response
            )
        else:
            return cls(
                extracted_text="",
                language_code="ru",
                language_name="Русский",
                success=False,
                error=response.get("error", "Неизвестная ошибка"),
                raw_response=response
            )
    
    def __str__(self):
        return self.extracted_text[:100] + ("..." if len(self.extracted_text) > 100 else "")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "extracted_text": self.extracted_text,
            "language_code": self.language_code,
            "language_name": self.language_name,
            "success": self.success,
            "confidence": self.confidence,
            "error": self.error,
            "characters": self.characters,
            "lines": self.lines,
            "timestamp": self.timestamp.isoformat()
        }


class ImageTranslationResult(OCRResult):
    """Результат OCR + перевод"""
    
    def __init__(
        self,
        extracted_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
        success: bool = True,
        ocr_confidence: float = 0.8,
        translation_confidence: float = 1.0,
        error: Optional[str] = None,
        characters: int = 0,
        raw_response: Optional[Dict] = None
    ):
        super().__init__(
            extracted_text=extracted_text,
            language_code=source_language,
            language_name="Карачаевский" if source_language == "qar" else "Русский",
            success=success,
            confidence=ocr_confidence,
            error=error,
            characters=characters or len(extracted_text),
            raw_response=raw_response
        )
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language
        self.translation_confidence = translation_confidence
    
    @classmethod
    def from_api_response(cls, response: Dict, parse_confidence_func=None):
        """Создание объекта из ответа API"""
        if response.get("success"):
            extracted = response.get("extracted_text", "")
            translated = response.get("translated_text", "")
            
            ocr_conf = response.get("ocr_confidence", 0.8)
            trans_conf = response.get("confidence", 1.0)
            
            if parse_confidence_func:
                ocr_conf = parse_confidence_func(ocr_conf)
                trans_conf = parse_confidence_func(trans_conf)
            
            return cls(
                extracted_text=extracted,
                translated_text=translated,
                source_language=response.get("from", "ru"),
                target_language=response.get("to", "qar"),
                success=True,
                ocr_confidence=ocr_conf,
                translation_confidence=trans_conf,
                characters=response.get("characters", len(extracted)),
                raw_response=response
            )
        else:
            return cls(
                extracted_text="",
                translated_text="",
                source_language="ru",
                target_language="qar",
                success=False,
                error=response.get("error", "Неизвестная ошибка"),
                raw_response=response
            )
    
    def __str__(self):
        return self.translated_text
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "translation_confidence": self.translation_confidence
        })
        return data


# ============= ФУНКЦИИ БЫСТРОГО ДОСТУПА =============

_global_client = None


def get_client() -> TiloClient:
    """Получение глобального экземпляра клиента"""
    global _global_client
    if _global_client is None:
        _global_client = TiloClient()
    return _global_client


def translate(text: str, **kwargs) -> str:
    """
    Быстрый перевод текста
    
    Пример:
        >>> from tilora import translate
        >>> translate("привет")
        'салам'
    """
    client = get_client()
    result = client.translate(text, **kwargs)
    return result.translated_text if result.success else text


def translate_batch(texts: List[str], **kwargs) -> List[str]:
    """
    Быстрый пакетный перевод
    
    Пример:
        >>> from tilora import translate_batch
        >>> translate_batch(["привет", "спасибо"])
        ['салам', 'сау бол']
    """
    client = get_client()
    results = client.translate_batch(texts, **kwargs)
    return [r.translated_text if r.success else t for r, t in zip(results, texts)]


def detect(text: str) -> str:
    """
    Быстрое определение языка
    
    Пример:
        >>> from tilora import detect
        >>> detect("салам")
        'qar'
    """
    client = get_client()
    result = client.detect_language(text)
    return result.language_code


def translate_image(image_path: str, **kwargs) -> str:
    """
    Быстрый перевод текста с изображения
    
    Пример:
        >>> from tilora import translate_image
        >>> translate_image("photo.jpg")
        'салам къалайса'
    """
    client = get_client()
    result = client.translate_image(image_path, **kwargs)
    return result.translated_text if result.success else ""


def ocr_image(image_path: str) -> str:
    """
    Быстрое распознавание текста с изображения
    
    Пример:
        >>> from tilora import ocr_image
        >>> ocr_image("text.jpg")
        'привет как дела'
    """
    client = get_client()
    result = client.ocr(image_path)
    return result.extracted_text if result.success else ""


def api_status() -> Dict[str, Any]:
    """Проверка статуса API"""
    client = get_client()
    return {
        "available": client.is_available,
        "health": client.get_health(),
        "stats": client.get_stats(),
        "client_stats": client.get_client_stats()
    }


# ============= ТЕСТИРОВАНИЕ =============

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(f"🧪 TILORA API CLIENT v{__version__}")
    print(f"👤 Автор: {__author__}")
    print("=" * 60)
    
    try:
        # Создание клиента
        client = TiloClient()
        
        # Проверка статуса
        print(f"\n🔌 Статус API: {'✅ Доступен' if client.is_available else '❌ Недоступен'}")
        
        # Получение статистики
        stats = client.get_stats()
        if stats:
            print(f"📚 Словарь API: {stats.get('dictionary', {}).get('words', 0)} слов")
            print(f"📖 Фраз: {stats.get('dictionary', {}).get('phrases', 0)}")
        
        # Тестовые переводы
        test_texts = [
            "привет",
            "доброе утро",
            "как дела",
            "спасибо",
            "до свидания"
        ]
        
        print("\n📝 ТЕСТОВЫЕ ПЕРЕВОДЫ:")
        print("-" * 60)
        
        for text in test_texts:
            result = client.translate(text)
            if result.success:
                print(f"📥 {text:15} → 📤 {result.translated_text:20} [{result.source_language}→{result.target_language}]")
            else:
                print(f"❌ {text}: {result.error}")
        
        # Тест определения языка
        print("\n🔍 ТЕСТ ОПРЕДЕЛЕНИЯ ЯЗЫКА:")
        print("-" * 60)
        
        test_detect = [
            "привет мир",
            "салам дюнья",
            "къалайса",
            "спасибо большое"
        ]
        
        for text in test_detect:
            result = client.detect_language(text)
            if result.success:
                confidence_percent = int(result.confidence * 100)
                print(f"📝 {text:15} → 🌐 {result.language_name:12} ({confidence_percent}%)")
            else:
                print(f"❌ {text}: {result.error}")
        
        # Статистика клиента
        print("\n📊 СТАТИСТИКА КЛИЕНТА:")
        print("-" * 60)
        client_stats = client.get_client_stats()
        print(f"   • Запросов: {client_stats['total_requests']}")
        print(f"   • Успешно: {client_stats['successful_requests']}")
        print(f"   • Кэш попаданий: {client_stats['cached_responses']}")
        print(f"   • Символов переведено: {client_stats['total_chars_translated']}")
        print(f"   • Изображений обработано: {client_stats['total_images_processed']}")
        
        print("\n" + "=" * 60)
        print("✅ Библиотека успешно протестирована!")
        print("=" * 60 + "\n")
        
    except TiloConnectionError as e:
        print(f"\n❌ Ошибка подключения: {e}")
        print("\n📌 Проверьте:")
        print("   1. Подключение к интернету")
        print("   2. Доступность сайта https://tilora.ru")
        print("   3. Работу API сервера")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()


# Экспортируемые классы и функции
__all__ = [
    "TiloClient",
    "TiloApiError",
    "TiloConnectionError",
    "TiloRateLimitError",
    "TranslationResult",
    "DetectionResult",
    "OCRResult",
    "ImageTranslationResult",
    "translate",
    "translate_batch",
    "detect",
    "translate_image",
    "ocr_image",
    "api_status",
    "get_client"
]