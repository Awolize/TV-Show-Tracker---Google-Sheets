from pprint import pprint

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1av9nZT4YQ3nTHvmbvQAjOdUZpq9WsuswVx7Spw8hGBs"
SAMPLE_RANGE_NAME = "Class Data!A2:E"
CELL_SIZE = 25
ROW_INDEX_OFFSET = 2 # offset added based on (+1 from index starting at 0, +1 from row starting at 2)

class Spreadsheet(object):
    def __init__(self, service):
        self.service = service
        self.sheet = service.spreadsheets()

        if not self.does_sheet_exist("ToC"):
            print("Page: [Table of Contents] does not exist.\nSetting up page...")
            self.create_ToC_page()

    def create_ToC_page(self):
        # get_sheet(index == 0)
        # rename sheet
        # resize sheet
        # add header:
            # add "Table of Contents" text
            # add rating text
            # add imdb rating text
            # add color box for [finished/dropped/watching] text
        # ----------
        raise NotImplementedError

    def new_page_sheet_init(self, movie):
        requests = []
        # Add sheet and set grid size
        requests.append({
            "addSheet": {
                "properties": {
                    "sheetId": movie.id,
                    "title": movie.title,
                    "tabColor": {
                        "red": 0.44,
                        "green": 0.99,
                        "blue": 0.50
                    },
                    "sheetType": "GRID",
                    "gridProperties": {
                        "columnCount": len(movie.seasons) + 2,
                        "rowCount": max(movie.seasons.values()) + 2,
                        "frozenRowCount": 2,
                        "frozenColumnCount": 2,
                    }
                }
            }
        })
        # Set Cell Size
        requests.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": movie.id,
                    "dimension": "COLUMNS",
                },
                "properties": {
                    "pixelSize": CELL_SIZE
                },
                "fields": "pixelSize"
            }
        })
        requests.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": movie.id,
                    "dimension": "ROWS",
                },
                "properties": {
                    "pixelSize": CELL_SIZE
                },
                "fields": "pixelSize"
            }
        })

        requests.append({
            "mergeCells": {
                "range": {
                    "sheetId": movie.id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 2
                },
                "mergeType": "MERGE_ALL"
            }
        })

        requests.append({
            "mergeCells": {
                "range": {
                    "sheetId": movie.id,
                    "startRowIndex": 2,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "mergeType": "MERGE_ALL"
            }
        })

        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": movie.id,
                    "startRowIndex": 0,
                    "startColumnIndex": 0
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE",
                    },
                },
                "fields": "*"
            }
        })

        # Red / End of season
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": movie.id,
                    "startRowIndex": 2,
                    "startColumnIndex": 2,
                },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                        "red": 0.8,
                        "green": 0.0,
                        "blue": 0.0
                    }
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
            }
        })

        # Yellow / not watched
        for season in movie.seasons:
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": movie.id,
                        "startRowIndex": 2,
                        "endRowIndex": 2+movie.seasons[season],
                        "startColumnIndex": 1+season,
                        "endColumnIndex": 2+season,
                    },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {
                            "red": 1.0,
                            "green": 0.65,
                            "blue": 0.0
                        }
                    }
                },
                "fields": "userEnteredFormat(backgroundColor)"
                }
            })

        # Green / Watched
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": movie.id,
                    "startRowIndex": 0,
                    "endRowIndex": 2,
                    "startColumnIndex": 0,
                    "endColumnIndex": 2,
                },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                        "red": 0.0,
                        "green": 0.8,
                        "blue": 0.0
                    }
                }
            },
            "fields": "userEnteredFormat(backgroundColor)"
            }
        })

        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": movie.id,
                    "startRowIndex": 2,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "textRotation": {
                            "angle": 90,
                            # "vertical": True
                        }
                    }
                },
                "fields": "userEnteredFormat.textRotation"
            }
        })

        body = {
            "requests": requests
        }
        service = self.service
        service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()

    def new_page_static_text(self, movie):
         # Fill sheet with information
        self.write_values(movie.title+"!C1",
                          "USER_ENTERED", [["Seasons"]])
        # Write nr of Seasons (s1,s2,s3...sn)
        self.write_values(movie.title+"!C2:2",
                          "USER_ENTERED", [list(movie.seasons.keys())])
        self.write_values(movie.title+"!A3",
                          "USER_ENTERED", [["Episodes"]])

        # Write nr of Episodes (1,2,3,4,5,6,7,8,9,...,n)
        temp = []
        for i in range(1, 1 + max(movie.seasons.values())):
            temp.append([i])

        self.write_values(
            movie.title+"!B3:B", "USER_ENTERED", temp)

    def create_page(self, movie):
        service = self.service

        try:
            self.new_page_sheet_init(movie)
        except Exception as e:
            print("Error [new_page_sheet_init]: {}".format(e))
            print(e)

        # fill Table of Contents with titles and hyperlink to the new sheet
        self.add_hyperlink_to_ToS(movie.title, movie.id)

        # Set up static information, such as "seasons" and "episodes"
        self.new_page_static_text(movie)

        # Update ToC with the IMDB rating
        column = self.find_header("ToC", text="IMDB")
        row = self.get_all_titles().index(movie.title) 
        self.update_rating("ToC", column, row, movie.rating)

    def write_values(self, range_name, value_input_option, _values):
        service = self.service

        values = _values
        body = {
            "values": values
        }
        response = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption=value_input_option,
            body=body).execute()

        return response

    def add_hyperlink_to_ToS(self, title, id):
        service = self.service

        # Check if title already in ToS
        # Get all titles
        titles = self.get_all_titles()
        # if title not in ToS -> Add it to ToC
        if title not in titles:
            requests = []
            requests.append({
                "appendCells": {
                    "sheetId": 0,
                    "rows": [
                        {
                            "values": [{
                                "userEnteredValue": {
                                    "formulaValue":"=HYPERLINK(\"#gid={}\";\"{}\")".format(id, title) 
                                }
                            }]
                        }
                    ],
                    "fields": "userEnteredValue",
                }})
            body = {
                "requests": requests
            }
            service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()

    def remove_all(self):
        service = self.service

        sheet = service.spreadsheets()
        sheet_metadata = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get("sheets", "")

        remove = []
        if sheets:
            for page in sheets:
                if "ToC" == page["properties"]["title"]:
                    continue
                remove.append(page["properties"]["sheetId"])

        if remove:
            requests = []
            for id in remove:
                requests.append([
                    {
                        "deleteSheet": {
                            "sheetId": id
                        },
                    }
                ])
            body = {
                "requests": requests
            }
            service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID, body=body).execute()

    def print(self):
        service = self.service

        sheet = service.spreadsheets()
        sheet_metadata = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get("sheets", "")
        if sheets:
            for page in sheets:
                title = page["properties"]["title"]
                print(title)

    def does_sheet_exist(self, title):
        service = self.service
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get("sheets", "")

        if sheets:
            for page in sheets:
                if title == page["properties"]["title"]:
                    return True
        return False

    def get_all_titles(self):
        service = self.service
        header_col = self.find_header("ToC", "Table of Contents") # Header text for the titles
        range = "ToC!{col}2:{col}".format(col=header_col)

        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range).execute()
        values = result.get('values', [])
        titles = [item for sublist in values for item in sublist]
        return titles

    def find_header(self, range_, text):
        service = self.service
        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=range_).execute()
        range_ = result.get('range', "")
        values = result.get('values', [])

        header = values[0]
        header_col = header.index(text)
        
        return chr(65 + header_col) # A + column_index

    def update_rating(self, page, column, row_index, rating):
        row = row_index + ROW_INDEX_OFFSET
        self.write_values("{page}!{column1}{row1}:{column2}{row2}".format(page=page, column1=column, row1=str(row), column2=column,row2= str(row+1) ), "USER_ENTERED", [[rating]])

