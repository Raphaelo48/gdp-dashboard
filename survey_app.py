import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- НАСТРОЙКА СТРАНИЦЫ (делаем красиво) ---
st.set_page_config(
    page_title="Питание и успеваемость",
    page_icon="🧠",
    layout="centered"
)

# --- ЗАГОЛОВОК ---
st.title("🧠 Влияние питания на успеваемость")
st.markdown("*Исследование связи между режимом питания, фастфудом и концентрацией внимания*")

# --- БОКОВАЯ ПАНЕЛЬ (для ввода данных) ---
with st.sidebar:
    st.header("📝 Заполните анкету")
    st.markdown("---")
    
    # 1. Базовые данные
    age = st.number_input("Ваш возраст", min_value=10, max_value=60, value=20)
    study_hours = st.slider("Часов учебы в день", 1, 12, 4)
    
    # 2. Режим питания (используем радиокнопки для четкого выбора)
    breakfast = st.radio("Завтракаете ли вы?", ["Да, каждый день", "Иногда", "Нет, пропускаю"])
    meals_per_day = st.selectbox("Количество приемов пищи в день", [1, 2, 3, 4, 5])
    
    # 3. Фастфуд (главный фактор)
    fastfood_freq = st.select_slider(
        "Как часто едите фастфуд?",
        options=["Никогда", "Раз в месяц", "Раз в неделю", "2-3 раза в неделю", "Каждый день"]
    )
    
    # 4. Субъективная оценка
    concentration = st.slider("Оцените свою концентрацию (от 1 до 10)", 1, 10, 5)
    
    # 5. Кнопка отправки (сердце всего приложения)
    submitted = st.button("✅ Отправить ответы")

# --- ОСНОВНАЯ ОБЛАСТЬ (где будет результат) ---

# Создаем переменную для хранения всех ответов (как словарь)
# Если данные еще не отправлены, показываем приглашение
if 'responses' not in st.session_state:
    st.session_state.responses = []

# Если кнопка нажата
if submitted:
    # Формируем запись
    new_record = {
        "Возраст": age,
        "Часы учебы": study_hours,
        "Завтрак": breakfast,
        "Приемов пищи": meals_per_day,
        "Фастфуд": fastfood_freq,
        "Концентрация": concentration,
        "Время заполнения": datetime.now().strftime("%H:%M")
    }
    
    # Добавляем в сессию (чтобы данные не пропадали при перезагрузке)
    st.session_state.responses.append(new_record)
    
    # Визуальный фидбек пользователю
    st.success("🎉 Спасибо! Ваши данные сохранены.")
    
    # --- МГНОВЕННАЯ АНАЛИТИКА (самое интересное) ---
    st.subheader("📊 Ваш персональный результат")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Ваша концентрация", f"{concentration}/10")
        if concentration >= 7:
            st.info("🧘 Вы хорошо концентрируетесь! Так держать.")
        elif concentration >= 4:
            st.warning("😐 Уровень средний. Возможно, стоит пересмотреть рацион.")
        else:
            st.error("⚡ Низкая концентрация. Попробуйте убрать фастфуд и наладить режим.")
    
    with col2:
        st.metric("Частота фастфуда", fastfood_freq)
        if fastfood_freq in ["Каждый день", "2-3 раза в неделю"]:
            st.warning("🍔 Много фастфуда. Это может снижать успеваемость.")
        else:
            st.success("🥗 Отличный баланс! Продолжайте в том же духе.")

    # --- ВИЗУАЛИЗАЦИЯ ЗАВИСИМОСТИ (если есть данные) ---
    if len(st.session_state.responses) > 1:
        st.subheader("📉 Статистика по всем участникам (наглядно)")
        
        # Превращаем список словарей в DataFrame
        df = pd.DataFrame(st.session_state.responses)
        
        # Создаем график: Завтрак vs Концентрация
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Группируем по завтраку и считаем среднюю концентрацию
        breakfast_group = df.groupby('Завтрак')['Концентрация'].mean().reset_index()
        
        # Строим столбчатую диаграмму
        bars = ax.bar(breakfast_group['Завтрак'], breakfast_group['Концентрация'], 
                      color=['#4CAF50', '#FFC107', '#F44336'])
        ax.set_ylim(0, 10)
        ax.set_ylabel('Средняя концентрация')
        ax.set_title('Связь завтрака и концентрации')
        
        # Добавляем значения на столбцы
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                    f'{height:.1f}', ha='center', va='bottom')
        
        st.pyplot(fig)
        
        # Показываем сырые данные (для любопытных)
        with st.expander("📋 Посмотреть все ответы"):
            st.dataframe(df)
            
    else:
        st.info("👥 Пока мало данных. Пригласите друзей пройти опрос, чтобы увидеть статистику!")

# --- ИНСТРУКЦИЯ ПРИ ПЕРВОМ ЗАПУСКЕ ---
else:
    st.markdown("""
    ### 👈 Заполните анкету слева и нажмите "Отправить"
    
    **Что вы узнаете:**
    - Ваш уровень концентрации в зависимости от привычек.
    - Сравнение ваших показателей с другими (после накопления данных).
    - Рекомендации по улучшению рациона.
    """)
    
    # Картинка-заглушка (эмодзи)
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="font-size: 80px;">🍎📚</h1>
        <p style="color: grey;">Здоровое питание = Острый ум</p>
    </div>
    """, unsafe_allow_html=True)
