"""
setup.py - Установка библиотеки tilora
Версия 1.0.0
Автор: Temirbolatov (@thetemirbolatov)
"""

from setuptools import setup
import os

# Читаем README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Читаем версию из файла
__version__ = "1.0.0"

setup(
    # Информация о пакете
    name="tilora",
    version=__version__,
    author="thetemirbolatov",
    author_email="mirajestory@gmail.com",
    description="🗣️ Двусторонний переводчик карачаевского и русского языков",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thetemirbolatov-official/tilora",
    license="MIT",
    
    # Файлы
    py_modules=["tilora"],
    include_package_data=True,
    package_data={
        "": ["data/words.json"],
    },
    
    # Зависимости
    python_requires=">=3.7",
    install_requires=[
        "Pillow>=9.0.0",
    ],
    
    # Опциональные зависимости для OCR
    extras_require={
        "ocr": [
            "pytesseract>=0.3.10",
        ],
    },
    
    # Классификаторы PyPI
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Linguistic",
        "Natural Language :: Russian",
    ],
    
    # Ключевые слова
    keywords="karachay russian translator ocr dictionary caucasian",
    
    # Социальные сети автора
    project_urls={
        "GitHub": "https://github.com/thetemirbolatov-official/tilora",
        "Telegram": "https://t.me/thetemirbolatov",
        "Instagram": "https://instagram.com/thetemirbolatov",
        "VK": "https://vk.com/thetemirbolatov",
    },
)