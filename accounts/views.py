from django.shortcuts import render, redirect
import json
from django.views import View
from django.http  import JsonResponse,HttpResponse
from .models      import Users
import bcrypt
import jwt
from acbaseball.settings import SECRET_KEY

# Create your views here.

def signup(request):
    return render(request, 'signup.html')

def create(request):
    
    result = CreateView.as_view()
    print(result)

def login(request):
    return render(request, 'login.html')

def logout(request):
    return render(request, 'login.html')

def chkid(request):
    try:
        user = Users.objects.get(user_id=request)
    except Exception:
        user = None
    print(user.count())
    if user.exists():
        return 'exist'
    else:
        return 'not exist'

#회원가입
class CreateView(View):
    # 1.post방식으로 요청할 경우 회원가입한다.
    def post(self, request):
        # 아이디 중복 체크 
        try: 
            print('exist')
            Users.objects.get(user_id=request.POST['user_id']) 
            return JsonResponse({'message' : "이미 가입된 아이디입니다."}) 
        except: # # 조회 결과가 없다. 등록되지 않은 id 
            print('not exist')    
            pass

        # 2.data에 request에 담긴 정보를 넣어준다
        # data = json.loads(request.body)

        # 3.이때 비밀번호의 경우 따로 암호화를 해줘야하기 때문에 password_not_hashed에 따로 담아준다
        password_not_hashed = request.POST["password1"]
        # 4.bcrypt를 사용해서 password_not_hashed를 암호화 해준다
        hashed_password = bcrypt.hashpw(password_not_hashed.encode('utf=8'), bcrypt.gensalt())
        
        try :
            # 5.Users 저장을 해준다
            # 6.기본적으로 data에 담긴 값을 저장하고, password의 경우 암호화 된 hashed_password를 넣어준다
  
            # Users( 
            #     user_id     = request.POST["user_id"],
            #     name    = request.POST["name"],
            #     email    = request.POST["email"],
            #     password = hashed_password.decode('utf=8')
            # ).save()

            #7.성공적으로 저장이 되었으면 성공 메시지를 보낸다.  
            # return JsonResponse({'message':'회원가입 성공'}, status=200)
            return redirect("index")

        # 8.예외처리
        except KeyError: 
            return JsonResponse({'message' : "INVALID_KEYS"},status =400) 

    # 9.테스트를 위한 get
    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({'users':list(user_data)}, status=200)      

class LoginView(View) :
    # 1. post로 받은 request 데이터를 인자로 받는다.
    def post(self, request) : 
    
    # 2. data는 request의 데이터(내용)을 json형태로 불러온다.
        data = json.loads(request.body) 

	# 3. 조건문을 건다. 만약 Users내 데이터 중에 request로 받아온 data['name']=키값이 존재한다면 코드를 그대로 진행한다. 
        try :
            if Users.objects.filter(user_id = data['user_id']).exists():
            
            # 4. 객체를 가져오는것 . Users의 데이터중 name = data['name']인 데이터를 새로운 객체로 만든다
                user = Users.objects.get(user_id = data['user_id'])
                user_password = user.password.encode('utf=8')

                #5. 새로 만든 객체에 담긴 password 데이터와 request로 받은 데이터를 비교해서 동일하면 200신호를 보낸다
                #if user.password == data['password']:

                #6. bcrypt.checkpw기능으로 현재 입력한 password를 encode한 값과 현재 데이터베이스에 저장된 암호화된 값을 비교한다.
                if bcrypt.checkpw(data['password'].encode('utf=8'), user_password):
                
                    #7. 만약 비밀번호가 맞다면 토크을 발행한다. 
                    #8. 토큰 값에는 현재 로그인하는 id의 pk값(해당 유저의 고유 넘버 )을 토큰에 넣어 발행한다.
                    token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = "HS256")
                   

                    return JsonResponse({"Authorization" : token,'message':f'{user.email}님 로그인 성공!'}, status=200)          

                
                    #9. 리턴할때 제이슨 레스펀스 안에 액세스 토큰 넣기 .
                    
                #10. 예외처리 
                return JsonResponse({'message' : "비밀번호가 틀렸습니다"},status =401) 
            return JsonResponse({'message' : "ID가 존재하지 않습니다"},status =400) 
        
        #11. 예외처리2
        except KeyError as e:
            return JsonResponse({'message' : "INVALID_KEYS_".e},status =400)         