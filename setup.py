"""
setup.py - Tilora Карачаевский переводчик
Версия: 1.0.1
Автор: Temirbolatov (@thetemirbolatov)
Лицензия: MIT
"""

from setuptools import setup
import os

# Читаем README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    # ========== ОСНОВНАЯ ИНФОРМАЦИЯ ==========
    name="tilora",
    version="1.0.1",
    author="thetemirbolatov",
    author_email="mirajestory@gmail.com",
    description="🗣️ Двусторонний переводчик карачаевского и русского языков с поддержкой OCR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thetemirbolatov-official/tilora",
    license="MIT",
    
    # ========== ВАЖНО! ВАШ КАК ОДИН ФАЙЛ ==========
    py_modules=["tilora"],  # Вместо packages=find_packages()
    
    # ========== ВКЛЮЧАЕМ JSON ФАЙЛЫ ==========
    include_package_data=True,
    package_data={
        "": ["data/*.json", "data/**/*.json"],
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
        "full": [
            "pytesseract>=0.3.10",
            "Pillow>=9.0.0",
        ],
    },
    
    # ========== ВАШИ СОЦСЕТИ ==========
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
        "Natural Language :: Karachay",
        "Typing :: Typed",
    ],
    
    # ========== КЛЮЧЕВЫЕ СЛОВА ==========
    keywords=[
        "karachay", "karachay-balkar", "russian", "translator",
        "translation", "dictionary", "ocr", "tesseract",
        "natural-language-processing", "nlp", "caucasian-languages",
        "turkkic-languages", "karachay-language", "tilora",
        "карачаевский", "переводчик", "къарачай", "til", "ora",
    ],
    
    zip_safe=False,
)
