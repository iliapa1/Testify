from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .forms import *
from .models import *
from . import *
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages


class QueryExceptionError(Exception):
	def __init__(self):
		super().__init__("No such object")

def index(request):
    return render(request, 'tests/home.html')

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'tests/home.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })

@login_required
def profile_managment(request):
	return render(request, 'tests/profile_managment.html')

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = UserCreationForm()
	return render(request, 'registration/signup.html', {'form': form})

def search(request):
	if request.method == 'POST':
		searchValue = request.POST.get('search', '')
		testFound = Test.objects.filter(name=searchValue)
		userFound = User.objects.filter(username=searchValue)
		if testFound:
			return render(request, 'tests/searchResults.html', {'resultTest' : testFound})
		
		elif userFound:	
			return render(request, 'tests/searchResults.html', {'resultUser' : userFound[0]})
		
		elif userFound and testFound:
			return render(request, 'tests/searchResults.html', {'resultTest' : testFound, 'resultUser' : userFound[0]})
		
		else:
			print('shit')
			return render(request, 'tests/searchResults.html')

def inbox(request):
	userReciever = request.POST.get('user', '')
	messeges = Messenger.objects.filter(userReciever=userReciever)
	userSenderList = list()
	for i in range(len(messeges)):
		userSenderList.append(messeges[i].userSender)

	counter = list(range(len(messeges)))
	return render(request, 'tests/inbox.html', {'messeges' : messeges, 'userSender' : userSenderList, 'counter' : counter})

def userPage(request):
	if request.method == 'POST':
		user = request.POST.get('user', '')
		return render(request, 'tests/userPage.html', {'userReciever' : user})

def sendingMessege(request):
	userReciever = request.POST.get('userReciever', '')
	return render(request, 'tests/sendingMessege.html', {'userReciever' : userReciever})

def messegeSend(request):
	if request.method == 'POST':
		text = request.POST.get('text', '')
		userSender = request.POST.get('userSender', '')
		userReciever = request.POST.get('userReciever', '')
		messege = Messenger(text=text, userSender=userSender, userReciever=userReciever)
		messege.save()
		return HttpResponse('Messege send')

def sendFriendRequest(request):
	if request.method == 'POST':
		userSender = request.POST.get('userSender', '')
		userReciever = request.POST.get('userReciever', '')
		friendship = Friends(userSender=userSender, userReciever=userReciever, stateOfRequest="pending")
		friendship.save()
	return HttpResponse('Request is send')

def friendRequestAccepted(request):
	pass


def uploadProfilePic(request):
	if request.method == 'POST':
		imageNew = request.POST.get('image', '')
		current_user = request.user
		userDb = UserNew.objects.filter(username=current_user)
		userDb.image = imageNew
		return HttpResponse("done")

@login_required
def solveChooseCategory(request):
	test = Test.objects.all()
	l = list()
	l2 = list(range(int(len(test))))

	for i in l2:
		try:
			if test[i].subject not in l:
				l.append(test[i].subject)
		except Exception:
			return HttpResponse("Wrong input")
	return render(request, 'tests/solveChooseCategory.html', {'subjects' : l})

@login_required
def solveChooseTest(request):
	subjects = request.POST.get('tests', '')
	names = [test.name for test in Test.objects.all().filter(subject=subjects)]
	users = list()
	tests = Test.objects.all().filter(subject=subjects)
	for i in range(len(names)):
		users.append(tests[i].user)
	len1 = len(tests)
	len_list = list(range(len1))
	print(len_list)
	return render(request, 'tests/solveChooseTest.html', {'tests' : tests, 'users' : users, 'len1' : len_list})

def createTest(request):
	return render(request, 'tests/createTest.html')

def addFirstQuestion(request):
	if request.method == 'POST':
		current_user = request.user
		name = request.POST.get('name', '')
		q_num = request.POST.get('q_num', '')
		a_num = request.POST.get('a_num', '')
		subject = request.POST.get('subject', '')
		if Test.objects.filter(name=name):
			alert = "Name already taken!"
			return render(request, 'tests/createTest.html', {"alert" : alert})

		if Test.objects.filter(subject=subject):
			if 'button_no' in request.POST:
				return render(request, 'tests/createTest.html', {'name' : name, 'subject' : subject, "q_num" : q_num, "a_num" : a_num})
			elif 'button_yes' in request.POST:
				q_num = request.POST.get('q_num', '')
				a_num = request.POST.get('a_num', '')
				name = request.POST.get('name', '')
				subject = request.POST.get('subject', '')
				l = list(range(int(a_num)))
				if request.user.is_authenticated():
					test = Test(user=current_user, name=name, subject=subject, a_num=a_num, q_num=q_num)
					test.save()
				return render(request, 'tests/addQuestion.html', {'name' : name, 'q_num' : q_num, 'a_num' : l})
			else:
				return render(request, 'tests/alert.html', {'name' : name, 'subject' : subject, "q_num" : q_num, "a_num" : a_num})

		if not q_num or not a_num or not subject or not name:
			alert = "One or more fields is empty or inccorect"
			return render(request, 'tests/createTest.html', {"names" : name, "alert" : alert})
		l = list(range(int(a_num)))
		if request.user.is_authenticated():
			test = Test(user=current_user, name=name, subject=subject, a_num=a_num, q_num=q_num)
			test.save()
		return render(request, 'tests/addQuestion.html', {'name' : name, 'q_num' : q_num, 'a_num' : l})

def addNextQuestions(request):
	if request.method == 'POST':
		test = Test.objects.get(name=request.POST.get('name', ''))
		question = request.POST.get('question', '')
		answer_r = request.POST.get('answer_r', '')
		q_num = request.POST.get("q_num", '')
		q_num = int(q_num)
		a_num = request.POST.get('a_num', '')
		a_num = list(range(int(len(a_num)/3)))
		if not q_num or not a_num or not answer_r:
			alert = "One or more fields are empty"
			return render(request, 'tests/addQuestion.html', {'name' : request.POST.get('name', ''), 'q_num' : q_num, 'a_num' : a_num, "alert" : alert})

		if int(answer_r) > int(len(a_num)) or int(answer_r) < 1:
			return HttpResponse("You did not select correct answer")
		question_o = Questions(name=test, question=question, answer_r=answer_r)
		question_o.save()

		answers = request.POST.getlist('answer', '')
		for a in answers:
			a = Answers(question=question_o, answer=a)
			a.save()

		if q_num > 1:
			return render(request, 'tests/addQuestion.html', {'q_num' : q_num - 1, 'name' : request.POST.get('name', ''), 'a_num' : a_num})
		else:
			if not request.user.is_authenticated:
				Test.objects.filter(name=request.POST.get('name', '')).delete()
				message = "Your test was created, but was not saved. If you'd like to save a test, please log in"
			else:
				message = "Test successfully created!"
			return render(request, 'tests/doneAdding.html', {"message" : message})

def solveFirstQuestion(request):
	if request.method == 'POST':
		name = request.POST.get('tests', '')
		print(name)
		test = Test.objects.get(name=name)
		questions = Questions.objects.filter(name=test)
		br = 0
		results = 0
		all_wrong = 1
		one_wrong = 0
		wrongs = ''
		len_wrongs = len(wrongs)
		answers = Answers.objects.filter(question=questions[br]).order_by('pk')

		return render(request, 'tests/solveQuestion.html', {'questions' : questions[br].question, 'tests' : name, 'br' : br, 'answers' : answers, 'wrongs' : wrongs, 'results' : results, 'all_wrong' : all_wrong, 'one_wrong' : one_wrong, 'len_wrongs' : len_wrongs})

def solveNextQuestions(request):
	if request.method == 'POST':
		name = request.POST.get('tests', '')
		test = Test.objects.get(name=name)
		questions = Questions.objects.filter(name=test)
		len_wrongs = request.POST.get('len_wrongs', '')
		wrongs = request.POST.get('wrongs', '')
		br = request.POST.get('br', '')
		br = int(br)
		results = request.POST.get('results', '')
		results = int(results)
		all_wrong = request.POST.get('all_wrong', '')
		all_wrong = int(all_wrong)
		one_wrong = request.POST.get('one_wrong', '')
		one_wrong = int(one_wrong)
		current_user = request.user
		q_num = request.POST.get('q_num', '')
		a_num = request.POST.get('a_num', '')

#TO DO: WRONGS IN DATABASE
		if br < len(questions):
			if br == 0:
				br += 1

			answers = Answers.objects.filter(question=questions[br]).order_by('pk')
			if str(questions[br].answer_r) in request.POST:
					results += 1
					all_wrong = 0
			else:
				post_data = request.POST.dict()
				for k, v in post_data.items():
					if k.isdigit():
						mistake = k
				m = Mistakes(user=request.user, name=test, question=questions[br], answer_w=mistake)
				m.save()
				wrongs = wrongs + '  ' + str(br)
				len_wrongs = len(wrongs)
				one_wrong = 1
			return render(request, 'tests/solveQuestion.html', {'questions' : questions[br].question, 'tests' : name, 'br' : br + 1, 'answers' : answers, 'results' : results, "all_wrong" : all_wrong, 'one_wrong' : one_wrong, "wrongs" : wrongs, "len_wrongs" : len_wrongs})

		else:
			if str(questions[br-1].answer_r) in request.POST:
				results += 1
				all_wrong = 0
			else:
				post_data = request.POST.dict()
				for k, v in post_data.items():
					if k.isdigit():
						mistake = k
				m = Mistakes(user=request.user, name=test, question=questions[br-1], answer_w=mistake)
				m.save()
				wrongs = wrongs + ' ' + str(br)
				len_wrongs = len(wrongs)
				one_wrong = 1

			wrongs = wrongs[1:]
			return render(request, 'tests/doneSolving.html', {'tests' : name, 'results' : results, "max" : len(questions), 'wrongs' : wrongs, "all_wrong" : all_wrong, 'one_wrong' : one_wrong})

@permission_required('tests.can_delete', raise_exception=True)
def deleteTests(request):
	if request.method == 'POST':
		name = request.POST.get('tests', '')
		test = Test.objects.get(name=name)
		test.delete()
		message = "Test successfully deleted!"
		return render(request, 'tests/doneDeleting.html', {'message' : message})
	else:
		names = [test.name for test in Test.objects.all()]
		users = list()
		subjects = list()
		tests = Test.objects.all()
		for i in range(len(names)):
			users.append(tests[i].user)
			subjects.append(tests[i].subject)
		len1 = len(tests)
		len_list = list(range(len1))
		return render(request, 'tests/deleteChooseTest.html', {'tests' : tests, 'users' : users, 'subjects' : subjects, 'len1' : len_list})

@login_required
def seeFirstMistake(request):
	if request.method == 'POST':
		name = request.POST.get('tests', '')
		test = Test.objects.get(name=name)
		br = 0
		temp_mistakes = Mistakes.objects.filter(user=request.user)
		temp_mistakes2 = temp_mistakes.filter(name=test)
		questions = [mistakes.question for mistakes in temp_mistakes2]
		answers = Answers.objects.filter(question=questions[br]).order_by('pk')
		answer_w = temp_mistakes2[br].answer_w
		answer_r = questions[br].answer_r
		return render(request, 'tests/seeMistakes.html', {'questions' : questions[br].question, 'answers' : answers, 'tests' : name, 'br' : br + 1, 'answer_w' : int(answer_w), 'answer_r' : int(answer_r)})

@login_required
def seeMistakes(request):
	if request.method == 'POST':
		name = request.POST.get('tests', '')
		test = Test.objects.get(name=name)
		br = request.POST.get('br', '')
		br = int(br)
		temp_mistakes = Mistakes.objects.filter(user=request.user)
		temp_mistakes2 = temp_mistakes.filter(name=test)
		print(len(temp_mistakes))
		questions = [mistakes.question for mistakes in temp_mistakes2]
		print("br: " + str(br))
		print(len(questions))
		if br < len(questions):
			if br==0:
				br+=1

			answers = Answers.objects.filter(question=questions[br]).order_by('pk')
			answer_w = temp_mistakes2[br].answer_w
			answer_r = questions[br].answer_r
			return render(request, 'tests/seeMistakes.html', {'questions' : questions[br].question, 'answers' : answers, 'tests' : name, 'br' : br + 1, 'answer_w' : int(answer_w), 'answer_r' : int(answer_r)})
		else:
			temp_mistakes = Mistakes.objects.filter(user=request.user)
			mistakes = temp_mistakes.filter(name=test)
			mistakes.delete()
			return render(request, 'tests/doneSeeing.html')
