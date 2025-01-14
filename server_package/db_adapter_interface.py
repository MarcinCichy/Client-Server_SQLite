from abc import ABC, abstractmethod


class DatabaseAdapter(ABC):
    """
    Interface (klasa bazowa) definiująca metody, któe musza zaimplementować apatery dla poszczególnych baz danych.
    """

    @abstractmethod
    def connect(self):
        """
        Nawiązuje połaczenia z baza danych
        """

    @abstractmethod
    def disconnect(self):
        """
        Zamyka połaczenie z baza danych
        """

    @abstractmethod
    def execute_query(self, query, params=None):
        """
        Wykonuje zapytanie SQL (typu INSERT, UPDATE, DELETE)
        bez zwracania wyników.
        """

    @abstractmethod
    def fetch_one(self, query, params=None):
        """
        Wykonuje zapytanie SELECT i pobiera jeden rekord z bazy danych
        lub None, jeśli brak wyników.
        """

    @abstractmethod
    def fetch_all(self, query, params=None):
        """
        Wykonuje zapytanie SELECT i zwraca listę krotek lub pustą listę.
        """
