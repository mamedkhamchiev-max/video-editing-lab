# Ferta Estate — контекст бренда

- Сайт: https://fertaestate.com
- Название бренда на материалах: «Ferta Estate»
- Бизнес: недвижимость в Стамбуле (Турция), в т.ч. объекты под гражданство Турции
- Язык контента: русский
- Палитра (взята с фото объектов, пока сайт недоступен из облачной сессии):
  тёмно-коричневый `#231B15`, кремовый `#F4EDE3`, золото `#C9A46A`
- Шрифты: Playfair Display (заголовки), Montserrat (текст)
- Шаблон карусели: `carousel/carousel.html`, рендер слайдов в `carousel/out/`

## PDF-каталог объектов
- Готовый файл: `catalog/Ferta-Estate-catalog.pdf` — отправлять пользователю по запросу.
- Сайт отдаёт данные через `https://fertaestate.com/api/projects` и `/api/projects/{id}`, страницы — `/obyekt/{id}`.
- Цвета сайта: navy `#0E1B2A`, accent `#35C5DD`, gold `#E7B15A`; шрифты Montserrat + Inter.
- Пересборка со свежими данными:
  1. Скачать `api/projects/{id}` в `<dir>/det/{id}.json` и `/obyekt/{id}` в `<dir>/html/{id}.html` для всех id из `api/projects`.
  2. `python3 catalog/parse.py <dir> catalog` — собирает `catalog/data.json` и фото.
  3. Сжать фото в `catalog/img_s/` (до ~1000px, JPEG), добавить поле `text` из `catalog/descriptions.json` (описания написаны вручную; для новых объектов дописать).
  4. `python3 catalog/build.py` → `catalog/catalog.html`; `node catalog/pdf.js $PWD/catalog/catalog.html $PWD/catalog/Ferta-Estate-catalog.pdf` → PDF.
- Правила в каталоге: гражданство от $400 000 (суммы квартир складываются), ВНЖ в Стамбуле от $200 000 — перепроверять актуальность.
