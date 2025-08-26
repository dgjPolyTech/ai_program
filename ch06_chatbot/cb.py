import streamlit as st #streamlit 라이브러리를 가져와(import), st라는 이름으로 사용
from openai import OpenAI #openai 패키지에서 OpenAI 클래스 import. gpt 모델을 직접적으로 사용하기 위해 불러오는 부분

# 1. 프로그램의 주요 로직이 들어갈 main() 함수 선언.
def main():
    # 2. 메인 페이지 화면 구성
    st.set_page_config(layout = "wide") # 구조를 wide(양 화면 꽉 차게)로 구성. 외에는 centered 옵션도 있음.
    st.title("친근한 AI 챗봇(셀프)") # 페이지 상단 제목 추가
    st.caption("스트림릿과 OpenAI API를 활용한 간단한 챗봇") # 제목 아래에 작은 글씨로 제목 생성

     # 아래처럼, markdown 언어로 스타일 지정하면 스트림릿 관련 css 설정도 가능함.
    # st.markdown(
    #     """
    #     <style>
    #     body {
    #         background-color: #f0f2f6; /* 연한 회색 배경 */
    #     }
    #     .stApp {
    #         background-color: #f0f2f6; /* Streamlit 앱 전체의 배경색 */
    #     }
    #     /* 추가적인 CSS 스타일을 여기에 작성할 수 있습니다. */
    #     /* 예: 사이드바 배경색 변경 */
    #     .css-vk325g.e1fqkh3o1 { /* Streamlit 사이드바 컴포넌트 클래스 */
    #         background-color: #e0e2e6;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True # HTML 태그를 허용해야 CSS가 적용됩니다.
    # )
    
    # 3. sidebar 추가(이미 만들어진 것 사용)(메인과 별개임)
    # with ~: ~안에 요소를 렌더링 시킬 때 사용함.
    with st.sidebar:
        st.subheader("OpenAI API Key 설정") # 사이드바 제목
        openai_api_key = st.text_input("OpenAI API Key", type="password") # apiKey를 password 형태로 입력 받아, openai_api_key라는 변수에 저장.
        st.write("[OpenAI API Key 받기]")
        # st.caption("여기도 캡션 되나?") # 이곳에 작성 시, 사이드바에 캡션 추가하게 됨.

    # ai의 답변 스타일을 설정하는 시스템 프롬프트 설정(향후 직접 입력 받게끔 할 예정)
    system_message = """
    너의 이름은 친구 봇이야.
	너는 항상 반말을 하는 챗봇이야. 절대로 다나까 같은 높임말을 사용하지 마.
	항상 반말로 친근하게 대답해줘.
	영어로 질문을 받아도 무조건 한글로 대답해줘.
	한글이 아닌 답변을 하게 되면 다시 생각해서 답변을 꼭 한글로 만들어줘.
	모든 답변 끝에 답변에 맞는 이모티콘도 추가해줘.
    """

    # 세션에 이전 메시지에 대한 내용이 없으면, 프롬프트를 토대로 답변
    # 세션: 프로그램이 한번 실행되는 동안 생기는 일종의 임시 저장공간.
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": 'system', "content": system_message}]

    # 반복문 초기 시작값
    idx = 0

    for message in st.session_state.messages:
        # 이전 메시지가 있으면(idx > 0), 화면 상에 다시 그려주는 부분
        if idx > 0:

            with st.chat_message(message["role"]):
                st.write(message["content"])
        idx = idx + 1
    
    # client = 위에서 임포트한 OpenAI 객체. 사용자가 입력한 api_key를 지닌. 
    # client는 OpenAI의 여러가지 기능을 활용하게끔 해주는 객체라고 볼 수 있음.
    client = OpenAI(api_key=openai_api_key) 

    user_input = st.chat_input("무엇이 궁금하신가요?") # 채팅창 생성. () 안은 채팅창 안에 입력될 문구

    # 사용자가 입력하면, 아래의 동작이 실행됨.
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        # 사용자의 채팅 메시지를 표시
        with st.chat_message("user"):
            st.write(user_input) # 입력값을 채팅창 형태로 표시.

        # with st.chat_message("assistant"):
        #     st.write("안녕! 난 친구 봇이야")

        # # 챗봇의 대답을 정의하는 구간.
        # with st.chat_message("assistant"):
        #      # 답변을 생성
        #      response = client.chat.completions.create( # client.chat.completions.create(model, message, stream...) <- OpenAI로부터 응답을 받아오는 함수
        #           model = "gpt-4o-mini", # 답변에 사용할 모델(gpt-4o-mini)
        #           messages=[{"role": "assistant", "content": user_input}], # ai의 역할/대화 내용 전달
        #           stream = True, # 답변을 받는 방식. stream=True이면, ai가 실시간으로 답변을 작성함. false이면 ai가 문장이 다 작성되었을 때 답변을 함.
        #      )

        # # 답변을 유저 메시지 형태로 작성함.
        # st.write_stream(response)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = st.session_state.messages,
                stream=True,
            )

            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})

# 대충 파이썬 파일이 "직접" 실행되었을 때만 실행하라는 의미 
if __name__ == "__main__":
 	main()