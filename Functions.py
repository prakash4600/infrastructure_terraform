import json
import os
import datetime
import langchain
import openai
from langchain.prompts import PromptTemplate
from langchain.llms import AzureOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory, ConversationSummaryBufferMemory, ConversationBufferWindowMemory
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
        # self.memory = ConversationSummaryBufferMemory(llm=self.llm, max_token_limit=300)
        self.memory = ConversationSummaryBufferMemory(llm=self.llm, maxTokenLimit=300)
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
            )

    def what_to_accomplish(self,inp):

        # user_quest = str(json.load(inp)["user_quest"])
        # mar_stages = json.load(inp)["stages"]
        mar_stages = ["Awareness", "Acquisition", "Activation", "Revenue", "Retention", "Referral"]
        out_format = {"funnel_focus": "...", "prompt": inp, "response": "...."}

        prompt_template = PromptTemplate.from_template("Given the list of {marketing_stages} \
         please provide a stage I should be focusing on based on my goal: {user_question}. \
         Also give me a brief explanation to achieve the goal w.r.t the focus stage. \n \
         The output format is like {out_form} where key response correponds to the explanation \
          and key funnel_focus corresponds to the recommended funnel focus. Use only double qoutes for strings.")
        edited_prompt = prompt_template.format(user_question=inp, marketing_stages=mar_stages, out_form=out_format)
        # print("prompt ........", edited_prompt)

        response = self.conversation.predict(input=edited_prompt)
        print("response ........", response)

        return response


    def options_in_funnel_focus(self,funnel):

        # user_quest = str(json.load(inp)["user_quest"])
        # mar_stages = json.load(inp)["stages"]
        out_format = {"options":["","","","",""]}

        prompt_template = PromptTemplate.from_template("I would like to focus on {funnel_focus} stage \
        as my funnel focus in marketing.\n Give me a list of strategies or options that I can consider \
        to achieve the goal mentioned earlier in my current focused stage.\n \
        Give me just the option names.\
        Do not provide any explanation or introductions for the list of options.\n \
        The output format is like {out_form}, the list should contain the options or strategies. \
        Provide upto 7 relevant options in a ranked order. Use only double qoutes for strings.")

        edited_prompt = prompt_template.format(funnel_focus=funnel, out_form=out_format)
        # print("prompt ........", edited_prompt)

        response = self.conversation.predict(input=edited_prompt)
        print("response ........", response)

        return response



    def generate_KPI(self, funnel, strategy, user_question):

        # user_quest = str(json.load(inp)["user_quest"])
        # mar_stages = json.load(inp)["stages"]

        prompt_template = PromptTemplate.from_template("I am planning for a {strategy} strategy focusing \
         on {funnel_focus}.\n Generate top 5 KPIs I should be analyzing for my {strategy} strategy.\n \
         Give me just the list KPI names. Do not provide any explanation or introductions for the list \
         of KPIs.\n The output format is dictionary with key as kpis and the value is a list \
         of the KPIs. Use only double qoutes for strings")
        edited_prompt = prompt_template.format(funnel_focus=funnel, strategy= strategy)
        # print("prompt ........", edited_prompt)

        response = self.conversation.predict(input=edited_prompt)
        # print("response ........", response)

        return response

    def generate_activity_theme(self,kpis, kpi_vals, comp):

        out_format = {"activity_themes": ["", "", "", "", ""]}

        prompt_template = PromptTemplate.from_template("Based on the strategy, goal and funnel focus \
        I chose earlier. \n \
        Here are the lists of {Kpi_list} and {Kpi_vals} . I want to achieve corresponding kpi values\
        as an improvement. Improvement could be percent reduction or increase based on the KPI. \
        Given that my company is {company}. Give me a list of key product activity themes I can work on \
        according to the choices I made to this point to achieve my goal, kpi improvement within my company.\n \
        Activity theme is like a theme or category of marketing solutions any marketer can apply for a company \
        (Examples : Educational series, Referal programs, Email campaigns etc)\
        Only provide the list of upto 7 activity themes ranked w.r.t the relevance with KPIs in the format \
        of a simple text dictionary like {out_form} suggested earlier without any explanations. Use only double qoutes for strings.")
        edited_prompt = prompt_template.format(Kpi_list=kpis, Kpi_vals=kpi_vals, company=comp, out_form=out_format)
        print("prompt ........", edited_prompt)

        response = self.conversation.predict(input=edited_prompt)
        print("response ........", response)

        return response

    def priscript_analy_recommendations(self, kpis, kpi_vals, theme):
        prompt_template = PromptTemplate.from_template("As explained earlier, I have this kpi list {Kpi_list} \
         and corresponding kpi improvement values {Kpi_vals}.\n\
         I want to select {activity_theme} from the suggested activity themes list.\n\
         Give me a list of specific Ideas I can implement within my company considering the theme, kpis and my goal.\n \
         Give me a list of prescriptive analysis and recommendations that I can work on to achieve my goal.\n \
         The output format is a dictionary with keys prescriptive_analysis_recommendations and Ideas \
         and the values are key points for prescriptive analysis, simple recommendations and a \
         list of Ideas or Idea names.\n \
         Do not provide any explanations, and the ideas can be catchy names inline with the company,\
          activity theme and my goal. Use only double qoutes for strings.")
        edited_prompt = prompt_template.format(Kpi_list=kpis, Kpi_vals=kpi_vals, activity_theme=theme)
        # print("prompt ........", edited_prompt)

        response = self.conversation.predict(input=edited_prompt)
        # print("response ........", response)

        return response

    def idea_detail_view(self,user_feedback, ai_recom):
        prompt_template = PromptTemplate.from_template("Based on my goal, strategy, kpis, activity theme, \
        user feedback : {usr_feed}, the prescriptive analytics and recommendations given eralier \
        and the list of Ideas given I want to go with the best idea among them.\n \
        Give me the best idea among the list, final recommendations w.r.t user feedback \
        (use summary as key), target audience I can focus on with the Idea,\
        a campaign Brief (list down my goal, strategy and all the choices \
        I made in this process), production plan and Business case for the Idea.\n \
        Give the output in previously defined output format.\n Ensure all the values in\
         the dictionary are simple texts. Use only double qoutes for strings.")
        edited_prompt = prompt_template.format(usr_feed=user_feedback)
        # print("prompt ........", edited_prompt)

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
    # ContentLab.idea_detail_view("PayPal PayLater Boost")

if __name__ == '__main__':
    print('ContentLab')
    main()