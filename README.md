# Инструкция по использованию скрипта `check_nexign_spell.py`

## Назначение

Скрипт `check_nexign_spell.py` предназначен для автоматической проверки орфографии на веб-страницах сайта Nexign. Он анализирует текстовое содержимое всех страниц, доступных с главной страницы, и выявляет возможные орфографические и грамматические ошибки.

## Функциональность

Скрипт выполняет следующие действия:
1. Запускает браузер Chrome в headless-режиме через Selenium WebDriver
2. Собирает все доступные ссылки с главной страницы Nexign (https://nexign.com/ru)
3. Последовательно открывает каждую страницу и извлекает текст из текстовых элементов (заголовки, параграфы и т.д.)
4. Анализирует орфографию и грамматику с помощью LanguageTool
5. Игнорирует определенные типы ошибок и слова из белого списка (например, "нэксайн", "nexign")
6. Формирует подробный отчет о найденных ошибках с контекстом

## Требования

- Python 3.x
- Установленный Google Chrome
- Библиотеки:
  - selenium
  - webdriver-manager
  - language_tool_python

## Установка зависимостей

```bash
pip install selenium webdriver-manager language_tool_python
```

## Запуск скрипта

Windows
```bash
python check_nexign_spell.py
```
Linux
```bash
python3 check_nexign_spell.py
```

## Особенности работы

- Скрипт использует headless-режим Chrome для повышения скорости работы
- Для каждой ошибки выводится контекст в виде фрагмента текста
- На��троен белый список слов для исключения ложных срабатываний
- Содержит список игнорируемых правил проверки (UPPERCASE_SENTENCE_START, WORD_REPEAT_RULE и т.д.)
- Извлекает текст только из элементов, кот��рые обычно содержат контент (h1-h5, p, span, li, div)

## Возможные проблемы

- Первый запуск может занять продолжительное время из-за загрузки языковых моделей LanguageTool
- Проверка большого количества страниц может занять значительное время
- Возможны ложные срабатывания для специализированных технических терминов
- Для корректной работы необходимо стабильное интернет-соединение
- Требуется установленный Chrome и соответствующий ChromeDriver (устанавливается автоматически через webdriver-manager)

## Настройка

Для управления проверкой орфографии доступны два основных параметра:
- `whitelist_words` - словарь слов, которые не будут отмечены как ошибки
- `ignore_rules` - список идентификаторов правил, которые будут игнорироваться при проверке