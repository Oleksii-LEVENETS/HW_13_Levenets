
from aggregation.forms import ReminderForm
from aggregation.models import Author, Book, Publisher, Store
from aggregation.forms import ContactForm

from aggregation.tasks import tasks
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Avg, Count
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView


# Create your views here.
def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_authors = Author.objects.count()
    num_publishers = Publisher.objects.count()
    num_books = Book.objects.count()
    num_stores = Store.objects.count()

    context = {
        'num_authors': num_authors,
        'num_publishers': num_publishers,
        'num_books': num_books,
        'num_stores': num_stores,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# List Views
class AuthorListView(generic.ListView):
    model = Author
    template_name = "aggregation/author_list.html"
    # paginate_by = 10
    queryset = Author.objects.annotate(num=Count("book__id"))
    context_object_name = "authors_books"

    def get_queryset(self):
        return super().get_queryset().order_by('name')


class PublisherListView(generic.ListView):
    model = Publisher
    template_name = "aggregation/publisher_list.html"
    # paginate_by = 10
    queryset = Publisher.objects.annotate(num=Count("book__id"))
    context_object_name = "publishers_books"

    def get_queryset(self):
        return super().get_queryset().order_by('name')


class BookListView(generic.ListView):
    template_name = "aggregation/book_list.html"
    model = Book
    paginate_by = 20
    context_object_name = "books"
    
    def get_queryset(self):
        return Book.objects.select_related("publisher").order_by('name')


class StoreListView(generic.ListView):
    model = Store
    template_name = "aggregation/store_list.html"
    # paginate_by = 10
    queryset = Store.objects.annotate(num=Count("books__id"))
    context_object_name = "stores_books"

    def get_queryset(self):
        return super().get_queryset().order_by('name')


# Detail Views
class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "aggregation/author_detail.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        book_author = Book.objects.filter(authors__id=self.object.id).annotate(num=Count("id"))
        context['author_books'] = book_author

        # Экономия одного запроса -- стоит ли len?
        context['written_total'] = len(book_author)
        # context['written_total'] = book_author.count()

        # Здесь prefetch_related("authors") экономии не дает, его можно убрать?
        context['author_avg_rating'] = round(Book.objects.prefetch_related("authors").filter(
                                authors=self.object.id).aggregate(a=Avg("rating"))["a"], 2)
        # context['author_avg_rating'] = round(Book.objects.filter(
        #     authors=self.object.id).aggregate(a=Avg("rating"))["a"], 2)
        return context


class PublisherDetailView(generic.DetailView):
    model = Publisher
    template_name = "aggregation/publisher_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PublisherDetailView, self).get_context_data(**kwargs)
        context['published_total'] = Book.objects.filter(publisher=self.object.id).count()
        context['publisher_books'] = Book.objects.filter(publisher=self.object.id)
        context['publisher_avg_rating'] = round(Book.objects.filter(
                                publisher=self.object.id).aggregate(a=Avg("rating"))["a"], 2)
        return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "aggregation/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['available_stores'] = Store.objects.filter(books=self.object.id)
        context['books_authors'] = Author.objects.filter(book=self.object.id)

        return context


class StoreDetailView(generic.DetailView):
    model = Store
    template_name = "aggregation/store_detail.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(StoreDetailView, self).get_context_data(**kwargs)
        context['store_books'] = Book.objects.filter(store=self.object.id)
        context['selling_total'] = Book.objects.filter(store=self.object.id).count()
        return context


def reminder_form(request):
    now = timezone.now()
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            reminder_text = form.cleaned_data.get("reminder_text")
            date_time = form.cleaned_data.get("date_time")
            tasks.reminder_task.apply_async(kwargs={"email": email, "reminder_text": reminder_text},
                                            eta=date_time)
            return redirect(reverse("aggregation:index"))
    else:
        form = ReminderForm(initial={"email": "example@dj.com", "date_time": now, "reminder_text": "Reminder"})
    return render(request, "aggregation/reminder_form.html", {"form": form})


# HW-16 =====================================================
class BookCreateView(LoginRequiredMixin, CreateView):
    raise_exception = True
    template_name = "aggregation/book_create.html"
    now = datetime.now()
    model = Book
    fields = ['name', 'pages', 'price', 'rating', 'authors', 'publisher', 'pubdate']
    initial = {'name': "book name", 'pages': 123, 'price': 9.99, 'rating': 10, 'pubdate': now}
    success_url = reverse_lazy("aggregation:book-list")


class BookUpdateView(LoginRequiredMixin, UpdateView):
    raise_exception = True
    template_name = "aggregation/book_update.html"
    model = Book
    fields = ['name', 'pages', 'price', 'rating', 'authors', 'publisher', 'pubdate']
    success_url = reverse_lazy("aggregation:book-list")


class BookDeleteView(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Book
    template_name = "aggregation/book_confirm_delete.html"
    success_url = reverse_lazy("aggregation:book-list")
    

class ContactFormView(FormView):
    template_name = 'aggregation/contact_form.html'
    initial = {'first_name': "User", "last_name": "Userenko", "email_address": "uu@example.com"}
    form_class = ContactForm
    success_url = reverse_lazy('aggregation:contact-form-thanks')
    
    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ContactTemplateView(generic.TemplateView):
    template_name = 'aggregation/contact_form_thanks.html'
