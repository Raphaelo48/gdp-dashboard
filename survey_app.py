import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(
    page_title="Питание и успеваемость",
    page_icon="🧠",
    layout="centered"
)

# --- ЗАГОЛОВОК ---
st.title("🧠 Питание и успеваемость: исследование")
st.markdown("*10 вопросов о связи режима питания, фастфуда и концентрации*")
st.markdown("---")

# --- БОКОВАЯ ПАНЕЛЬ (все 10 вопросов) ---
with st.sidebar:
    st.header("📝 Анкета (10 вопросов)")
    st.markdown("---")
    
    # Вопрос 1: Возраст
    age = st.number_input("1. Ваш возраст", min_value=10, max_value=60, value=20, step=1)
    
    # Вопрос 2: Режим учебы
    study_hours = st.slider("2. Сколько часов в день вы учитесь?", 1, 12, 4)
    
    # Вопрос 3: Завтрак
    breakfast = st.radio(
        "3. Как часто вы завтракаете?", 
        ["Каждый день", "5-6 раз в неделю", "3-4 раза в неделю", "Редко (1-2 раза)", "Никогда"]
    )
    
    # Вопрос 4: Количество приемов пищи
    meals_per_day = st.selectbox("4. Сколько раз в день вы едите?", [1, 2, 3, 4, 5, "6 и более"])
    
    # Вопрос 5: Перекусы
    snacks = st.radio(
        "5. Что вы предпочитаете на перекус?",
        ["Фрукты/овощи", "Орехи/йогурт", "Булочки/печенье", "Чипсы/сухарики", "Не перекусываю"]
    )
    
    # Вопрос 6: Частота фастфуда (ключевой вопрос!)
    fastfood_freq = st.select_slider(
        "6. Как часто вы едите фастфуд (бургеры, пицца, картошка фри)?",
        options=["Никогда", "Раз в месяц", "2-3 раза в месяц", "Раз в неделю", "2-3 раза в неделю", "Каждый день"]
    )
    
    # Вопрос 7: Сладкое
    sweets = st.radio(
        "7. Как часто вы едите сладкое (шоколад, конфеты, торты)?",
        ["Не ем", "Раз в неделю", "2-3 раза в неделю", "Каждый день", "Несколько раз в день"]
    )
    
    # Вопрос 8: Вода
    water = st.select_slider(
        "8. Сколько стаканов воды в день вы выпиваете?",
        options=["Меньше 2", "2-3", "4-5", "6-7", "8 и более"]
    )
    
    # Вопрос 9: Энергия и сон
    energy = st.slider("9. Оцените вашу энергию в течение дня (1-10)", 1, 10, 5)
    sleep_hours = st.slider("   Сколько часов вы спите?", 3, 12, 7)
    
    # Вопрос 10: Самооценка концентрации и успеваемости
    concentration = st.slider("10. Оцените вашу концентрацию на учебе (1-10)", 1, 10, 5)
    avg_grade = st.selectbox("   Ваш средний балл (оценка)", ["2", "3", "4", "5", "Не знаю/нет оценок"])
    
    st.markdown("---")
    submitted = st.button("✅ Отправить ответы", use_container_width=True)

# --- ОСНОВНАЯ ОБЛАСТЬ ---
if 'responses' not in st.session_state:
    st.session_state.responses = []

if submitted:
    # Формируем запись из 10 вопросов
    new_record = {
        "Возраст": age,
        "Часы учебы": study_hours,
        "Завтрак": breakfast,
        "Приемов пищи": meals_per_day,
        "Перекус": snacks,
        "Фастфуд": fastfood_freq,
        "Сладкое": sweets,
        "Вода": water,
        "Энергия": energy,
        "Сон": sleep_hours,
        "Концентрация": concentration,
        "Средний балл": avg_grade,
        "Время": datetime.now().strftime("%H:%M")
    }
    
    st.session_state.responses.append(new_record)
    st.success("🎉 Спасибо! Ваши данные сохранены.")
    
    # --- ПЕРСОНАЛЬНЫЙ РЕЗУЛЬТАТ ---
    st.subheader("📊 Ваш профиль питания и успеваемости")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Концентрация", f"{concentration}/10")
        if concentration >= 8:
            st.success("🔥 Отличная концентрация!")
        elif concentration >= 5:
            st.warning("📈 Хорошо, но есть потенциал для роста")
        else:
            st.error("🧐 Возможно, питание влияет на фокус")
    
    with col2:
        st.metric("Энергия", f"{energy}/10")
        st.caption(f"Сон: {sleep_hours} ч.")
    
    with col3:
        st.metric("Фастфуд", fastfood_freq)
        if fastfood_freq in ["Каждый день", "2-3 раза в неделю"]:
            st.warning("🍔 Попробуйте сократить")
        else:
            st.success("✅ Хороший баланс!")
    
    # --- СВОДНАЯ ТАБЛИЦА ОТВЕТОВ ---
    with st.expander("📋 Посмотреть все мои ответы"):
        df_single = pd.DataFrame([new_record])
        st.dataframe(df_single.T, use_container_width=True)
    
    # --- АНАЛИТИКА ПО ВСЕМ УЧАСТНИКАМ (если их больше 1) ---
    if len(st.session_state.responses) > 1:
        st.subheader("📈 Общая статистика опроса")
        
        df = pd.DataFrame(st.session_state.responses)
        
        # График 1: Фастфуд vs Концентрация
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        fastfood_group = df.groupby('Фастфуд')['Концентрация'].mean().sort_values().reset_index()
        ax1.barh(fastfood_group['Фастфуд'], fastfood_group['Концентрация'], color='coral')
        ax1.set_xlabel('Средняя концентрация')
        ax1.set_title('Связь фастфуда и концентрации')
        st.pyplot(fig1)
        
        # График 2: Завтрак vs Энергия
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        breakfast_group = df.groupby('Завтрак')['Энергия'].mean().reset_index()
        ax2.bar(breakfast_group['Завтрак'], breakfast_group['Энергия'], color=['#4CAF50', '#FFC107', '#F44336'])
        ax2.set_ylabel('Средняя энергия')
        ax2.set_title('Влияние завтрака на энергию')
        ax2.set_ylim(0, 10)
        st.pyplot(fig2)
        
        # Показать все данные
        with st.expander("📊 Полная таблица ответов"):
            st.dataframe(df)
            
            # Кнопка для скачивания
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Скачать данные (CSV)",
                data=csv,
                file_name=f"survey_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
    else:
        st.info("👥 Пригласите друзей! Сейчас вас один, а для статистики нужно больше данных.")

# --- ПРИВЕТСТВИЕ ---
else:
    st.markdown("""
    ### 👈 Заполните анкету (10 вопросов) и нажмите "Отправить"
    
    **Что вы узнаете:**
    - Как ваш режим питания влияет на концентрацию
    - Сравнение с другими участниками
    - Персональные рекомендации
    
    ⏱ Время заполнения: 2-3 минуты
    """)

    # Красивая заглушка
    st.markdown("""
    <div style="text-align: center; padding: 30px; background: #f0f2f6; border-radius: 10px;">
        <h1 style="font-size: 60px;">🍎📚</h1>
        <h3 style="color: #444;">Здоровое питание = Острый ум</h3>
        <p style="color: grey;">Исследование для школьников и студентов</p>
    </div>
    """, unsafe_allow_html=True)
