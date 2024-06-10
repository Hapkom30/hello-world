from django.core.management.base import BaseCommand, CommandError
from NewsLents2.models import Post, Category


class Command(BaseCommand):
    help = 'Обнуляет количество всех товаров'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')

        if answer == 'yes':
            try:
                category = Category.objects.get(category=options['category'])
                Post.objects.filter(category=category).delete()
                self.stdout.write(self.style.SUCCESS(f'Successffuly delete all news from category {category.category}'))
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category {options['category']}'))
        else:
            return

