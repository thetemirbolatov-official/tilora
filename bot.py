import telebot
import requests
import json
import base64
import io
import time
from PIL import Image
import threading

# Конфигурация
BOT_TOKEN = "ваш апи токен"
API_URL = "https://tilora.ru/api/v2"
API_KEY = "KARACHAY-OPEN-KEY"

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Функция для отображения прогресс-бара
def show_progress(chat_id, message_id, duration=2):
    """Анимированный прогресс-бар"""
    progress_chars = ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']
    steps = 8
    
    for i in range(steps + 1):
        progress = int((i / steps) * 100)
        bar_length = 10
        filled = int(bar_length * i / steps)
        bar = '█' * filled + '▁' * (bar_length - filled)
        
        text = f"Обработка... [{bar}] {progress}%"
        try:
            bot.edit_message_text(text, chat_id, message_id)
        except:
            pass
        
        time.sleep(duration / steps)
    
    return message_id

# Функция для отправки запроса к API
def translate_text(text):
    """Перевод текста через API"""
    try:
        headers = {
            'X-API-KEY': API_KEY,
            'Content-Type': 'application/json'
        }
        data = {'text': text}
        
        response = requests.post(
            f"{API_URL}/translate", 
            headers=headers, 
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return result['translated_text']
            else:
                return f"Ошибка: {result.get('error', 'Неизвестная ошибка')}"
        else:
            return f"Ошибка сервера: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "Таймаут соединения. Попробуйте позже."
    except requests.exceptions.ConnectionError:
        return "Ошибка подключения к серверу."
    except Exception as e:
        return f"Ошибка: {str(e)}"

def translate_image(image_data):
    """Перевод текста с изображения через API"""
    try:
        headers = {
            'X-API-KEY': API_KEY,
            'Content-Type': 'application/json'
        }
        
        # Конвертируем изображение в base64
        buffered = io.BytesIO()
        image_data.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        data = {
            'image_data': f'data:image/png;base64,{img_str}'
        }
        
        response = requests.post(
            f"{API_URL}/translate/image", 
            headers=headers, 
            json=data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return result['translated_text']
            else:
                return f"Ошибка: {result.get('error', 'Неизвестная ошибка')}"
        else:
            return f"Ошибка сервера: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "Таймаут при обработке изображения."
    except Exception as e:
        return f"Ошибка обработки: {str(e)}"

# Команды бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Приветственное сообщение с фото"""
    try:
        # Пробуем отправить фото
        with open('hi.png', 'rb') as photo:
            bot.send_photo(
                message.chat.id, 
                photo, 
                caption="Переводчик карачаевского языка\n\n"
                       "Отправьте текст или фото для перевода.\n"
            )
    except:
        # Если фото нет, отправляем текст
        bot.send_message(
            message.chat.id,
            "Переводчик карачаевского языка\n\n"
            "Отправьте текст или фото для перевода.\n"
        )

@bot.message_handler(commands=['help'])
def send_help(message):
    """Справка по использованию"""
    help_text = (
        "Использование переводчика:\n\n"
        "📝 Текстовый перевод:\n"
        "Просто отправьте любой текст на русском или карачаевском языке.\n\n"
        "📸 Перевод с фото:\n"
        "Отправьте фото, содержащее текст для распознавания и перевода.\n\n"
        "⚙️ Команды:\n"
        "/start - Начало работы\n"
        "/help - Эта справка\n"
        "/stop - Остановить диалог\n\n"
        "Языки:\n"
        "• Русский → Карачаевский\n"
        "• Карачаевский → Русский\n"
        "Определение языка происходит автоматически."
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['stop'])
def stop_chat(message):
    """Остановить диалог"""
    bot.send_message(
        message.chat.id,
        "Диалог остановлен. Используйте /start для начала нового."
    )

# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Обработка текстовых сообщений"""
    user_text = message.text.strip()
    
    if not user_text or user_text.startswith('/'):
        return
    
    # Проверка на слишком длинный текст
    if len(user_text) > 2000:
        bot.reply_to(message, "Текст слишком длинный (максимум 2000 символов)")
        return
    
    # Отправляем сообщение о начале обработки
    status_msg = bot.reply_to(message, "Обработка...")
    
    # Запускаем прогресс-бар в отдельном потоке
    progress_thread = threading.Thread(
        target=show_progress, 
        args=(message.chat.id, status_msg.message_id, 1.5)
    )
    progress_thread.start()
    
    # Получаем перевод
    result = translate_text(user_text)
    
    # Ждем завершения прогресс-бара
    progress_thread.join()
    
    # Удаляем сообщение о статусе и отправляем результат
    try:
        bot.delete_message(message.chat.id, status_msg.message_id)
    except:
        pass
    
    # Отправляем результат
    bot.reply_to(message, result)

# Обработка фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """Обработка фотографий"""
    # Отправляем сообщение о начале обработки
    status_msg = bot.reply_to(message, "Обработка изображения...")
    
    # Запускаем прогресс-бар в отдельном потоке
    progress_thread = threading.Thread(
        target=show_progress, 
        args=(message.chat.id, status_msg.message_id, 3)
    )
    progress_thread.start()
    
    try:
        # Получаем файл фото
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Конвертируем в PIL Image
        image = Image.open(io.BytesIO(downloaded_file))
        
        # Получаем перевод с изображения
        result = translate_image(image)
        
        # Ждем завершения прогресс-бара
        progress_thread.join()
        
        # Удаляем сообщение о статусе
        try:
            bot.delete_message(message.chat.id, status_msg.message_id)
        except:
            pass
        
        # Отправляем результат
        bot.reply_to(message, result)
        
    except Exception as e:
        # Останавливаем прогресс-бар
        progress_thread.join(timeout=0.1)
        
        try:
            bot.delete_message(message.chat.id, status_msg.message_id)
        except:
            pass
        
        bot.reply_to(message, f"Ошибка: Не удалось обработать изображение")

# Обработка документов (если отправляют файл изображения)
@bot.message_handler(content_types=['document'])
def handle_document(message):
    """Обработка документов (изображений)"""
    mime_type = message.document.mime_type
    if mime_type and mime_type.startswith('image/'):
        # Обрабатываем как фото
        handle_photo(message)
    else:
        bot.reply_to(message, "Отправьте изображение или текст")

# Фильтр для отлова всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    """Обработка всех сообщений"""
    # Игнорируем команды
    if message.text and message.text.startswith('/'):
        return
    
    # Отвечаем стандартным сообщением
    bot.reply_to(
        message, 
        "Отправьте текст или фото для перевода.\n"
        "Используйте /help для справки."
    )


# Функция для проверки соединения с API сервером
def check_api_connection():
    """Проверяет доступность API сервера"""
    print("🔍 Проверка соединения с API сервером...")
    print(f"📡 API URL: {API_URL}")
    print(f"🔑 API Key: {API_KEY[:10]}...")  # Показываем только первые 10 символов ключа
    
    try:
        headers = {
            'X-API-KEY': API_KEY,
            'User-Agent': 'Telegram-Translator-Bot/1.0'
        }
        
        test_response = requests.get(f"{API_URL}/health", headers=headers, timeout=10)
        
        if test_response.status_code == 200:
            response_data = test_response.json()
            if response_data.get('success'):
                status = response_data.get('status', 'unknown')
                
                # Проверяем статусы сервисов
                services = response_data.get('services', {})
                service_statuses = []
                
                for service, status in services.items():
                    service_statuses.append(f"  • {service}: {status}")
                
                print("✅ Соединение с API установлено успешно!")
                print(f"📊 Общий статус: {status}")
                
                if service_statuses:
                    print("🔧 Статус сервисов:")
                    for status_line in service_statuses:
                        print(status_line)
                
                # Проверяем словари
                if 'dictionary' in response_data.get('stats', {}):
                    stats = response_data['stats']['dictionary']
                    print(f"📚 Загружено слов: {stats.get('words', 'N/A')}")
                    print(f"📝 Загружено фраз: {stats.get('phrases', 'N/A')}")
                    print(f"💬 Загружено предложений: {stats.get('sentences', 'N/A')}")
                
                return True
            else:
                print(f"❌ API вернул ошибку: {response_data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Ошибка HTTP: {test_response.status_code}")
            print(f"📄 Ответ сервера: {test_response.text[:200]}...")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Таймаут при подключении к API серверу")
        return False
    except requests.exceptions.ConnectionError:
        print("🔌 Ошибка подключения: сервер недоступен")
        return False
    except requests.exceptions.JSONDecodeError:
        print("📄 Ошибка разбора JSON ответа")
        return False
    except Exception as e:
        print(f"⚠️ Неизвестная ошибка: {str(e)}")
        return False

# В основном блоке запуска используйте эту функцию:
if __name__ == '__main__':
    print("🤖 Запуск Telegram бота переводчика...")
    print("=" * 50)
    
    # Проверяем соединение с API
    if not check_api_connection():
        print("\n⚠️ Предупреждение: API сервер недоступен")
        print("🔄 Бот будет продолжать работу, но переводы могут не работать")
        print("💡 Проверьте:")
        print("  1. Запущен ли Flask сервер (app.py)")
        print("  2. Правильный ли IP адрес в API_URL")
        print("  3. Совпадает ли API_KEY в боте и на сервере")
    else:
        print("\n✨ API сервер готов к работе!")
    
    print("=" * 50)
    
    # Запускаем бота
    print("\n🤖 Бот запущен и ожидает сообщений...")
    print("📱 Используйте /start для начала работы")
    print("❌ Используйте Ctrl+C для остановки\n")
    
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")