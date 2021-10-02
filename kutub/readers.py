import csv
import re
import pandas as pd
from lxml import etree


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


def import_bischoff(manuscripts_excel, omeka_xml=None):
    repository, _ = models.Repository.objects.update_or_create(
        identifier="Monash University, Bischoff Collection",
        defaults=dict(
            url='https://www.monash.edu/library/bischoff',
            settlement="Melbourne",
            latitude=-37.912890798928274,
            longitude=145.13442309216325,
        )
    )
    if omeka_xml:
        omeka = etree.parse(omeka_xml).getroot()
    else:
        omeka = None

    df = pd.read_excel(manuscripts_excel)
    print(df.columns)
    for index, row in df.iterrows():
        empty_fields = pd.isna(row)
        if not empty_fields['Identifier (Shelf Mark)']:

            values = {}

            def add_value(field, column):
                if not empty_fields[column]:
                    values[field] = row[column]
            
            add_value('alt_identifier', 'Identifier (eg. MS number)')
            add_value('heading', 'Title')
            add_value('extent_description', 'Extent')
            add_value('origin_date_description', 'Date')
            add_value('origin_place', 'Creator')
            add_value('source', 'Creator')
            add_value('note', 'Description\n')
            values['source'] = f"Imported from Excel file '{manuscripts_excel}' (Shelf Mark: {row['Identifier (Shelf Mark)']})."

            # 'Subject' is '(keywords separated by '@')'
            # 'Language' TODO
            # 'Filename', "As assigned by Digitisation. Filename recorded on paper slip with physical item."

            manuscript, _ = models.Manuscript.objects.update_or_create(
                repository=repository,
                identifier=row['Identifier (Shelf Mark)'],
                defaults=values
            )                
            print(manuscript)

            if omeka:
                items = omeka.xpath(f"./o:item[.//*[contains(text(), '{manuscript.identifier}')]]", namespaces={'o':'http://omeka.org/schemas/omeka-xml/v5'})
                if len(items) == 1:
                    omeka_id = items[0].get('itemId')
                    if omeka_id:
                        manuscript.iiif_manifest_url = f"https://repository.monash.edu/items/presentation/{omeka_id}/manifest"
                        print(manuscript.iiif_manifest_url)
                        manuscript.save()