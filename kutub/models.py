from lxml import etree

from django.db import models
from django.urls import reverse_lazy, reverse
from django.core.validators import MaxValueValidator, MinValueValidator

from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel

from next_prev import next_in_order, prev_in_order
from publications.models import ReferenceModel

def DescriptionField(**kwargs):
    return models.CharField(max_length=1023, default="", blank=True, **kwargs)

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


class Manuscript(XMLModel, ReferenceModel, IdentifierModel):
    """
    
    https://tei-c.org/release/doc/tei-p5-doc/en/html/MS.html

    Help text for fields frequently draws on the text if this document.
    """
    repository = models.ForeignKey(
        Repository, 
        default=None, 
        null=True, 
        blank=True, 
        on_delete=models.SET_DEFAULT, 
        help_text="The repository where this manuscript is held."
    )    
    identifier = models.CharField(max_length=255, help_text="The identifier of the manuscript.")
    alt_identifier = models.CharField(max_length=255, default="", blank=True, help_text="An alternative identifier of the manuscript.")
    content_summary = DescriptionField(help_text="A summary of the intellectual content in this manuscript. More details can be added below.")
    extent_numeric = models.PositiveIntegerField(default=None, null=True, blank=True, help_text="The number of leaves in the manuscript as an integer.")
    extent_description = DescriptionField(help_text="A description of the number of leaves in the manuscript.")
    height = models.PositiveIntegerField(default=None, blank=True, null=True, help_text="The measurement of the manuscript leaves in millimetres along the axis parallel to its bottom, e.g. perpendicular to the spine of a book or codex.")
    width = models.PositiveIntegerField(default=None, blank=True, null=True, help_text="The measurement in millimetres leaves along the axis at a right angle to the bottom of the manuscript.")
    dimensions_description = DescriptionField(help_text="A description of the dimensions of the leaves which can be used if the basic height and width values are not sufficient.")
    collation = DescriptionField(help_text="A description of the arrangement of the leaves and quires of the manuscript.")
    catchwords = DescriptionField(help_text="The system used to ensure correct ordering of the quires or similar making up a codex, typically by means of annotations at the foot of the page.")
    signatures = DescriptionField(help_text="A description of the leaf or quire signatures found within a codex.")
    foliation = DescriptionField(help_text="The scheme, medium or location of folio, page, column, or line numbers written in the manuscript, frequently including a statement about when and, if known, by whom, the numbering was done.")
    condition = DescriptionField(help_text="A summary of the overall physical state of a manuscript, in particular where such information is not recorded elsewhere in the description.")
    layout = DescriptionField(help_text="How how text is laid out on the page or surface of the manuscript, including information about any ruling, pricking, or other evidence of page-preparation techniques.")
    hand_description = DescriptionField(help_text="A description of all the different hands used in the manuscript.")
    decoration_description = DescriptionField(help_text="A description of the decoration of the manuscript.")

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

        #######################
        ## Contents
        #######################
        contents = etree.Element("msContents")
        if self.content_summary:
            etree.SubElement(contents, "summary").text = self.content_summary

        if len(contents):
            root.append( contents )

        #########################
        ## Physical Description
        #########################
        physical_description = etree.Element("physDesc")
        
        # Object Description #
        object_description = etree.Element("objectDesc")

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

        if len(physical_description):
            root.append( physical_description )

        return root
