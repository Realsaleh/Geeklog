from django.contrib import admin, messages
from .models import Post, Category, IPAddress
from django.utils.translation import ngettext


#Post Actions
def make_published(modeladmin, request, queryset):
	updated = queryset.update(status='p')
	modeladmin.message_user(request, ngettext(
		'%d پست منتشر شد.',
		'%d پست منتشر شدند.',
		updated,
	 ) % updated, messages.SUCCESS)
make_published.short_description = "منتشر کردن"

def make_draft(modeladmin, request, queryset):
	updated = queryset.update(status='d')
	modeladmin.message_user(request, ngettext(
		'%d پست پیش نویس شد.',
		'%d پست پیش نویس شدند.',
		updated,
	 ) % updated, messages.SUCCESS)
make_draft.short_description = "پیش نویس کردن"

#Category Actions
def make_cat_active(modeladmin, request, queryset):
	updated = queryset.update(status=True)
	modeladmin.message_user(request, ngettext(
		'%d دسته بندی فعال شد.',
		'%d دسته بندی فعال شدند.',
		updated,
	 ) % updated, messages.SUCCESS)
make_cat_active.short_description = "فعال کردن"

def make_cat_inactive(modeladmin, request, queryset):
	updated = queryset.update(status=False)
	modeladmin.message_user(request, ngettext(
		'%d دسته بندی غیرفعال شد.',
		'%d دسته بندی غیرفعال شدند.',
		updated,
	 ) % updated, messages.SUCCESS)
make_cat_inactive.short_description = "غیرفعال کردن"



class CategoryAdmin(admin.ModelAdmin):
	list_display = ('position', 'title', 'slug', 'parent', 'status')
	list_filter = (['status'])
	search_fields = ('title', 'slug')
	prepopulated_fields = {'slug': ('title',)}
	actions = [make_cat_active, make_cat_inactive]

admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'thumbnail_tag', 'slug', 'author', 'jpublish', 'category_to_str', 'is_special', 'status')
	list_filter = ('publish', 'status', 'author')
	search_fields = ('title', 'content')
	prepopulated_fields = {'slug': ('title',)}
	ordering = ['-status', '-publish']
	actions = [make_published, make_draft]

admin.site.register(Post, PostAdmin)

admin.site.register(IPAddress)
