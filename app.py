import streamlit as st
import openai
import base64

# Streamlit secrets에서 API 키 로드
openai.api_key = st.secrets["openai_key"]

st.title("사진으로 보는 성격과 인상 분석 웹앱")

uploaded_file = st.file_uploader("사람의 얼굴 사진을 업로드 해주세요", type=["png", "jpg", "jpeg"])

def get_image_base64(image_file):
    image_file.seek(0)  # 스트림 위치 초기화 (중요)
    return base64.b64encode(image_file.read()).decode()

@st.cache_data(show_spinner=False)
def analyze_personality(image_b64):
    prompt = (
        "아래는 사람 얼굴 사진의 base64 인코딩 데이터입니다.\n"
        "이 사람의 사진을 기반으로 상상해서, 성격과 첫 인상에 대해 3~4문장으로 친절하고 전문적으로 설명해줘.\n\n"
        f"사진 데이터: {image_b64[:100]}... (생략)\n\n"
        "참고: 실제 사진 분석은 불가능하지만, AI가 사진을 보고 추론하는 것처럼 설명해줘."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 친절하고 전문적인 성격 분석가입니다."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.8,
    )
    return response['choices'][0]['message']['content']

if uploaded_file:
    st.image(uploaded_file, caption="업로드한 사진", use_column_width=True)
    with st.spinner("분석 중입니다... 잠시만 기다려주세요."):
        try:
            image_b64 = get_image_base64(uploaded_file)
            result = analyze_personality(image_b64)
            st.markdown("### 분석 결과")
            st.write(result)
        except Exception as e:
            st.error(f"분석 중 오류가 발생했습니다: {e}")
