from django.contrib import admin
from reversion.admin import VersionAdmin

from . import models


# class DocumentInline(admin.StackedInline):
#     model = models.Document
#     extra = 0


# class InfoInline(admin.StackedInline):
#     model = models.Info
#     extra = 0


# class ContentInline(admin.StackedInline):
#     model = models.Content
#     extra = 0


@admin.register(models.Repository)
class RepositoryAdmin(VersionAdmin):
    search_fields = ['__all__']
    # inlines = (DocumentInline,)


@admin.register(models.Language)
class LanguageAdmin(VersionAdmin):
    search_fields = ['__all__']


@admin.register(models.Manuscript)
class ManuscriptAdmin(VersionAdmin):
    search_fields = ['__all__']
    # inlines = (DocumentInline,)


# @admin.register(models.Document)
# class DocumentAdmin(PlaceholderAdminMixin, VersionAdmin):
#     search_fields = ['__all__']
#     inlines = (InfoInline,ContentInline)


# @admin.register(models.Language)
# class LanguageAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.InfoCategory)
# class InfoCategoryAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.Script)
# class ScriptAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.Material)
# class MaterialAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.DocumentTag)
# class DocumentTagAdmin(admin.ModelAdmin):
#     pass

