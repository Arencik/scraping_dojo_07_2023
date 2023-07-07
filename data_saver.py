import jsonlines


class DataSaver:
    def __init__(self, filename, quotes):
        self.filename = filename
        self.quotes = quotes

    # writing files to jsonl function
    def save_quotes_to_jsonl(self):
        with jsonlines.open(self.filename, mode="w") as writer:
            writer.write_all(self.quotes)
