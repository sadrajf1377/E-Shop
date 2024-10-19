#!/usr/bin/env python

import os
import sys

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foroush_gah_postgresql.settings')
django.setup()
from user_Module.models import normal_user
class functions:

    def add_admin(self,args):
        try:
            username=args[args.index('-username')+1]
            password=args[args.index('-password')+1]
            admin_level=args[args.index('-admin_level')+1]
            new_user = normal_user(username=username, admin_level=int(admin_level),user_type='admin')
            new_user.set_password(password)
            new_user.save()
        except Exception as e:
            print(str(e)+'\n')
            #print('Sorry!The Syntax You Entered for creating an admin Was Wrong ! \n The Correct Syntax =>'+
                  #'python my_functions.py -username youusername -password youpassword -admin_level admin level \n Note:admin lvl must be between 1 and 3')


if __name__=='__main__':
    function_name=sys.argv[1]
    instance=functions()
    func=instance.__getattribute__(function_name)
    func(sys.argv)
