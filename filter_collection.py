import csv
from pathlib import Path
from typing import List
from datetime import datetime

class Card:
    def __init__(self, scryfallId, quantity, name):
        self.scryfallId = scryfallId
        self.quantity = quantity
        self.name = name

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

            quantity = int(row[0])
            name = row[1]
            scryfall_id = row[-1]
            card = Card(scryfall_id, quantity, name)
            cards.append(card)

def write_to_markdown(path, cards: List[Card]):
    folder = Path(path)
    folder.mkdir(parents=True, exist_ok=True)

    date_now = datetime.now()
    date_formatted = str(date_now.year) + '-' + str(date_now.month) + '-'  + str(date_now.day) + '_' + str(date_now.hour) + ',' + str(date_now.minute) + ',' + str(date_now.second)
    md_file_name = 'filtered_deck_' + date_formatted + '.md'


    with (folder / md_file_name).open("w", encoding="utf-8") as file:
        for card in cards:
            archideckt_input:str = str(card.quantity) + 'x ' + card.name
            
            file.write(archideckt_input + '\n')

def filter_decks_from_collections(decks: List[Card], collections: List[Card]):
    filtered_list: List[Card] = []
    for collection_card in collections:
        for deck_card in decks:
            if deck_card.scryfallId == collection_card.scryfallId:
                collection_card.quantity = collection_card.quantity - deck_card.quantity
        if collection_card.quantity > 0:
            filtered_list.append(collection_card)
    return filtered_list

def standardize_list(old_cards: List[Card]):
    cards = old_cards.copy()
    list_len = len(cards)
    for i in range(list_len):
        if i+1 >= list_len:
            break
        if cards[i].name == cards[i+1].name:
            cards[i].quantity = cards[i+1].quantity
            cards.pop(i+1)
            list_len -= 1
            i -= 1
    return cards

def get_card_count(cards: List[Card]):
    count:int = 0
    for card in cards:
        count += int(card.quantity)
    return count

def print_count_stats(collections: List[Card], standardized_collection: List[Card], decks: List[Card], filtered_list: List[Card]):
    print("collections ", get_card_count(collections))
    print("standardized_collection ", get_card_count(standardized_collection))
    print("decks ", get_card_count(decks))
    print("filtered_list ", get_card_count(filtered_list))


def print_count_stats(collections: List[Card], decks: List[Card], filtered_list: List[Card]):
    print("collections ", get_card_count(collections))
    print("decks ", get_card_count(decks))
    print("filtered_list ", get_card_count(filtered_list))

def print_card_list(cards: List[Card]):
    for card in cards:
        print(card.scryfallId, card.quantity, card.name)


collections: List[Card] = []
decks: List[Card] = []

read_from_folder("decks", decks)
read_from_folder("collections", collections)

filtered_list: List[Card] = filter_decks_from_collections(decks, collections)

print_count_stats(collections, decks, filtered_list)
write_to_markdown('filtered', filtered_list)

