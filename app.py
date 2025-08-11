# import Statement

import os
import ast
import pandas as pd 
from dotenv import load_dotenv
import streamlit as st 
import ast

#load variable 

load_dotenv() 
Euron_Key=os.getenv("Euron_Key")

st.set_page_config('RAGiFY-Rag Concepts Quiz',page_icon=":sunrise:",layout="wide")
st.header(" '🌈 ' Welcome To RAGIFY:-RAG concepts QUIZ")


# init Seeesion_state

if 'StartQuiz' not in st.session_state:
   st.session_state['StartQuiz']=False

#------

if 'isQuestionGenerated' not in st.session_state:
    st.session_state['isQuestionGenerated']=False

if 'isAnswerGenerated' not in st.session_state:
      st.session_state['isAnswerGenerated']=False

if 'isSubmitAnswer' not in st.session_state:
    st.session_state['isSubmitAnswer']=False

#------------------------------------------------------------------

if st.session_state['isSubmitAnswer']==False:
    if st.session_state['isQuestionGenerated']==False:
        StartButton=st.button("Start the Quiz",icon="👋")
        if StartButton:
            st.session_state['StartQuiz']=True
        
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


#--------------------------------------------------------------------------

if st.session_state['StartQuiz']==True:
    with st.spinner("Generating Question   Please wait...."):
        response = client.generate_completion(
                prompt=QuesGenPrompt,
                temperature=0.7,
                max_tokens=1000
        )

        #Output Processing 

        Response=response['choices'][0]['message']['content']
        Response=Response.replace('{{','{').replace('}}','}')

        Response=Response.replace(")","-")
        Responselst=Response.split("\n\n")
        st.session_state['QuestionBank']=[]
        for Question in Responselst:
            dictResponse=ast.literal_eval(Question)
            if type(dictResponse)!= dict:
                st.session_state['QuestionBank'].append(dictResponse[0])
            else:
                st.session_state['QuestionBank'].append(dictResponse)

        st.session_state['isQuestionGenerated']=True
 
    st.session_state['StartQuiz']=False
    st.rerun()

if st.session_state['isQuestionGenerated']==True:
    user_answers = {}
    for idx,Question in enumerate(st.session_state['QuestionBank']):
        if Question['Categary']=='MCQ':
            st.subheader(f"Q{idx+1}: {Question['Question']}")
            selected = st.radio(f"Select an answer for Q{idx+1}", Question['Options'], key=f"q_{idx+1}")
            user_answers[idx+1] = selected
                    # st.session_state['user_answers']=user_answers

        if Question['Categary']=='TF':
            st.subheader(f"Q{idx+1}: {Question['Question']}")
            selected = st.radio(f"Select an answer for Q{idx+1}", Question['Options'], key=f"q_{idx+1}")
            user_answers[idx+1] = selected
            # st.session_state['user_answers']=user_answers

        if Question['Categary']=='SAQ':
            st.subheader(f"Q{idx+1}: {Question['Question']}")
            selected = st.text_area(f"Select an answer for Q{idx+1}", key=f"q_{idx+1}")
            user_answers[idx+1] = selected
                    # st.session_state['user_answers']=user_answers
    st.session_state['userAnswers']=user_answers

if st.session_state['isAnswerGenerated']==False:
    if st.session_state['isQuestionGenerated']==True:
        SubmitButton=st.button("SubmitAnswer")

        if SubmitButton:
            st.session_state['isSubmitAnswer']=True
            st.session_state['isQuestionGenerated']=False
            st.rerun()

if st.session_state['isSubmitAnswer']==True:
        with st.spinner("Wait>>> Result Generation in processs"):
            #Creating the question Answer Bank send back to LLM 

            QuestionAnswerBank=[]
            for num in range(len(st.session_state['QuestionBank'])):
                tempdict=dict()
                tempdict['Categary']=st.session_state['QuestionBank'][num]['Categary']
                tempdict[f"Question No:-{num}"]=st.session_state['QuestionBank'][num]['Question']
                tempdict[f"Answer:-"]=st.session_state['userAnswers'][num+1]
                QuestionAnswerBank.append(tempdict)
        
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
            st.session_state['isAnswerGenerated']=True
            
            for Result in ResultBank:
                for key in list(Result.keys()):
                    st.write(f"{key}:- {Result[key]}")
                st.write("=========================================================")
                st.write()
           
if 'isSubmitAnswer' in st.session_state:
    if st.session_state['isSubmitAnswer']==True:  
        Resetbutton=st.button("Reset")
        st.session_state['isSubmitAnswer']=False
        if Resetbutton:
            for key in st.session_state.keys():
                del st.session_state[key]
                st.rerun()

            



                





