# Setup on windows!

> using Python 3.7!

> Make sure you're using virtual env, for python version conflicts!  
https://docs.djangoproject.com/en/2.1/howto/windows/  
now by using 'python' command, we should enter in python 3.x shell!  
after that, install all the packages, in the requirements.txt
now every packages are in a directory like: C:\Users\<user>\Envs\<virtualenv-name>\lib\site-packages\
So if the sources needs changing, do it in here!

> You might need to download Visual Studio 2017 Buildtools, Microsoft Visual C++ 14.0:  
https://www.scivision.co/python-windows-visual-c++-14-required/

> Fix problem for installing 'simple-crypt' or 'pycrypt' or 'crypto' (the upvoted answers):  
https://stackoverflow.com/questions/41843266/microsoft-windows-python-3-6-pycrypto-installation-error  
https://stackoverflow.com/questions/24804829/no-module-named-winrandom-when-using-pycrypto/24822876#24822876

> if using Python 3.'7', the `async` word is now reserved! So for the tweepy package, you need to change to source code:  
https://github.com/tweepy/tweepy/issues/1017  
https://github.com/tweepy/tweepy/pull/1042 (see the file changes and change accordingly)  
This will be fixed in the next version of tweepy, but currently, we need to do this manually!  
  open <virtual-env-package-dir>\tweepy\streaming.py  
  repalce all `async` words in the file with `is_async` for example, just to avoid using the reserved word, as there would be errors!

> create .env file with the following info (for the time being):  
  DB_USERNAME=  
  DB_PASSWORD=  
  DB_URI=  
  HOST=  

> `python manage.py makemigrations <for-each-app>`  
  apps: postchiapp, tg_handler  

> `python manage.py migrate`  

> `python manage.py runserver`  

> ENJOY!


## For Each Time Running:

> change current directory to the root of the project  
`workon <virtual-env-name>`
`python3 manage.py runserver`