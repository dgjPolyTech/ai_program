import streamlit as st
from openai import OpenAI

# 1. 프로그램의 주요 로직이 들어갈 main() 함수 선언.
def main():
    # 2. 메인 페이지 화면 구성
    st.set_page_config(layout = "wide")
    st.title("나만의 AI 챗봇")
    st.caption("스트림릿과 OpenAI API를 활용한 간단한 챗봇")

    # 3. sidebar 추가
    with st.sidebar:
        st.subheader("OpenAI API Key 설정")
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        st.write("[OpenAI API Key 받기](https://platform.openai.com/account/api-keys)")
        
        model_options = ["gpt-4o-mini", "gpt-4o"]

        with st.popover("⚙️ 설정"):
            st.title("프롬프트 설정하기")
            st.caption("모델 설정")

            select_model = st.selectbox("사용 모델 설정", model_options)
            system_prompt = st.text_area(
                "AI 챗봇의 역할을 정의하는 시스템 프롬프트를 입력하세요",
                value=""
            )

            session_clear = st.checkbox('프롬프트 변경 시 세션 초기화')

            #영역 나누는 가로선
            st.divider()


        # expander: 설정창 추가
        # with st.expander("상세 설정하기."):
        #     st.title("프롬프트 설정하기")
        #     st.caption("프롬프트를 설정해 챗봇의 스타일을 조정하세요.")

        #     system_prompt = st.text_area(
        #         "AI 챗봇의 역할을 정의하는 시스템 프롬프트를 입력하세요:",
        #         value=""
        #     )

    # 기본 프롬프트 값 정의
    default_prompt = """
            너의 이름은 친구 봇이야.
            너는 항상 반말을 하는 챗봇이야. 절대로 다나까 같은 높임말을 사용하지 마.
            항상 반말로 친근하게 대답해줘.
            영어로 질문을 받아도 무조건 한글로 대답해줘.
            한글이 아닌 답변을 하게 되면 다시 생각해서 답변을 꼭 한글로 만들어줘.
            모든 답변 끝에 답변에 맞는 이모티콘도 추가해줘.
        """
    
    # system_prompt의 값이 비어있다면(그냥 if 문에다 사용해도, 값이 있으면 true, 없으면 false로 인식함.), 위에서 설정한 기본 프롬프트 값 사용.
    if not system_prompt:
        system_prompt = default_prompt

    # 세션 상태에 메시지 내용이 없으면 시스템 프롬프트로 초기화
    # 만약 사용자가 직접 입력한 system_prompt가 비어 있다면, default_prompt 사용
    if "messages" not in st.session_state:
        if system_prompt == "":
            st.session_state.messages = [{"role": 'system', "content": system_prompt}]
        else:
            st.session_state.messages = [{"role": 'system', "content": system_prompt}]
    
    # 사용자가 세션 초기화 옵션에 동의 + 사용자가 프롬프트를 변경했을 때, 기존 메시지가 남아있다면 세션을 초기화
    if session_clear and (len(st.session_state.messages) > 0 and st.session_state.messages[0]["content"] != system_prompt):
        # 사용자가 입력한 프롬프트가 비어 있다면 위에서 설정한 기본값으로 설정
        if system_prompt == "":
            st.session_state.messages = [{"role": 'system', "content": system_prompt}]
        else:
            st.session_state.messages = [{"role": 'system', "content": system_prompt}]
        st.rerun()

    if openai_api_key:
        # OpenAI 클라이언트 생성
        client = OpenAI(api_key=openai_api_key) 

        # 반복문 초기 시작값
        idx = 0
        for message in st.session_state.messages:
            # 이전 메시지가 있으면 화면 상에 다시 그려주는 부분
            if idx > 0:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
            idx = idx + 1
        
        user_input = st.chat_input("무엇이 궁금하신가요?")

        # 사용자가 입력하면, 아래의 동작이 실행됨
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model = select_model,
                    messages = st.session_state.messages,
                    stream=True,
                )
                response = st.write_stream(stream)
            
            st.session_state.messages.append({"role": "assistant", "content": response})

    else:
        st.info("사이드바에 OpenAI API Key를 입력해주세요. ")

# 대충 파이썬 파일이 "직접" 실행되었을 때만 실행하라는 의미
if __name__ == "__main__":
    main()