import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import scipy

import preprocessor,helper

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df = preprocessor.process(df,region_df)
st.sidebar.title("Olympic Analysis")
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country wise Analysis','Athlete wise Analysis')
)

st.dataframe(df)

if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("select year",years)
    selected_country = st.sidebar.selectbox("select country", country)

    medal_Tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Overall Tally")
    elif selected_year!='Overall' and selected_country=='Overall':
        st.title("Medal Tally in " +str(selected_year)+ " Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country+" Overall Performance")
    elif selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country+ "Performance in"+ str(selected_year)+ "Olympics")
    st.table(medal_Tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)


    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the Years")
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the Years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the Years")
    st.plotly_chart(fig)


    st.title("No of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Sucessful Athletes")
    sport_list=df['Sport'].unique().tolist();
    sport_list.sort();
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select a Sport',sport_list)
    x=helper.most_sucessful(df,selected_sport)
    st.table(x)

if user_menu == 'Country wise Analysis':
    st.sidebar.title('Country wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_countr=st.sidebar.selectbox('Select a country',country_list)
    country_df=helper.year_wise_medaltally(df,country_list)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_countr+"Medal Tally over the Years")
    st.plotly_chart(fig)

    st.title(selected_countr+"Excels in the following sport")
    pt=helper.country_even_heatmap(df,selected_countr)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athlete of "+selected_countr)
    top10df=helper.most_sucessful_countryWise(df,selected_countr)
    st.table(top10df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)

    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)


    x = []
    name = []
    famous_sports = ['Basketball',
                     'Judo',
                     'Football',
                     'Tug-Of-War',
                     'Athletics',
                     'Swimming',
                     'Badminton',
                     'Sailing',
                     'Gymnastics',
                     'Art Competitions',
                     'Handball',
                     'Weightlifting',
                     'Wrestling',
                     'Water Polo',
                     'Hockey',
                     'Rowing',
                     'Fencing',
                     'Equestrianism',
                     'Shooting',
                     'Boxing',
                     'Taekwondo',
                     'Cycling',
                     'Diving',
                     'Canoeing',
                     'Tennis',
                     'Modern Pentathlon',
                     'Golf' ]
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sport(Gold Medalist)")
    st.plotly_chart(fig)


    sport_list=df['Sport'].unique().tolist();
    sport_list.sort();
    sport_list.insert(0,'Overall')

    st.title("Weight vs Height")
    selected_sport=st.selectbox('Select a Sport',sport_list)
    temp_df=helper.weight_vs_height(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)

    st.pyplot(fig)

    st.title("Men vs Women Participation In the World")
    final_df=helper.men_VS_women(df)
    fig = px.line(final_df, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


