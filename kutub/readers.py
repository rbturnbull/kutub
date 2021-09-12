import csv
import re

from . import models


def clean_settlement(settlement):
    substitutions = {
        "Canberra, A.C.T.": "Canberra",
    }
    if settlement in substitutions:
        settlement = substitutions[settlement]

    return settlement

def import_europa_inventa(manuscripts_csv_path):
    with open(manuscripts_csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print( f"{row['repository']} {row['library_ref']}")
            repository, _ = models.Repository.objects.update_or_create(
                settlement=clean_settlement(row['settlement']),
                identifier=row['repository'],
            )

            height, width = None, None
            dimensions_description = ""
            if m := re.match(r'(\d+) x (\d+) mm', row['dimensions']):
                height, width = int(m.group(1)), int(m.group(2))
            if m := re.match(r'(\d+\.?\d*) x (\d+\.?\d*) cm', row['dimensions']):
                height, width = int(float(m.group(1)) * 10), int(float(m.group(2)) * 10)
            elif not row['dimensions']:
                height, width = None, None                
            else:
                dimensions_description = row['dimensions']

            manuscript, _ = models.Manuscript.objects.update_or_create(
                repository=repository,
                identifier=row['library_ref'],
                alt_identifier=row['library_ref_alt'],
                content_summary=row['name'],
                extent_description=row['extent'],
                width=width,
                height=height,
                dimensions_description=dimensions_description,
                collation=row['collation'],
                catchwords=row['catchwords'],
                foliation=row['foliation'],
                condition=row['condition'],
                layout=row['layout'],
                hand_description=row['hand_desc'],
                decoration_description=row['deco_desc'],
            )

