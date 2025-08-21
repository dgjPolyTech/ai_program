import streamlit as st
from openai import OpenAI

# 여행 일정 함수 정의
def generate_travel_plan(city, client):
	prompt = """
	## 요청 사항
	너는 여행 계획 전문가야.
	- 입력받은 도시에 대해 오전, 오후, 저녁으로 나눠 여행 일정을 작성해.
	- 오전, 오후, 저녁 일정은 반드시 1. 오전:, 2. 오후:, 3. 저녁:으로 시작해.
	- 각 일정마다 4줄씩 bullet point로 작성해.
	- 일정에 대해서만 얘기해.
	- 일정은 구체적이고 친절하게 얘기해.

	## 응답 예시(도시: 이스탄불)
	1. 오전:
	- 아침 일찍 일어나 블루 모스크(술탄 아흐메트 모스크)를 방문하세요. 오전의 햇살 속에서 더욱 아름답습니다.
	- 블루 모스크 내부의 멋진 타일과 아치형 구조를 감상하며 걸어보세요. 무료 입장이 가능합니다.
	- 그 후 아야 소피아를 향해 걸어보세요. 이곳은 역사적으로 중요한 건축물이며 놀라운 도감을 제공합니다.
	- 인근의 정원에서 기념 촬영을 하고, 주변 카페에서 전통적인 터키식 아침 식사를 즐겨보세요.

	2. 오후:
	- 그랜드 바자르를 방문해 현지의 다양한 상품을 구경하고 쇼핑을 즐기세요. 활기찬 분위기를 느낄 수 있습니다.
	- 바자르에서 가까운 스파이스 바자르로 이동해 향신료와 터키 과자를 구입하세요. 향이 그윽한 시장입니다.
	- 점심 식사는 카라쾨이 지역의 유명한 생선 샌드위치를 추천합니다. 신선한 생선의 맛을 즐길 수 있습니다.
	- 점심 식사 후에는 갈라타 다리 근처에서 강가를 따라 산책하며 도시의 풍경을 만끽하세요.

	3. 저녁:
	- 저녁에는 보스포루스 해협 유람선을 타고 도시의 아름다운 야경을 감상하세요. 해가 질 때의 풍경이 특히 장관입니다.
	- 유람선 투어 후 이슬람 문화의 향기를 느낄 수 있는 근처의 레스토랑에서 저녁 식사를 즐기세요.
	- 현지인이 추천하는 터키식 케밥이나 메제 플래터를 주문해보세요. 맛있는 음식과 함께하는 시간이 될 것입니다.
	- 저녁 식사 후에는 거리를 산책하며 이스탄불의 밤 문화와 분위기를 느껴보세요.
	"""
	content = prompt + "\n" + city
	response = client.chat.completions.create(
		model="gpt-4o-mini",
		messages=[{"role": "user", "content": content}],
	)
	return response.choices[0].message.content

# 여행 일정 분할 함수 정의
def parse_schedule(input_text):
	morning_part=input_text.split('1. 오전:')[1].split('2. 오후:')[0].strip()
	afternoon_part=input_text.split('2. 오후:')[1].split('3. 저녁:')[0].strip()
	evening_part=input_text.split('3. 저녁:')[1].strip()
	return [morning_part, afternoon_part, evening_part]

# 이미지 생성 함수 정의
def generate_image_url(prompt: str, client):
	response = client.images.generate(
		model="dall-e-3",
		prompt=prompt,
	)
	return response.data[0].url

def main():
	st.set_page_config(layout="wide")
	st.title("여행 가이드 프로그램")
	with st.sidebar:
		openai_api_key = st.text_input("OpenAI API Key", type="password")
		if openai_api_key:
			client = OpenAI(api_key=openai_api_key)
	# 도시 입력
	user_input = st.text_input(
		"여행 가고 싶은 도시를 입력하세요.",
		value="이스탄불",
	)
	if st.button("여행 계획 작성"):
		if not openai_api_key:
			st.info("계속하려면 OpenAI API Key를 추가하세요.")
			st.stop()
		if not user_input.strip():
			st.warning("요약할 텍스트를 입력하세요.")
			st.stop()
		with st.spinner("작성 중..."):
			travel_plan = generate_travel_plan(user_input, client)
			plan_items = parse_schedule(travel_plan)
			plan_times = ['오전', '오후', '저녁']
			# 시간대별 여행 일정 출력
			for index, item in enumerate(plan_items):
				col1, col2 = st.columns([3, 2])
				with col1:
					st.write("## " + plan_times[index])
					st.write(item)
				with col2:
					# 시간대별 이미지 생성
					image_url = generate_image_url(item, client)
					st.image(image_url)

if __name__ == "__main__":
	main()