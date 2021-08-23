import io
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
from main.models import Note, Text, Fav, NoteLog
from main.forms import NoteForm, TextForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm


class NoteSearch(ListView):
    template_name = 'main/search.html'
    context_object_name = 'note_search'
    queryset = Note.objects.order_by('-id')
    model = Note
    paginate_by = 10

    def get_queryset(self):
        queryset = Note.objects.order_by('-id')
        query = self.request.GET.get('query')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
            )
        return queryset


def index(request):
    if request.user.is_authenticated:
        data = {
            'fav_notes': Fav.objects.filter(user=request.user).order_by('-created_at')[:5],
            'fav_all': len(Fav.objects.filter(user=request.user)),
            'logs': NoteLog.objects.filter(user=request.user).order_by('-created_at')[:5],
        }
        return render(request, 'main/dashboard.html', data)
    else:
        return render(request, 'main/index.html')


@login_required
def favorite(request):
    data = {
        'favs': Fav.objects.filter(user=request.user).order_by('-created_at')
    }
    return render(request, 'main/favorite.html', data)


@login_required
def history(request):
    data = {
        'logs': NoteLog.objects.filter(user=request.user).order_by('-created_at')[:100]
    }
    return render(request, 'main/history.html', data)


@method_decorator(login_required(), name='dispatch')
class MyNoteListView(ListView):
    template_name = 'main/mynote.html'

    def get_queryset(self):
        current_user = self.request.user
        return Note.objects.filter(user=current_user).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note_form'] = NoteForm
        return context

    def post(self, request):
        form = NoteForm(request.POST)
        if form.is_valid():
            mynote = form.save(commit=False)
            mynote.user = request.user
            mynote.save()
            return JsonResponse({'title': mynote.title, 'note_id': mynote.id, 'user': str(mynote.user)})


def note(request, note_id):
    if request.method == 'POST':
        if request.POST.get('name') == "add_text":
            form = TextForm(request.POST)
            index = request.POST.get('index')
            if form.is_valid:
                text = form.save(commit=False)
                words = text.sentence.replace('　', ' ').replace('/', '')
                text.words = words.replace(',', '/').split(' ')
                text.if_hide = ['N'] * len(text.words)
                text.note = get_object_or_404(Note, pk=note_id)
                if Text.objects.filter(note=text.note).exists():
                    if index == "first":
                        for t in Text.objects.filter(note=text.note):
                            t.order += 1
                            t.save()
                        text.order = 0
                    else:
                        text.order = Text.objects.filter(note=text.note).order_by('order').last().order + 1
                else:
                    text.order = 0
                text.save()
                data = {
                    'ajaxed_id': text.id,
                    'sentence': text.sentence,
                    'translation': text.translation,
                    'words': words.split(' '),
                }
                return JsonResponse(data)
        elif request.POST.get('name') == "add_check":
            hides = request.POST.getlist('checks[]')
            hides = ["Y" if h == "true" else "N" for h in hides]
            text = get_object_or_404(Text, id=request.POST.get('text_id'))
            text.if_hide = hides
            text.save()
            data = {
                "text_id": text.id,
                "hides": hides,
                "words": text.words,
                "translation": text.translation,
            }
            return JsonResponse(data)
        elif request.POST.get('name') == "name_form":
            title = request.POST.get("title")
            n = get_object_or_404(Note, id=note_id)
            n.title = title
            n.save()
            data = {
                "title": n.title
            }

            return JsonResponse(data)

    else:
        n = get_object_or_404(Note, pk=note_id)
        i = 0
        texts = Text.objects.filter(note=n).order_by('order', '-id')
        for text in texts:
            text.order = i
            text.save()
            i += 1
        if request.user.is_authenticated:
            if NoteLog.objects.filter(user=request.user, note=n).exists():
                # if NoteLog.objects.filter(user=request.user, note=n).latest("created_at").note != n:
                NoteLog.objects.filter(user=request.user, note=n).delete()
                NoteLog.objects.create(note=n, user=request.user)
            else:
                NoteLog.objects.create(note=n, user=request.user)
            if_fav = Fav.objects.filter(note=n, user=request.user).exists()
        else:
            if_fav = None
        word_count = 0
        for text in texts:
            word_count += len(text.words)
        data = {
            'id': note_id,
            'note': n,
            'texts': texts,
            'form': TextForm,
            'word_count': word_count,
            'if_fav': if_fav
        }
        return render(request, 'main/note.html', data)


@login_required
def ordering(request, note_id):
    if request.method == 'POST':
        n = get_object_or_404(Note, id=note_id)
        texts = Text.objects.filter(note=n).order_by('order', '-id')
        orders = request.POST.getlist('all_order[]')
        ids = request.POST.getlist('all_id[]')
        for i in range(len(texts)):
            text = get_object_or_404(texts, id=ids[i])
            text.order = i
            text.save()

        return JsonResponse({"Response is": "OK"})
    else:
        return Http404


def PDFView(request, note_id):
    if Note.objects.filter(id=note_id).exists():
        n = Note.objects.get(pk=note_id)
        texts = Text.objects.filter(note=n).order_by('order', '-id')
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setTitle(n.title + ".pdf")
        font_name = 'HeiseiKakuGo-W5'
        pdfmetrics.registerFont(UnicodeCIDFont(font_name))

        w, h = A4
        p.setFont(font_name, 18)
        p.drawCentredString(w / 2, 280 * mm, n.title)
        p.setFont(font_name, 10)
        p.drawCentredString(w / 2, 276 * mm, "author: " + str(n.user))
        p.drawRightString(w / 2 - 80, 765, "氏名")
        p.line(w / 2 - 75, 765, w / 2 + 75, 765)
        pos = 700
        i = 1
        for text in texts:
            s = ""
            for j in range(len(text.words)):
                word = text.words[j]
                if text.if_hide[j] == 'Y':
                    s += "(    )"
                    if word[0] in ['"', "'"] and len(word) > 2:
                        s = word[0] + s
                    if word[-1] in ['.', '/', ',', '!', '?', '"', "'"]:
                        s += word[-1].replace('/', ',')
                    if len(word) >= 2:
                        if word[-2] in ['.', '/', ',', '!', '?', '"', "'"]:
                            s += word[-2].replace('/', ',')
                else:
                    s += word.replace('/', ',')
                s += " "
            p.drawString(25, pos, str(i) + ".")
            p.drawString(25, pos-20, s)
            p.drawString(25, pos-40, text.translation)
            p.line(25, pos-65, w-25, pos-65)
            pos -= 90
            i += 1

            if pos < 90:
                p.showPage()
                p.setFont(font_name, 10)
                pos = 800

        p.showPage()
        p.setFont(font_name, 18)
        p.drawCentredString(w / 2, 280 * mm, "答え")
        pos = 750
        p.setFont(font_name, 10)
        i = 1
        for text in texts:
            s = ""
            for k in range(len(text.words)):
                if text.if_hide[k] == 'Y':
                    w = text.words[k].replace('/', ',')
                    if w[0] in ['"', "'"]:
                        w = w[1:]
                    if len(w) != 0:
                        if w[-1] in ['.', '/', ',', '!', '?', '"', "'"]:
                            w = w[:-1]
                            if len(w) != 0:
                                if w[-1] in ['.', '/', ',', '!', '?', '"', "'"]:
                                    w = w[:-1]
                    s += w + ' / '
            if len(s) != 0:
                s = s[:-3]
            p.drawString(25, pos, str(i) + '. ' + s)
            pos -= 20
            i += 1
            if pos < 40:
                p.showPage()
                p.setFont(font_name, 10)
                pos = 800
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=False, filename=n.title + ".pdf")
    else:
        return Http404


@login_required
def delete_note(request, note_id):
    n = get_object_or_404(Note, id=note_id)
    if n.user == request.user:
        n.delete()
    return redirect('main:mynote')


@login_required
def delete_text(request, text_id):
    t = get_object_or_404(Text, id=text_id)
    n = t.note
    if n.user == request.user:
        t.delete()
    return redirect('main:note', n.id)


@login_required
def fav_note(request, note_id):
    if request.method == "POST":
        if Note.objects.filter(id=note_id).exists():
            n = get_object_or_404(Note, id=note_id)
            if request.POST.get('status') == 'true':
                Fav.objects.filter(note=n, user=request.user).delete()
            else:
                Fav.objects.create(note=n, user=request.user)
            data = {
                "test": "complited!",
            }
            return JsonResponse(data)
        return Http404
    else:
        return Http404


@login_required
def delete_log(request):
    NoteLog.objects.filter(user=request.user).delete()
    return redirect(request.META['HTTP_REFERER'])



