from email.header import decode_header
import imaplib
import email

# (1) 메일 수신 함수 정의
def fetch_emails(email_id: str, email_password: str):
    try:
        mail = imaplib.IMAP4_SSL("imap.naver.com")
        mail.login(email_id, email_password)
        # (2) 수신 메일함 선택
        mail.select("inbox")
        result, data = mail.search(None, "ALL")
        # (3) 최근 메일 열 개 가져오기
        mail_ids = data[0].split()[-10:]
        fetched_emails = []
        for mail_id in mail_ids:
            result, data = mail.fetch(mail_id, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            # (4) 딕셔너리 선언(메일 발신인/제목 디코딩, 메일 본문 가져오기)
            email_data = {
                "날짜": msg.get("Date"),
                "발신인": decode_mime_words(msg.get("From")),
                "제목": decode_mime_words(msg.get("Subject")),
                "본문": get_email_content(msg),
            }
            fetched_emails.append(email_data)
        # (5) 결과 리스트 반전 및 반환
        fetched_emails.reverse()
        return fetched_emails
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

# (6) 메일 발신인/제목 디코딩 함수 정의
def decode_mime_words(encoded_string):
    if encoded_string is None:
        return ""
    decoded_words = decode_header(encoded_string)
    decoded_string = ""
    for content, charset in decoded_words:
        if isinstance(content, bytes):
            try:
                decoded_string += content.decode(charset or "utf-8")
            except (UnicodeDecodeError, TypeError):
                decoded_string += content.decode("latin1", errors="ignore")
        else:
            decoded_string += content
    return decoded_string
    
# (7) 메일 본문 가져오기 함수 정의
def get_email_content(message):
    if message.is_multipart():
        parts = [get_email_content(part) for part in message.get_payload()
                 if part.get_content_type() == "text/plain"]
        return "\n".join(parts) if parts else ""
    else:
        content_type = message.get_content_type()
        if content_type == "text/plain":
            content = message.get_payload(decode=True)
            if content:
                charset = message.get_content_charset()
                try:
                    return content.decode(charset or "utf-8")
                except (UnicodeDecodeError, TypeError):
                    return content.decode("latin1", errors="ignore")
        return ""

def main():
    naver_id = "네이버_아이디_입력" 
    naver_password = "네이버_비밀번호_입력"
    # (8) 메일 수신 함수 호출
    result = fetch_emails(naver_id, naver_password)
    # (9) 최근에 수신한 메일 출력
    print(result[0])

if __name__ == "__main__":
    main()