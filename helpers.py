import random
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from pages.base_page import BasePage


def generate_post_code():
    return ''.join(random.choices('0123456789', k=10))


def post_code_to_first_name(s, pad=False):
    if pad and len(s) % 2:
        s += '0'
    return ''.join(chr(ord('a') + int(s[i:i + 2]) % 26) for i in range(0, len(s) - 1, 2))


def closest_name_to_mean(names):
    if not names:
        raise ValueError("Список имён пуст")

    lengths = [len(n) for n in names]
    mean = sum(lengths) / len(lengths)
    return min(names, key=lambda n: abs(len(n) - mean))


class PagesHelpers(BasePage):

    def get_all_first_names(self):
        soup = BeautifulSoup(self.page_source, "html.parser")

        table = soup.find("table", {"class": "table table-bordered table-striped"})

        header = table.find("tr")
        headers = [th.get_text(strip=True) for th in header.find_all(["th", "td"])]
        first_name_col_index = headers.index("First Name")

        values = []
        for row in table.find_all("tr")[1:]:
            cells = row.find_all(["td", "th"])
            if len(cells) > first_name_col_index:
                values.append(cells[first_name_col_index].get_text(strip=True))
        return values

    def find_row_by_column_value(self, search_column_index, search_value):
        rows = self.find_elements(By.CSS_SELECTOR, "table tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > search_column_index:
                if cells[search_column_index].text == search_value:
                    row_data = {}
                    for i, cell in enumerate(cells):
                        row_data[i] = cell.text
                    return row_data
        return None
