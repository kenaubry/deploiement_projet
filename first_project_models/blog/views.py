from datetime import date
from django.shortcuts import redirect, render
from .models import Post
all_posts = [
    {
        "slug": "pourquoi-python",
        "image": "pythonlogo.png",
        "author": "FormationDjango",
        "date": date(2021, 7, 21),
        "title": "Pourquoi Python ?",
        "excerpt": "Rien de mieux que le langage Python pour coder ! Adaptatif et simple à apprendre",
        "content": """
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
        """
    },
    {
        "slug": "programmer-cest-cool",
        "image": "coding.jpg",
        "author": "FormationDjango",
        "date": date(2022, 3, 10),
        "title": "Programmer c'est cool !",
        "excerpt": "Vous avez deja passé des heures à chercher une erreur dans votre code ? C'est ce qu'il m'est arrivé hier...",
        "content": """
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
        """
    },
    {
        "slug": "quartier-picpus",
        "image": "picpus.jpeg",
        "author": "FormationDjango",
        "date": date(2020, 8, 5),
        "title": "Quartier Picpus",
        "excerpt": "Le quartier de Picpus est le 46e quartier administratif de Paris situé dans le 12 arrondissement.",
        "content": """
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.

          Lorem ipsum dolor sit amet consectetur adipisicing elit. Officiis nobis
          aperiam est praesentium, quos iste consequuntur omnis exercitationem quam
          velit labore vero culpa ad mollitia? Quis architecto ipsam nemo. Odio.
        """
    }
]

def get_date(post):
  return post['date']

# Create your views here.

def starting_page(request):
    sorted_posts = Post.objects.order_by("-date")[:3] # tri par date et récupère 3
    return render(request, "blog/index.html", {
        "posts": sorted_posts
    })

def posts(request):
    all_posts = Post.objects.all()
    return render(request, "blog/all-posts.html", {
        "all_posts": all_posts
    })

from .forms import CommentForm

def post_detail(request, slug):
    identified_post = Post.objects.get(slug=slug)
    comments = identified_post.commentaires.order_by("-date") 
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # recupere un objet sans 
            comment.post = identified_post
            comment.save()
            return redirect("post-detail-page", slug=slug)
    else:
        form = CommentForm()

    return render(request, "blog/post-detail.html", {
        "post": identified_post,
        "form": form,
        "comments": comments
    })

from .models import Comment

'''
from django.views.generic import DetailView
from .models import Post
from .forms import CommentForm
from django.views.generic import ListView
from django.shortcuts import reverse
'''
# StartingPageView
'''
class StartingPageView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    queryset = Post.objects.order_by("-date")[:3]

# PostsView
class PostsView(ListView):
    model = Post
    template_name = "blog/all-posts.html"
    context_object_name = "all_posts"
    queryset = Post.objects.all()

# PostDetailView

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post-detail.html"
    context_object_name = "post"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.order_by("-date")
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail-page", kwargs={"slug": self.object.slug})
    
# EXPLICATIONS DETAILLÉES DES CLASS VIEWS


# Importation des classes DetailView et ListView depuis le module django.views.generic
from django.views.generic import DetailView, ListView

# Importation de la classe Post depuis le module .models
from .models import Post

# Importation de la classe CommentForm depuis le module .forms
from .forms import CommentForm

# Importation de la fonction reverse depuis le module django.shortcuts
from django.shortcuts import reverse


# Définition de la classe StartingPageView qui hérite de la classe ListView
class StartingPageView(ListView):
    # Spécification du modèle utilisé par la vue
    model = Post

    # Spécification du nom du template utilisé par la vue
    template_name = "blog/index.html"

    # Spécification du nom de la variable de contexte utilisée pour passer les objets à afficher dans le template
    context_object_name = "posts"

    # Spécification de la requête utilisée pour récupérer les objets à afficher dans la vue
    queryset = Post.objects.order_by("-date")[:3]


# Définition de la classe PostsView qui hérite de la classe ListView
class PostsView(ListView):
    # Spécification du modèle utilisé par la vue
    model = Post

    # Spécification du nom du template utilisé par la vue
    template_name = "blog/all-posts.html"

    # Spécification du nom de la variable de contexte utilisée pour passer les objets à afficher dans le template
    context_object_name = "all_posts"

    # Spécification de la requête utilisée pour récupérer tous les objets du modèle à afficher dans la vue
    queryset = Post.objects.all()


# Définition de la classe PostDetailView qui hérite de la classe DetailView
class PostDetailView(DetailView):
    # Spécification du modèle utilisé par la vue
    model = Post

    # Spécification du nom du template utilisé par la vue
    template_name = "blog/post-detail.html"

    # Spécification du nom de la variable de contexte utilisée pour passer l'objet à afficher dans le template
    context_object_name = "post"

    # Spécification du nom de l'argument de la requête contenant le slug de l'objet à afficher
    slug_url_kwarg = "slug"

    # Définition d'une méthode pour récupérer les données de contexte supplémentaires à passer au template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.order_by("-date")
        context["form"] = CommentForm()
        return context

    # Définition de la méthode post pour traiter les soumissions de formulaire en POST
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # Définition de la méthode form_valid pour traiter les soumissions de formulaire valides
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        return super().form_valid(form)

    # Définition de la méthode get_success_url pour rediriger l'utilisateur après une soumission de formulaire réussie
    def get_success_url(self):
        return reverse("post-detail-page", kwargs={"slug": self.object.slug
'''