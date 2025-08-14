N = 4 #set max padding length of the tape
class DTM:
    def __init__(self, input_str):
        self.origin = input_str #contains original tape for logging purposes
        self.tape = ''.join(['b']*N)
        self.head_pos = N//2
        self.tape = self.tape[:self.head_pos] + input_str + self.tape[self.head_pos:]
        self.current_state = 'q0'
        """
        Γ : 0,1,b,+,-
        Q : q0,q1,q2,q3 q_add0,q_add1,q_add2,q_add3,q_add4,q_add5 q_sub0,q_sub1,q_sub2,q_sub3,q_sub4,q_sub5 qH qY qN
        S : -1,+1,0 (left,right,halt)
        δ : shown in list below
        Σ ⊂ Γ : symbols in input
        b ∈ Γ - Σ : b (blank symbol)
        """
        self.transitions = {
            
            'q0': { #base table in Fig 1 with operator condtions
                '0': ('q0', '0', +1),
                '1': ('q0', '1', +1),
                'b': ('q1', 'b', -1),
                '+': ('q_add1', 'b', +1),#Jump to addition
                '-': ('q_sub1', 'b', +1)#Jump to subtraction
            },
            'q1': {
                '0': ('q2', 'b', -1),
                '1': ('q3', 'b', -1),
                'b': ('qN', 'b', -1)
            },
            'q2': {
                '0': ('qY', 'b', -1),
                '1': ('qN', 'b', -1),
                'b': ('qN', 'b', -1)
            },
            'q3': {
                '0': ('qN', 'b', -1),
                '1': ('qN', 'b', -1),
                'b': ('qN', 'b', -1)
            },#binary addition code
            'q_add0':{#move right to end of first block
                '0': ('q_add0','0',+1),
                '1': ('q_add0','1',+1),
                'b': ('q_add1','b',+1)
            },
            'q_add1':{#move right to end of second block
                '0': ('q_add1','0',+1),
                '1': ('q_add1','1',+1),
                'b': ('q_add2','b',-1)
            },
            'q_add2':{#subtract 1 in binary
                '0': ('q_add2','1',-1),
                '1': ('q_add3','0',-1),
                'b': ('q_add5','b',+1)
            },
            'q_add3':{#move left to end of first block
                '0': ('q_add3','0',-1),
                '1': ('q_add3','1',-1),
                'b': ('q_add4','b',-1)
            },
            'q_add4':{#add 1 in binary
                '0': ('q_add0','1',+1),
                '1': ('q_add4','0',-1),
                'b': ('q_add0','1',+1)
            },
            'q_add5':{#clean up
                '1': ('q_add5','b',+1),
                'b': ('qH','b',0)
            },
            #binary subtraction code
            'q_sub0':{#move right to end of first block
                '0': ('q_sub0','0',+1),
                '1': ('q_sub0','1',+1),
                'b': ('q_sub1','b',+1)
            },
            'q_sub1':{#move right to end of second block
                '0': ('q_sub1','0',+1),
                '1': ('q_sub1','1',+1),
                'b': ('q_sub2','b',-1)
            },
            'q_sub2':{#subtract 1 in binary from second block
                '0': ('q_sub2','1',-1),
                '1': ('q_sub3','0',-1),
                'b': ('q_sub5','b',+1)
            },
            'q_sub3':{#move left to end of first block
                '0': ('q_sub3','0',-1),
                '1': ('q_sub3','1',-1),
                'b': ('q_sub4','b',-1)
            },
            'q_sub4':{#subtract 1 in binary from first block
                '0': ('q_sub4','1',-1),
                '1': ('q_sub0','0',+1),
                'b': ('q_sub0','1',+1)
            },
            'q_sub5':{#clean up leading zeroes
                '0': ('q_sub5','b',+1),
                'b': ('qH','b',0),
                '1': ('qH','1',0)
            },
            'qH': {},
            'qY': {},
            'qN': {}
        }
    
    def step(self):
        if self.current_state in ('qH','qY', 'qN'):
            return False  # Halted, no step taken
        current_symbol = self.tape[self.head_pos]
        curr_transition = self.transitions[self.current_state]
        if current_symbol not in curr_transition:
            raise RuntimeError(f"No transition from state {self.current_state} on symbol {current_symbol}")
        #print(self.current_state,curr_transition[current_symbol], self.head_pos,"\n")
        # Write symbol
        if curr_transition:
            next_state, write_symbol, move_dir = curr_transition[current_symbol]
            self.tape = self.tape[:self.head_pos] + write_symbol + self.tape[self.head_pos+1:]
            # Move head
            if move_dir != 0:
                self.head_pos += move_dir
            # Update state
            self.current_state = next_state
        return True
    
    def run(self):
        num_transitions = 0
        curr_state = self.tape[:self.head_pos]
        print("Current state:"+curr_state)
        log = ""
        try:
            while self.step():
                num_transitions += 1
                curr_state = ""
                for _ in range(self.head_pos):
                    if self.tape[_] != 'b':
                        curr_state = curr_state + str(self.tape[_])
                log = log + "Current state:"+curr_state+"\n"
                if num_transitions > 1000:#meant for transitions that take too long or loop infinitely
                    raise RecursionError("Expected computation time exceeded")
        except Exception as e:
            print(e,", aborting operation")
            return False, ""
        if num_transitions > 30:
            print("Outputting log to file output.txt")
            file = open("output.txt","a")
            file.write("Input: "+self.origin+"\n\n")
            file.write(log+"\n")
            file.write(curr_state+"\n")
            file.close()
            print("Finished state:"+curr_state)
            return self.current_state == 'qY',""
        else: 
            print(log)
            return self.current_state == 'qY',curr_state
    