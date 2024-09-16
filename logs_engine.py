from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from chat_engine import ChatEngine

load_dotenv()
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

class LogsChatEngine(ChatEngine):
    def __init__(self):
        self.logs_history = []

    def load_logs_chain(self):
        try:
            llm = self.load_chat_model()
            prompt_template = '''
            You are a AI assistant. Answer the following question considering the history of the conversation:
    
            User question: {query}
    
            Cisco firewall logs: {logs}
            '''
            prompt = ChatPromptTemplate.from_template(template=prompt_template)
            chain = prompt | llm
            return chain
        except:
            print("Issue has been occurred while loading chat model or chat chain....")

    def ask_logs(self, query, logs):
        try:
            response = self.load_logs_chain().invoke({"query": query, "logs": logs})
            self.logs_history.append((query, logs, response.content))
            print("Initiated query and extracted response....")
            print("-" * 100)
            print("Result:")
            return response.content
        except:
            print("Issue has been occurred while querying....")

if __name__=="__main__":
    chat = LogsChatEngine()
    logs = '''
    Sep 16 2024 15:17:04 FW06 : %ASA-3-318109: OSPFv3 has received an unexpected message	0
    Sep 16 2024 15:17:04 FW13 : %ASA-4-400013: IPS:2003 ICMP Redirect 22.164.193.248 to 221.23.198.142 on interface GigabitEthernet0/4	0
    Sep 16 2024 15:17:04 FW07 : %ASA-4-400020: IPS:2010 ICMP Information Reply 163.51.68.161 to 182.249.139.22 on interface GigabitEthernet0/1	0
    Sep 16 2024 15:17:04 FW17 : %ASA-4-400045: IPS:6153 ypupdated (YP update daemon) Portmap Request 148.139.230.251 to 170.241.3.227 on interface GigabitEthernet0/3	0
    Sep 16 2024 15:17:04 FW14 : %ASA-5-507001: Terminating TCP-Proxy connection from GigabitEthernet0/4:151.24.82.42/18660 to GigabitEthernet0/5:152.219.186.9/17760 - reassembly limit of 156000 bytes exceeded	0
    Sep 16 2024 15:17:04 FW08 : %ASA-1-104500: (Primary) Switching to ACTIVE (cause: reason)	0
    Sep 16 2024 15:17:04 FW19 : %ASA-4-400037: IPS:6053 DNS Request for All Records 5.230.132.202 to 63.94.137.206 on interface GigabitEthernet0/0	0
    Sep 16 2024 15:17:04 FW20 : %ASA-6-302033: Pre-allocated H323 GUP Connection for faddr GigabitEthernet0/4: 192.22.190.50/19375 to laddr GigabitEthernet0/1: 172.30.212.165/21673	0
    Sep 16 2024 15:17:04 FW17 : %ASA-4-716022: Unable to connect to proxy server.	0
    Sep 16 2024 15:17:04 FW16 : %ASA-7-713164: The Firewall Server has requested a list of active user sessions	0
    '''
    print(chat.ask_logs("Give me summary.", logs=logs))