import csv
import re

from . import models


def clean_xml_string(string):
    """ 
    Removes characters not valid in XML standard.

    https://stackoverflow.com/a/8735509 
    """
    return re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]+', '', string)


def europa_inventa_source_str(ms_id):
    return f"Imported from Europa Inventa (manuscript id: {ms_id})."

def clean_settlement(settlement):
    substitutions = {
        "Canberra": "Canberra, A.C.T.",
        "Sydney": "Sydney, N.S.W.",
        "Box Hill": "Box Hill, Victoria",
        "Sydney, in the University of Sydney": "Sydney, N.S.W.",
    }
    if settlement in substitutions:
        settlement = substitutions[settlement]

    return settlement

def clean_repositories(repository):
    substitutions = {
        "Public Library of New South Wales, Dixson Library": "State Library of New South Wales, Dixson Library",
        "Mitchell Library, Special Collections": "State Library of New South Wales, Mitchell Library, Special Collections",
        "Mitchell Library, Special Collections, State Library of New South Wales": "State Library of New South Wales, Mitchell Library, Special Collections",
    }
    if repository in substitutions:
        repository = substitutions[repository]

    return repository

def import_europa_inventa_manuscripts(manuscripts_csv_path):
    with open(manuscripts_csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            # Only allow XML valid characters
            for key, value in row.items():
                if isinstance(value, str):
                    row[key] = clean_xml_string(value)

            print( f"{row['repository']} {row['library_ref']}")
            repository, _ = models.Repository.objects.update_or_create(
                settlement=clean_settlement(row['settlement']),
                identifier=clean_repositories(row['repository']),
            )

            height, width = None, None
            dimensions_description = ""
            if m := re.match(r'(\d+) x (\d+) mm', row['dimensions']):
                height, width = int(m.group(1)), int(m.group(2))
            elif m := re.match(r'(\d+\.?\d*) x (\d+\.?\d*) cm', row['dimensions']):
                height, width = int(float(m.group(1)) * 10), int(float(m.group(2)) * 10)
            elif not row['dimensions']:
                height, width = None, None                
            else:
                dimensions_description = row['dimensions']

            source = europa_inventa_source_str(row['id'])

            manuscript, _ = models.Manuscript.objects.update_or_create(
                repository=repository,
                identifier=row['library_ref'],
                alt_identifier=row['library_ref_alt'],
                content_summary=row['name'],
                support_description=row['support'],
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
                music_notation=row['music_notation'],
                binding_description=row['binding'],
                origin_place=row['orig_place'],
                provenance=row['provenance'],
                acquisition=row['acquisition'],
                source=source,
            )


def import_europa_inventa_content_items(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            # Only allow XML valid characters
            for key, value in row.items():
                if isinstance(value, str):
                    row[key] = clean_xml_string(value)

            # Get Manuscript
            manuscript = models.Manuscript.objects.filter(
                source=europa_inventa_source_str(row['manuscript_id'])
            ).first()
            if not manuscript:
                print(f"Could not find manuscript with id {row['manuscript_id']} for {row}")
                continue

            # Get Creator
            # row['creator_id']
            author = ""

            # Get Language
            # text_lang
            
            # Store ID
            # id

            models.ContentItem.objects.update_or_create(
                manuscript=manuscript,
                locus_description=row['locus'],
                title=row['title'],
                author=author,
                responsibility_statement=row['resp_stmt'],
                rubric=row['rubric'],
                incipit=row['incipit'],
                explicit=row['explicit'],
                colophon=row['colophon'],
                summary=row['summary'],
                note=row['note'],
            )


