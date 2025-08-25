import smtplib
from email.message import EmailMessage

# (1) 메일 생성 함수 정의
def create_email(to_addr, subject, body, naver_id):
    from_addr = f"{naver_id}@naver.com"
    email_message = EmailMessage()
    email_message["To"] = to_addr
    email_message["From"] = from_addr
    email_message["Subject"] = subject
    email_message.set_content(body)
    return email_message

# (2) 메일 전송 함수 정의
def send_email(message, naver_id, naver_password):
    smtp_server = "smtp.naver.com"
    port = 587
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(naver_id, naver_password)
        server.send_message(message)

def main():
    naver_id = "네이버_아이디_입력" 
    naver_password = "네이버_비밀번호_입력"
    # (3) 메일의 주요 정보 입력
    recipient_email = "받는_사람_메일_주소_입력"
    subject = "테스트 메일"
    body = "안녕하세요. 이 메일은 테스트 메일입니다."
    # (4) 메일 생성 함수 호출
    email_message = create_email(recipient_email, subject, body, naver_id)
    # (5) 메일 전송 함수 호출
    send_email(email_message, naver_id, naver_password)
    print(" 메일이 성공적으로 전송됐습니다!")

if __name__ == "__main__":
    main()