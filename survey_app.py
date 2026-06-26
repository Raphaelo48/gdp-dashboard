import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

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

# --- ИНИЦИАЛИЗАЦИЯ ХРАНИЛИЩА ---
if 'responses' not in st.session_state:
    st.session_state.responses = []

# --- ВСЕ ВОПРОСЫ НА ГЛАВНОЙ СТРАНИЦЕ ---
st.header("📝 Пройдите опрос (10 вопросов)")
st.markdown("---")

# Вопрос 1
age = st.number_input("1. Ваш возраст", min_value=10, max_value=60, value=20, step=1)

# Вопрос 2
study_hours = st.slider("2. Сколько часов в день вы учитесь?", 1, 12, 4)

# Вопрос 3
breakfast = st.radio(
    "3. Как часто вы завтракаете?",
    ["Каждый день", "5-6 раз в неделю", "3-4 раза в неделю", "Редко (1-2 раза)", "Никогда"]
)

# Вопрос 4
meals_per_day = st.selectbox("4. Сколько раз в день вы едите?", [1, 2, 3, 4, 5, "6 и более"])

# Вопрос 5
snacks = st.radio(
    "5. Что вы предпочитаете на перекус?",
    ["Фрукты/овощи", "Орехи/йогурт", "Булочки/печенье", "Чипсы/сухарики", "Не перекусываю"]
)

# Вопрос 6
fastfood_freq = st.select_slider(
    "6. Как часто вы едите фастфуд (бургеры, пицца, картошка фри)?",
    options=["Никогда", "Раз в месяц", "2-3 раза в месяц", "Раз в неделю", "2-3 раза в неделю", "Каждый день"]
)

# Вопрос 7
sweets = st.radio(
    "7. Как часто вы едите сладкое (шоколад, конфеты, торты)?",
    ["Не ем", "Раз в неделю", "2-3 раза в неделю", "Каждый день", "Несколько раз в день"]
)

# Вопрос 8
water = st.select_slider(
    "8. Сколько стаканов воды в день вы выпиваете?",
    options=["Меньше 2", "2-3", "4-5", "6-7", "8 и более"]
)

# Вопрос 9 - разбит на два подвопроса
energy = st.slider("9.1 Оцените вашу энергию в течение дня (1-10)", 1, 10, 5)
sleep_hours = st.slider("9.2 Сколько часов вы спите?", 3, 12, 7)

# Вопрос 10 - разбит на два подвопроса
concentration = st.slider("10.1 Оцените вашу концентрацию на учебе (1-10)", 1, 10, 5)
avg_grade = st.selectbox("10.2 Ваш средний балл (оценка)", ["2", "3", "4", "5", "Не знаю/нет оценок"])

st.markdown("---")

# --- КНОПКА ОТПРАВКИ ---
submitted = st.button("✅ Отправить ответы", use_container_width=True)

# --- ОБРАБОТКА ОТВЕТОВ ---
if submitted:
    # Проверка на заполнение всех вопросов
    st.success("🎉 Спасибо! Ваши данные сохранены.")
    
    # Формируем запись
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
    
    # Сохраняем в session_state
    st.session_state.responses.append(new_record)
    
    # ДОПОЛНИТЕЛЬНО: Сохраняем в CSV-файл (чтобы не терялись при перезапуске)
    df_all = pd.DataFrame(st.session_state.responses)
    df_all.to_csv("survey_data.csv", index=False, encoding='utf-8-sig')
    
    # --- ПОКАЗЫВАЕМ РЕЗУЛЬТАТ ---
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
    
    # --- ОБЩАЯ СТАТИСТИКА ---
    if len(st.session_state.responses) > 1:
        st.subheader("📈 Статистика по всем участникам")
        
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
        ax2.bar(breakfast_group['Завтрак'], breakfast_group['Энергия'], 
                color=['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#F44336'])
        ax2.set_ylabel('Средняя энергия')
        ax2.set_title('Влияние завтрака на энергию')
        ax2.set_ylim(0, 10)
        st.pyplot(fig2)
        
        # Таблица со всеми ответами
        with st.expander("📊 Полная таблица ответов"):
            st.dataframe(df)
            
            # Кнопка скачивания
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Скачать данные (CSV)",
                data=csv,
                file_name=f"survey_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
            )
    else:
        st.info("👥 Пригласите друзей! Вы первый участник.")

# --- ИНСТРУКЦИЯ ПРИ ПЕРВОМ ПОСЕЩЕНИИ ---
else:
    st.markdown("""
    ### 📝 Заполните все вопросы и нажмите "Отправить"
    
    **Что вы узнаете:**
    - Как ваш режим питания влияет на концентрацию
    - Сравнение с другими участниками
    - Персональные рекомендации
    
    ⏱ Время заполнения: 2-3 минуты
    """)
    
    # Приятная заглушка
    st.markdown("""
    <div style="text-align: center; padding: 30px; background: #f0f2f6; border-radius: 10px; margin-top: 20px;">
        <h1 style="font-size: 60px;">🍎📚</h1>
        <h3 style="color: #444;">Здоровое питание = Острый ум</h3>
        <p style="color: grey;">Исследование для школьников и студентов</p>
    </div>
    """, unsafe_allow_html=True)
