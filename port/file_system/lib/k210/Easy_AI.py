import _thread

class Easy_AI:
    def __init__(self, repl,Serial):
        self.repl = repl
        self.Serial=Serial 
        self.break_flags=1

    def AI_run(self,func,*args):
        self.break_flags=1
        try:
            _thread.start_new_thread (func,args)
        except:
            raise RuntimeError('Unable to start the thread, please check if the format and content of the parameters you passed in are correct' )

    def Color_recognition(self,args,hmirror=1):
        cmd="AI_run=Easy_AI.Easy_AI_thread(Easy_AI.Color_recognition,"+str(args)+","+str(hmirror)+")\n"+"AI_run.keep_run()\n"
        self.repl.exec_(cmd)
        self.uart_ret()

    def Classification(self,hmirror=1):
        cmd="AI_run=Easy_AI.Easy_AI_thread(Easy_AI.Classification,"+str(hmirror)+")\n"+"AI_run.keep_run()\n"
        self.repl.exec_(cmd)
        self.uart_ret()
    
    def Face_recognition(self,hmirror=1):
        cmd="AI_run=Easy_AI.Easy_AI_thread(Easy_AI.Face_recognition,"+str(hmirror)+")\n"+"AI_run.keep_run()\n"
        self.repl.exec_(cmd)
        self.uart_ret()
    
    def Mnist(self,hmirror=1):
        cmd="AI_run=Easy_AI.Easy_AI_thread(Easy_AI.Mnist,"+str(hmirror)+")\n"+"AI_run.keep_run()\n"
        self.repl.exec_(cmd)
        self.uart_ret()
        

    def uart_ret(self):
        while 1:
            pass
            ret=self.repl.read_until(min_num_bytes=1,ending=b"\n").strip()
            ret=str(ret,'utf-8')
            print(ret)
            
    
    def break_func(self):
        self.break_flags=2
        self.Serial.write(str(self.break_flags))
    
    def test(self):
        cmd="Easy_AI_thread(Easy_AI.Color_recognition,1)"
        self.repl.exec_(cmd)
        self.uart_ret()

