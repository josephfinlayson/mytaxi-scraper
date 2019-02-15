import sys
from extract import parse_bill
import os
import pandas as pds
import json

from datetime import date, time


def get_metas(path):
    metas = []
    for file in os.listdir(path):
        if not file.endswith('.pdf'):
            continue

        meta = parse_bill(path + file)
        metas.append(meta)
    return metas


def main(path):
    metas = get_metas(path)
    data = [({'supplier': 'myTaxi',
              'id': meta['id'],
              'price': meta['price'],
              'to': meta['to'],
              'from': meta['from'],
              'date': meta['date'].isoformat()}) for meta in metas]
    df = pds.DataFrame(data)
    df = df.drop_duplicates(subset='id')
    df = df.sort_values('date')
    excelWriter = pds.ExcelWriter('bills.xlsx')
    df.to_excel(excelWriter, 'Sheet1', columns=['supplier', 'price', 'date'])
    excelWriter.save()

    total = sum(meta['price'] for meta in metas)
    print(total)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Not enough arguments. Please specify path with the mytaxi receipts.')
    path = sys.argv[1]
    main(path)
