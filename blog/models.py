from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]


class BlogPage(Page):

    # Database fields
    intro = models.TextField(help_text="Text to describe the page")
    body = RichTextField()
    date_created = models.DateField("Post date")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date_created'),
    ]


    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('date_created'),
        FieldPanel('body'),
        FieldPanel('image'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('image'),
    ]

    parent_page_types = ['blog.BlogIndexPage']
