import streamlit as st
from matplotlib import pyplot as plt

import preprocess_data,helper
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file= st.sidebar.file_uploader(label="Choose file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess_data.preprocess(data)
    st.title("Orignal Chat")
    st.dataframe(df)

    # fetch unique users name

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall ")
    st.title("Total Number of users")
    st.dataframe(user_list)
    selected_user=st.sidebar.selectbox("Select user whose data you want to analysis", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

    # finding the busiest users in the group(Group level)
    if selected_user == 'Overall':
        st.title('Most Busy Users')
        x,new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)
    # WordCloud
    st.title("Wordcloud")
    df_wc = helper.create_wordcloud(selected_user,df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    # most common words
    most_common_df = helper.most_common_words(selected_user,df)

    fig,ax = plt.subplots()

    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation='vertical')

    st.title('Most commmon words')
    st.pyplot(fig)

# emoji analysis
    emoji_df = helper.emoji_helper(selected_user,df)
    st.title("Emoji Analysis")

    col1,col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax = plt.subplots()
        ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
        st.pyplot(fig)

# bad word used in chat
    st.title("Bad word used by users")
    data_of_bad_words=helper.bad_word_used_by_user(selected_user,df)
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(data_of_bad_words)
    fig, ax = plt.subplots()

    ax.barh(data_of_bad_words[0], data_of_bad_words[1])
    plt.xticks(rotation='vertical')

    with col2:
         st.pyplot(fig)
