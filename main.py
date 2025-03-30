from config import ROOT_DIR
from src.reports import spending_by_category
from src.services import (
    read_excel_file,
    rec_search_request,
    search_mobile_number_excel,
    search_transactions_to_people,
)
from src.views import page_main


def main():
    data_excel = read_excel_file(ROOT_DIR + "/data/operations.xlsx")
    data_transaction = rec_search_request(data_excel, "Супермаркеты")
    mobile_number = search_mobile_number_excel(data_excel)
    search_people = search_transactions_to_people(data_excel)
    views_data = page_main("2021-12-20 11:11:11")
    reports_data = spending_by_category(
        data_excel, "Супермаркеты", "2021-12-20 11:11:11"
    )
    print(data_transaction)
    print(mobile_number)
    print(search_people)
    print(views_data)
    print(reports_data)


if __name__ == "__main__":
    main()
