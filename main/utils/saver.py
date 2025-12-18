import pandas as pd
import json

class Saver:
    @staticmethod
    def saveJson(data, path):
        if isinstance(data, pd.DataFrame):
            data.to_json(path, orient='records', indent=4)
        else:
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)

    @staticmethod
    def saveCsv(data, path):
        if isinstance(data, pd.DataFrame):
            data.to_csv(path, index=False)
        else:
            pd.DataFrame(data).to_csv(path, index=False)

    @staticmethod
    def run(data, path, format):
        if format.lower() == 'json':
            Saver.saveJson(data, path)
        elif format.lower() == 'csv':
            Saver.saveCsv(data, path)
        else:
            raise ValueError(f"Unsupported format: {format}")