#!/usr/bin/python3
'''console'''

import cmd
import json
import re

import models
from models import BaseModel, User, State, \
    City, Amenity, Place, Review

def isfloat(s):
    '''Checks if a string is a decimal'''
    try:
        float(s)
        return True
    except ValueError:
        return False

class HBNBCommand(cmd.Cmd):
    '''Shell for database
    '''

    prompt = '(hbnb) '
    model_list = ['BaseModel', 'User', 'State',
                  'City', 'Amenity', "Place", "Review"
                  ]
    queries = ['all', 'count', 'show', 'destroy', 'update']

    @classmethod
    def handle_errors(cls, args: str, **kwargs):
        '''Error Handler for all commands'''

        if "all" in kwargs.values():
            if not args:
                return False

        if not args:
            print("** class name missing **")
            return True
        else:
            args = args.split(" ")

        n = len(args)

        if n < 1:
            print("** class name missing **")
            return True

        if args[0] not in HBNBCommand.model_list:
            print("** class doesn't exist **")
            return True

        if 'command' not in kwargs:
            return False

        for _, arg in kwargs.items():
            if arg in ['create', 'show', 'destroy']:
                if n < 2:
                    print("** instance id missing **")
                    return True
            elif arg in ['update']:
                if n < 2:
                    print("** instance id missing **")
                    return True
                elif n < 3:
                    print("** attribute name missing **")
                    return True
                elif n < 4:
                    print("** value missing **")
                    return True
                elif n == 4 and args[2] == "":
                    print("** attribute name missing **")
                    return True

        return False

    def do_quit(self, args: str):
        '''Quit command to exit the program'''

        return True

    def do_EOF(self, args):
        '''EOF command to exit the program'''

        return True

    def do_create(self, args: str):
        '''
        Creates a new instance of a class, saves it to JSON
        file, prints the instance id
        Usage: create <class name>
        '''

        if HBNBCommand.handle_errors(args):
            return

        args = args.split(" ")
        obj = eval(args[0])()
        obj.save()
        print(obj.id)

    def do_show(self, args: str):
        '''
        Prints the string representation of an instance
        based on the class name and id
        Usage: show <class name> <id>
               <class name>.show("<id>")
        '''

        if HBNBCommand.handle_errors(args, command='show'):
            return

        args = args.split(" ")
        objects = models.storage.all()
        key = ".".join(args)
        obj = objects.get(key)
        if obj:
            print(obj)
        else:
            print("** no instance found **")

    def do_destroy(self, args: str):
        '''
        Deletes an instance based on the class name and id
        Usage: destroy <class name> <id>
               <class name>.destroy("<id>")
        '''

        if HBNBCommand.handle_errors(args, command='destroy'):
            return

        args = args.split(" ")
        objects = models.storage.all()
        key = ".".join(args)

        delete = False
        if key in objects and models.storage.delete(objects[key]):
            pass
        else:
            print("** no instance found **")

    def do_count(self, args: str):
        '''
        counts all string representation of all instances based
        or not on the class name.
        Usage: count <class_name>
               <class name>.count()
        '''

        if HBNBCommand.handle_errors(args):
            return

        args = args.split(" ")
        objects = models.storage.all()
        _all = []

        for k, v in objects.items():
            key = k.split(".")
            if key[0] == args[0]:
                _all.append(str(v))

        print(len(_all))

    def do_all(self, args: str):
        '''
        Prints all string representation of all instances based
        or not on the class name.
        Usage: all
               all <class name>
               <class name>.all()
        '''

        if HBNBCommand.handle_errors(args, command='all'):
            return

        args = args.split(" ")

        objects = models.storage.all()

        if args[0] == "":
            for obj in objects.values():
                print(obj)

        else:
            for key in objects:
                k = key.split(".")
                if k[0] == args[0]:
                    print(objects[key])

    def do_update(self, args: str):
        '''
        Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file).
        Usage: update <class name> <id> <attr_name> <attr_value>
               <class name>.update("<id>", <attr_name>, "<attr_vale>")
               <class name>.update("<id>", <dictionary>)
        '''

        if HBNBCommand.handle_errors(args, command='update'):
            return

        args = args.split(" ")
        attr_name = args[2]
        attr_value = str(args[3])
        if attr_value[0] == "\"" or attr_value[0] == "'":
            attr_value = attr_value[1:-1]
        if attr_value.isdigit():
            attr_value = int(attr_value)
        elif isfloat(attr_value) :
            attr_value = float(attr_value)

        objects = models.storage.all()
        key = ".".join(args[:2])

        obj = objects.get(key)
        if obj:
            setattr(obj, attr_name, attr_value)
            obj.save()
        else:
            print("** no instance found **")

    def onecmd(self, args: str):
        pattern = re.compile(
            r"(\w+)\.(\w+)\(((\"[\w|-]+\"),?\s?(\"\w+\")?,?\s?(\"?[\w\.]+\"?)?)?\)"
        )

        pattern2 = re.compile(
            r"(\w+)\.(\w+)\((\"[\w-]+\"),\s?\{(.+)\}\)"
        )

        match = pattern.search(args)
        match2 = pattern2.search(args)
        if match:
            self.handle_match(match)
        elif match2:
            self.handle_match2(match2)
        elif args == "quit":
            return self.do_quit(args)
        elif args == "EOF":
            return self.do_EOF(args)
        else:
            cmd.Cmd.onecmd(self, args)

    def handle_match(self, match: re.Match):
        groups = match.groups()
        if groups[0] not in HBNBCommand.model_list:
            print("** class doesn't exist **")
            return
        if groups[1] not in HBNBCommand.queries:
            print(f"** unknown command: '{groups[1]}' **")
            return
        if groups[1] == 'all':
            args = f"{groups[1]} {groups[0]}"
            cmd.Cmd.onecmd(self, args)
            return
        elif groups[1] == 'count':
            args = f"{groups[1]} {groups[0]}"
            cmd.Cmd.onecmd(self, args)
            return
        elif groups[1] == 'show':
            if groups[3]:
                id = groups[3][1:-1]
            else:
                id = ""
            args = f"{groups[1]} {groups[0]} {id}"
            cmd.Cmd.onecmd(self, args)
            return
        elif groups[1] == "destroy":
            if groups[3]:
                id = groups[3][1:-1]
            else:
                id = ""
            args = f"{groups[1]} {groups[0]} {id}"
            cmd.Cmd.onecmd(self, args)
            return
        elif groups[1] == 'update':
            if groups[3]:
                id = groups[3][1:-1]
            else:
                id = ""
            if groups[4]:
                attr_name = groups[4][1:-1]
            else:
                attr_name = ""
            
            if not groups[5]:
                attr_value = ""
            elif "\"" not in groups[5]:
                attr_value = groups[5]
            elif groups[5]:
                attr_value = groups[5][1:-1]
            
            args = f"{groups[1]} {groups[0]} {id} {attr_name} {attr_value}"
            cmd.Cmd.onecmd(self, args)
            return

    def handle_match2(self, match: re.Match):
        groups1 = match.groups()
        if groups1[0] not in HBNBCommand.model_list:
            print("** class doesn't exist **")
            return
        if groups1[1] != 'update':
            print(f"** This only works for update command **")
            return

        if groups1[3]:
            pattern = re.compile(
                r"[\'\"](\w+)[\'\"]\s?:\s?[\'\"]?([\w\.]+)[\'\"]?,?\s?"
            )
            match = pattern.finditer(groups1[3])
            results = []
            for m in match:
                for part in m.groups():
                    results.append(part)

        if not results or len(results) % 2 != 0:
            print("** something went wrong in the dictionary argument **")
            return
        else:
            class_name = groups1[0]
            query = groups1[1]
            id = groups1[2]
            if id[0] == "\"" or id[-1] == "\"":
                id = id[1:-1]

            for i in range(0, len(results), 2):
                attr_name = results[i]
                attr_value = results[i+1]
                args = f"{query} {class_name} {id} {attr_name} {attr_value}"
                cmd.Cmd.onecmd(self, args)

    def emptyline(self):
        return False


if __name__ == '__main__':
    interpreter = HBNBCommand()
    interpreter.cmdloop()
