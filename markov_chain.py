from os import stat
from turtle import st
import numpy as np

from sim_parameters import HOLDING_TIMES, TRASITION_PROBS

def markov_chain(steps, age):
    start_state = 'H'
    prev_state = start_state
    states = []
    while steps>0:
        possible_states = TRASITION_PROBS[age][prev_state]
        curr_state = np.random.choice(a=list(possible_states),p=list(possible_states.values()))
        if(curr_state == 'H'):
            states.append((curr_state,0))
            steps -= 1
        elif(curr_state == 'D'):
            states.append((curr_state,0))
            steps -= 1
        else:
            if(HOLDING_TIMES['less_5'][curr_state] > steps):
                states.append((curr_state, steps))
            else:    
                states.append((curr_state, HOLDING_TIMES['less_5'][curr_state]))
            steps -= HOLDING_TIMES['less_5'][curr_state]
        
        prev_state = curr_state

    return states

#print(markov_chain(130,'less_5'))