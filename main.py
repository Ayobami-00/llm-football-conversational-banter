import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
import pandas as pd
from pulp import *
from typing import Optional
import random

os.environ['OPENAI_API_KEY'] = "<YOUR OPENAI API KEY>"


class ConversationModel:
    
    def __init__(self, model_name: str, system_message: str, human_name: str):
        self.model = ChatOpenAI(name=model_name)
        self.system_message = system_message
        self.human_name = human_name
        self.conversation_history = [SystemMessage(content=system_message)]
        
    def handle_prompt(self, prompt):
        
        self.conversation_history.append(HumanMessage(content=prompt))
        
        result = self.model.invoke(self.conversation_history)

        print(f"{self.human_name}: {result.content} \n")
        
        self.conversation_history.append(AIMessage(content=result.content))
        
        return result.content

class ConversationPair:
    
    def __init__(self, model_a: ConversationModel, model_b: ConversationModel):
        self.model_a = model_a
        self.model_b = model_b
        
    def start_conversation(self, initial_prompt: str, steps: int = 5):
        
        response_a = self.model_a.handle_prompt(initial_prompt)

        print(f"Ife: {response_a}\n")
        
        for _ in range(steps):
            
            response_b = self.model_b.handle_prompt(response_a)
            print(f"Tunde: {response_b}\n")
            response_a = self.model_a.handle_prompt(response_b)
            print(f"Ife: {response_a}\n")
        
        return self.model_a.conversation_history + self.model_b.conversation_history


class ThreeWayConversation:
    
    def __init__(self, model_a: ConversationModel, model_b: ConversationModel, model_c: ConversationModel):
        
        self.models = [model_a, model_b, model_c]
        
        self.last_model_index = None
        
    def start_conversation(self, initial_prompt: str, steps: int = 5):
        
        current_prompt = initial_prompt
        
        for _ in range(steps):
            
            available_models = [i for i in range(3) if i != self.last_model_index]
            
            next_model_index = random.choice(available_models)
            
            next_model = self.models[next_model_index]
            
            self.last_model_index = next_model_index
            
            current_prompt = next_model.handle_prompt(current_prompt)
        
        # Collect and return the full conversation history
        return sum([model.conversation_history for model in self.models], [])




model_a = ConversationModel(
    model_name="gpt-4", 
    human_name="Ife",
    system_message=
    """
    You are a fiercely loyal Manchester United fan, convinced that your team has the richest history and legacy in football. 
     
     You believe that Manchester United's historical success, legendary players, and iconic moments make them superior to any other team, especially Chelsea. 
     
     Your objective is to argue passionately that Manchester United is the greatest football club in history, using trophies, key matches, and influential figures as evidence.
     
     Defend Manchester United with unwavering confidence, countering any claims that Chelsea or Arsenal have a more impressive history

     Make each response 2 or 3 sentences short an straight to the point and feel free to add a lot of subtle banters to the conversation.

     Your name is Ife.
    .
    
    """
    )

model_b = ConversationModel(
    model_name="gpt-4", 
    human_name="Tunde",
    system_message=
     """
    You are a die-hard Chelsea fan, absolutely certain that your team's historical achievements and recent dominance set them apart as the best football club. 
     
     You believe that Chelsea's success in domestic and European competitions, coupled with the influence of world-class players and managers,
     
     makes them superior to any other team, especially Manchester United. Your goal is to argue fervently that Chelsea's history is more impressive, 
     
     focusing on key trophies, pivotal moments, and influential figures. Always maintain a strong stance that Chelsea outshines Manchester United and Arsenal in every aspect.

     Make each response 2 or 3 sentences short an straight to the point and feel free to add a lot of subtle banters to the conversation.

     Your name is Tunde.
    
     """
)

model_c = ConversationModel(
    model_name="gpt-4", 
    human_name="Phillip",
    system_message=
     """
     You are a passionate Arsenal fan, devoted to defending the club's rich history and legacy. 
     
     You believe that Arsenal's tradition of excellence, legendary players, and iconic moments make them one of the greatest football clubs in history. 
     
     Your goal is to argue that Arsenal's historical success, particularly their undefeated 'Invincibles' season and their longstanding presence in the top tier of English football, places them above Manchester United and Chelsea. Use historical data, trophies, and the influence of key figures to support your case, and never concede that Manchester United or 
     
     Chelsea have a more impressive history.

    Make each response 2 or 3 sentences short an straight to the point and feel free to add a lot of subtle banters to the conversation.

     Your name is Phillip.
     """
)

# conversation_pair = ConversationPair(model_a, model_b)
# conversation_history = conversation_pair.start_conversation(initial_prompt="Hello, Ife!", steps=10)

three_way_convo = ThreeWayConversation(model_a, model_b, model_c)

conversation_history = three_way_convo.start_conversation(initial_prompt="Which team has the most impressive history?", steps=30)