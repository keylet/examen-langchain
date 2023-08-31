import os

import streamlit
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
os.environ['OPENAI_API_KEY']='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'
default_doc_name = 'doc.pdf'

def proccess_doc(
    path: str = 'https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf',
    is_local: bool = False,
    question:str='Cuales son los autores del pdf?'
):
   _, loader = os.system(f'curl -o{default_doc_name} {path}'), PyPDFLoader(f"./{default_doc_name}") if not is_local \
        else PyPDFLoader(path)

   doc = loader.load_and_split()

   print(doc[-1])

   db = Chroma.from_documents(doc, embedding=OpenAIEmbeddings())

   qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type='stuff',  retriever = db.as_retriever())

   streamlit.write(qa.run(question))
  # print(qa.run(question))

def client():
    streamlit.title('Manage LLM with LangChain')
    uploader = streamlit.file_uploader('Upload PDF', type='pdf')

    if uploader:
        with open(f'./{default_doc_name}', 'wb') as f:
            f.write(uploader.getbuffer())
        streamlit.success('PDF saved!!')

    question = streamlit.text_input('Generar un resumen de 20 palabras sobre el pdf',
                             placeholder='Give response about your PDF', disabled=not uploader)



if __name__=='__main__':
       client()
       #process_doc()