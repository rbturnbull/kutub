
import csv

from .models import Manuscript

def manuscripts_to_csv(manuscripts, file, **fmtparams):

    fields = [
        'heading',
        'identifier',
        'alt_identifier',
        'url',
        'repository',
        'content_summary',
        'iiif_manifest_url',
        'support_description',
        'extent_numeric',
        'extent_description',
        'height',
        'width',
        'dimensions_description',
        'collation',
        'catchwords',
        'signatures',
        'foliation',
        'condition',
        'layout',
        'hand_description',
        'decoration_description',
        'music_notation',
        'binding_description',
        'seal_description',
        'origin',
        'origin_place',
        'origin_date_description',
        'origin_date_earliest',
        'origin_date_latest',
        'provenance',
        'acquisition',
        'source',
        'note',        
    ]

    writer = csv.writer(file, **fmtparams)
    writer.writerow(fields)
    for manuscript in manuscripts:
        values = [str(getattr(manuscript, field)) for field in fields]
        writer.writerow(values)

    return writer


def all_manuscripts_to_csv(file, **fmtparams):
    return manuscripts_to_csv(Manuscript.objects.all(), file, **fmtparams)
