from notion.client import NotionClient


def filtered_rows(filter_func, rows):
    for row in filter(filter_func, rows):
        yield row


class NotionExporter:
    def __init__(self, *args, **kwargs):
        self.client = NotionClient(*args, **kwargs)

    def get_collection(self, collection_id):
        block = self.client.get_block(collection_id)
        self.collection = self.client.get_collection(block.collection.id)
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
        return rows

    def get_select_options(self, column_name):
        prop = self.collection.get_schema_properties()
        for p in prop:
            if p.get("name") == column_name and p.get("type") == "multi_select":
                return [i.get("value") for i in p.get("options")]

    def get_unposted(self, rows):
        galleries_tags = self.get_select_options("Posted")
        available_galleries_cnt = len(galleries_tags)
        unposted = filtered_rows(
            lambda x: len(x.posted) < available_galleries_cnt, rows
        )
        artworks = []
        for row in unposted:
            print("Name: '{}', and posted state: {}".format(row.name, row.posted))
            artworks.append(self.parse_page(row.id.replace("-", "")))
            print()
        return artworks

    def parse_page(self, page_id):
        page = self.client.get_block("https://www.notion.so/" + page_id)
        artItem = Art(page.name)
        artItem.add_property("page_id", page_id)
        for child in page.children:
            print("Parsing %s block" % child.type)
            if child.type == "table":
                properties = self.table_to_dict(child)
                for key in properties:
                    artItem.add_property(key, properties[key])
            if child.type == "text":
                print(child.title)
                artItem.add_property("description", child.title)
            artItem.add_property("posted", page.posted)
        return artItem

    def export(self, table_id):
        return self.get_unposted(self.get_collection(table_id))

    @staticmethod
    def table_to_dict(tableBlock):
        prop_dict = {}
        for child in tableBlock.children:
            k = child.get("properties.xqir")
            v = child.get("properties.ln@{")

            def normalize_filed(field):
                return field[0][0] if field is not None else ""

            v = normalize_filed(v)
            k = normalize_filed(k)
            print(k + " = " + v)
            if k == "":
                continue
            prop_dict[k] = v
        return prop_dict

    def update_label(self, art, value):
        row = self.client.get_block(art.page_id)
        for prop in row.schema:
            if prop["name"] == "Posted":
                art.posted.append(value)
                row.set_property(prop["id"], art.posted)
                break


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
