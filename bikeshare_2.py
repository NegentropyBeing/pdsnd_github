import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('choose one of the three cities in our Database (chicago, new york city or washington): ') 
    while city.lower() not in ('chicago', 'new york city', 'washington'):
        print('Database only have info for chicago, new york city or washington')
        city = input('choose one of the three cities in our Database (chicago, new york city or washington): ')

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input('Choose a month (january, february, march, april, may, june) or all: ')
    while month.lower() not in months:
        print('invalid month. Check if it is one the current available months')
        month = input('choose one of the current available months january, february, march, april, may, june or all: ')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = input('Choose a day of the week (monday, tuesday, wednesday, thursday, fridary, saturday or sunday) and all for every data. Which one: ')
    while day.lower() not in days:
        print('check for typo')
        day = input('Choose a day of the week (monday, tuesday, wednesday, thursday, fridary, saturday or sunday). Which one: ')
        
    print('-'*40)
    return city.lower(), month.lower(), day.lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
  
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is: ', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(' The most common day is: ', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common start hour is:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station is:', Start_Station)

    # display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('The most commonly used end station is:', End_Station)

    # display most frequent combination of start station and end station trip
    Combination_Station = df.groupby(['Start Station', 'End Station']).count()
    print('The most commonly used combination of start station and end station trip is: ', Start_Station, " & ", End_Station)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print('The total travel time in seconds is:', total_travel_time)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time in seconds is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Users are:', user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("minimium year: " + str(df['Birth Year'].min()))
        print("maximum year: " + str(df['Birth Year'].max()))
        print("most common year: " + str(df['Birth Year'].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    print('Displaying Data...')
    start = 0
    while True:
        data_input = input('Do you want to display more data? yes or no?').lower()
        if data_input == 'yes':
            print(df.iloc[start:start:5])
            start += 5
        else:
            break
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()