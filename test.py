from tilora import TiloClient, translate, translate_image

# Вариант 1: Класс-клиент (рекомендуется)
client = TiloClient()
result = client.translate("привет как дела")
print(result.translated_text)  # салам къалайса

# Вариант 2: Быстрые функции
print(translate("спасибо"))  # сау бол

# Перевод с фото
result = client.translate_image("photo.jpg")
print(result.translated_text)

# Пакетный перевод
results = client.translate_batch(["привет", "пока"])
for r in results:
    print(f"{r.original_text} → {r.translated_text}")