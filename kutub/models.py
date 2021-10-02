import re
from django.db.models.fields import CharField
from lxml import etree

from django.db import models
from django.urls import reverse_lazy, reverse
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel

from next_prev import next_in_order, prev_in_order
from publications.models import ReferenceModel
from partial_date.fields import PartialDateField

from .fields import DescriptionField

# def DescriptionField(**kwargs):
#     return models.TextField(default="", blank=True, **kwargs)

def clean_xml_string(string):
    return re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]+', '', string)


class Language(models.Model):
    tag = DescriptionField(
        docs="https://www.w3.org/International/articles/language-tags/index.en",
        help_text="The tag for this language. This is generated from the other fields and should not be edited manually."
    )
    language_subtag = DescriptionField(
        help_text="The IANA-registered code for the language. Written in lower case.",
        docs='https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry',
        validators=[RegexValidator(r"^[a-z]+$", message='The language code must be written in lower case.', code='language_subtag')],
        blank=False,
    )
    extlang = DescriptionField(
        help_text="The extended language subtag.",
        docs='https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry',
        validators=[RegexValidator(r"^[a-z]*$", message='The extended language subtag must be written in lower case.', code='invalid_extlang')]
    )
    script = DescriptionField(
        help_text="The script subtag. Omit unless making a necessary distinction.",
        docs='https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry',
        validators=[RegexValidator(r"[A-Z][a-z]{3}$", message='The script is four characters long with the first character uppercase.', code='invalid_script')]
    )
    region = DescriptionField(
        help_text="The two-letter ISO 3166 country code or the 3-digit UN M.49 region code.",
        docs='https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry',
        validators=[RegexValidator(r"^[A-Z]{2}|\d{3}$", message='Not a valid two-letter ISO 3166 country code or 3-digit UN M.49 region code.', code='invalid_region')]
    )
    description = DescriptionField(
        help_text="A description of this language.",
    )

    class Meta:
        ordering = ('description', 'language_subtag','extlang','script','region',)

    def generate_tag(self):
        components = [component for component in [self.language_subtag, self.extlang, self.script, self.region] if component]
        return "-".join(components)
    
    def save(self, *args, **kwargs):
        self.tag = self.generate_tag()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.description:
            return self.description
        if self.tag:
            return self.tag
        return self.generate_tag()


class TextLangModel(models.Model):
    main_language = models.ForeignKey(Language, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT, help_text="The main language used.", related_name='main_language_set')
    other_languages = models.ManyToManyField(Language, help_text="Other languages used.", related_name='other_language_set')
    text_language_description = DescriptionField(
        tag="textLang",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#mslangs",
        help_text="A description of the language(s).",
    )

    class Meta:
        abstract = True

    def get_text_language_description(self):
        if self.text_language_description:
            return self.text_language_description
        else:
            if self.other_languages.count():
                other_languages_description = "; ".join([language.description for language in self.other_languages.all()])
                if self.main_language:
                    return f"Main Language: {self.main_language.description}. Other Languages: {other_languages_description}"
                else:
                    return other_languages_description
            elif self.main_language:
                return self.main_language.description
        return ""

    def text_language_xml(self):
        if not (self.main_language or self.other_languages.count() or self.text_language_description):
            return None
        
        attributes = dict()
        if self.main_language:
            attributes['mainLang'] = self.main_language.tag
        if self.other_languages.count():
            attributes['otherLangs'] = " ".join([language.tag for language in self.other_languages.all()])

        element = etree.Element("textLang", **attributes)
        element.text = self.get_text_language_description()

        return element


class XMLModel(models.Model):
    class Meta:
        abstract = True

    def xml_element(self):
        """ 
        Returns an etree element for this object which conforms to TEI P5.
        """
        raise NotImplementedError

    def xml_string(self, **kwargs):
        return etree.tostring(self.xml_element(), **kwargs)

    def xml_pretty_print(self, **kwargs):
        return self.xml_string(pretty_print=True).decode("utf-8")

    def add_sub_element(self, parent, field_name):
        value = getattr(self, field_name)
        if value:
            tag = field_name
            for field in self._meta.fields:
                if field.name == field_name:
                    tag = field.tag

            etree.SubElement(parent, tag).text = value

    def field_attr(self, field_name, attribute):
        field = self._meta.get_field(field_name)
        if hasattr(field, attribute):
            return getattr(field, attribute)

    def help_text(self, field_name):
        return self.field_attr( field_name, "help_text")

    def field_help(self, field_name):
        return self.field_attr( field_name, "help_text")

    def field_docs(self, field_name):
        return self.field_attr( field_name, "docs")

    def field_tag(self, field_name):
        return self.field_attr( field_name, "tag")


class NextPrevMixin(models.Model):
    class Meta:
        abstract = True

    def next_in_order(self, **kwargs):
        return next_in_order( self )

    def prev_in_order(self, **kwargs):
        return prev_in_order( self )


class IdentifierModel(NextPrevMixin, TimeStampedModel, models.Model):
    identifier = models.CharField(max_length=255, help_text="The identifier of this object.")
    slug = AutoSlugField(populate_from='identifier', unique=True)

    def __str__(self):
        return self.identifier

    class Meta:
        abstract = True
        ordering = ('identifier',)

    def get_absolute_url(self):
        return reverse_lazy(f"{self._meta.app_label}:{self.__class__.__name__.lower()}-detail", kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        return reverse_lazy(f"{self._meta.app_label}:{self.__class__.__name__.lower()}-update", kwargs={"slug": self.slug})

    def get_admin_url(self):
        return reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=(self.pk,))


class Repository(XMLModel, ReferenceModel, IdentifierModel):
    """
    Details for a repository within which manuscripts or other objects are stored, possibly forming part of an institution.
    
    https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-repository.html
    """
    identifier = models.CharField(max_length=255, default="", help_text="The name of this repository.")
    url = models.CharField(max_length=1023, default="", blank=True, help_text="An external URL for this location.", verbose_name="URL",)
    location_description = models.CharField(max_length=255, blank=True, default="", help_text="A verbose description of the location.")
    settlement = models.CharField(max_length=255, blank=True, default="", help_text="The name of a settlement such as a city, town, or village identified as a single geo-political or administrative unit.")
    latitude = models.FloatField(
        blank=True, 
        default=None, 
        null=True, 
        help_text="The latitude coordinate of this repository (in decimals).",
        validators=[MinValueValidator(-90), MaxValueValidator(90)],        
    )
    longitude = models.FloatField(
        blank=True, 
        default=None, 
        null=True, 
        help_text="The longitude coordinate of this repository (in decimals).",
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )

    class Meta:
        ordering = ["identifier"]

    def xml_element(self):
        """ 
        Returns an etree element for this repository which conforms to TEI P5.
        
        https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-repository.html
        """
        root = etree.Element("repository") # TODO  {'xml:id':'respository:{self.slug}'
        etree.SubElement(root, "name").text = self.identifier

        if self.url:
            etree.SubElement(root, "ref", target=self.url)

        location = None
        if self.location_description: 
            location = etree.SubElement(root, "location")
            etree.SubElement(location, "desc").text = self.location_description

        if self.settlement:
            if location is None:
                location = etree.SubElement(root, "location")
            # https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-geo.html
            etree.SubElement(location, "settlement").text = str(self.settlement)

        if self.latitude is not None and self.longitude is not None:
            if location is None:
                location = etree.SubElement(root, "location")
            # https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-geo.html
            etree.SubElement(location, "geo").text = f"{self.latitude} {self.longitude}"

        return root

    def has_coords(self):
        return self.latitude is not None and self.longitude is not None


class Manuscript(XMLModel, TextLangModel, ReferenceModel, IdentifierModel):
    """
    
    https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html

    Help text for fields frequently draws on the text if this document.
    """
    heading = DescriptionField(
        tag="head", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msdo", 
        help_text="A brief description of the manuscript (for example, the title)."
    )
    identifier = models.CharField(max_length=255, help_text="The identifier of the manuscript.")
    alt_identifier = models.CharField(max_length=255, default="", blank=True, help_text="An alternative identifier of the manuscript.")
    url = DescriptionField(
        tag="ref",
        help_text="An external URL for this manuscript.", 
        verbose_name="URL",
    )
    repository = models.ForeignKey(
        Repository, 
        default=None, 
        null=True, 
        blank=True, 
        on_delete=models.SET_DEFAULT, 
        help_text="The repository where this manuscript is held."
    )    
    content_summary = DescriptionField(
        tag="summary", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msco", 
        help_text="A summary of the intellectual content in this manuscript. More details can be added below."
    )
    iiif_manifest_url = DescriptionField( help_text="A URL to a IIIF manifest with facsimiles of this manuscript.", verbose_name="IIIF Manifest URL" )
    # Physical Description
    support_description = DescriptionField(
        tag="supportDesc",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msph1sup",
        help_text="A description of the physical support for the written part of a manuscript.",
    )    
    extent_numeric = models.PositiveIntegerField(default=None, null=True, blank=True, help_text="The number of leaves in the manuscript as an integer.")
    extent_description = DescriptionField(
        tag="extent",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msph1ext",
        help_text="A description of the number of leaves in the manuscript.",
    )
    height = models.PositiveIntegerField(default=None, blank=True, null=True, help_text="The measurement of the manuscript leaves in millimetres along the axis parallel to its bottom, e.g. perpendicular to the spine of a book or codex.")
    width = models.PositiveIntegerField(default=None, blank=True, null=True, help_text="The measurement in millimetres leaves along the axis at a right angle to the bottom of the manuscript.")
    dimensions_description = DescriptionField(
        tag="dimensions",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msph1ext",
        help_text="A description of the dimensions of the leaves which can be used if the basic height and width values are not sufficient."
    )
    collation = DescriptionField(
        tag="collation",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msph1col",
        help_text="A description of the arrangement of the leaves and quires of the manuscript.",
    )
    catchwords = DescriptionField(
        tag="catchwords",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msmisc",
        help_text="The system used to ensure correct ordering of the quires or similar making up a codex, typically by means of annotations at the foot of the page.",
    )
    signatures = DescriptionField(
        tag="signatures",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msmisc",
        help_text="A description of the leaf or quire signatures found within a codex.",
    )
    foliation = DescriptionField(
        tag="foliation",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msphfo",
        help_text="The scheme, medium or location of folio, page, column, or line numbers written in the manuscript, frequently including a statement about when and, if known, by whom, the numbering was done.",
    )
    condition = DescriptionField(
        tag="condition",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msphco",
        help_text="A summary of the overall physical state of a manuscript, in particular where such information is not recorded elsewhere in the description.",
    )
    layout = DescriptionField(
        tag="layout",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msphla",
        help_text="How how text is laid out on the page or surface of the manuscript, including information about any ruling, pricking, or other evidence of page-preparation techniques.",
    )
    hand_description = DescriptionField(
        tag="handDesc",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msphwr",
        help_text="A description of all the different hands used in the manuscript.",
    )
    decoration_description = DescriptionField(
        tag="decoDesc",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msphdec",
        help_text="A description of the decoration of the manuscript.",
    )
    music_notation = DescriptionField(
        tag="musicNotation",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msphmu",
        help_text="A description of the type of musical notation.",
    )
    binding_description = DescriptionField(
        tag="bindingDesc",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msphbi",
        help_text="A description of the state of the present and former bindings of a manuscript, including information about its material, any distinctive marks, and provenance information.",
    )
    seal_description = DescriptionField(
        tag="sealDesc",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msphse",
        help_text="information about the seal(s) attached to documents to guarantee their integrity, or to show authentication of the issuer or consent of the participants.",
    )
    # History
    origin = DescriptionField(
        tag="origin",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#mshy",
        help_text="Any descriptive or other information concerning the origin of a manuscript."
    )
    origin_place = DescriptionField(
        tag="origPlace",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msdates",
        help_text="Any form of place name, used to identify the place of origin for a manuscript."
    )
    origin_date_description = DescriptionField(
        tag="origDate",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msdates",
        help_text="Any form of date, used to identify the date of origin for a manuscript, manuscript part, or other object."
    )
    origin_date_earliest = PartialDateField(
        blank=True,
        default=None,
        null=True,
        help_text="The earliest possible date for the origin of the manuscript.",
    )
    origin_date_latest = PartialDateField(
        blank=True,
        default=None,
        null=True,
        help_text="The latest possible date for the origin of the manuscript.",
    )
    provenance = DescriptionField(
        tag="provenance",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#mshy",
        help_text="Any description or other information concerning a single identifiable episode during the history of a manuscript, manuscript part, or other object after its creation but before its acquisition. Separated by one or more line breaks."
    )
    acquisition = DescriptionField(
        tag="acquisition",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#mshy",
        help_text="Any descriptive or other information concerning the process by which the manuscript entered the holding institution."
    )
    source = DescriptionField(
        tag="source",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msrh",
        help_text="Describes the original source for the information contained with this manuscript description."
    )
    note = DescriptionField(
        tag="note",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html",
        help_text="A general description of the manuscript if the content cannot be easily placed in the other fields."
    )

    def __str__(self):
        if self.heading:
            return self.heading

        return f"{self.repository} {self.identifier}".strip()
    
    class Meta:
        ordering = ["repository","identifier"]

    def xml_element(self):
        """ 
        Returns an etree element for this manuscript which conforms to TEI P5.
        
        https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-msDesc.html
        """
        root = etree.Element("msDesc")
        msIdentifier = etree.SubElement(root, "msIdentifier")

        if self.repository:
            repository_xml = self.repository.xml_element()
            msIdentifier.append( repository_xml )
        
        etree.SubElement(msIdentifier, "idno").text = self.identifier

        if self.alt_identifier:
            alt = etree.SubElement(msIdentifier, "altIdentifier")
            etree.SubElement(alt, "idno").text = self.alt_identifier

        if self.url:
            etree.SubElement(root, "ref", target=self.url)

        #######################
        ## Contents
        #######################
        contents = etree.Element("msContents")
        if self.content_summary:
            etree.SubElement(contents, "summary").text = self.content_summary

        text_language_element = self.text_language_xml()
        if text_language_element is not None:
            contents.append(text_language_element)

        for item_index, item in enumerate(self.contentitem_set.all()):
            item_xml = item.xml_element()
            item_xml.set("n", str(item_index+1))
            contents.append(item_xml)

        if len(contents):
            root.append( contents )

        #########################
        ## Physical Description
        #########################
        physical_description = etree.Element("physDesc")
        
        # Object Description #
        object_description = etree.Element("objectDesc")

        ## Support ##
        if self.support_description:
            etree.SubElement(etree.SubElement(object_description, "supportDesc"), "p").text = self.support_description

        ## Extent ##
        extent = etree.Element("extent")
        dimensions = etree.Element("dimensions", unit="mm")
        if self.height:
            etree.SubElement(dimensions, "height").text = str(self.height)
        if self.width:
            etree.SubElement(dimensions, "width").text = str(self.width)
        if self.dimensions_description:
            dimensions.text = self.dimensions_description
        if self.extent_description:
            extent.text = self.extent_description
        if self.extent_numeric:
            etree.SubElement(extent, "measure", unit="leaf", quantity=str(self.extent_numeric))
        if len(dimensions) or dimensions.text:
            extent.append( dimensions )
        if len(extent) or extent.text:
            object_description.append( extent )

        ## Collation ##
        collation = etree.Element("collation")
        if self.collation:
            etree.SubElement(collation, "p").text = self.collation
        if self.catchwords:
            etree.SubElement(collation, "catchwords").text = self.catchwords
        if self.signatures:
            etree.SubElement(collation, "signatures").text = self.signatures
        if len(collation):
            object_description.append( collation )
            
        ## Foliation ##
        if self.foliation:
            etree.SubElement(etree.SubElement(object_description, "foliation"), "p").text = self.foliation

        ## Condition ##
        if self.condition:
            etree.SubElement(etree.SubElement(object_description, "condition"), "p").text = self.condition

        if len(object_description):
            physical_description.append( object_description )

        # Layout #
        if self.layout:
            #TODO Add columns
            etree.SubElement(physical_description, "layout").text = self.layout

        # Hand Description #
        if self.hand_description:
            etree.SubElement(physical_description, "handDesc").text = self.hand_description

        # Decoration Description #
        if self.decoration_description:
            etree.SubElement(physical_description, "decoDesc").text = self.decoration_description

        # Music Notation #
        if self.music_notation:
            etree.SubElement(physical_description, "musicNotation").text = self.music_notation

        # Binding #
        if self.binding_description:
            etree.SubElement(etree.SubElement(physical_description, "bindingDesc"), "p").text = self.binding_description

        # Seal #
        if self.seal_description:
            etree.SubElement(etree.SubElement(physical_description, "sealDesc"), "p").text = self.seal_description
        
        if len(physical_description):
            root.append( physical_description )

        #########################
        ## History
        #########################
        history = etree.Element("history")
        
        # Origin
        kwargs = {}
        if self.origin_date_earliest:
            kwargs['notBefore'] = str(self.origin_date_earliest)
        if self.origin_date_latest:
            kwargs['notAfter'] = str(self.origin_date_latest)
        origin = etree.Element("origin", **kwargs)
        
        if self.origin:
            etree.SubElement(origin, "p").text = self.origin
        
        if self.origin_place:
            etree.SubElement(origin, "origPlace").text = self.origin_place
        
        if self.origin_date_description:
            etree.SubElement(origin, "origDate").text = self.origin_date_description

        if len(origin):
            root.append( history )

        # Provenance
        for item in self.provenance_items():
            etree.SubElement(etree.SubElement(history, "provenance"), "p").text = item

        # Acquisition
        if self.acquisition:
            etree.SubElement(etree.SubElement(history, "acquisition"), "p").text = self.acquisition
        
        history = etree.Element("history")
 
        #########################
        ## Additional
        #########################
        if self.source:
            additional = etree.SubElement(root, "additional")
            admin = etree.SubElement(additional, "adminInfo")
            record_history = etree.SubElement(admin, "recordHist")
            source = etree.SubElement(record_history, "source")
            etree.SubElement(source, "p").text = self.source

        if self.note:
            etree.SubElement(root, "note").text = self.note

        return root

    def provenance_items(self):
        items = []
        for component in self.provenance.split("\n"):
            component = component.strip()
            if component:
                items.append(component)
        return items


class Side(models.TextChoices):
    UNKNOWN = ''
    RECTO = 'r'
    VERSO = 'v'


class ContentItem(XMLModel, TextLangModel, ReferenceModel, TimeStampedModel, models.Model):
    """
    An individual work or item within the intellectual content of a manuscript.

    https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msco
    https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-msItem.html
    """
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE, help_text="The manuscript in which this item is found.")
    locus_description = DescriptionField(
        tag="locus", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msloc", 
        help_text="A description identify any reference to one or more folios within a manuscript. If it is empty, it will be filled out by the fields to determin the start and end folios."
    )
    start_folio = models.PositiveIntegerField(blank=True, null=True, default=None, help_text='The folio number where this content item begins.')
    start_folio_side = models.CharField(max_length=1, blank=True, default=Side.UNKNOWN, choices=Side.choices, help_text='The folio side (i.e. recto or verso) where this content item begins.')
    end_folio = models.PositiveIntegerField(blank=True, null=True, default=None, help_text='The folio number where this content item ends.')
    end_folio_side = models.CharField(max_length=1, blank=True, default=Side.UNKNOWN, choices=Side.choices, help_text='The folio side (i.e. recto or verso) where this content item ends.')
    defective = models.BooleanField(default=None, null=True, blank=True, help_text="Whether the content item is incomplete through loss or damage.")
    author = DescriptionField(
        tag="author", 
        blank=True,
        default="",
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msat", 
        help_text="The normalized form of an author's name, irrespective of how this form of the name is cited in the manuscript.",
    )
    responsibility_statement = DescriptionField(
        tag="respStmt", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msat", 
        help_text="A statement of responsibility for the intellectual content of a content item, where the author field does not suffice.",
    )
    title = DescriptionField(
        tag="title", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msat", 
        help_text="A regularized form of the item's title, as distinct from any rubric quoted from the manuscript."
    )
    summary = DescriptionField(
        tag="p", 
        help_text="A summary of the content of this item."
    )
    rubric = DescriptionField(
        tag="rubric", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#mscorie", 
        help_text="the text of any rubric or heading attached to a particular content item.",
    )
    incipit = DescriptionField(
        tag="incipit", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#mscorie", 
        help_text="the text of any rubric or heading attached to a particular content item.",
    )
    quote = DescriptionField(
        tag="quote", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#mscorie", 
        help_text="A phrase or passage attributed by the narrator or author to some agency external to the text.",
    )
    explicit = DescriptionField(
        tag="explicit", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#mscorie", 
        help_text="The explicit of the item, that is, the closing words of the text proper, exclusive of any rubric or colophon which might follow it.",
    )
    final_rubric = DescriptionField(
        tag="finalRubric", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#mscorie", 
        help_text="the string of words that denotes the end of a text division, often with an assertion as to its author and title.",
    )
    colophon = DescriptionField(
        tag="colophon", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#mscorie", 
        help_text="The colophon of an item: that is, a statement providing information regarding the date, place, agency, or reason for production of the manuscript.",
    )
    deco_note = DescriptionField(
        tag="decoNote", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msphdec", 
        help_text="A note describing either a decorative component of a manuscript.",
    )
    filiation = DescriptionField(
        tag="filiation", 
        docs="https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msfil", 
        help_text="Information concerning the manuscript or other object's filiation, i.e. its relationship to other surviving manuscripts.",
    )
    note = DescriptionField(
        tag="note", 
        help_text="A note or annotation.",
    )
    main_language = models.ForeignKey(Language, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT, help_text="The main language used in this content item.", related_name='main_language_item_set')
    other_languages = models.ManyToManyField(Language, help_text="Other languages used in this content item.", related_name='other_language_item_set')

    class Meta:
        ordering = ["manuscript", "start_folio", "end_folio_side", "end_folio", "end_folio_side", "author", "title"]

    def __str__(self):
        return f"{self.manuscript}: {self.title}"

    def get_absolute_url(self):
        return self.manuscript.get_absolute_url()

    def folio_range(self):
        start_folio = self.start_folio or ""
        end_folio = self.end_folio or ""
        start_ref = f"{start_folio}{self.start_folio_side}"
        if start_folio == end_folio:
            if self.start_folio_side == self.end_folio_side:
                return start_ref
            return f"{start_ref}–{self.end_folio_side}"
        return f"{start_ref}–{end_folio}{self.end_folio_side}"

    def xml_element(self):
        """ 
        Returns an etree element for this content item which conforms to TEI P5.
        
        https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html#msco
        https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-msItem.html
        """
        root = etree.Element("msItem")

        # Locus
        locus_description = self.locus_description
        if not locus_description:
            locus_description = self.folio_range()
        
        if locus_description:
            kwargs = {}
            if self.start_folio and self.start_folio_side:
                kwargs["from"] = f"{self.start_folio}{self.start_folio_side}"
            if self.end_folio and self.end_folio_side:
                kwargs["to"] = f"{self.end_folio}{self.end_folio_side}"
            
            etree.SubElement(root, "locus", **kwargs).text = locus_description
        
        self.add_sub_element(root, "author")
        self.add_sub_element(root, "responsibility_statement") # should there be sub elements?
        self.add_sub_element(root, "title")
        self.add_sub_element(root, "summary")
        self.add_sub_element(root, "rubric")
        self.add_sub_element(root, "incipit")
        self.add_sub_element(root, "quote")
        self.add_sub_element(root, "explicit")
        self.add_sub_element(root, "final_rubric")
        self.add_sub_element(root, "colophon")
        self.add_sub_element(root, "deco_note")
        self.add_sub_element(root, "filiation")
        self.add_sub_element(root, "note")

        text_language_element = self.text_language_xml()
        if text_language_element is not None:
            root.append(text_language_element)

        return root

