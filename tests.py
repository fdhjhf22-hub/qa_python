from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_rating()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()


import pytest
from main import BooksCollector

class TestBooksCollector:

    # ---------- Тесты для add_new_book ----------
    @pytest.mark.parametrize('name', [
        'Война и мир',
        'Мастер и Маргарита',
        '1984'
    ])
    def test_add_new_book_adds_book_with_valid_name(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.get_books_genre()

    def test_add_new_book_does_not_add_existing_book(self):
        collector = BooksCollector()
        collector.add_new_book('Преступление и наказание')
        collector.add_new_book('Преступление и наказание')
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize('name, expected', [
        ('', False),
        ('Книга с названием длиной ровно сорок символов!', True),  # 40 символов
        ('Очень длинное название, которое превышает сорок символов и поэтому не должно добавиться', False)
    ])
    def test_add_new_book_checks_name_length(self, name, expected):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected

    # ---------- Тесты для set_book_genre и get_book_genre ----------
    def test_set_book_genre_sets_genre_if_book_exists_and_genre_valid(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        assert collector.get_book_genre('Дюна') == 'Фантастика'

    def test_set_book_genre_does_not_set_genre_if_book_does_not_exist(self):
        collector = BooksCollector()
        collector.set_book_genre('Несуществующая книга', 'Ужасы')
        # Проверим, что никаких изменений не произошло (можно через пустой словарь)
        assert collector.get_books_genre() == {}

    def test_set_book_genre_does_not_set_invalid_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Шерлок Холмс')
        collector.set_book_genre('Шерлок Холмс', 'Триллер')  # Триллера нет в списке genre
        assert collector.get_book_genre('Шерлок Холмс') == ''

    # ---------- Тест для get_books_with_specific_genre ----------
    def test_get_books_with_specific_genre_returns_correct_books(self):
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.add_new_book('Зеленая миля')
        collector.set_book_genre('Зеленая миля', 'Детективы')
        collector.add_new_book('Шрэк')
        collector.set_book_genre('Шрэк', 'Мультфильмы')
        result = collector.get_books_with_specific_genre('Ужасы')
        assert result == ['Оно']

    # ---------- Тест для get_books_genre ----------
    def test_get_books_genre_returns_dict(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 1', 'Комедии')
        expected = {'Книга 1': 'Комедии', 'Книга 2': ''}
        assert collector.get_books_genre() == expected

    # ---------- Тесты для get_books_for_children ----------
    @pytest.mark.parametrize('book, genre, expected_in_children', [
        ('Гарри Поттер', 'Фантастика', True),
        ('Сияние', 'Ужасы', False),
        ('Убийство в Восточном экспрессе', 'Детективы', False),
        ('Ну, погоди!', 'Мультфильмы', True)
    ])
    def test_get_books_for_children_filters_age_rating(self, book, genre, expected_in_children):
        collector = BooksCollector()
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)
        children_books = collector.get_books_for_children()
        assert (book in children_books) == expected_in_children

    # ---------- Тесты для избранного ----------
    def test_add_book_in_favorites_adds_book_if_in_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Метро 2033')
        collector.add_book_in_favorites('Метро 2033')
        assert 'Метро 2033' in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_does_not_add_if_book_not_in_books_genre(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Неизвестная книга')
        assert collector.get_list_of_favorites_books() == []

    def test_add_book_in_favorites_does_not_add_duplicate(self):
        collector = BooksCollector()
        collector.add_new_book('Пикник на обочине')
        collector.add_book_in_favorites('Пикник на обочине')
        collector.add_book_in_favorites('Пикник на обочине')
        assert collector.get_list_of_favorites_books() == ['Пикник на обочине']

    def test_delete_book_from_favorites_removes_book(self):
        collector = BooksCollector()
        collector.add_new_book('451 градус по Фаренгейту')
        collector.add_book_in_favorites('451 градус по Фаренгейту')
        collector.delete_book_from_favorites('451 градус по Фаренгейту')
        assert '451 градус по Фаренгейту' not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_does_nothing_if_book_not_in_favorites(self):
        collector = BooksCollector()
        collector.delete_book_from_favorites('Отсутствующая книга')
        # просто не должно быть ошибки
        assert True