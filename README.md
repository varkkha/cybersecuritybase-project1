# Cyber Security Base - Project I

### LINK: https://github.com/varkkha/cybersecuritybase-project1

## Installation instructions

This software has been implemented by using Python & Django.

1. Clone the repository and move to the root folder
```bash
git clone git@github.com:varkkha/cybersecuritybase-project1.git
cd cybersecuritybase-project1
```

2. Set up a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a .env file in the root folder with the following content:
```bash
SECRET_KEY=your_secret_key_here
DEBUG=True
```

5. Run migrations. Make sure you're in the src folder.
```bash
cd src
python manage.py migrate
```
6. Start the development server
```bash
python manage.py runserver
```
7. Visit http://localhost:8000 in your browser

## Security flaws

This software has been constructed for the course _Cyber Security Base: Course Project I_. The software has five security flaws that are pointed out below. In addition, there are provided the steps to fix them.

### Flaw 1: A01:2021-Broken Access Control

**Source link:**
See the code on [line 27 of views.py](https://github.com/varkkha/cybersecuritybase-project1/blob/main/src/blog/views.py#L27)

**Description of flaw:**
In these kind of flaws, users can act outside of their intented permissions because the system does not properly verify the ownership. The inadequate verification can lead to unauthorized access, data breaches, and potential manipulation or destruction of other users’ sensitive information.

In this software flaw comes from views.py file where view_profile(request, user_id) view does not check that the profile belongs to the logged in user. This view allows any authenticated user to access any profile by simply changing the user_id in the URL.

```bash
def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'blog/profile.html', {'profile_user': user})
```

In the snapshot below, signed in is user with user_id = 3. But if one opens url http://localhost:8000/blog/profile/2/, that includes user_id = 2 information, one can see user_id = 2 profile information.

![Flaw1Before](screenshots/flaw-1-before.png)

**How to fix it:**

This flaw can be fixed by adding a check to ensure that the profile belongs to the logged-in user. This fix can be found in the code commented out starting from line 32.

```bash
@login_required
def profile_view(request, user_id):
    if request.user.id != user_id:
        return HttpResponseForbidden("You do not have permission to view this profile.")
    user = get_object_or_404(User, id=user_id)
    return render(request, 'blog/profile.html', {'profile_user': user})
```
Now one cannot see the profile page of another user.

![Flaw1After](screenshots/flaw-1-after.png)

### Flaw 2: A03:2021-Injection

**Source link:**
See the code on [line 40 of views.py](https://github.com/varkkha/cybersecuritybase-project1/blob/main/src/blog/views.py#L40)

**Description of flaw:**

In SQL injection vulnerability, the unsafe use of SQL queries allows attackers to manipulate database quieries by using crafted input.

In this sofware the flaw comes from the unsafe_search(request) view where user's input is directly embedded in an SQL query without using proper sanitization. With this vulnerable code, the user can access the following URL with a crafted parameter: "http://localhost:8000/blog/unsafe-search/?name=' OR '1'='1" and this will return all users from the auth_user table instead of just one — revealing sensitive user data.

In the snapshot below, when visiting url "http://localhost:8000/blog/unsafe-search/?name=' OR '1'='1", user can see listed all the users. In the case of the screenshot, there are two users created: testuser1 and admin.

![Flaw2Before](screenshots/flaw-2-before.png)

**How to fix it:**

This flaw can be fixed by replacing the vulnerable query with a parameterized one. This ensures that user input is handled safely. This fix can be found in the code commented out starting from line 47.

Now, when trying to open URL "http://localhost:8000/blog/unsafe-search/?name=' OR '1'='1" the results page is empty, because "OR '1'='1" is not anymore SQL injection, but just a string. So the database looks for a username literally matching ' OR '1'='1, which doesn't exist, resulting in an empty results page. This prevents the classic SQL injection attack from succeeding.

![Flaw2After](screenshots/flaw-2-after.png)

### Flaw 3: A04:2021 – Insecure Design

**Source link:**
See the code on [line 56 of views.py](https://github.com/varkkha/cybersecuritybase-project1/blob/main/src/blog/views.py#L56)

**Description of flaw:**

Insecure design can include a large variety of different kinds of weaknesses. This software has a vulnerability with API key as the API view uses a hardcoded API key. This is insecure since the key is directly embedded in the source code, and that way it can leak through version control or code sharing. The flaw can be found on views.py line 58.

When opening URL http://localhost:8000/blog/secret-api/?apikey=my-secret-api-key, one can see the secret data, see the screenshot below.

![Flaw3Before](screenshots/flaw-3-before.png)

**How to fix it:**

This flaw can be fixed by storing the API key to .env file and loading it securely at runtime. Now, only requests with the correct API key stored in the environment file will see the secret data.

Thus, when fixin the flaw, one should add enviroment file .env and add the API key there:
```bash
API_KEY=my-secret-api-key
```
After that, the view.py should be changed to a version where the API key is loaded from .env file:
```bash
API_KEY = config('API_KEY')

def secret_api(request):
    key = request.GET.get('apikey')

    if key == API_KEY:
        return JsonResponse({'data': 'Secrets!'})
    else:
        return JsonResponse({'error': 'Incorrect API key'}, status=403)
```

The fixed code can be found as commented out starting from views.py line 64.

The before and after screenshots look visually identical because both show the secret data page:

![Flaw3After1](screenshots/flaw-3-after-1.png)

However, in the fixed version, if you try to access the API with an incorrect or missing API key, the data will be hidden or an error shown:

![Flaw3After2](screenshots/flaw-3-after-2.png)
