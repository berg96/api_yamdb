from django.contrib import admin

from .models import Category, Genre, Title, Review, Comments, CustomUser


class TitleInline(admin.StackedInline):
    model = Title
    extra = 0


class TitleInlineGenre(admin.TabularInline):
    model = Genre.titles.through
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        TitleInline,
    )
    list_display = (
        'name', 'slug'
    )


class GenreAdmin(admin.ModelAdmin):
    inlines = (
        TitleInlineGenre,
    )
    list_display = (
        'name', 'slug'
    )


class ReviewInLine(admin.StackedInline):
    model = Review
    extra = 0


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'year', 'category', 'display_genres', 'description'
    )
    inlines = (ReviewInLine, )
    filter_horizontal = ('genre',)
    list_filter = ('genre', 'category', 'year')
    list_editable = ('category', )
    search_fields = ('name', )

    def display_genres(self, obj):
        """Функция для отображения жанров в list_display."""
        return ", ".join([genre.name for genre in obj.genre.all()])

    display_genres.short_description = 'Жанр'


class CommentsInLine(admin.StackedInline):
    model = Comments
    extra = 0


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'author', 'title', 'score', 'pub_date'
    )
    inlines = (CommentsInLine, )
    list_filter = ('score', 'title')
    search_fields = ('text', )


class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'author', 'review', 'pub_date'
    )
    list_filter = ('review', )
    search_fields = ('text', )


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'role'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
