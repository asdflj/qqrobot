import importlib
import os
from multiprocessing import Process
from script import models
import sys
from ..middleware import BaseEventMiddleware
from handler import util,response
from .parse import Parsetext
from handler.settings import ADMIN,BLACK_LIST,EVENT_MIDDLEWARE,MESSAGE_TYPE


class BaseFilter:
    def filter(self,text,L):
        if text in L:
            return True
        else:
            return False
            
class Import_py(BaseEventMiddleware,BaseFilter):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            if len(obj.args()) == 0:
                return response.jsonResponse({'reply':'文件名不能为空'})
            elif self.filter(obj.args()[0],BLACK_LIST):
                return response.jsonResponse({'reply':'创建失败,该名字为保留关键字'})
            elif not obj.content():
                return response.jsonResponse({'reply':'创建失败,不能为空'})
            else:
                self._saveScript(
                    obj.args()[0],
                    os.path.join(util.PYTHON_SCRIPT_DIR, obj.args()[0] + '.py'),
                    obj.content(),
                    content['user_id'],
                )
                return response.jsonResponse({'reply':'创建成功'})


    def _saveScript(self,name,path,text,creator):
        util.saveFile(path,text, 'w')
        scripts = models.PythonScript.objects.filter(name=name)
        if len(scripts) == 0:
            pys = models.PythonScript(name=name, path=path, creator=creator)
            pys.save()
        else:
            scripts[0].creator = creator
            scripts[0].save()

    def __str__(self):
        return 'import_py'

class Bind(BaseEventMiddleware,BaseFilter):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            if len(obj.args()) == 0:
                return response.jsonResponse({'reply':'文件名不能为空'})
            elif self.filter(obj.args()[0],BLACK_LIST):
                return response.jsonResponse({'reply':'创建失败,该名字为保留关键字'})
            elif len(obj.args()) == 1:
                obj.args().append(obj.args()[0])
            return self._bind(obj.args()[0],obj.args()[1],content['user_id'])

    def _bind(self,inside,external,user_id):
        if self._checkScriptExists(inside):
            scripts = self._script(inside)
            commands = models.Command.objects.filter(external_name=external)
            if len(commands) == 0:
                cmd = models.Command(inside_name=scripts[0],external_name=external,last_bind_user_id=user_id)
                cmd.save()
            else:
                commands[0].inside_name = scripts[0]
                commands[0].external_name = external
                commands[0].last_bind_user_id = user_id
                commands[0].save()
            return response.jsonResponse({'reply': '绑定成功'})
        else:
            return response.jsonResponse({'reply': '绑定失败,请重新创建文件'})

    def _script(self,name):
        return models.PythonScript.objects.filter(name=name)

    def _checkScriptExists(self,fileName):
        scripts = self._script(fileName)
        if len(scripts) == 0:
            return False
        else:
            if util.fileExists(scripts[0].path):
                return True
            else:
                return False
    
    def __str__(self):
        return 'bind'

class Disable(BaseEventMiddleware,BaseFilter):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            if len(obj.args()) == 0:
                return response.jsonResponse({'reply':'命令不能为空'})
            elif self.filter(obj.args()[0],BLACK_LIST):
                return response.jsonResponse({'reply':'禁用失败,该名字为保留关键字'})
            if self._disable(obj.args()[0]):
                return response.jsonResponse({'reply': '禁用成功'})
            else:
                return response.jsonResponse({'reply': '禁用失败,未找到该命令'})
    def _disable(self,external):
        commands = models.Command.objects.filter(external_name=external)
        if len(commands) == 0:
            return False
        else:
            commands[0].is_ban = True
            commands[0].save()
            return True

    def __str__(self):
        return 'disable'

class Enable(BaseEventMiddleware,BaseFilter):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            if len(obj.args()) == 0:
                return response.jsonResponse({'reply':'命令不能为空'})
            elif self.filter(obj.args()[0],BLACK_LIST):
                return response.jsonResponse({'reply':'启用失败,该名字为保留关键字'})
            if self._enable(obj.args()[0]):
                return response.jsonResponse({'reply': '启用成功'})
            else:
                return response.jsonResponse({'reply': '启用失败,未找到该命令'})

    def _enable(self,external):
        commands = models.Command.objects.filter(external_name=external)
        if len(commands) == 0:
            return False
        else:
            commands[0].is_ban = False
            commands[0].save()
            return True

    def __str__(self):
        return 'enable'

class List(BaseEventMiddleware):
    simple_page_num = 10
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            if len(obj.args()) == 0:
                return response.jsonResponse({
                    'reply': '当前拥有命令:\n%s\n当前第1页'%' '.join(self._allCommands()[:self.simple_page_num])
                })
            if obj.args()[0].isdigit():
                page = int(obj.args()[0])
                return response.jsonResponse({
                    'reply': '当前拥有命令:\n%s\n当前第%s页' %(
                        ' '.join(self._allCommands()[page*self.simple_page_num:(page+1)*self.simple_page_num]),
                        page
                    )
                })


    def _allCommands(self):
        L1 = self._middlewareCommands(EVENT_MIDDLEWARE['message'])
        L2 = self._userCommands()
        L1.extend(L2)
        return L1

    def _userCommands(self):
        return list(models.Command.objects.values_list('external_name',flat=True))

    def _middlewareCommands(self, middleware):
        L = []
        for mid in middleware:
            m = self._split(mid)
            mod = importlib.import_module(m[0])
            cls = getattr(mod, m[1])
            obj = cls(lambda x : 1)
            result = obj.__str__()
            if result:
                L.append(result)
        return L

    def _split(self,moduleName):
        L = moduleName.split('.')
        filename = '.'.join(L[:-1])
        moduleClass = L[-1]
        return (filename,moduleClass)

    def __str__(self):
        return 'list'

class Print(BaseEventMiddleware,BaseFilter):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            if len(obj.args()) == 0:
                return response.jsonResponse({'reply':'命令不能为空'})
            elif self.filter(obj.args()[0],BLACK_LIST):
                return response.jsonResponse({'reply':'输出失败,该名字为保留关键字'})
            result = self._print(obj.args()[0])
            if result:
                return response.privateResponse(content,result)
            else:
                return response.jsonResponse({'reply': '输出失败,未找到该文件'})

    def _print(self,external):
        commands = models.Command.objects.filter(external_name=external)
        if len(commands) == 0:
            return False
        else:
            path = commands[0].inside_name.path
            name = commands[0].inside_name.name
            if util.checkPythonFileExists(name+'.py'):
                return util.readPythonScriptFile(path)
            else:
                return False

    def __str__(self):
        return 'print'

class Eval(BaseEventMiddleware,BaseFilter):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            if len(obj.args()) == 0:
                return response.jsonResponse({'reply':'命令不能为空'})
            else:
                try:
                    return response.jsonResponse({'reply':str(eval(obj.args()[0]))})
                except Exception:
                    return response.jsonResponse({'reply':'错误语法'})

    def __str__(self):
        return 'eval'

class RunScript(BaseEventMiddleware):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if content['message_type'] == 'group':
            path = self._commandExists(obj.command())
            if path:
                path = util.filterFileExtension([path],'.py')[0]
                process = Process(target=self._runScript,args=(path,content,' '.join(obj.args())))
                process.start()

    def _runScript(self,path,content,args):
        sys.path.append(util.PYTHON_SCRIPT_DIR)
        obj = importlib.import_module(path)
        obj.main(content['group_id'], content['user_id'], args)

    def _commandExists(self,external):
        cmds =models.Command.objects.filter(external_name=external)
        if len(cmds) == 0:
            return None
        else:
            return cmds[0].inside_name.path

class Ping(BaseEventMiddleware):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            return response.jsonResponse({'reply':'Pong'})

    def __str__(self):
        return 'ping'

class SavePic(BaseEventMiddleware):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() and content['message_type'] == 'group':
            util.savePic(content['message'])

class Help(BaseEventMiddleware):
    simple_page_num = 10
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            if len(obj.args()) == 0:
                return response.jsonResponse(self._display(1))
            elif obj.args()[0] == 'add':
                if len(obj.args()) >= 3:
                    self._save(obj.args()[1],' '.join(obj.args()[2:]))
                    return response.jsonResponse({'reply': '添加成功'})
                else:
                    return response.jsonResponse({'reply':'错误参数!\n示例: /help add command xxxx xxx'})
            elif obj.args()[0] == 'del':
                if len(obj.args()) == 2:
                    if self._del(obj.args()[1]):
                        return response.jsonResponse({'reply': '删除成功'})
                    else:
                        return response.jsonResponse({'reply': '未找到该帮助'})
                else:
                    return response.jsonResponse({'reply': '错误参数!\n示例: /help del command'})
            elif obj.args()[0].isdigit():
                return response.jsonResponse(self._display(obj.args()[0]))
            elif len(obj.args()) == 1:
                result =self._query(obj.args()[0])
                if result:
                    return response.jsonResponse({'reply': result})
                else:
                    return response.jsonResponse({'reply': '没有找到该帮助'})

    def _query(self,command):
        helps =models.Help.objects.filter(command=command)
        if len(helps) == 0:
            return None
        else:
            return helps[0].explain
    def _display(self,page):
        page = int(page)
        return {
            'reply': '当前拥有命令:\n%s\n当前第%s页' % (
                ' '.join(self._helpList(page * self.simple_page_num,(page + 1) * self.simple_page_num)),
                page
            )
        }
    def _helpList(self,start,end):
        return list(models.Help.objects.values_list('command',flat=True).all()[start:end])

    def _save(self,command,explain):
        helps = models.Help.objects.filter(command=command)
        if len(helps) == 0:
            obj = models.Help(command=command,explain=explain)
            obj.save()
        else:
            helps[0].explain = explain
            helps[0].save()

    def _del(self,command):
        helps = models.Help.objects.filter(command=command)
        if len(helps) == 0:
            return False
        else:
            helps[0].delete()
            return True

    def __str__(self):
        return 'help'

class Register(BaseEventMiddleware,BaseFilter):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            if len(obj.args()) == 0:
                return response.jsonResponse({'reply': '缺少参数'})
            elif len(obj.args()) ==1:
                return response.jsonResponse({'reply':'缺少文件名'})
            else:
                for TYPE in MESSAGE_TYPE:
                    if MESSAGE_TYPE[TYPE] == obj.args()[0]:
                        pass
                else:
                    return response.jsonResponse({'reply':'注册类型错误'})



    def __str__(self):
        return 'Register'

        # def _user(self,user_id):
        #     users = Creator.objects.filter(user_id=user_id)
        #     if len(users) == 0:
        #         # 创建用户
        #         admin = lambda x:1 if x in ADMIN else 0
        #         creator = Creator(user_id=user_id,user_authority=admin(user_id))
        #         creator.save()
        #         return creator
        #     else:
        #         creator = users[0]
        #         return creator
