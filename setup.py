"""
setup.py - Файл установки для библиотеки tilora
Версия 1.0.0

Автор: thetemirbolatov
Лицензия: MIT
"""

from setuptools import setup, find_packages
from pathlib import Path

# Читаем длинное описание из README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Зависимости проекта
install_requires = [
    "requests>=2.28.0",
    "Pillow>=9.0.0",
]

# Дополнительные зависимости для разработки
extras_require = {
    "dev": [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "black>=22.0.0",
        "flake8>=5.0.0",
        "mypy>=0.990",
        "build>=0.9.0",
        "twine>=4.0.0",
    ],
}

setup(
    # Основная информация
    name="tilora",
    version="1.0.0",
    author="thetemirbolatov",
    author_email="mirajestory@gmail.com",  
    
    # Описание
    description="Официальная библиотека API tilora.ru для перевода с/на карачаевский язык",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Ссылки
    url="https://github.com/thetemirbolatov-official/tilora",
    project_urls={
        "Документация": "https://tilora.ru/api.html",
        "Исходный код": "https://github.com/thetemirbolatov-official/tilora",
        "Баг-трекер": "https://github.com/thetemirbolatov-official/tilora/issues",
        "Автор (ВКонтакте)": "https://vk.com/thetemirbolatov",
        "Автор (Instagram)": "https://instagram.com/thetemirbolatov",
        "Автор (Telegram)": "https://t.me/thetemirbolatov",
        "Сайт проекта": "https://tilora.ru",
    },
    
    # Лицензия
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Russian",
        "Natural Language :: Karachay-Balkar",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    
    # Ключевые слова
    keywords="karachay, russian, translation, ocr, nlp, api, tilora, карачаевский, перевод, распознавание",
    
    # Пакеты
    packages=find_packages(include=["tilora", "tilora.*"]),
    py_modules=["tilora"],
    
    # Зависимости
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require=extras_require,
    
    # Включаем файлы
    include_package_data=True,
    package_data={
        "tilora": ["py.typed", "*.pyi"],
    },
    
    # Консольные скрипты (опционально)
    entry_points={
        "console_scripts": [
            "tilora=tilora.cli:main",  # Если добавите CLI интерфейс
        ],
    },
    
    # Метаданные
    zip_safe=False,
)