"""
setup.py - Tilora Карачаевский переводчик
Версия: 1.0.0
Автор: Temirbolatov (@thetemirbolatov)
Лицензия: MIT
"""

from setuptools import setup, find_packages
import os

# Читаем README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    # ========== ОСНОВНАЯ ИНФОРМАЦИЯ ==========
    name="tilora",
    version="1.0.0",
    author="thetemirbolatov",
    author_email="mirajestory@gmail.com",
    description="🗣️ Двусторонний переводчик карачаевского и русского языков с поддержкой OCR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thetemirbolatov-official/tilora",
    license="MIT",
    
    # ========== ВАЖНО! ПАКЕТЫ И ДАННЫЕ ==========
    # Находим все пакеты
    packages=find_packages(),
    
    # Включаем файлы из data/
    include_package_data=True,
    package_data={
        "tilora": ["data/*.json", "data/**/*.json"],  # Явно указываем JSON файлы
        "": ["data/*.json"],  # Запасной вариант
    },
    
    # ========== ЗАВИСИМОСТИ ==========
    python_requires=">=3.7",
    install_requires=[
        "Pillow>=9.0.0",
    ],
    extras_require={
        "ocr": [
            "pytesseract>=0.3.10",
        ],
    },
    
    # ========== ВСЕ СОЦИАЛЬНЫЕ СЕТИ ==========
    project_urls={
        "GitHub": "https://github.com/thetemirbolatov-official/tilora",
        "PyPI": "https://pypi.org/project/tilora/",
        "Telegram": "https://t.me/thetemirbolatov",
        "Instagram": "https://instagram.com/thetemirbolatov",
        "ВКонтакте": "https://vk.com/thetemirbolatov",
        "Документация": "https://github.com/thetemirbolatov-official/tilora#readme",
        "Сообщить об ошибке": "https://github.com/thetemirbolatov-official/tilora/issues",
        "Автор": "https://github.com/thetemirbolatov-official",
    },
    
    # ========== КЛАССИФИКАТОРЫ ==========
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Natural Language :: Russian",
        "Natural Language :: Karachay",
        "Typing :: Typed",
    ],
    
    # ========== КЛЮЧЕВЫЕ СЛОВА ==========
    keywords=[
        "karachay",
        "karachay-balkar",
        "russian",
        "translator",
        "translation",
        "dictionary",
        "ocr",
        "tesseract",
        "natural-language-processing",
        "nlp",
        "caucasian-languages",
        "turkkic-languages",
        "karachay-language",
        "tilora",
        "карачаевский",
        "переводчик",
        "къарачай",
        "til",
        "ora",
    ],
    
    # ========== ДОПОЛНИТЕЛЬНО ==========
    zip_safe=False,
    include_package_data=True,
)
