from django.contrib import admin

from .models import Category, Comment, CustomUser, Genre, Review, Title


class TitleInline(admin.StackedInline):
    model = Title
    extra = 0


class TitleInlineGenre(admin.TabularInline):
    model = Genre.titles.through
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        TitleInline,
    )
    list_display = (
        'name', 'slug'
    )


@admin.register(Genre)
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


@admin.register(Title)
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


class CommentInLine(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'author', 'title', 'score', 'pub_date'
    )
    inlines = (CommentInLine, )
    list_filter = ('score', 'title')
    search_fields = ('text', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'author', 'review', 'pub_date'
    )
    list_filter = ('review', )
    search_fields = ('text', )


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'role'
    )
