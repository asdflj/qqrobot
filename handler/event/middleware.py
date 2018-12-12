import importlib
import json
import os
from multiprocessing import Process
import traceback
import sys

import event.models
import script.models
from ..middleware import BaseEventMiddleware
from handler import util,response
from .parse import Parsetext
from handler.settings import ADMIN,BLACK_LIST,EVENT_MIDDLEWARE,MESSAGE_TYPE,DEBUG,VERSION
import qqrobot.settings

sys.path.append(os.path.join(qqrobot.settings.BASE_DIR,util.PYTHON_SCRIPT_DIR))

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
                    os.path.join(os.path.join(qqrobot.settings.BASE_DIR,util.PYTHON_SCRIPT_DIR), obj.args()[0] + '.py'),
                    obj.content(),
                    content['user_id'],
                )
                return response.jsonResponse({'reply':'创建成功'})


    def _saveScript(self,name,path,text,creator):
        try:
            util.saveFile(path,text, 'w')
            scripts = script.models.PythonScript.objects.filter(name=name)
            if len(scripts) == 0:
                pys = script.models.PythonScript(name=name, path=path, creator=creator)
                pys.save()
            else:
                scripts[0].creator = creator
                scripts[0].save()
        except Exception as e:
            traceback.print_exc()
            raise 'a'

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
            commands = script.models.Command.objects.filter(external_name=external)
            if len(commands) == 0:
                cmd = script.models.Command(inside_name=scripts[0],external_name=external,last_bind_user_id=user_id)
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
        return script.models.PythonScript.objects.filter(name=name)

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
        commands = script.models.Command.objects.filter(external_name=external)
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
        commands = script.models.Command.objects.filter(external_name=external)
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
        L3 = self._thirdMiddleware()
        L1.extend(L2)
        L1.extend(L3)
        return L1

    def _thirdMiddleware(self):
        L = []
        moduleName = []
        objects = event.models.Message.objects.all()
        for i in objects:
            L.append(i.script.path)
        L = util.filterFileExtension(L, '.py')
        for file in L:
            obj = importlib.import_module(file)
            result = obj.__str__()
            if result:
                moduleName.append(result)
        return moduleName

    def _userCommands(self):
        return list(script.models.Command.objects.values_list('external_name',flat=True))

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
        commands = script.models.Command.objects.filter(external_name=external)
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
        obj = importlib.import_module(path)
        obj.main(content['group_id'], content['user_id'], args)

    def _commandExists(self,external):
        cmds =script.models.Command.objects.filter(external_name=external)
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
            # content['message'] = util.replacePic(content['message'])

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
        helps =script.models.Help.objects.filter(command=command)
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
        return list(script.models.Help.objects.values_list('command',flat=True).all()[start:end])

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

class Debug(BaseEventMiddleware):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            if len(obj.args()) == 0:
                self.mode = self._debug()
            else:
                if obj.args()[0] == 'true':
                    self.mode = self._debug(True)
                elif obj.args()[0] == 'false':
                    self.mode = self._debug(False)
                elif obj.args()[0] == 'meta':
                    self.mode = 'meta'
                else:
                    self.mode = self._debug()
            global DEBUG
            DEBUG['mode'] = self.mode
            DEBUG['user_id'] = content['user_id']
            return response.privateResponse(content,'DEBUG已开启' if DEBUG['mode'] else 'DEBUG已关闭')
        if DEBUG['mode'] == True:
            string = '用户ID:%s\n消息:%s\n'%(content['user_id'],content['message'])
            content['user_id'] = DEBUG['user_id']
            return response.privateResponse(content,string)
        elif DEBUG['mode'] == 'meta':
            original = content.copy()
            content['user_id'] = DEBUG['user_id']
            return response.privateResponse(content,json.dumps(original))

    def _debug(self,swich=None):
        if swich == None:
            return False if DEBUG['mode'] else True
        elif swich == True:
            return True
        elif swich == False:
            return False
        else:
            return False

    def process_exception(self,exception):
        return response.privateResponse(exception)

    def __str__(self):
        return 'debug'

class Register(BaseEventMiddleware):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            if len(obj.args()) == 0:
                return response.jsonResponse({'reply': '缺少参数'})
            elif len(obj.args()) == 1:
                return response.jsonResponse({'reply':'缺少文件名'})
            elif len(obj.args()) == 2:
                scripts = script.models.PythonScript.objects.filter(name=obj.args()[1])
                if len(scripts) == 0:
                    return response.jsonResponse({'reply':'文件不存在'})
                else:
                    if obj.args()[0] == MESSAGE_TYPE['MESSAGE']:
                        self._register(event.models.Message,scripts[0],content['user_id'])
                    elif obj.args()[0] == MESSAGE_TYPE['NOTICE']:
                        self._register(event.models.Notice, scripts[0], content['user_id'])
                    elif obj.args()[0] == MESSAGE_TYPE['REQUEST']:
                        self._register(event.models.Request, scripts[0], content['user_id'])
                    elif obj.args()[0] == MESSAGE_TYPE['META_EVENT']:
                        self._register(event.models.Meta_event, scripts[0], content['user_id'])
                    else:
                        return response.jsonResponse({'reply':'注册类型错误'})
                    return response.jsonResponse({'reply':'注册成功'})

    def _register(self,myModel,script,userId):
        objects = myModel.objects.filter(script=script)
        if len(objects) != 0:
            objects[0].delete()
        obj = myModel(script=script,register_id=userId)
        obj.save()

    def __str__(self):
        return 'register'

class UnRegister(BaseEventMiddleware,BaseFilter):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            if len(obj.args()) == 0:
                return response.jsonResponse({'reply': '缺少参数'})
            elif len(obj.args()) == 1:
                return response.jsonResponse({'reply':'缺少文件名'})
            elif len(obj.args()) == 2:
                scripts = script.models.PythonScript.objects.filter(name=obj.args()[1])
                if len(scripts) == 0:
                    return response.jsonResponse({'reply':'文件不存在'})
                else:
                    if obj.args()[0] == MESSAGE_TYPE['MESSAGE']:
                        return self._response(self._unRegister(event.models.Message,scripts[0]))
                    elif obj.args()[0] == MESSAGE_TYPE['NOTICE']:
                        return self._response(self._unRegister(event.models.Notice, scripts[0]))
                    elif obj.args()[0] == MESSAGE_TYPE['REQUEST']:
                        return self._response(self._unRegister(event.models.Request, scripts[0]))
                    elif obj.args()[0] == MESSAGE_TYPE['META_EVENT']:
                        return self._response(self._unRegister(event.models.Meta_event, scripts[0]))
                    else:
                        return response.jsonResponse({'reply':'注册类型错误'})

    def _response(self,result):
        if result:
            return response.jsonResponse({'reply': '反注册成功'})
        else:
            return response.jsonResponse({'reply': '未注册该中间件'})

    def _unRegister(self,myModel,script):
        objects = myModel.objects.filter(script=script)
        if len(objects) != 0:
            objects[0].delete()
            return True
        return False

    def __str__(self):
        return 'unregister'

class RunThirdPartyMiddleware(BaseEventMiddleware, BaseFilter):
    def __init__(self,get_response):
        super(RunThirdPartyMiddleware, self).__init__(get_response)
        self.model = {
            MESSAGE_TYPE['MESSAGE']:event.models.Message,
            MESSAGE_TYPE['NOTICE']: event.models.Notice,
            MESSAGE_TYPE['REQUEST']: event.models.Request,
            MESSAGE_TYPE['META_EVENT']: event.models.Meta_event,
        }
        self.myModels = []

    def process_request(self, content):
        for post_type in MESSAGE_TYPE:
            if MESSAGE_TYPE[post_type] == content['post_type']:
                MyModels = self.model[MESSAGE_TYPE[post_type]].objects.filter(is_ban=False)
                for myModel in MyModels:
                    path = util.filterFileExtension([myModel.script.path],'.py')[0]
                    obj = importlib.import_module(path)
                    obj = obj.Main(response)
                    self.myModels.append((myModel,obj))
                    try:
                        result = self._run_process_request(content,obj)
                        if result:
                            return result
                    except Exception as e:
                        self._error(content,myModel,traceback.format_exc())

    def process_response(self,content,response):
        for i in self.myModels[::-1]:
            try:
                result = self._run_process_response(content,response,i[1])
                if result:
                    return result
            except Exception as e:
                self._error(content, i[0],traceback.format_exc())

    def _error(self,content,myModel,error):
        myModel.error_num += 1
        if myModel.error_num >= 5:
            myModel.is_ban = True
            content['user_id'] = myModel.register_id
            response.privateResponse(content, '错误次数过多,禁用该中间件,中间件名字:%s\n最后错误信息:\n%s' %(
                myModel.script.name,
                error
            ))
        myModel.save()

    def _run_process_response(self,content,response,obj):
        try:
            return obj.process_response(content,response)
        except Exception as e:
            return obj.process_exception(traceback.format_exc())

    def _run_process_request(self,content,obj):
        try:
            return obj.process_request(content)
        except Exception as e:
            return obj.process_exception(traceback.format_exc())

class Version(BaseEventMiddleware):
    def process_request(self,content):
        obj = Parsetext(content['message'])
        if obj.command() == self.__str__() and content['message_type'] == 'group':
            return response.jsonResponse({'reply':"Version:%s %s"%(VERSION[0],VERSION[1])})

    def __str__(self):
        return 'version'