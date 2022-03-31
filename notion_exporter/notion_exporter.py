from notion.client import NotionClient


def filtered_rows(filter_func, rows):
    for row in filter(filter_func, rows):
        yield row


class NotionExporter:
    def __init__(self, token):
        self.client = NotionClient(token_v2=token)

    def get_collection(self, collection_id):
        self.collection = self.client.get_collection(collection_id)
        sort_params = [
            {
                "direction": "descending",
                "property": "posted",
            }
        ]

        try:
            rows = self.collection.get_rows(sort=sort_params)
        except Exception as e:
            print(e)
            return []
        print(rows)
        return rows

    def get_unposted(self, rows):
        unposted = filtered_rows(lambda x: x.posted == "no", rows)
        artworks = []
        for row in unposted:
            print("Name: '{}', and state: {}".format(row.name, row.posted))
            artworks.append(self.parse_page(row.id.replace("-", "")))
            print()
        return artworks

    def parse_page(self, page_id):
        page = self.client.get_block("https://www.notion.so/" + page_id)
        artItem = Art(page.name)
        for child in page.children:
            print("Persing %s block" % child.type)
            if child.type == "table":
                properties = self.table_to_dict(child)
                for key in properties:
                    artItem.add_property(key, properties[key])
            if child.type == "text":
                print(child.title)
                artItem.add_property("description", child.title)
        return artItem

    def export(self, table_id):
        return self.get_unposted(self.get_collection(table_id))

    @staticmethod
    def table_to_dict(tableBlock):
        prop_dict = {}
        for child in tableBlock.children:
            k = child.get("properties.xqir")
            v = child.get("properties.ln@{")
            def normalize_filed(
                field): return field[0][0] if field is not None else ""
            v = normalize_filed(v)
            k = normalize_filed(k)
            print(k + " = " + v)
            if k == "":
                continue
            prop_dict[k] = v
        return prop_dict


class Art:
    def __init__(self, name):
        self.name = name

    def add_property(self, prop_name, prop_value):
        self.__dict__[prop_name] = prop_value

    def print(self):
        print(self.__dict__)

    def get_property(self, prop_name):
        if hasattr(self, prop_name):
            return getattr(self, prop_name)
        else:
            return ""  # All properties are in text format now
