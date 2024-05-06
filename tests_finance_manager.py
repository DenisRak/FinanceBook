import pytest
import os
from main import FinanceManager

@pytest.fixture
def finance_manager():
    filename = 'test_records.json'
    manager = FinanceManager(filename)
    yield manager
    os.remove(filename)

def test_add_record(finance_manager):
    record = ('2024-05-03', 'Доход', 1000, 'Test income')
    finance_manager.add_record(*record)
    assert len(finance_manager.records) == 1

def test_edit_record(finance_manager):
    record = ('2024-05-03', 'Доход', 1000, 'Test income')
    finance_manager.add_record(*record)
    new_record = ('2024-05-04', 'Расход', 500, 'Test expense')
    finance_manager.edit_record(0, *new_record)
    assert finance_manager.records[0]['Изменен'] == '2024-05-04'

def test_calculate_balance(finance_manager):
    income_record = ('2024-05-03', 'Доход', 1000, 'Test income')
    expense_record = ('2024-05-04', 'Расход', 500, 'Test expense')
    finance_manager.add_record(*income_record)
    finance_manager.add_record(*expense_record)
    assert finance_manager.calculate_balance(0) == 500
    assert finance_manager.calculate_balance(1) == 1000
    assert finance_manager.calculate_balance(2) == 500

def test_search_records(finance_manager):
    income_record = ('2024-05-03', 'Доход', 1000, 'Test income')
    finance_manager.add_record(*income_record)
    results = finance_manager.search_records(category='Доход')
    assert len(results) == 1
    assert results[0]['Описание'] == 'Test income'

    results = finance_manager.search_records(amount=1000)
    assert len(results) == 1
    assert results[0]['Категория'] == 'Доход'

    results = finance_manager.search_records(date='2024-05-03')
    assert len(results) == 1
    assert results[0]['Описание'] == 'Test income'

    results = finance_manager.search_records(category='Расход')
    assert len(results) == 0
