from django.shortcuts import render,HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Home Page

def error_404(request, exception):
    return render(request, '404.html',{})
def landing(request):
    return render(request,'main.html',{})
def home(request):
    cats = Category.objects.all()
    users= CustomUser.objects.all()
    badges = Badge.objects.all().order_by('title')[:9]
    questions = Question.objects.all().order_by('-topic_views')
    tags=[]
    for quest in questions:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    tagg = tag_with_count[:30]
    trend_quest= Question.objects.order_by('-topic_views')[:5]
    answers = Answer.objects.all().count()
    quests=Question.objects.annotate(total_comments=Count('answer__comment')).all().order_by('-id')
    paginator=Paginator(quests,10)

    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    if quests.count() > 0:
        for quest in quests:
            quest.tags = quest.tags.split(',')

    notif=[]    
    if request.user.is_authenticated:    
        notif = Notification.objects.filter(user = request.user).order_by('-id')[:4] 
    return render(request,'home.html',{
        'quests':quests,
        'cats':cats,
        'questions':questions,
        'answers':answers,
        'quest.tags':quest.tags,
        'users':users,
        'trend_quest':trend_quest,
        'tagg':tagg,
        'badges':badges,
        'notif':notif,
        
        })

def home_search(request):
    searched = request.GET.get('q')
    quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(title__icontains = searched).order_by('-id')
    questions = Question.objects.all().order_by('-topic_views')
    tags=[]
    for quest in questions:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    tagg = tag_with_count[:6]
    trend_quest= Question.objects.order_by('-topic_views')[:5]
    for quest in quests:
        quest.tags = quest.tags.split(',')
    notif=[]    
    if request.user.is_authenticated:    
        notif = Notification.objects.filter(user = request.user).order_by('-id')[:4] 
    return render(request,'search/home-search.html',{
        'searched':searched,
        'quests':quests,
        'quest.tags':quest.tags,
        'trend_quest':trend_quest,
        'tagg':tagg,
        'notif':notif,
        
        })   

def question_list(request):
    questions = Question.objects.all().order_by('-topic_views')
    tags=[]
    for quest in questions:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    tagg = tag_with_count[:6]
    trend_quest= Question.objects.order_by('-topic_views')[:5]
    searched = request.GET.get('q')
    if searched == None:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).all().order_by('-id')
    else:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(title__icontains=searched).order_by('-id')    
    paginator=Paginator(quests,25)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    for quest in quests:
        quest.tags = quest.tags.split(',')
    notif=[]    
    if request.user.is_authenticated:    
        notif = Notification.objects.filter(user = request.user).order_by('-id')[:4] 
    return render(request,'quest_page/quest-list.html',{
        'searched':searched,
        'quests':quests,
        'quest.tags':quest.tags,
        'trend_quest':trend_quest,
        'tagg':tagg,'notif':notif,
        
        })    

def popular_quest(request):
    questions = Question.objects.all().order_by('-topic_views')
    tags=[]
    for quest in questions:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    tagg = tag_with_count[:6]
    searched = request.GET.get('q')
    if searched == None:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).all().order_by('-topic_views')
    else:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(title__icontains=searched).order_by('-topic_views')
    paginator=Paginator(quests,20)

    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    for quest in quests:
        quest.tags = quest.tags.split(',')
    notif=[]    
    if request.user.is_authenticated:    
        notif = Notification.objects.filter(user = request.user).order_by('-id')[:4] 
    return render(request,'quest_page/pop-list.html',{
        'quests':quests,
        'quest.tags':quest.tags,
        'tagg':tagg,'notif':notif,
        
        })

@login_required
def recommend_quest(request):
    questions = Question.objects.all().order_by('-topic_views')
    tags=[]
    for quest in questions:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    tagg = tag_with_count[:6]
    trend_quest= Question.objects.order_by('-topic_views')[:5]
    if request.user.department == 'Mechone':
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(category_id = 5).order_by('-topic_views')
    elif request.user.department == 'Civilone':
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(category_id = 4).order_by('-topic_views') 
    elif request.user.department == 'Electrone':
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(category_id = 3).order_by('-topic_views')
    elif request.user.department == 'Computone':
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(category_id = 2).order_by('-topic_views')
    elif request.user.department == 'Industrone': 
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(category_id = 1).order_by('-topic_views')   
    else:
        quests = Question.objects.annotate(total_comments=Count('answer__comment')).order_by('-topic_views')
    paginator=Paginator(quests,20)

    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    for quest in quests:
        quest.tags = quest.tags.split(',')
    notif=[]    
    if request.user.is_authenticated:    
        notif = Notification.objects.filter(user = request.user).order_by('-id')[:4] 
    return render(request,'quest_page/recom-list.html',{
        'quests':quests,
        'quest.tags':quest.tags,
        'trend_quest':trend_quest,
        'tagg':tagg,'notif':notif,
        
        })                           

def unanswer(request):
    questions = Question.objects.all().order_by('-topic_views')
    tags=[]
    for quest in questions:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    tagg = tag_with_count[:6]
    trend_quest= Question.objects.order_by('-topic_views')[:5]
    searched = request.GET.get('q')
    if searched == None:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).all().order_by('-id')
    else:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(title__icontains=searched).order_by('-id')
    paginator=Paginator(quests,20)

    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    for quest in quests:
        quest.tags = quest.tags.split(',')
    notif=[]    
    if request.user.is_authenticated:    
        notif = Notification.objects.filter(user = request.user).order_by('-id')[:4] 
    return render(request,'quest_page/unanswered.html',{
        'quests':quests,
        'quest.tags':quest.tags,
        'trend_quest':trend_quest,
        'tagg':tagg,'notif':notif,
        
        })    

def detail(request,id,slug):
    quest=Question.objects.get(pk=id)
    quest.topic_views = quest.topic_views+1
    quest.save()
    if 9999  < quest.topic_views and quest.topic_views < 10001 :
        Badge_Input.objects.create(typename_id = 1, user = quest.user, badge_id = 6)
    elif 2499  < quest.topic_views and quest.topic_views < 2501 :
        Badge_Input.objects.create(typename_id = 2, user = quest.user, badge_id = 5)
    elif 999  < quest.topic_views and quest.topic_views < 1001 :
        Badge_Input.objects.create(typename_id = 3, user = quest.user, badge_id = 4) 
    elif 99 < quest.topic_views and quest.topic_views < 101:
        Badge_Input.objects.create(typename_id=3, user=quest.user, badge_id = 1) 
    elif 249 < quest.topic_views and quest.topic_views < 251:
        Badge_Input.objects.create(typename_id=2, user=quest.user, badge_id = 2) 
    elif 499 < quest.topic_views and quest.topic_views < 501:
        Badge_Input.objects.create(typename_id=1, user=quest.user, badge_id = 3)            
    tags=quest.tags.split(',')
    for tag in tags:
        related_quest = Question.objects.filter(category=quest.category).exclude(pk=quest.id)
    answers=Answer.objects.filter(question=quest)
    for answer in answers:
        vote_score = (answer.upvote_set.count())-(answer.downvote_set.count())
        if 99 < vote_score and vote_score < 101:
            Badge_Input.objects.create(typename_id = 1, user = answer.user, badge_id = 11)
        if 24 < vote_score and vote_score < 26:
            Badge_Input.objects.create(typename_id = 2, user = answer.user, badge_id = 10)
        if 9 < vote_score and vote_score < 11:
            Badge_Input.objects.create(typename_id = 3, user = answer.user, badge_id = 9) 

    trend_quest= Question.objects.order_by('-topic_views')[:5]
    answerform=AnswerForm
    if request.method=='POST':
        answerData=AnswerForm(request.POST, request.FILES)
        if answerData.is_valid():
            answer=answerData.save(commit=False)
            answer.question=quest
            answer.user=request.user  
            answer.save()
            if answer.user == quest.user:
                Badge_Input.objects.create(typename_id = 3, user = answer.user, badge_id = 12)
            Notification.objects.create(user = quest.user, quest=quest, action_user = request.user, action= 'answer')
            Notification.objects.create(user = quest.user, quest=quest, action_user= request.user, action= 'following')
            messages.success(request,'Answer has been submitted.')
        value = request.POST.get('value') 
        if value == 'follow':
            quest_followers = QuestFollower.objects.create(quest = quest, user = quest.user, follower = request.user)
            Notification.objects.create(user = quest.user, quest=quest, action_user = request.user, action= 'follow')
        elif value == 'unfollow':
            quest_followers = QuestFollower.objects.filter(quest = quest, follower = request.user).delete()     
    questFollower = QuestFollower.objects.filter(quest = quest)
    questfollower = []
    for i in questFollower:
        questfollower = i.follower
    if request.user == questfollower:
        follow_btn_val = 'unfollow' 
    else:
        follow_btn_val = 'follow' 

    notif=[]    
    if request.user.is_authenticated:    
        notif = Notification.objects.filter(user = request.user).order_by('-id')[:4]
    return render(request,'detail.html',{
        'quest':quest,
        'tags':tags,
        'answers':answers,
        'answerform':answerform,
        'trend_quest':trend_quest,
        'related_quest':related_quest,'notif':notif,
        'follow_btn_val':follow_btn_val,

    }) 

def category_quest(request,cat_id,title):
    category=Category.objects.get(id=cat_id)
    searched = request.GET.get('q')
    if searched == None:
        quests=Question.objects.filter(category=category).order_by('-id')
    else:    
        quests=Question.objects.filter(category=category).filter(title__icontains=searched).order_by('-id')
    cats=Category.objects.exclude(id=cat_id)
    trend_quest= Question.objects.order_by('-topic_views')[:5]
    for quest in quests:
        quest.tags = quest.tags.split(',')
    questions = Question.objects.all().order_by('-tags')
    tags=[]
    for quest in questions:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    tagg = tag_with_count[:5]
    notif=[]    
    if request.user.is_authenticated:    
        notif = Notification.objects.filter(user = request.user).order_by('-id')[:4]
    return render(request, 'category.html',
        {'quests':quests,'cats':cats,'category':category,
        'quest.tags':quest.tags,'tagg':tagg,'trend_quest':trend_quest,
        'notif':notif
        })     

# Save Comment
@login_required
def save_comment(request):
    comments=Comment.objects.filter(user=request.user).order_by('-id')
    if request.method=='POST':
        comment=request.POST['comment']
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        Comment.objects.create(
            answer=answer,
            comment=comment,
            user=user
        )
        if comments.count() == 10:
            Badge_Input.objects.create(typename_id = 3, user = userpk, badge_id = 14)
        return JsonResponse({'bool':True})

# Save Upvote
@login_required
def save_upvote(request):
    upvotes= UpVote.objects.filter(user=request.user).count()
    downvotes= DownVote.objects.filter(user=request.user).count() 
    all_vote = upvotes + downvotes
    if all_vote == 100:
        Badge_Input.objects.create(typename_id = 3, user = request.user, badge_id = 15)
    if request.method=='POST':
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=UpVote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            UpVote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})

# Save Downvote
@login_required
def save_downvote(request):
    upvotes= UpVote.objects.filter(user=request.user).count()
    downvotes= DownVote.objects.filter(user=request.user).count() 
    all_vote = upvotes + downvotes
    if all_vote == 100:
        Badge_Input.objects.create(typename_id = 3, user = request.user, badge_id = 15)
    if request.method=='POST':
        answerid=request.POST['answerid']
        answer=Answer.objects.get(pk=answerid)
        user=request.user
        check=DownVote.objects.filter(answer=answer,user=user).count()
        if check > 0:
            return JsonResponse({'bool':False})
        else:
            DownVote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool':True})

# User Register
def register(request):
    if request.method == 'POST':
        # fill the form with requested data
        reg_form = UserRegisterForm(request.POST)

        if reg_form.is_valid():
            user = reg_form.save()
            if user.email_alert == True:
                Subscriber.objects.create(user= user.username ,email = user.email)

            messages.success(request, f"Congrats! Your account was created successfully. Please login to continue.")
            return redirect('login')
    else:
        reg_form = UserRegisterForm()

    context = {
        'reg_form':reg_form,
    }
    return render(request,'registration/register2.html',context)

def loginView(request):
    # restrict login page for logged in user 
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            # get username
            username = request.POST.get('username')
            # get password
            password = request.POST.get('password')
            # check authentication
            user = authenticate(request, username=username, password=password)
            # if user exists log them in
            if user is not None:
                login(request, user)
                redirect_url = request.GET.get('next','home')
                return redirect(redirect_url)
            else:
                # show error message
                messages.error(request, f"Oops! Username or Password is invalid. Please try again.")
                
        return render(request, 'registration/login2.html')

# Ask Form
@login_required
def ask_form(request):
    quests=Question.objects.filter(user=request.user).order_by('-topic_views')
    form=QuestionForm
    if request.method=='POST':
        questForm=QuestionForm(request.POST, request.FILES)
        if questForm.is_valid():
            questForm=questForm.save(commit=False)
            questForm.user=request.user
            questForm.save()
            if quests.count() == 1:
                student = Badge_Input.objects.create(typename_id = 3, user = request.user, badge_id = 8)
            return redirect('home')
            messages.success(request,'Question has been added.')
    return render(request,'ask-question1.html',{'form':form})

def quest_edit(request,id):
    quest=Question.objects.get(pk=id)
    form=QuestionForm(instance = quest )
    if request.method=='POST':
        questForm=QuestionForm(request.POST, request.FILES, instance=quest)
        if questForm.is_valid():
            questForm.save()
            return redirect('home')
            messages.success(request,'Question has been added.')
    return render(request,'quest-edit.html',{'form':form,'quest':quest})

# Questions according to tag
def tag(request,tag):
    trend_quest= Question.objects.order_by('-topic_views')[:3]
    searched= request.GET.get('q')
    if searched == None:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(tags__icontains=tag).order_by('-id')
    else:
        quests=Question.objects.annotate(total_comments=Count('answer__comment')).filter(tags__icontains=tag).filter(tags__icontains=searched).order_by('-id')    
    paginator=Paginator(quests,15)
    page_num=request.GET.get('page',1)
    quests=paginator.page(page_num)
    return render(request,'tag1.html',{'quests':quests,'tag':tag,'trend_quest':trend_quest,'trends_blog':trends_blog})


# Profile
def profile(request,id,username):
    userpk = CustomUser.objects.get(pk=id)
    userall = CustomUser.objects.all().aggregate(Sum('reputation')).get('reputation__sum')
    quests=Question.objects.filter(user=userpk).order_by('-topic_views')
    ans=Answer.objects.filter(user=userpk)
    answers=Answer.objects.filter(user=userpk).order_by('-id')[:5]
    comments=Comment.objects.filter(user=userpk).order_by('-id')
    upvotes= UpVote.objects.filter(answer__user=userpk).count()
    downvotes= DownVote.objects.filter(answer__user=userpk).count() 
    all_vote = int(upvotes)-int(downvotes)
    user_gold = Badge_Input.objects.filter(user = userpk, typename_id=1).order_by('-add_time')[:4]
    gold = Badge_Input.objects.filter(user = userpk, typename_id=1)
    user_silver = Badge_Input.objects.filter(user = userpk, typename_id=2).order_by('-add_time')[:4]
    silver = Badge_Input.objects.filter(user = userpk, typename_id=2)
    user_bronze = Badge_Input.objects.filter(user = userpk, typename_id=3).order_by('-add_time')[:4]
    bronze = Badge_Input.objects.filter(user = userpk, typename_id=3)
    total_badge = int(gold.count())+int(silver.count())+int(bronze.count())
    total_reached=Question.objects.filter(user=userpk).aggregate(Sum('topic_views')).get('topic_views__sum')
    if total_reached == None:
        reput =int(quests.count())+int(answers.count())+int(comments.count())+all_vote
    else:    
        reput = int(total_reached)+int(quests.count())+int(answers.count())+int(comments.count())+int(all_vote)+int(total_badge)
    if userall == 0:
        over_mult = 0
    else:
        over_mult = reput / int(userall)     
    overall = over_mult * 100
    userpk.reputation= int(reput)
    userpk.questions = int(quests.count())
    userpk.answers = int(ans.count())
    userpk.gold_badge = int(gold.count())
    userpk.silver_badge = int(silver.count())
    userpk.bronze_badge = int(bronze.count())
    userpk.total_badge = int(total_badge)
    userpk.save()
    notif=[]    
    if request.user.is_authenticated:    
        notif = Notification.objects.filter(user = request.user).order_by('-id')[:4]
    return render(request,'registration/profile2.html',{
        'userpk':userpk,
        'quests':quests,'answers':answers,'ans':ans,'comments':comments,
        'upvotes':upvotes,'downvotes':downvotes,
        'total_reached':total_reached,'reput':reput,'overall':overall,
        'user_gold':user_gold,'user_silver':user_silver,'user_bronze':user_bronze,
        'gold':gold,'silver':silver,'bronze':bronze,'notif':notif,
    })

def users(request):
    searched= request.GET.get('q')
    if searched == None:
        users = CustomUser.objects.all().order_by('-reputation')
    else:
        users = CustomUser.objects.filter(username__icontains=searched).order_by('-reputation') 
    paginator=Paginator(users,60)
    page_num=request.GET.get('page',1)
    users=paginator.page(page_num)
    return render(request,'user_list/users.html',{'users':users})

def new_users(request):
    searched= request.GET.get('q')
    if searched == None:
        users = CustomUser.objects.all().order_by('-id')
    else:
        users = CustomUser.objects.filter(username__icontains=searched).order_by('-id') 
    paginator=Paginator(users,60)
    page_num=request.GET.get('page',1)
    users=paginator.page(page_num)
    return render(request,'user_list/new-users.html',{'users':users})  

def moderator(request):
    searched= request.GET.get('q')
    if searched == None:
        users = CustomUser.objects.filter(moderator = True).order_by('-reputation')
    else:
        users = CustomUser.objects.filter(moderator = True).filter(username__icontains=searched).order_by('-id') 
    paginator=Paginator(users,60)
    page_num=request.GET.get('page',1)
    users=paginator.page(page_num)
    return render(request,'user_list/moderators.html',{'users':users})        

def badges(request):
    searched = request.GET.get('q')
    if searched == None:
        badges = Badge.objects.all().order_by('title') 
    else:
        badges = Badge.objects.filter(title__icontains=searched).order_by('title') 
    return render(request,'badges.html',{'badges':badges})
# Tags Page
def tags(request):
    searched = request.GET.get('q')
    if searched == None:
        quests=Question.objects.all()
    else:
        quests=Question.objects.filter(tags__icontains=searched)    
    tags=[]
    for quest in quests:
        qtags=[tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count=[]
    for tag in tags:
        tag_data={
            'name':tag,
            'count':Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)

    paginator=Paginator(tag_with_count,60)
    page_num=request.GET.get('page',1)
    tag_with_count=paginator.page(page_num)    
    return render(request,'tags1.html',{'tags':tag_with_count})
          
@login_required
def profile_edit(request):
    if request.method=='POST':
        profileForm=ProfileForm(request.POST,request.FILES, instance=request.user)
        passwordform = ChangePassword(data=request.POST, user=request.user)
        if profileForm.is_valid():
            profileForm.save()
            if request.user.bio is not None:
                Badge_Input.objects.create(typename_id = 3, user = request.user, badge_id = 13)
            messages.success(request,'Profile has been updated.') 
        if passwordform.is_valid():
            passwordform.save()
            messages.success(request, 'Password Updated!') 
        else:
            messages.error(request, f"Oops! Password is incorrect. Check passwords again!.")         
    form=ProfileForm(instance=request.user)
    passwordform = ChangePassword(CustomUser)
    return render(request,'registration/profile-edit.html',{
        'form':form,'passwordform':passwordform,
    })       

def contact(request):
    form=ContactForm
    if request.method=='POST':
        Form=ContactForm(request.POST)
        if Form.is_valid():
            Form=Form.save(commit=False)
            Form.user=request.user
            Form.save()
            messages.success(request,'Thank You! Your message has been sent.')
    return render(request, 'footer/contact.html', {'form':form})


def faq(request):
    faqs = Faq.objects.all().order_by('-id')
    form=ContactForm
    if request.method=='POST':
        Form=ContactForm(request.POST)
        if Form.is_valid():
            Form=Form.save(commit=False)
            Form.user=request.user
            Form.save()
            messages.success(request,'Thank You! Your message has been sent.')
    return render(request, 'footer/faq.html', {'form':form,'faqs':faqs})    

def about(request):
    return render(request, 'footer/about.html', {})

def privacy_policy(request):
    return render(request, 'footer/privacy-policy.html', {})

def terms(request):
    return render(request, 'footer/terms.html', {})    

def notifications(request):
    questfollow = Notification.objects.filter(user = request.user).order_by('-id')
    notif = Notification.objects.filter(user = request.user).order_by('-id')[:5]
    if request.method == 'POST':
        question = request.POST.get('question')
        action_user = request.POST.get('action_user')
        action = request.POST.get('action')
        post = request.POST.get('post') 
        if post == 'yes':
            Notification.objects.filter(user= request.user, quest = question, action_user= action_user, action= action).delete() 

    paginator=Paginator(questfollow,15)

    page_num=request.GET.get('page',1)
    questfollow=paginator.page(page_num)# 
    trend_quest= Question.objects.order_by('-topic_views')[:5]           
    return render(request, 'notifications.html', {
        'questfollow':questfollow,'notif':notif,
        'trend_quest':trend_quest,
        })