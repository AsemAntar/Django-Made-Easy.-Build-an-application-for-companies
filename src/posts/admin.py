from django.contrib import admin

from .models import ProblemPost, GeneralPost


class ProblemPostAdmin(admin.ModelAdmin):
    list_display = [
        '__str__', 'author', 'num_likes', 'created'
    ]
    fields = ('author', 'report', 'problem_reported', )
    list_display_links = ('__str__', 'author', )
    list_filter = ('created', )
    search_fields = ('author__user__username', )

    class Meta:
        model = GeneralPost


class GeneralPostAdmin(admin.ModelAdmin):
    list_display = [
        '__str__', 'author', 'num_likes', 'created'
    ]
    exclude = ('liked',)

    class Meta:
        model = GeneralPost


admin.site.register(GeneralPost, GeneralPostAdmin)
admin.site.register(ProblemPost, ProblemPostAdmin)
