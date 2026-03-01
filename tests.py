import pytest
from main import BooksCollector

class TestBooksCollector:

    # ---------- add_new_book ----------
    @pytest.mark.parametrize('name', [
        'Война и мир',
        'Мастер и Маргарита',
        '1984'
    ])
    def test_add_new_book_adds_book_with_valid_name(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.books_genre

    def test_add_new_book_does_not_add_existing_book(self):
        collector = BooksCollector()
        collector.add_new_book('Преступление и наказание')
        collector.add_new_book('Преступление и наказание')
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize('name, expected', [
        ('', False),
        ('a' * 40, True),   # ровно 40 символов
        ('b' * 41, False)   # больше 40
    ])
    def test_add_new_book_checks_name_length(self, name, expected):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert (name in collector.books_genre) == expected

    # ---------- set_book_genre ----------
    def test_set_book_genre_sets_genre_if_book_exists_and_genre_valid(self):
        collector = BooksCollector()
        collector.books_genre['Дюна'] = ''
        collector.set_book_genre('Дюна', 'Фантастика')
        assert collector.books_genre['Дюна'] == 'Фантастика'

    def test_set_book_genre_does_not_change_genre_if_book_does_not_exist(self):
        collector = BooksCollector()
        collector.set_book_genre('Несуществующая книга', 'Ужасы')
        assert collector.books_genre == {}

    def test_set_book_genre_does_not_set_invalid_genre(self):
        collector = BooksCollector()
        collector.books_genre['Шерлок Холмс'] = ''
        collector.set_book_genre('Шерлок Холмс', 'Триллер')
        assert collector.books_genre['Шерлок Холмс'] == ''

    # ---------- get_book_genre ----------
    def test_get_book_genre_returns_genre_for_existing_book_with_genre(self):
        collector = BooksCollector()
        collector.books_genre['Оно'] = 'Ужасы'
        assert collector.get_book_genre('Оно') == 'Ужасы'

    def test_get_book_genre_returns_empty_string_for_existing_book_without_genre(self):
        collector = BooksCollector()
        collector.books_genre['Зеленая миля'] = ''
        assert collector.get_book_genre('Зеленая миля') == ''

    def test_get_book_genre_returns_none_for_non_existent_book(self):
        collector = BooksCollector()
        assert collector.get_book_genre('Нет такой книги') is None

    # ---------- get_books_with_specific_genre ----------
    def test_get_books_with_specific_genre_returns_correct_books(self):
        collector = BooksCollector()
        collector.books_genre = {
            'Оно': 'Ужасы',
            'Зеленая миля': 'Детективы',
            'Шрэк': 'Мультфильмы'
        }
        result = collector.get_books_with_specific_genre('Ужасы')
        assert result == ['Оно']

    # ---------- get_books_genre ----------
    def test_get_books_genre_returns_dict(self):
        collector = BooksCollector()
        collector.books_genre = {'Книга 1': 'Комедии', 'Книга 2': ''}
        assert collector.get_books_genre() == {'Книга 1': 'Комедии', 'Книга 2': ''}

    # ---------- get_books_for_children ----------
    @pytest.mark.parametrize('book, genre, expected_in_children', [
        ('Гарри Поттер', 'Фантастика', True),
        ('Сияние', 'Ужасы', False),
        ('Убийство в Восточном экспрессе', 'Детективы', False),
        ('Ну, погоди!', 'Мультфильмы', True)
    ])
    def test_get_books_for_children_filters_age_rating(self, book, genre, expected_in_children):
        collector = BooksCollector()
        collector.books_genre[book] = genre
        children_books = collector.get_books_for_children()
        assert (book in children_books) == expected_in_children

    # ---------- add_book_in_favorites ----------
    def test_add_book_in_favorites_adds_book_if_in_books_genre(self):
        collector = BooksCollector()
        collector.books_genre['Метро 2033'] = 'Фантастика'
        collector.add_book_in_favorites('Метро 2033')
        assert 'Метро 2033' in collector.favorites

    def test_add_book_in_favorites_does_not_add_if_book_not_in_books_genre(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Неизвестная книга')
        assert collector.favorites == []

    def test_add_book_in_favorites_does_not_add_duplicate(self):
        collector = BooksCollector()
        collector.books_genre['Пикник на обочине'] = 'Фантастика'
        collector.favorites = ['Пикник на обочине']
        collector.add_book_in_favorites('Пикник на обочине')
        assert collector.favorites == ['Пикник на обочине']

    # ---------- delete_book_from_favorites ----------
    def test_delete_book_from_favorites_removes_book(self):
        collector = BooksCollector()
        collector.favorites = ['451 градус по Фаренгейту']
        collector.delete_book_from_favorites('451 градус по Фаренгейту')
        assert '451 градус по Фаренгейту' not in collector.favorites

    def test_delete_book_from_favorites_does_nothing_if_book_not_in_favorites(self):
        collector = BooksCollector()
        collector.favorites = ['Книга']
        collector.delete_book_from_favorites('Отсутствующая книга')
        assert collector.favorites == ['Книга']

    # ---------- get_list_of_favorites_books ----------
    def test_get_list_of_favorites_books_returns_favorites_list(self):
        collector = BooksCollector()
        collector.favorites = ['Книга 1', 'Книга 2']
        assert collector.get_list_of_favorites_books() == ['Книга 1', 'Книга 2']