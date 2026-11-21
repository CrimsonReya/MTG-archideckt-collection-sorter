import csv
from pathlib import Path
from typing import List
from datetime import datetime

class Card:
    def __init__(self, scryfallId, quantity, archideckt_str):
        self.scryfallId = scryfallId
        self.quantity = quantity
        self.archideckt_str = archideckt_str

def read_from_folder(folder_path, cards: List[Card]):
    for path in Path(folder_path).iterdir():
        if path.is_file():
            read_from_csv_file(path, cards)

def read_from_csv_file(path, cards: List[Card]):
    with path.open("r", newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            if row[0] == 'Quantity':
                continue

            import_format:str = row[0] + 'x ' + row[1]
            card = Card(row[-1], row[0], import_format)
            cards.append(card)

def write_to_markdown(path, cards: List[Card]):
    folder = Path(path)
    folder.mkdir(parents=True, exist_ok=True)

    date_now = datetime.now()
    date_formatted = str(date_now.year) + '-' + str(date_now.month) + '-'  + str(date_now.day) + '_' + str(date_now.hour) + ',' + str(date_now.minute) + ',' + str(date_now.second)
    md_file_name = 'filtered_deck_' + date_formatted + '.md'

    with (folder / md_file_name).open("w", encoding="utf-8") as file:
        for card in cards:
            file.write(card.archideckt_str + '\n')

def filter_decks_from_collections(decks: List[Card], collections: List[Card]):
    filtered_list: List[Card] = []
    for collection_card in collections:
        used:bool = False
        for deck_card in decks:
            if deck_card.scryfallId == collection_card.scryfallId:
                used = True
                break
        if used == False:
            filtered_list.append(collection_card)
    return filtered_list

def get_card_count(cards: List[Card]):
    count:int = 0
    for card in cards:
        count += int(card.quantity)
    return count

def print_count_stats(collections: List[Card], decks: List[Card], filtered_list: List[Card]):
    print("collections ", get_card_count(collections))
    print("decks ", get_card_count(decks))
    print("filtered_list ", get_card_count(filtered_list))

def print_card_list(cards: List[Card]):
    for card in cards:
        print(card.scryfallId, card.quantity, card.archideckt_str)


collections: List[Card] = []
decks: List[Card] = []

read_from_folder("decks", decks)
read_from_folder("collections", collections)

filtered_list: List[Card] = filter_decks_from_collections(decks, collections)

print_count_stats(collections, decks, filtered_list)
write_to_markdown('filtered', filtered_list)

