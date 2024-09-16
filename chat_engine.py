import os
from dotenv import load_dotenv
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

load_dotenv()
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

class ChatEngine():
    def __init__(self):
        self.chat_history = []

    def gemini_embeddings(self):
        try:
            gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)
            print("Initiated gemini embeddings model....")
            return gemini_embeddings
        except:
            print("Issue has been occurred while initiating the gemini model....")

    def load_pdf_and_generate_embeddings(self, document_path):
        try:
            loader = PyPDFLoader(document_path)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = text_splitter.split_documents(documents=documents)
            gemini_embeddings = self.gemini_embeddings()
            vectorstore = Chroma.from_documents(documents=docs, embedding=gemini_embeddings, persist_directory="./embeddings")
            print("Generated gemini embeddings and stored in local....")
            return vectorstore
        except:
            print("Issue has been occurred while generating embeddings....")

    def load_embeddings(self):
        try:
            gemini_embeddings = self.gemini_embeddings()
            vectorstore = Chroma(persist_directory="./embeddings", embedding_function=gemini_embeddings)
            print("Loading embeddings from the local....")
            return vectorstore.as_retriever()
        except:
            print("Issue has been occurred while loading embeddings....")

    def load_chat_model(self):
        try:
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                                         temperature=0,
                                         top_p=0.85,
                                         api_key=GEMINI_API_KEY
                                         )
            print("Initiated chat model...")
            return llm
        except:
            print("Issue has been occurred while loading chat model....")

    def load_rag_chain(self):
        try:
            llm = self.load_chat_model()
            system_instruction = """ 
            As an AI assistant, you must answer the query from the user in english language 
            only from the retrieved content, if no relevant information is available, answer 
            the question by using your knowledge about the topic"""

            template = (
                f"{system_instruction} "
                "Combine the chat history{chat_history} and follow up question into"
                "a standalone question to answer from the {context}. "
                "Follow up question: {question}"
            )

            prompt = PromptTemplate.from_template(template)
            chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.load_embeddings(),
                combine_docs_chain_kwargs={'prompt': prompt},
                chain_type="stuff"
            )
            print("Initiated RAG chain...")
            return chain
        except:
            print("Issue has been occurred while loading RAG chain....")

    def ask_pdf(self, query):
        try:
            response = self.load_rag_chain()({"question":query,"chat_history": self.chat_history})
            self.chat_history.append((query, response["answer"]))
            print("Initiated query and extracted response....")
            print("-"*100)
            print("Result:")
            return response['answer']
        except:
            print("Issue has been occurred while querying....")

if __name__=="__main__":
    chat = ChatEngine()
    print(chat.ask_pdf("How to Check the Software and Install a New Version?"))

