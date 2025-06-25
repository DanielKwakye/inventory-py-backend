from patterns.strategies.sort_strategy import SortStrategy


class CreatedAtSortStrategy(SortStrategy):
    def sort(self, data: list) -> list:
        return sorted(data, key=lambda item: item['created_at'])