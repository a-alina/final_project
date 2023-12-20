from calendar import prmonth
from django.shortcuts import render, redirect
import openai
from django.contrib import messages
from django.http import JsonResponse
from django.template import loader, Context
from django.template.loader import render_to_string
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA 
from django.views.decorators.csrf import csrf_exempt
from .forms import DocumnetForm, RegistrationForm
from django.urls import reverse
from .models import Document, Quiz
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def main(request):
    return render(request, 'rakendus/main.html')

@login_required(login_url='/login/')
def choose_file(request):
    documents = Document.objects.filter(author=request.user)
    names = [documnent.name for documnent in documents]
    if request.method == 'POST':
        if "upload" in request.POST:
            form = DocumnetForm(request.POST, request.FILES)
            
            
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
            return redirect('choose_file')
        else:
            doc_name = request.POST.get("selected_document")
            pdf = Document.objects.get(name=doc_name).pdf

            #generating quiz
            q_number = 6
            openai_api_key = ""

            pdf_reader = PdfReader(pdf)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # spliting text into chunks
            splitter = CharacterTextSplitter(
                separator='\n', 
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
                )
            chunks = splitter.split_text(text)

            # converting chunks into embeddings
            embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            document = FAISS.from_texts(chunks, embeddings)
            document_main = document

            counter = Quiz.objects.filter(quiz_name=doc_name).count()
                
            if counter == 0:
                attempt_number =  1
            else:
                attempt_number = counter//q_number + 1

            questions = ""
            for i in range(0, q_number):
                task = "generate a question based on text diffrent from " + questions
                retriver = document_main.as_retriever(search_kwargs={"k": 5})
                llm = OpenAI(openai_api_key=openai_api_key)
                qa = RetrievalQA.from_chain_type(llm=llm, 
                        retriever=retriver,
                        chain_type="stuff")
                
                questions += f", "

                question = qa.run(query=task)
                snd_taks = f"answer {question}"
                retriver = document_main.as_retriever(search_kwargs={"k": 5})
                llm = OpenAI(openai_api_key=openai_api_key)
                qa = RetrievalQA.from_chain_type(llm=llm, 
                        retriever=retriver,
                        chain_type="stuff")
                ai_answer = qa.run(query=snd_taks)
                            
                quiz = Quiz(quiz_name=doc_name, question=question, 
                            correct_answer= ai_answer, attempt_number=attempt_number)
                quiz.author = request.user
                quiz.save()

            return redirect("quiz", param1=doc_name, param2=attempt_number)

    else:
        form = DocumnetForm()
        

    return render(request, 'rakendus/choose_file.html', {'form': form, "names": names})

@login_required(login_url='/login/')
def quiz(request, param1, param2):
    quiz = Quiz.objects.filter(quiz_name=param1, attempt_number=param2)

    if request.method == "POST":
        for key, value in request.POST.items():
            Quiz.objects.filter(question=key).update(user_answer=value)
            print(key, value)
        return redirect("test", param1=param1, param2=param2)

    return render(request, 'rakendus/quiz.html', {"quiz": quiz,
                                         "quiz_name": param1,
                                         "attempt_number": param2})

@login_required(login_url='/login/')
def test(request, param1, param2):
    results = Quiz.objects.filter(quiz_name=param1, attempt_number=param2)
    all_questions = [quiz.question for quiz in results]


    if request.method == "POST":
        true_questions = [key for key, value in request.POST.items()]
        for i in all_questions:
            if i in true_questions:
                Quiz.objects.filter(question=i).update(correct=True)
            else:
                Quiz.objects.filter(question=i).update(correct=False)

        return redirect("list_of_quizes")
    
    return render(request, 'rakendus/test.html',
                  {"results": results,
                   "quiz_name": param1,
                    "attempt_number": param2})

    
@login_required(login_url='/login/')
def list_of_quizes(request):
    quizes = Quiz.objects.values('quiz_name', 'attempt_number').distinct()
    
    
    content = {}

    for i, quiz in enumerate(quizes):
        true_values = Quiz.objects.filter(quiz_name=quiz["quiz_name"], 
                            attempt_number=quiz["attempt_number"], 
                            correct=True).count()
        all_values = Quiz.objects.filter(quiz_name=quiz["quiz_name"], 
                            attempt_number=quiz["attempt_number"]).count()
        print(true_values)
        if true_values == 0:
            score = 0
        else:
            score = round(true_values/all_values*100)
        
        content[i] = {"quiz_name": quiz["quiz_name"],
                                "attempt_number":quiz["attempt_number"],
                                "score":score}
   
    if request.method == "POST":
        delete_value = request.POST.get('delete_button')
        quiz_name, attempt_number = delete_value.split('|')
        quizzes_to_delete = Quiz.objects.filter(quiz_name=quiz_name, attempt_number=attempt_number)
        quizzes_to_delete.delete()
        return redirect("list_of_quizes")

    return render(request, 'rakendus/list_of_quizes.html', 
                  {"content": content})
    
@login_required(login_url='/login/')
def files(request):
    content = Document.objects.all()
    print(content)

    if request.method == "POST":
        delete_value = request.POST.get('delete_button')
        quizzes_to_delete = Document.objects.filter(name=delete_value, author=request.user)
        quizzes_to_delete.delete()


    return render(request, 'rakendus/files.html', 
                  {"content": content})


def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/choose_file")
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {'form': form})
