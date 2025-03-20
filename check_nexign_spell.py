from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import language_tool_python

tool = language_tool_python.LanguageTool('ru-RU')

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-images")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

whitelist_words = {
    "нэксайн", "nexign"
}

ignore_rules = [
    "UPPERCASE_SENTENCE_START",
    "WORD_REPEAT_RULE",
    "MORFOLOGIK_RULE_RU_RU",
    "PUNCTUATION",
    "DASH_RULE",
    "RU_UNPAIRED_BRACKETS",
    "RU_COMPOUNDS",
    "AGREEMENT_CASE",
    "TAUTOLOGY"
]


def get_links(base_url="https://nexign.com/ru"):
    driver.get(base_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(("tag name", "body"))
    )
    links = []
    elements = driver.find_elements("tag name", "a")
    for element in elements:
        href = element.get_attribute("href")
        if href and href.startswith(base_url) and href not in links:
            links.append(href)
    return links


def check_spelling(text):
    matches = tool.check(text)
    errors = []

    for match in matches:
        error_word = text[match.offset:match.offset + match.errorLength]

        if (
                match.ruleId in ignore_rules or
                error_word.lower() in whitelist_words
        ):
            continue

        errors.append({
            "Слово с ошибкой": error_word,
            "Тип ошибки": match.message,
            "Контекст": text[max(0, match.offset - 20):min(len(text), match.offset + match.errorLength + 20)]
        })

    return errors


def extract_text_from_elements(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(("tag name", "body"))
    )
    all_errors = []
    text_elements = driver.find_elements(
        "xpath",
        "//h1 | //h2 | //h3 | //h4 | //h5 | //p | //span[not(ancestor::nav)] | //li | //div[not(child::*) and string-length(normalize-space(text())) > 5]"
    )

    for element in text_elements:

        element_text = element.text.strip()
        if element_text and len(element_text) > 1:
            element_errors = check_spelling(element_text)

            if element_errors:
                tag_name = element.tag_name
                print(f"Найдены ошибки в элементе <{tag_name}>")

                for error in element_errors:
                    all_errors.append(error)
                    print(f"{error['Слово с ошибкой']}: {error['Тип ошибки']}\nКонтекст: {error['Контекст']}")

    return all_errors


def main():
    links = get_links()
    print(f"Найдено {len(links)} ссылок для проверки")

    all_results = []
    for i, url in enumerate(links, 1):
        print(f"Обработка страницы {i}/{len(links)}: {url}")

        errors = extract_text_from_elements(url)

        result = {
            "url": url,
            "errors": errors
        }

        all_results.append(result)
        print(f"На странице {url} найдено {len(errors)} ошибок")


    print("\n--- РЕЗУЛЬТАТЫ ПРОВЕРКИ ---")
    for result in all_results:
        if result["errors"]:
            print(f"\nСтраница: {result['url']}")
            print(f"Найдено ошибок: {len(result['errors'])}")

            for i, error in enumerate(result["errors"][:5], 1):
                print(f"  {i}. Ошибка: '{error['Слово с ошибкой']}' - {error['Тип ошибки']}")
                print(f"     Контекст: ...{error['Контекст']}...")

            if len(result["errors"]) > 5:
                print(f"     ...и еще {len(result['errors']) - 5} ошибок")

if __name__ == "__main__":
    main()
