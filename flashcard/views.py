
from django.shortcuts import render, redirect, get_object_or_404,  HttpResponseRedirect
from .form import WordFormset, SetForm, WordForm
from django.views.generic import ListView 

from .models import Word, StudySet
from django.contrib import  messages

from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home_view(request): 
    return  render(request, 'base.html')


@login_required
def flash_card_home_view(request): 
    return render(request, 'flashcard/home_view.html')



# class StudySetInline(): 

#     form_class = SetForm
#     model = StudySet
#     template_name = "flashcard/studyset_form.html"

#     def form_valid(self, form): 
#         named_formsets = self.get_named_formsets()

#         if not all((x.is_valid() for x in named_formsets.values())): 
#             return self.render_to_response(self.get_context_data(form=form))
        
#         self.object = form.save()

#         for name, formset in named_formsets.items(): 
#             formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)

#             if formset_save_func is not None: 
#                 formset_save_func(formset)
#             else: 
#                 formset.save()

#         return redirect('flashcard:list_studyset')
    
#     def formset_word_valid(self, formset): 

#         words = formset.save(commit  = False)

#         for obj in formset.deleted_objects: 
#             obj.delete()
        
#         for word in words: 
#             word.studyset = self.object
#             word.save()


# class StudySetCreate(StudySetInline, CreateView): 

#     def get_context_data(self, **kwargs):
#         ctd =  super(StudySetCreate, self).get_context_data(**kwargs)
#         ctd['named_formsets'] = self.get_named_formsets()
#         return ctd 

#     def get_named_formsets(self): 
#         if self.request.method == "GET":
#             return {
#                 'words': WordFormset(prefix = "words"),
#             }
        
#         else : 
#             return {
#                 'words': WordFormset(self.request.POST or None, self.request.FILES or None, prefix = "words"), 
#             }

# class StudySetUpdate(StudySetInline, UpdateView):

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         ctd =  super(StudySetUpdate, self).get_context_data(**kwargs)
#         ctd['named_formsets'] = self.get_named_formsets()

#         return ctd

#     def get_named_formsets(self): 

#         return {
#             'words' : WordFormset(self.request.POST or None, self.request.FILES or None, instance = self.object, prefix = "words")
#         }




@login_required
def delete_word(request, form_id, word_id):
    '''Hàm view thực hiện xóa word trong form - sử dụng button'''
    word = get_object_or_404(Word, id=word_id)

    if request.method == 'POST': 
        word.delete()
        return redirect('flashcard:update_studyset', id=form_id)
    else : 
        return JsonResponse({'status': 'error'}, status = 400)
    


@login_required
def delete_studyset(request, id): 
    '''Hàm xóa studyset tại node delete của list_studyset'''
    studyset = get_object_or_404(StudySet, pk=id)

    if request.method == "POST": 
        studyset.delete()

        return HttpResponseRedirect('/flashcard/studysets')
    
    return redirect('flashcard:studysets')



@login_required
def new_studyset(request): 
    '''Hàm tạo studyset mới'''
    if request.method == 'POST':
            form = SetForm(request.POST)
            if form.is_valid():
                studyset = form.save(commit=False)

                studyset.user = request.user 

                studyset.save()
                if 'save' in request.POST:
                    # Nếu người dùng nhấn nút "Save"
                    return redirect('flashcard:studysets')
                elif 'saveandadd' in request.POST:
                    # Nếu người dùng nhấn nút "Save and Add Card"
                    # Chuyển hướng đến URL với ID của studyset vừa được tạo
                    return redirect(reverse('flashcard:new_word', args=[studyset.id]))
    else:
        form = SetForm()

    return render(request, 'flashcard/new_studyset.html', {'form': form})

@login_required
def new_word(request, id): 
    '''Tạo formset mới'''
    try :  
        studyset = StudySet.objects.get(id = id)

    except StudySet.DoesNotExist: 
        return redirect('flashcard:studysets')
    

    if request.method != "POST": 
        formset = WordFormset(instance = studyset)

    else : 
        formset = WordFormset(data = request.POST, instance = studyset)

        if formset.is_valid(): 

            formset.save()

        return redirect('flashcard:studysets')

    context = {'formset': formset}

    return render(request, 'flashcard/new_word.html', context = context)


@login_required
def update_studyset(request,  id): 
    '''Hàm update thông tin của formset '''
    studyset = get_object_or_404(StudySet, id=id)
    form = SetForm(instance= studyset)
    
    words = Word.objects.all( ).filter (studyset = id)

    if request.method == "POST": 
        form = SetForm(data = request.POST, instance = studyset)
       
        if form.is_valid() :


            form.save()
            if 'save' in request.POST: 
                return redirect('flashcard:studysets')
            elif 'addmore' in request.POST: 
                return redirect('flashcard:new_word', id=id)

    return render(request, 'flashcard/edit_studyset.html', {'form': form, 'words': words})

@login_required
def edit_word(request, form_id, word_id): 

    word = get_object_or_404(Word, id = word_id )
    form = WordForm(instance=word)

    if request.method == "POST" :  
        form = WordForm(instance=word , data=request.POST)

        if form.is_valid(): 
            form.save()

            return redirect('flashcard:update_studyset', id=form_id)

    return render(request, 'flashcard/edit_word.html', {'form': form, 'word': word, 'form_id': form_id})



@login_required 
def studysets(request): 

    studysets = StudySet.objects.filter(user= request.user)

    context = {'studysets': studysets}


    return render(request, 'flashcard/studysets.html', context)


@login_required
def learn(request, id):

    studysets = get_object_or_404(StudySet, id = id)
    words = Word.objects.all().filter(studyset = id)

    current_indx = int(request.GET.get("index", 0))

    next_indx = (current_indx + 1) % len(words)

    prev_indx = (current_indx - 1) % len(words)
    
    word_num =  len(words)
    context = {
        "studysets" : studysets, 
        "curr_word" : words[current_indx],
        "next_indx" : next_indx,
        "prev_indx" : prev_indx, 
        "word_num" : word_num, 
        "curr_indx" : current_indx
    }

    return render(request, 'flashcard/learn.html', context) 




    