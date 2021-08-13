import io
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from main.models import Note, Text, Fav
from main.forms import NoteForm, TextForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm


def index(request):
    # data = {
    #     'random_note':
    # }
    if request.user.is_authenticated:
        return render(request, 'main/dashboard.html')
    else:
        return render(request, 'main/index.html')


# @login_required()
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
        # print(request.POST.get('name'))
        # print(request.POST)
        if request.POST.get('name') == "add_text":
            form = TextForm(request.POST)
            if form.is_valid:
                text = form.save(commit=False)
                words = text.sentence.replace('　', ' ').replace('/', '')
                text.words = words.replace(',', '/').split(' ')
                text.if_hide = ['N'] * len(text.words)
                text.note = get_object_or_404(Note, pk=note_id)
                text.save()
                data = {
                    'ajaxed_id': text.id,
                    'sentence': text.sentence,
                    'translation': text.translation,
                    'words': words.split(' '),
                }
                return JsonResponse(data)
        # elif request.POST.get('name') == "add_check":
        elif request.POST.get('name') == "add_check":
            hides = request.POST.getlist('checks[]')
            hides = ["Y" if h == "true" else "N" for h in hides]
            text = get_object_or_404(Text, id=request.POST.get('text_id'))
            text.if_hide = hides
            text.save()
            # print(request.POST.get('text_id'))
            # print(hides)
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
        texts = Text.objects.filter(note=n).order_by('-id')
        if_fav = Fav.objects.filter(user=request.user, note_id=note_id).exists()
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


def PDFView(request, note_id):
    if Note.objects.filter(id=note_id).exists():
        n = Note.objects.get(pk=note_id)
        texts = Text.objects.filter(note=n).order_by('-id')
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
                if text.if_hide[j] == 'Y':
                    s += "(    )"
                    if text.words[j][-1] in ['.', '/', ',', '!', '?']:
                        s += text.words[j][-1].replace('/', ',')
                else:
                    s += text.words[j].replace('/', ',')
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
                    s += text.words[k].replace('/', ',') + " / "
            p.drawString(25, pos, str(i) + '.' + s)
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


def delete_note(request, note_id):
    n = get_object_or_404(Note, id=note_id)
    if n.user == request.user:
        n.delete()
    return redirect('main:mynote')


def delete_text(request, text_id):
    t = get_object_or_404(Text, id=text_id)
    n = t.note
    if n.user == request.user:
        t.delete()
    return redirect('main:note', n.id)
