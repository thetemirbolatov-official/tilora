from tilora import KarachayTranslator, translate, detect_language, translate_image

# Простой перевод
print(translate("привет"))  # салам

# Перевод с фото
text = translate_image("photo.jpg")
print(f"Перевод с фото: {text}")

# Расширенный перевод
tr = KarachayTranslator()
result = tr.translate("доброе утро", return_details=True)
print(f"{result.translated_text} ({result.confidence:.0%})")