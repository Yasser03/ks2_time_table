# kumon project
#Yasser Mustafa WE. 13/11/2019
from random import randint
import streamlit as st

@st.cache
def get_two_random_numbers(n):
    x = randint(1, 10)
    y = randint(1, 10)
    return x, y

x, y = get_two_random_numbers( st.number_input('Please enter n ', 1))
result = x * y
st.write(x, ' * ', y , '= ') #, x*y)
st.write('_________')

answer = st.number_input('Please enter your answer ', 1)

if st.button("Submit"):
    if  answer == result:
        st.write('Your answer is', answer)
        st.write('The correct answer is', result)
        st.success('الاجابة صحيحة')
        st.balloons()
        
    else:
        st.write('Your answer is', answer)
        st.write('The correct answer is', result)
        st.warning("OOOPS, please try again!")
