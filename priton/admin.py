from django.contrib import admin
from priton.models import Person, Phrase, Comics, Essense

class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'short_name',)
    #list_editable = ('sort', )


class PhraseAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'author',)


class EssenseInline(admin.TabularInline):
    model = Essense.comics.through


class ComicsAdmin(admin.ModelAdmin):
    list_display = ('title', 'comics_descr',)
    inlines = (EssenseInline,)
#    exclude = ('participants', )
    #list_editable = ('sort', )


class EssenseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('comics',)

admin.site.register(Person, PersonAdmin)
admin.site.register(Phrase, PhraseAdmin)
admin.site.register(Comics, ComicsAdmin)
#admin.site.register(Essense, EssenseAdmin)