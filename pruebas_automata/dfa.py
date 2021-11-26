from tkinter import messagebox

class DFA:
    def __init__(self) -> None:
        pass
    def step_dfa(self,DFA, q, key):
        q = q.replace('{',"")
        q = q.replace('}',"")
        try:
            assert(key in DFA["S"])
        except AssertionError:
            messagebox.showerror(title='No encontrado',message=f'El Símbolo {key} no se encuentra en el alfabeto')
        try:
            assert(q in DFA["Q"])
        except AssertionError:
            messagebox.showerror(title='No encontrado',message=f'El Estado {q} no se encuentra en el Autómata')
        try:
            return DFA["D"][(q,key)]
        except KeyError:
            return False

    def run_dfa(self,word, DFA):
        initial_state = DFA["q0"]
        if word=="":
            return initial_state
        else:
            res_step = self.step_dfa(DFA, initial_state, word[0])
            if res_step == False: return res_step
            return self.run_dfa_h(DFA, word[1:], res_step)

    def accepts_dfa(self,word,DFA):
        res = self.run_dfa(word, DFA)
        if res == False: return res
        return  res in DFA["F"]

    def run_dfa_h(self,DFA, word, q):
        if word=="":
            return q
        else:
            current_step = self.step_dfa(DFA, q, word[0])
            if current_step == False: return current_step
            return self.run_dfa_h(DFA, word[1:], current_step)