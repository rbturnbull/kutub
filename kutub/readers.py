import csv

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
            repository, _ = models.Repository.objects.update_or_create(
                settlement=clean_settlement(row['settlement']),
                identifier=row['repository'],
            )

            manuscript, _ = models.Manuscript.objects.update_or_create(
                repository=repository,
                identifier=row['library_ref'],
                alt_identifier=row['library_ref_alt'],
                content_summary=row['name'],
            )

