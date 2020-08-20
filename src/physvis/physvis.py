from pathlib import Path
import re

import pandas as pd


def convert(
    input: str = "input", output: str = "output", delimiter: str = ";"
) -> None:
    print("Getting .csv data files ...")

    all_files = list(Path(input).glob('*.csv'));

    li = []

    for filename in all_files:
        print(filename.stem)
        df = pd.read_csv(filename, index_col=None, header=0, delimiter=delimiter, keep_default_na=False)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    print(frame.head(20))

    '''
    with open(data, "rt") as csvfile:
        csvdict = csv.DictReader(csvfile, delimiter=delimiter)
        csv_headers = csvdict.fieldnames
        if csv_headers and name not in csv_headers:
            print("Column name not found. Please enter valid column name")
            exit(1)
        docx = MailMerge(template)
        docx_mergefields = docx.get_merge_fields()

        print(f"DOCX fields : {docx_mergefields}")
        print(f"CSV field   : {csv_headers}")

        # see if all fields are accounted for in the .csv header
        column_in_data = set(docx_mergefields) - set(csv_headers)
        if len(column_in_data) > 0:
            print(f"{column_in_data} is in the word document, but not csv.")
            return

        print("All fields are present in your csv. Generating Word docs ...")
        output_path = create_output_folder(path)

        for row in csvdict:
            # Must create a new MailMerge for each file
            docx = MailMerge(template)
            single_document = {key: row[key] for key in docx_mergefields}
            docx.merge_templates([single_document], separator="page_break")
            filename = create_unique_name(row[name], output_path)
            docx.write(filename)
    '''
