import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    

    cities = ['chicago', 'new york', 'washington']
    valid_city = False

    while not valid_city:
        city = input('Would you like to see data for Chicago, New York or Washington: ').lower()

        if city in cities:
            valid_city = True
            break
        else:
            print ('Invalid input. Please try again.')

    # get user input for month (all, january, february, ... , june)
    
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    
    while True:
        month = input('Which month would you like to filter by (i.e January, February, etc or all): ').lower()

        if month in months:
            break
        else:
            print ('Invalid input. Please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    valid_day = False

    while not valid_day:
        day = input('Which day of the week to review, or all: ').lower()

        if day in days:
            valid_day = True
            break
        else:
            print ('Invalid input. Please try again.')

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

      # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns    
    df['month'] = df['Start Time'].dt.strftime('%B').str.lower()
    df['day'] = df['Start Time'].dt.strftime('%A').str.lower()
    df['hour'] = df['Start Time'].dt.strftime('%-I').str.lower()
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        df = df[df['month'] == month.lower()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.lower()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0].upper()
    print('The most common month for bike rentals: ', popular_month)

    # display the most common day of week
    popular_day = df['day'].mode()[0].upper()
    print('The most popular day for bike rentals: ', popular_day)

    # display the most common start hour

    popular_hour = df['hour'].mode()[0]
    print('The most popular hour to rent bicycles: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station and usage count
    popular_start = df['Start Station'].mode()[0]
    count_start = df['Start Station'].value_counts()[popular_start]
    print('The most commonly used start station is:', popular_start+',', 'Usage Count:', count_start)

    # display most commonly used end station and usage count
    popular_end = df['End Station'].mode()[0]
    count_end = df['End Station'].value_counts()[popular_end]
    print('The most commonly used start station is:', popular_end+',', 'Usage Count:', count_end)

    # display most frequent combination of start station and end station trip
    df['combination_station'] = df['Start Station'] + ' ' + df['End Station']
    pop_comb_station = df['combination_station'].mode()[0]
    count_comb = df['combination_station'].value_counts()[pop_comb_station]
    print('The most frequent combo stations: ', pop_comb_station+',', 'Usage Count: ', count_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is', sum(df['Trip Duration']))

    # display mean travel time
    print('The mean travel time is', np.mean(df['Trip Duration']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender

    try:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    except:
        print('No data provided for user gender.')

    # Display earliest, most recent, and most common year of birth,
    try:
        print('Most recent birth year:', df['Birth Year'].max())
        print('Earliest birth year:', df['Birth Year'].min())
        
        pop_birth = df['Birth Year'].mode()[0]
        pop_birth_count = df['Birth Year'].value_counts()[pop_birth]
        print(f'Most Common Birth Year is {pop_birth}. This year appeared {pop_birth_count} times.')
        
    except:
        print('No data provided for the user birth year.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays the raw data on bikeshare users"""
    print('\nRaw Data Section\n')
    
    all_rows = len(df)
    start_row = 0

    # get user input for displaying raw data
    while start_row < all_rows:
        response = input('Would you like to see 5 rows of data? ').lower()
    
        if response.lower() == 'yes':
            print(df.iloc[start_row:start_row+5])
            start_row += 5
        
        elif response.lower() == 'no':
            break

        else:
            print('This is an invalid input')
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
