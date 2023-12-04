import json
import os
import datetime
import langchain
import openai
from langchain.prompts import PromptTemplate
from langchain.llms import AzureOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import AzureChatOpenAI


import warnings
warnings.filterwarnings('ignore')


# OPENAI_API_KEY = "c9c15fe92ffc49d68f1194e1b84320ef"
# OPENAI_DEPLOYMENT_NAME = "content"
# MODEL_NAME = "text-davinci-003"
#
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://cmo-dev-ai.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "099c9c6cf8c945469d6d15d2312fa6de"
# os.environ["DEPLOYMENT_NAME"] = "content_lab"
# os.environ["MODEL_NAME"] = "gpt-4"

openai.api_type = "azure"
# openai.api_version = "2023-09-01-preview"
# openai.api_version = "2023-05-15"
# openai.api_endpoint = "https://cmo-dev-ai.openai.azure.com/"
# openai.api_key = "099c9c6cf8c945469d6d15d2312fa6de"
# openai.deployment_name = "contentlab2"
# openai.model_name = "gpt-35-turbo"


class ContentLab():
    def __init__(self):

        self.llm = AzureChatOpenAI(temperature=0.0,
                               openai_api_key="099c9c6cf8c945469d6d15d2312fa6de",
                               deployment_name="content_lab", model_name="gpt-4")
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
            )

    def what_to_accomplish(self,inp):

        # user_quest = str(json.load(inp)["user_quest"])
        # mar_stages = json.load(inp)["stages"]
        mar_stages = ["Awareness", "Acquisition", "Activation", "Revenue", "Retention", "Referral"]

        prompt_template = PromptTemplate.from_template("Assume a role of marketer but do not acknowledge it in the response.\n \
            Give me a brief explanation to achieve my goal: {user_question}.\n \
            Given the list of {marketing_stages} please provide a stage I should be focusing on based on my goal.\n \
            The output format is a dictionary with one key as text and the value as the explanation and the \
            other key is funnel focus and the value is your recommended funnel focus.")
        edited_prompt = prompt_template.format(user_question=inp, marketing_stages=mar_stages)
        print("prompt ........", edited_prompt)

        response = self.conversation.predict(input=edited_prompt)
        print("response ........", response)

        return response


    def options_in_funnel_focus(self,funnel,user_question):

        # user_quest = str(json.load(inp)["user_quest"])
        # mar_stages = json.load(inp)["stages"]

        prompt_template = PromptTemplate.from_template("My focus now is {funnel_focus} stage in marketing.\n \
             Give me a list of strategies or options that I can consider to achieve {user_quest} \
             in my current focused stage?\n Give me just the option names. Do not provide any explanation or \
             introductions for the list of options.\n The output format is dictionary with key as options and\
              the value is a python list of the options")

        edited_prompt = prompt_template.format(funnel_focus=funnel, user_quest=user_question)
        print("prompt ........", edited_prompt)

        response = self.conversation.predict(input=edited_prompt)
        print("response ........", response)

        return response



    def generate_KPI(self, funnel, strategy, user_question):

        # user_quest = str(json.load(inp)["user_quest"])
        # mar_stages = json.load(inp)["stages"]

        prompt_template = PromptTemplate.from_template("I am planning for a {strategy} marketing strategy to \
            focus on {funnel_focus}.\n Generate a top 5 KPIs I should be analyzing for my {strategy} marketing \
            strategy\n Give me just the list KPI names. Do not provide any explanation or introductions for the list of KPIs.\n \
            The output format is dictionary with key as kpis and the value is a python list of the KPIs")
        edited_prompt = prompt_template.format(funnel_focus=funnel, strategy= strategy)
        print("prompt ........", edited_prompt)

        response = self.conversation.predict(input=edited_prompt)
        print("response ........", response)

        return response

    def generate_activity_theme(self,kpis, kpi_vals, comp):
        prompt_template = PromptTemplate.from_template("Based on the strategy I choose earlier, \
        goal I have choosen and the funnel focus. \n \
        Here are the lists of {Kpi_list} and {Kpi_vals} . I want to achieve corresponding kpi values\
         as an improvement within the strategy and focus. Given that my company is {company}. Give me a \
         list of key product activity themes I can work on to achieve my goal and kpi improvement within my company.\n \
         Activity theme is like a generic theme of solutions or like a category of solutions I can work on \
         to acheive my goal within the choices I made to this point. Do not provide any explanation for the activity themes.\
          Only provide the list of activity themes in the format suggested earlier and try to incorporate company name into the activity themes if necessary")
        edited_prompt = prompt_template.format(Kpi_list=kpis, Kpi_vals=kpi_vals, company = comp)
        print("prompt ........", edited_prompt)

        response = self.conversation.predict(input=edited_prompt)
        print("response ........", response)

        return response

    def priscript_analy_recommendations(self, kpis, kpi_vals, theme):
        prompt_template = PromptTemplate.from_template("As explained earlier, I have this kpi list {Kpi_list} \
         and corresponding kpi improvement values as such {Kpi_vals}. I want to select {activity_theme} \
         from earlier activity themes list. Give me a list of specific Ideas I can implement within my company \
         considering the theme, kpis and my goal. \n \
         Give me a list of prescriptive analyis and recommendations that I can work on to achieve my goal.\n \
         The output format is a dictionary with keys prescriptive analysis, recommendations and Ideas \
         and the values are key bullet points for prescriptive analysis, one line recommendations and a \
         list of Ideas or Idea names.\n \
         Donot provide any explanations, and the ideas can be catchy names inline with the company, activity theme and my goal..")
        edited_prompt = prompt_template.format(Kpi_list=kpis, Kpi_vals=kpi_vals, activity_theme=theme)
        print("prompt ........", edited_prompt)

        response = self.conversation.predict(input=edited_prompt)
        print("response ........", response)

        return response

    def idea_detail_view(self,user_feedback, ai_recom):
        prompt_template = PromptTemplate.from_template("Based on my goal, strategy, kpis, activity theme, \
        {usr_feed}, {ai_rec} and the list of Ideas given I want to go with the best idea among them.\n \
        Give me the Target audience, a campaign Brief (list down my goal, strategy and all the choices \
        I made in this process), production plan and Business case for the Idea.\n \
        Give the output in previously defined output format.")
        edited_prompt = prompt_template.format(usr_feed=user_feedback, ai_rec=ai_recom)
        print("prompt ........", edited_prompt)

        response = self.conversation.predict(input=edited_prompt)
        print("response ........", response)

        return response

def main():

    ContentLab.what_to_accomplish("How can I improve business?")
    ContentLab.options_in_funnel_focus("awareness", "How can I improve business?")
    ContentLab.generate_KPI("awareness","product_marketing", "How can I improve business?")
    ContentLab.generate_activity_theme(["Website traffic", "Social media engagement", "Influencer reach"], ["50%", "50%", "50%"], "paypal")
    ContentLab.priscript_analy_recommendations(["Website traffic", "Social media engagement", "Influencer reach"],
                                       ["50%", "50%", "50%"], "Buy first Pay Later","Improve website traffic and Influencer reach")
    ContentLab.idea_detail_view("PayPal PayLater Boost")

if __name__ == '__main__':
    print('ContentLab')
    main()