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
    
    # Get user input for city (chicago, new york city, washington).
    while True:
        city = input('Enter a city - Chicago, New York City or Washington: ').lower()
        if city in CITY_DATA:
            break
        else:
            print('That\'s not in the list! Type either Chicago, New York City or Washington please!')

    # Get user input for month (all, january, february, ... , june)
    while True:
        months = ['january','february','march','april','may','june']
        month = input('Enter a month - all, or January, February, March, April, May, June: ').lower()
        if month in months or month == 'all':
            break
        else:
            print('That\'s not in the list! Try again please')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = input('Enter the day of the week - all, or Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: ').lower()
        if day in days or day == 'all':
            break
        else:
            print('That\'s not in the list! Try again please')
        
    print('-'*40)
    print('You have entered {}, {}, {}.'.format(city.title(),month.title(),day.title()))
    print('-'*40)
    return city, month, day


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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    df['start_month'] = df['Start Time'].dt.month
    popular_start_month = df['start_month'].mode()[0]
    print('Most common start month (1-12):', popular_start_month)

    # Display the most common day of week
    df['start_dow'] = df['Start Time'].dt.weekday_name
    popular_start_dow = df['start_dow'].mode()[0]
    print('Most common start day:', popular_start_dow)

    # Display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    popular_start_hour = df['start_hour'].mode()[0]
    print('Most common start hour (0-23):', popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    mode_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', mode_start_station)

    # Display most commonly used end station
    mode_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ', mode_end_station)

    # Display most frequent combination of start station and end station trip
    mode_station_combo = ('From: ' + df['Start Station'] + '; To: ' + df['End Station']).mode()[0]
    print('Most frequent combination of start and end station: ', mode_station_combo)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time in seconds: ', total_travel_time)
    print('Total travel time in minutes: ', total_travel_time/60)
    print('Total travel time in hours: ', total_travel_time/3600)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time in seconds: ', mean_travel_time)
    print('Mean travel time in minutes: ', mean_travel_time/60)
    print('Mean travel time in hours: ', mean_travel_time/3600)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('Count of user types: \n', user_type)

    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    # Handle Washington, which does not have Gender or Birth Year data
    if 'Gender' not in df.columns:
        print('Sorry, no gender or date of birth data is available')
    else:
        gender = df['Gender'].value_counts()
        print('Count of gender: \n', gender)
        
        min_yob = df['Birth Year'].min()
        max_yob = df['Birth Year'].max()
        mode_yob = df['Birth Year'].mode()[0]
        print('Earliest year of birth is {}; Most recent year of birth is {}; Most common year of birth is {}.'.format(int(min_yob),int(max_yob),int(mode_yob)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_raw_data(df):
    """Displays 5 rows of raw data upon request."""    
    row = 0
    while True:
        viewData = input("Would you like to see 5 rows of raw data? Type 'Yes' or 'No'.").lower()
        if viewData == 'yes':
            print(df.iloc[[row,row+1,row+2,row+3,row+4]])
            row += 5
        else:
            break
     
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
