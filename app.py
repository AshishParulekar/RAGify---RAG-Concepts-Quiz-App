# import Statement

import os
import ast
import pandas as pd 
from dotenv import load_dotenv


#load variable 
load_dotenv() 

Euron_Key=os.getenv("Euron_Key")

#Prompt Reading

promptFile=pd.read_excel("Prompt.xlsx")

QuesGenPrompt=AnswerCheckPrompt=promptFile['Prompt'][0]
AnswerCheckPrompt=AnswerCheckPrompt=promptFile['Prompt'][1]
#------------------------------------------------------------------------


#Model Loading 
from euriai import EuriaiClient
client = EuriaiClient(
    api_key=Euron_Key,
    model="gpt-4.1-mini")
response = client.generate_completion(
    prompt=QuesGenPrompt,
    temperature=0.7,
    max_tokens=1000
)

#Output Processing 

Response=response['choices'][0]['message']['content']
Response=Response.replace('{{','{').replace('}}','}')

Test=Response.replace(")","-")
Test=Test.split("\n\n")

QuestionBank=[]
import ast
for Question in Test:
    dictResponse=ast.literal_eval(Question)
    print(dictResponse)
    if type(dictResponse)!= dict:
        print(dictResponse[0])
        QuestionBank.append(dictResponse[0])
    else:
        QuestionBank.append(dictResponse)

# StramlitCode 
import streamlit as st

if 'SubmitButton' not in st.session_state:
    st.session_state['SubmitButton']=False

if st.session_state['SubmitButton']==False:
    user_answers = {}
    for idx,Question in enumerate(QuestionBank):
        if Question['Categary']=='MCQ':
            st.write(idx,)
            st.subheader(f"Q{idx+1}: {Question['Question']}")
            selected = st.radio(f"Select an answer for Q{idx+1}", Question['Options'], key=f"q_{idx+1}")
            user_answers[idx+1] = selected
            # st.session_state['user_answers']=user_answers

        if Question['Categary']=='TF':
            st.write(idx,)
            st.subheader(f"Q{idx+1}: {Question['Question']}")
            selected = st.radio(f"Select an answer for Q{idx+1}", Question['Options'], key=f"q_{idx+1}")
            user_answers[idx+1] = selected
            # st.session_state['user_answers']=user_answers

        if Question['Categary']=='SAQ':
            st.write(idx,)
            st.subheader(f"Q{idx+1}: {Question['Question']}")
            selected = st.text_area(f"Select an answer for Q{idx+1}", key=f"q_{idx+1}")
            user_answers[idx+1] = selected
            # st.session_state['user_answers']=user_answers
        st.session_state['user_answers']=user_answers


    SubmitButton=st.button("Submit")
    if SubmitButton:
        st.session_state['SubmitButton']=True
        st.rerun()

if st.session_state['SubmitButton']==True:
    with st.spinner("Wait>>> Result Generation in processs"):
        st.write(st.session_state['user_answers'])

        #Creating the question Answer Bank send back to LLM 

        QuestionAnswerBank=[]
        for num in range(len(QuestionBank)):
            tempdict=dict()
            tempdict['Categary']=QuestionBank[num]['Categary']
            tempdict[f"Question No:-{num}"]=QuestionBank[num]['Question']
            tempdict[f"Answer:-"]=st.session_state['user_answers'][num+1]
            QuestionAnswerBank.append(tempdict)

        st.write(QuestionAnswerBank)

    
        AnswerCheckPrompt=AnswerCheckPrompt.format(QuestionAnswerBank=QuestionAnswerBank)
        responseA = client.generate_completion(
        prompt=AnswerCheckPrompt,
        temperature=0.7,
        max_tokens=1000
                    )

        # Output Processing 

        ResponseAnswer=responseA['choices'][0]['message']['content']
        
        tempsplit=ResponseAnswer.split("|,")
        ResultBank=[]
        for result in tempsplit:
            import json
            dictResult=data_dict = json.loads(result)
            ResultBank.append(dictResult)
        st.success("Result is Generated")
        
        for Result in ResultBank:
            for key in list(Result.keys()):
                st.write(f"{key}:- {Result[key]}")
            st.write("=========================================================")
            st.write()

        Resetbutton=st.button("Reset")
        if Resetbutton:
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()






  



