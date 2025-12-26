import streamlit as st
import matplotlib.pyplot as plt
import preprocessor, helper
import seaborn as sns

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="📱",
)

st.markdown("""
<style>
/* Remove Streamlit default UI */
#MainMenu, footer, header {visibility: hidden;}

/* App background */
.stApp {
    background-color: #0E1117;
    color: #E6EDF3;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161B22;
    padding: 20px;
}

/* Headings */
h1 {
    font-size: 2.4rem;
    margin-bottom: 0.3rem;
}
h2 {
    margin-top: 1.5rem;
}
h1, h2, h3 {
    color: #E6EDF3;
    font-weight: 600;
}

/* Buttons */
.stButton>button {
    background-color: #25D366;
    color: #000;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
    border: none;
    width: 100%;
}
.stButton>button:hover {
    background-color: #1EBE5D;
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #30363D;
    border-radius: 12px;
    padding: 16px;
}

/* Metrics cards */
[data-testid="stMetric"] {
    background-color: #161B22;
    padding: 15px;
    border-radius: 12px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Horizontal divider */
hr {
    border: 0.5px solid #30363D;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style="text-align:center;">📱 WhatsApp Chat Analyzer</h1>
<p style="text-align:center; color:#8B949E;">
Analyze WhatsApp chats with interactive insights
</p>
<hr>
""", unsafe_allow_html=True)

st.sidebar.image("whatsapp_logo.jpg")
st.sidebar.title("See More Than Just Messages")

#st.sidebar.markdown("## 📊 Controls")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # to convert the text into string
    data = bytes_data.decode("utf-8",errors="ignore")
    df = preprocessor.preprocess(data)

    # show the dataframe of all messages
    #st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    # arrange all the users in ascending order
    user_list.sort()
    user_list.insert(0, "Overall")
    # show a dropdown list of all users in the sidebar
    selected_user = st.selectbox("Show analysis wrt", user_list)
    if st.button("Show Analysis") :
        num_messages, words, media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("TOP STATISTICS")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Messages", num_messages)

        with col2:
            st.metric("Total Words", words)

        with col3:
            st.metric("Media Shared", media_messages)

        with col4:
            st.metric("Links Shared", num_links)



        # monthly timeline
        st.header("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.header("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.header('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.header("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.header('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.header("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)
        #st.dataframe(most_common_df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.header('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.header("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)


        # show the dataframe of all messages
        st.dataframe(df)

st.markdown("""
<hr>
<p style="text-align:center; color:#6E7681;">
From Messages to Meaning
</p>
""", unsafe_allow_html=True)