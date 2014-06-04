from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

def user_login(request):
    #context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
		response = HttpResponse("Login Successful!!")
		response.set_cookie('chatdemo_user', user)
                return response
            else:
                return HttpResponse("Your Account is disabled.")
        else:
            print "Incorrect Username/Password"
            return HttpResponse("Invalid login details supplied.")

    else:
	c = {}
        c.update(csrf(request))
        return render_to_response('login/login.html',c)
     #   return render_to_response('login/login.html', {}, context)
