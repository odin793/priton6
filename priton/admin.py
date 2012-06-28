from django.contrib import admin
from priton.models import Person, Phrase, Comics, Essense

class PhraseInline(admin.TabularInline):
    model = Phrase
    
    
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'short_name',)
    list_filter = ('doctor',)
    inlines = (PhraseInline,)


class PhraseAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'author',)


class EssenseInline(admin.TabularInline):
    model = Essense.comics.through


class ComicsAdmin(admin.ModelAdmin):
    list_display = ('title', 'comics_descr',)
    inlines = (EssenseInline,)
#    exclude = ('participants', )


class EssenseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('comics',)

admin.site.register(Person, PersonAdmin)
admin.site.register(Phrase, PhraseAdmin)
admin.site.register(Comics, ComicsAdmin)
admin.site.register(Essense, EssenseAdmin)